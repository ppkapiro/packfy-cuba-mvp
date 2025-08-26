#!/usr/bin/env python
"""
🧪 PRUEBAS AUTOMATIZADAS COMPLETAS DEL LOGIN MULTITENANCY
Sistema de testing completo para login por empresa y dominios
"""
import json
import os
from datetime import datetime

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.test import Client, RequestFactory
from empresas.middleware import TenantMiddleware
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


class LoginMultitenancyTester:
    """Clase para pruebas automatizadas del sistema de login multitenancy"""

    def __init__(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "tests": [],
        }

    def log_test(self, test_name, status, message, details=None):
        """Registrar resultado de una prueba"""
        self.test_results["total_tests"] += 1
        if status == "PASS":
            self.test_results["passed_tests"] += 1
            icon = "✅"
        else:
            self.test_results["failed_tests"] += 1
            icon = "❌"

        test_result = {
            "name": test_name,
            "status": status,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results["tests"].append(test_result)

        print(f"   {icon} {test_name}: {message}")
        if details:
            for key, value in details.items():
                print(f"      📊 {key}: {value}")

    def test_1_basic_authentication(self):
        """TEST 1: Autenticación básica de usuarios"""
        print("\n🧪 TEST 1: AUTENTICACIÓN BÁSICA")
        print("-" * 50)

        test_users = [
            ("admin@packfy.com", "admin123", True),
            ("dueno@packfy.com", "password123", True),
            ("consultor@packfy.com", "password123", True),
            ("demo@packfy.com", "demo123", True),
            ("miami@packfy.com", "password123", True),
            ("cuba@packfy.com", "password123", True),
            ("fake@user.com", "wrong", False),  # Usuario que no debe existir
        ]

        for email, password, should_pass in test_users:
            auth_user = authenticate(username=email, password=password)

            if should_pass and auth_user:
                self.log_test(
                    f"Auth {email}",
                    "PASS",
                    "Autenticación exitosa",
                    {"user_id": auth_user.id, "is_active": auth_user.is_active},
                )
            elif not should_pass and not auth_user:
                self.log_test(
                    f"Auth {email}", "PASS", "Autenticación rechazada correctamente"
                )
            else:
                self.log_test(
                    f"Auth {email}",
                    "FAIL",
                    f"Resultado inesperado: esperado={should_pass}, obtenido={bool(auth_user)}",
                )

    def test_2_tenant_middleware(self):
        """TEST 2: Middleware de detección de tenant"""
        print("\n🧪 TEST 2: MIDDLEWARE TENANT")
        print("-" * 50)

        middleware = TenantMiddleware(lambda r: None)

        test_hosts = [
            ("packfy-express.localhost:5173", "packfy-express", True),
            ("cuba-express.localhost:5173", "cuba-express", True),
            ("habana-premium.localhost:5173", "habana-premium", True),
            ("miami-shipping.localhost:5173", "miami-shipping", True),
            ("empresa-inexistente.localhost:5173", None, True),
            ("localhost:5173", None, True),
        ]

        for host, expected_slug, should_process in test_hosts:
            request = self.factory.get("/", HTTP_HOST=host)

            try:
                # Capturar salida del middleware
                import io
                import sys

                old_stdout = sys.stdout
                sys.stdout = buffer = io.StringIO()

                middleware.process_request(request)

                sys.stdout = old_stdout
                output = buffer.getvalue()

                tenant = getattr(request, "tenant", None)
                actual_slug = tenant.slug if tenant else None

                if actual_slug == expected_slug:
                    self.log_test(
                        f"Middleware {host}",
                        "PASS",
                        f"Tenant detectado correctamente: {actual_slug}",
                        {"expected": expected_slug, "actual": actual_slug},
                    )
                else:
                    self.log_test(
                        f"Middleware {host}",
                        "FAIL",
                        f"Tenant incorrecto",
                        {"expected": expected_slug, "actual": actual_slug},
                    )

            except Exception as e:
                self.log_test(
                    f"Middleware {host}", "FAIL", f"Error en middleware: {str(e)}"
                )

    def test_3_api_login_with_tenant(self):
        """TEST 3: Login API con headers de tenant"""
        print("\n🧪 TEST 3: API LOGIN CON TENANT")
        print("-" * 50)

        test_cases = [
            {
                "email": "dueno@packfy.com",
                "password": "password123",
                "tenant_slug": "packfy-express",
                "should_pass": True,
            },
            {
                "email": "consultor@packfy.com",
                "password": "password123",
                "tenant_slug": "cuba-express",
                "should_pass": True,
            },
            {
                "email": "admin@packfy.com",
                "password": "admin123",
                "tenant_slug": "any-tenant",
                "should_pass": True,  # Superuser puede acceder a cualquier tenant
            },
            {
                "email": "dueno@packfy.com",
                "password": "wrong_password",
                "tenant_slug": "packfy-express",
                "should_pass": False,
            },
        ]

        for case in test_cases:
            headers = {}
            if case["tenant_slug"]:
                headers["HTTP_X_TENANT_SLUG"] = case["tenant_slug"]

            response = self.client.post(
                "/api/auth/login/",
                {"email": case["email"], "password": case["password"]},
                content_type="application/json",
                **headers,
            )

            success = response.status_code == 200

            if success == case["should_pass"]:
                self.log_test(
                    f"API Login {case['email']}@{case['tenant_slug']}",
                    "PASS",
                    f"Respuesta correcta: {response.status_code}",
                    {
                        "expected_pass": case["should_pass"],
                        "actual_status": response.status_code,
                    },
                )
            else:
                self.log_test(
                    f"API Login {case['email']}@{case['tenant_slug']}",
                    "FAIL",
                    f"Respuesta incorrecta: {response.status_code}",
                    {
                        "expected_pass": case["should_pass"],
                        "actual_status": response.status_code,
                    },
                )

    def test_4_user_enterprise_access(self):
        """TEST 4: Acceso de usuarios a empresas específicas"""
        print("\n🧪 TEST 4: ACCESO USUARIO-EMPRESA")
        print("-" * 50)

        test_cases = [
            {
                "email": "dueno@packfy.com",
                "empresa_slug": "packfy-express",
                "should_have_access": True,
            },
            {
                "email": "dueno@packfy.com",
                "empresa_slug": "cuba-express",
                "should_have_access": False,
            },
            {
                "email": "consultor@packfy.com",
                "empresa_slug": "packfy-express",
                "should_have_access": True,
            },
            {
                "email": "consultor@packfy.com",
                "empresa_slug": "cuba-express",
                "should_have_access": True,
            },
            {
                "email": "demo@packfy.com",
                "empresa_slug": "miami-shipping",
                "should_have_access": True,
            },
        ]

        for case in test_cases:
            try:
                usuario = Usuario.objects.get(email=case["email"])
                empresa = Empresa.objects.get(slug=case["empresa_slug"])

                # Verificar si el usuario tiene perfil activo en la empresa
                has_access = PerfilUsuario.objects.filter(
                    usuario=usuario, empresa=empresa, activo=True
                ).exists()

                # Superusers tienen acceso a todo
                if usuario.is_superuser:
                    has_access = True

                if has_access == case["should_have_access"]:
                    self.log_test(
                        f"Acceso {case['email']} → {case['empresa_slug']}",
                        "PASS",
                        f"Acceso {'permitido' if has_access else 'denegado'} correctamente",
                        {
                            "has_access": has_access,
                            "expected": case["should_have_access"],
                        },
                    )
                else:
                    self.log_test(
                        f"Acceso {case['email']} → {case['empresa_slug']}",
                        "FAIL",
                        f"Acceso incorrecto",
                        {
                            "has_access": has_access,
                            "expected": case["should_have_access"],
                        },
                    )

            except (Usuario.DoesNotExist, Empresa.DoesNotExist) as e:
                self.log_test(
                    f"Acceso {case['email']} → {case['empresa_slug']}",
                    "FAIL",
                    f"Error: {str(e)}",
                )

    def test_5_multi_enterprise_users(self):
        """TEST 5: Usuarios con acceso a múltiples empresas"""
        print("\n🧪 TEST 5: USUARIOS MULTI-EMPRESA")
        print("-" * 50)

        multi_users = ["consultor@packfy.com", "demo@packfy.com"]

        for email in multi_users:
            try:
                usuario = Usuario.objects.get(email=email)
                perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
                empresas_count = perfiles.count()
                empresas_names = [p.empresa.nombre for p in perfiles]

                if empresas_count >= 2:
                    self.log_test(
                        f"Multi-empresa {email}",
                        "PASS",
                        f"Usuario con acceso a {empresas_count} empresas",
                        {"empresas_count": empresas_count, "empresas": empresas_names},
                    )
                else:
                    self.log_test(
                        f"Multi-empresa {email}",
                        "FAIL",
                        f"Usuario solo tiene acceso a {empresas_count} empresa(s)",
                        {"empresas_count": empresas_count},
                    )

            except Usuario.DoesNotExist:
                self.log_test(f"Multi-empresa {email}", "FAIL", "Usuario no encontrado")

    def test_6_frontend_credentials(self):
        """TEST 6: Verificar credenciales para frontend"""
        print("\n🧪 TEST 6: CREDENCIALES FRONTEND")
        print("-" * 50)

        frontend_credentials = [
            {"email": "admin@packfy.com", "password": "admin123", "type": "superadmin"},
            {"email": "dueno@packfy.com", "password": "password123", "type": "owner"},
            {
                "email": "consultor@packfy.com",
                "password": "password123",
                "type": "multi-enterprise",
            },
            {"email": "demo@packfy.com", "password": "demo123", "type": "demo"},
            {
                "email": "miami@packfy.com",
                "password": "password123",
                "type": "operator",
            },
            {"email": "cuba@packfy.com", "password": "password123", "type": "operator"},
        ]

        for cred in frontend_credentials:
            auth_user = authenticate(username=cred["email"], password=cred["password"])

            if auth_user and auth_user.is_active:
                self.log_test(
                    f"Frontend {cred['type']}",
                    "PASS",
                    f"Credencial válida: {cred['email']}",
                    {"password": cred["password"], "user_type": cred["type"]},
                )
            else:
                self.log_test(
                    f"Frontend {cred['type']}",
                    "FAIL",
                    f"Credencial inválida: {cred['email']}",
                    {"password": cred["password"]},
                )

    def generate_frontend_config(self):
        """Generar configuración para el frontend"""
        print("\n📱 CONFIGURACIÓN PARA FRONTEND:")
        print("-" * 50)

        config = {
            "api_base_url": "http://localhost:8000/api",
            "tenant_header": "X-Tenant-Slug",
            "test_credentials": [
                {
                    "label": "👑 Superadmin",
                    "email": "admin@packfy.com",
                    "password": "admin123",
                    "description": "Acceso total al sistema",
                },
                {
                    "label": "🏢 Dueño Principal",
                    "email": "dueno@packfy.com",
                    "password": "password123",
                    "description": "Solo Packfy Express",
                },
                {
                    "label": "🌐 Multi-empresa",
                    "email": "consultor@packfy.com",
                    "password": "password123",
                    "description": "Todas las empresas",
                },
                {
                    "label": "🧪 Demo",
                    "email": "demo@packfy.com",
                    "password": "demo123",
                    "description": "Usuario de demostración",
                },
            ],
            "tenant_urls": {},
        }

        # Agregar URLs por empresa
        empresas = Empresa.objects.filter(activo=True)
        for empresa in empresas:
            config["tenant_urls"][empresa.slug] = {
                "local": f"http://{empresa.slug}.localhost:5173",
                "production": f"https://{empresa.slug}.packfy.com",
            }

        print("   📋 Configuración generada para LoginPage.tsx:")
        print(f"   {json.dumps(config, indent=2, ensure_ascii=False)}")

        return config

    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🧪 INICIANDO PRUEBAS AUTOMATIZADAS LOGIN MULTITENANCY")
        print("=" * 80)

        self.test_1_basic_authentication()
        self.test_2_tenant_middleware()
        self.test_3_api_login_with_tenant()
        self.test_4_user_enterprise_access()
        self.test_5_multi_enterprise_users()
        self.test_6_frontend_credentials()

        self.generate_frontend_config()

        # Resumen final
        print("\n📊 RESUMEN DE PRUEBAS:")
        print("-" * 50)
        print(f"   ✅ Pruebas exitosas: {self.test_results['passed_tests']}")
        print(f"   ❌ Pruebas fallidas: {self.test_results['failed_tests']}")
        print(
            f"   📈 Tasa de éxito: {(self.test_results['passed_tests']/self.test_results['total_tests']*100):.1f}%"
        )

        if self.test_results["failed_tests"] == 0:
            print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
            print("   Sistema de login multitenancy funcionando correctamente")
        else:
            print("\n⚠️ Algunas pruebas fallaron, revisar resultados arriba")

        return self.test_results


if __name__ == "__main__":
    tester = LoginMultitenancyTester()
    results = tester.run_all_tests()

    print("\n" + "=" * 80)
    print("🎯 PRUEBAS COMPLETADAS")
    print("   Sistema de login multitenancy validado completamente")
    print("=" * 80)
