#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO COMPLETO DEL FRONTEND

Este script realiza un diagnóstico exhaustivo del estado actual del frontend
para identificar qué está fallando y crear un plan de reparación.
"""

import json
import subprocess
import time
from datetime import datetime

import requests


def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")


def test_backend_api():
    """Probar conectividad y endpoints del backend"""
    log("🔍 Probando conectividad del backend...")

    try:
        # Test de conectividad básica
        response = requests.get("http://localhost:8000/api/", timeout=5)
        log(f"✅ Backend respondiendo - Status: {response.status_code}")

        # Test de endpoint de login
        login_response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"email": "admin@packfy.com", "password": "admin123!"},
            timeout=5,
        )

        if login_response.status_code == 200:
            token_data = login_response.json()
            log("✅ Login funcionando - Token obtenido")

            # Test de endpoint de usuario actual
            me_response = requests.get(
                "http://localhost:8000/api/usuarios/me/",
                headers={"Authorization": f"Bearer {token_data['access']}"},
                timeout=5,
            )

            if me_response.status_code == 200:
                user_data = me_response.json()
                log(
                    f"✅ /usuarios/me/ funcionando - Usuario: {user_data.get('email', 'Unknown')}"
                )

                if "empresas" in user_data:
                    log(
                        f"✅ Empresas en respuesta: {len(user_data['empresas'])} empresas"
                    )
                else:
                    log(
                        "❌ No hay campo 'empresas' en respuesta de /usuarios/me/"
                    )

                return True, token_data["access"]
            else:
                log(
                    f"❌ /usuarios/me/ falló - Status: {me_response.status_code}"
                )
        else:
            log(f"❌ Login falló - Status: {login_response.status_code}")
            log(f"Response: {login_response.text}")

    except Exception as e:
        log(f"❌ Error conectando al backend: {e}")

    return False, None


def test_frontend_pages():
    """Probar accesibilidad de páginas del frontend"""
    log("🔍 Probando páginas del frontend...")

    pages = ["/", "/login", "/dashboard", "/envios", "/usuarios"]

    results = {}

    for page in pages:
        try:
            response = requests.get(f"http://localhost:5173{page}", timeout=10)
            if response.status_code == 200:
                log(f"✅ Página {page} accesible")
                results[page] = True
            else:
                log(f"❌ Página {page} falló - Status: {response.status_code}")
                results[page] = False
        except Exception as e:
            log(f"❌ Error accediendo a {page}: {e}")
            results[page] = False

    return results


def check_docker_containers():
    """Verificar estado de containers Docker"""
    log("🔍 Verificando containers Docker...")

    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
        )

        containers = []
        for line in result.stdout.strip().split("\n"):
            if line:
                containers.append(json.loads(line))

        for container in containers:
            name = container.get("Names", "Unknown")
            status = container.get("Status", "Unknown")
            if "healthy" in status.lower():
                log(f"✅ Container {name}: {status}")
            elif "unhealthy" in status.lower():
                log(f"⚠️ Container {name}: {status}")
            else:
                log(f"ℹ️ Container {name}: {status}")

        return True

    except Exception as e:
        log(f"❌ Error verificando containers: {e}")
        return False


def check_frontend_build():
    """Verificar si el frontend tiene errores de build"""
    log("🔍 Verificando build del frontend...")

    try:
        # Obtener logs recientes del container frontend
        result = subprocess.run(
            ["docker", "logs", "packfy-frontend", "--tail", "20"],
            capture_output=True,
            text=True,
        )

        logs = result.stdout + result.stderr

        # Buscar errores comunes
        if "error" in logs.lower() or "failed" in logs.lower():
            log("❌ Errores detectados en logs del frontend:")
            for line in logs.split("\n")[-10:]:
                if line.strip():
                    log(f"  {line}")
        else:
            log("✅ No se detectaron errores en logs del frontend")

        return True

    except Exception as e:
        log(f"❌ Error verificando logs del frontend: {e}")
        return False


def test_tenant_context():
    """Probar funcionalidad específica del TenantContext"""
    log("🔍 Probando funcionalidad TenantContext...")

    backend_ok, token = test_backend_api()

    if not backend_ok or not token:
        log("❌ No se puede probar TenantContext sin acceso al backend")
        return False

    try:
        # Verificar empresas endpoint
        empresas_response = requests.get(
            "http://localhost:8000/api/empresas/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )

        if empresas_response.status_code == 200:
            empresas = empresas_response.json()
            log(
                f"✅ Endpoint /empresas/ funcionando - {len(empresas.get('results', []))} empresas"
            )
        else:
            log(
                f"❌ Endpoint /empresas/ falló - Status: {empresas_response.status_code}"
            )

        return True

    except Exception as e:
        log(f"❌ Error probando TenantContext: {e}")
        return False


def create_diagnostic_report():
    """Crear reporte completo de diagnóstico"""
    log("📋 Iniciando diagnóstico completo del sistema...")

    report = {
        "timestamp": datetime.now().isoformat(),
        "backend_api": False,
        "frontend_pages": {},
        "docker_containers": False,
        "frontend_build": False,
        "tenant_context": False,
        "issues": [],
        "recommendations": [],
    }

    # Test 1: Backend API
    log("\n" + "=" * 50)
    log("TEST 1: BACKEND API")
    log("=" * 50)
    backend_ok, token = test_backend_api()
    report["backend_api"] = backend_ok

    if not backend_ok:
        report["issues"].append(
            "Backend API no está funcionando correctamente"
        )
        report["recommendations"].append(
            "Verificar configuración del backend y base de datos"
        )

    # Test 2: Docker Containers
    log("\n" + "=" * 50)
    log("TEST 2: DOCKER CONTAINERS")
    log("=" * 50)
    containers_ok = check_docker_containers()
    report["docker_containers"] = containers_ok

    if not containers_ok:
        report["issues"].append("Problemas con containers Docker")
        report["recommendations"].append(
            "Reiniciar containers con docker-compose down && docker-compose up"
        )

    # Test 3: Frontend Build
    log("\n" + "=" * 50)
    log("TEST 3: FRONTEND BUILD")
    log("=" * 50)
    build_ok = check_frontend_build()
    report["frontend_build"] = build_ok

    # Test 4: Frontend Pages
    log("\n" + "=" * 50)
    log("TEST 4: FRONTEND PAGES")
    log("=" * 50)
    pages_result = test_frontend_pages()
    report["frontend_pages"] = pages_result

    failed_pages = [page for page, ok in pages_result.items() if not ok]
    if failed_pages:
        report["issues"].append(
            f"Páginas del frontend no accesibles: {failed_pages}"
        )
        report["recommendations"].append(
            "Verificar rutas y configuración del frontend"
        )

    # Test 5: TenantContext
    log("\n" + "=" * 50)
    log("TEST 5: TENANT CONTEXT")
    log("=" * 50)
    tenant_ok = test_tenant_context()
    report["tenant_context"] = tenant_ok

    if not tenant_ok:
        report["issues"].append(
            "TenantContext no está funcionando correctamente"
        )
        report["recommendations"].append(
            "Revisar implementación de TenantContext y APIs de empresas"
        )

    # Resumen final
    log("\n" + "=" * 50)
    log("RESUMEN DEL DIAGNÓSTICO")
    log("=" * 50)

    all_ok = all(
        [
            report["backend_api"],
            report["docker_containers"],
            report["frontend_build"],
            all(report["frontend_pages"].values()),
            report["tenant_context"],
        ]
    )

    if all_ok:
        log(
            "🎉 ¡Todos los tests pasaron! El sistema parece estar funcionando correctamente."
        )
    else:
        log("⚠️ Se detectaron problemas que requieren atención:")
        for issue in report["issues"]:
            log(f"  - {issue}")

        log("\n📋 Recomendaciones:")
        for rec in report["recommendations"]:
            log(f"  - {rec}")

    # Guardar reporte
    with open(
        "diagnostico_frontend_completo.json", "w", encoding="utf-8"
    ) as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    log(f"\n💾 Reporte guardado en: diagnostico_frontend_completo.json")

    return report


if __name__ == "__main__":
    create_diagnostic_report()
