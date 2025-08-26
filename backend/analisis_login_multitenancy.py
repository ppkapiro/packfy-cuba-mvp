#!/usr/bin/env python
"""
🔐 ANÁLISIS COMPLETO DEL SISTEMA DE LOGIN MULTITENANCY
Análisis del estado actual del login por empresa y dominios
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.test import RequestFactory
from empresas.middleware import TenantMiddleware
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def analizar_estado_usuarios_login():
    """Analizar el estado actual de usuarios para login"""
    print("🔐 ANÁLISIS DEL SISTEMA DE LOGIN MULTITENANCY")
    print("=" * 80)

    print("\n1. 👥 USUARIOS REGISTRADOS:")
    print("-" * 50)

    usuarios = Usuario.objects.all().order_by("id")
    for usuario in usuarios:
        # Obtener perfiles activos
        perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
        empresas_list = [f"{p.empresa.slug}({p.rol})" for p in perfiles]

        # Verificar si puede hacer login
        can_login = usuario.is_active and usuario.check_password("password123")
        login_status = "✅ LOGIN OK" if can_login else "❌ LOGIN FAIL"

        # Determinar tipo de usuario
        user_type = "👑 SUPER" if usuario.is_superuser else "👤 USER"

        print(f"   {user_type} {usuario.email}")
        print(f"      🏢 Empresas: {empresas_list if empresas_list else 'Ninguna'}")
        print(f"      🔐 Estado: {login_status}")
        print(f"      📊 Activo: {usuario.is_active}, Staff: {usuario.is_staff}")
        print()


def analizar_empresas_dominios():
    """Analizar configuración de empresas para dominios"""
    print("\n2. 🏢 EMPRESAS Y CONFIGURACIÓN DE DOMINIOS:")
    print("-" * 50)

    empresas = Empresa.objects.all().order_by("id")
    for empresa in empresas:
        usuarios_count = PerfilUsuario.objects.filter(
            empresa=empresa, activo=True
        ).count()

        # URLs de prueba
        local_url = f"{empresa.slug}.localhost:5173"
        prod_url = f"{empresa.slug}.packfy.com"

        print(f"   🏢 {empresa.nombre}")
        print(f"      🔗 Slug: '{empresa.slug}'")
        print(f"      👥 Usuarios: {usuarios_count}")
        print(f"      🌐 URL Local: {local_url}")
        print(f"      🌐 URL Prod: {prod_url}")
        print(f"      📊 Activa: {empresa.activo}")
        print()


def probar_middleware_tenant():
    """Probar el middleware de tenant con diferentes dominios"""
    print("\n3. 🔧 PRUEBA DEL MIDDLEWARE TENANT:")
    print("-" * 50)

    factory = RequestFactory()
    middleware = TenantMiddleware(lambda r: None)

    # Casos de prueba
    test_cases = [
        ("packfy-express.localhost:5173", "packfy-express"),
        ("cuba-express.localhost:5173", "cuba-express"),
        ("habana-premium.localhost:5173", "habana-premium"),
        ("miami-shipping.localhost:5173", "miami-shipping"),
        ("empresa-inexistente.localhost:5173", None),
        ("localhost:5173", None),
    ]

    for host, expected_slug in test_cases:
        request = factory.get("/", HTTP_HOST=host)

        # Simular procesamiento del middleware
        try:
            middleware.process_request(request)
            tenant_found = getattr(request, "tenant", None)
            tenant_slug = tenant_found.slug if tenant_found else None

            status = "✅ OK" if tenant_slug == expected_slug else "❌ ERROR"
            print(f"   {status} Host: {host}")
            print(f"        Esperado: {expected_slug}")
            print(f"        Obtenido: {tenant_slug}")
            print()

        except Exception as e:
            print(f"   ❌ ERROR Host: {host}")
            print(f"        Error: {str(e)}")
            print()


def probar_autenticacion_usuarios():
    """Probar autenticación de usuarios clave"""
    print("\n4. 🧪 PRUEBA DE AUTENTICACIÓN:")
    print("-" * 50)

    usuarios_prueba = [
        ("superadmin@packfy.com", "admin123"),
        ("admin@packfy.com", "admin123"),
        ("dueno@packfy.com", "password123"),
        ("consultor@packfy.com", "password123"),
        ("miami@packfy.com", "password123"),
        ("cuba@packfy.com", "password123"),
        ("empresa@test.cu", "password123"),
        ("cliente@test.cu", "password123"),
    ]

    for email, password in usuarios_prueba:
        try:
            usuario = Usuario.objects.get(email=email)

            # Probar autenticación Django
            auth_user = authenticate(username=email, password=password)
            auth_status = "✅ AUTH OK" if auth_user else "❌ AUTH FAIL"

            # Verificar password manual
            pass_check = usuario.check_password(password)
            pass_status = "✅ PASS OK" if pass_check else "❌ PASS FAIL"

            # Contar empresas
            empresas_count = PerfilUsuario.objects.filter(
                usuario=usuario, activo=True
            ).count()

            print(f"   👤 {email}")
            print(f"      🔐 Autenticación: {auth_status}")
            print(f"      🔑 Password: {pass_status}")
            print(f"      🏢 Empresas: {empresas_count}")
            print()

        except Usuario.DoesNotExist:
            print(f"   ❌ {email}: Usuario no existe")
            print()


def generar_urls_prueba():
    """Generar URLs de prueba para cada empresa"""
    print("\n5. 🔗 URLS DE PRUEBA GENERADAS:")
    print("-" * 50)

    empresas = Empresa.objects.filter(activo=True)

    print("   📋 URLs para desarrollo local:")
    for empresa in empresas:
        print(f"      🌐 http://{empresa.slug}.localhost:5173/login")

    print("\n   📋 URLs para producción:")
    for empresa in empresas:
        print(f"      🌐 https://{empresa.slug}.packfy.com/login")

    print("\n   📋 URLs con header X-Tenant-Slug (API):")
    for empresa in empresas:
        print(
            f"      📡 http://localhost:8000/api/auth/login/ (X-Tenant-Slug: {empresa.slug})"
        )


def verificar_configuracion_frontend():
    """Verificar configuración del frontend"""
    print("\n6. 🖥️ VERIFICACIÓN CONFIGURACIÓN FRONTEND:")
    print("-" * 50)

    # Verificar archivos clave del frontend
    frontend_files = [
        "frontend-multitenant/src/pages/LoginPage.tsx",
        "frontend-multitenant/src/contexts/AuthContext.tsx",
        "frontend-multitenant/src/contexts/TenantContext.tsx",
        "frontend-multitenant/src/services/api.ts",
        "frontend-multitenant/src/App.tsx",
    ]

    base_path = os.path.dirname(os.path.dirname(__file__))

    for file_path in frontend_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (NO ENCONTRADO)")

    print("\n   📊 Estado del Frontend:")
    print("      - LoginPage.tsx: Maneja credenciales de prueba")
    print("      - AuthContext.tsx: Gestiona tokens JWT")
    print("      - TenantContext.tsx: Maneja selección de empresa")
    print("      - api.ts: Envía headers X-Tenant-Slug automáticamente")


def generar_plan_pruebas():
    """Generar plan de pruebas para login multitenancy"""
    print("\n7. 📋 PLAN DE PRUEBAS LOGIN MULTITENANCY:")
    print("-" * 50)

    print("   🎯 CASOS DE PRUEBA CRÍTICOS:")
    print()

    print("   1. LOGIN POR DOMINIO:")
    print("      • Acceder a packfy-express.localhost:5173")
    print("      • Login con dueno@packfy.com / password123")
    print("      • Verificar que solo ve datos de Packfy Express")
    print()

    print("   2. LOGIN MULTI-EMPRESA:")
    print("      • Login con consultor@packfy.com / password123")
    print("      • Verificar TenantSelector con 4 empresas")
    print("      • Cambiar entre empresas y verificar datos")
    print()

    print("   3. LOGIN SUPERUSUARIO:")
    print("      • Login con admin@packfy.com / admin123")
    print("      • Verificar acceso a todas las empresas")
    print("      • Verificar bypass de restricciones tenant")
    print()

    print("   4. LOGIN CON HEADER API:")
    print("      • POST /api/auth/login/ con X-Tenant-Slug")
    print("      • Verificar token JWT generado")
    print("      • Verificar acceso solo a datos del tenant")
    print()

    print("   5. REDIRECCIÓN DOMINIO INVÁLIDO:")
    print("      • Acceder a empresa-inexistente.localhost:5173")
    print("      • Verificar redirección a localhost:5173")
    print("      • Verificar mensaje de error apropiado")


def mostrar_credenciales_prueba():
    """Mostrar credenciales de prueba organizadas"""
    print("\n8. 🔑 CREDENCIALES DE PRUEBA ORGANIZADAS:")
    print("-" * 50)

    print("   👑 SUPERUSUARIOS:")
    print("      • admin@packfy.com / admin123 (Acceso total)")
    print("      • superadmin@packfy.com / admin123 (Acceso total)")
    print()

    print("   🏢 DUEÑOS DE EMPRESA:")
    print("      • dueno@packfy.com / password123 (Solo Packfy Express)")
    print("      • consultor@packfy.com / password123 (Todas las empresas)")
    print()

    print("   👥 OPERADORES:")
    print("      • miami@packfy.com / password123 (Operador Miami)")
    print("      • cuba@packfy.com / password123 (Operador Cuba)")
    print()

    print("   🇨🇺 CLIENTES:")
    print("      • remitente1@packfy.com / password123")
    print("      • destinatario1@cuba.cu / password123")
    print()

    print("   🧪 USUARIOS DE PRUEBA:")
    print("      • empresa@test.cu / password123 (Sin empresa)")
    print("      • cliente@test.cu / password123 (Sin empresa)")


if __name__ == "__main__":
    analizar_estado_usuarios_login()
    analizar_empresas_dominios()
    probar_middleware_tenant()
    probar_autenticacion_usuarios()
    generar_urls_prueba()
    verificar_configuracion_frontend()
    generar_plan_pruebas()
    mostrar_credenciales_prueba()

    print("\n" + "=" * 80)
    print("🎯 ANÁLISIS COMPLETADO")
    print("   Sistema de login multitenancy analizado completamente")
    print("   Revisar los resultados para identificar problemas")
    print("=" * 80)
