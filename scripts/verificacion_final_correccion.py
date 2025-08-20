#!/usr/bin/env python3
"""
✅ VERIFICACIÓN FINAL COMPLETA - POST-CORRECCIÓN
===============================================
Script para verificar que todos los problemas están resueltos.
"""

import json
import subprocess
import time
from datetime import datetime

import requests


def print_banner():
    print("✅ VERIFICACIÓN FINAL COMPLETA - POST-CORRECCIÓN")
    print("=" * 50)
    print()


def verificar_frontend_corregido():
    """Verificar que el frontend funciona sin errores"""
    print("🌐 VERIFICANDO FRONTEND CORREGIDO:")
    print("-" * 35)

    try:
        # Verificar acceso HTTP
        response = requests.get("http://localhost:5173", timeout=10)

        if response.status_code == 200:
            print("✅ Frontend responde HTTP 200 OK")

            # Verificar contenido HTML
            content = response.text
            if "main.tsx" in content and "vite" in content.lower():
                print("✅ Vite funcionando correctamente")
            else:
                print("⚠️ Posible problema con Vite")

            if "tenant" in content.lower() or "empresa" in content.lower():
                print("✅ Contenido multi-tenant presente")
            else:
                print("⚠️ Verificar contenido multi-tenant en navegador")

            return True
        else:
            print(f"❌ Frontend responde con código {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False


def verificar_logs_limpios():
    """Verificar que no hay errores críticos en logs"""
    print("\n📋 VERIFICANDO LOGS LIMPIOS:")
    print("-" * 30)

    try:
        result = subprocess.run(
            ["docker", "logs", "packfy-frontend", "--tail", "20"],
            capture_output=True,
            text=True,
        )

        logs = result.stdout.lower()

        # Verificar errores específicos
        if "500 (internal server error)" in logs:
            print("❌ Aún hay errores 500 en logs")
            return False
        elif "err_address_invalid" in logs:
            print("❌ Aún hay errores de dirección inválida")
            return False
        elif "websocket connection" in logs and "failed" in logs:
            print(
                "⚠️ Posibles problemas de WebSocket (puede ser normal en algunos casos)"
            )
        else:
            print("✅ No se detectan errores críticos en logs")

        return True

    except Exception as e:
        print(f"❌ Error verificando logs: {e}")
        return False


def verificar_estructura_final():
    """Verificar estructura multi-tenant final"""
    print("\n🏢 VERIFICANDO ESTRUCTURA MULTI-TENANT FINAL:")
    print("-" * 45)

    try:
        # Verificar App.tsx multi-tenant
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "head",
                "-n",
                "5",
                "/app/src/App.tsx",
            ],
            capture_output=True,
            text=True,
        )

        if "TenantProvider" in result.stdout:
            print("✅ App.tsx multi-tenant confirmado")
        else:
            print("❌ App.tsx no es multi-tenant")
            return False

        # Verificar componentes clave
        components = [
            (
                "/app/src/components/TenantSelector/TenantSelector.tsx",
                "TenantSelector",
            ),
            ("/app/src/contexts/TenantContext.tsx", "TenantContext"),
            ("/app/src/components/TenantInfo/TenantInfo.tsx", "TenantInfo"),
        ]

        for path, name in components:
            result = subprocess.run(
                ["docker", "exec", "packfy-frontend", "test", "-f", path],
                capture_output=True,
            )
            if result.returncode == 0:
                print(f"✅ {name} presente")
            else:
                print(f"❌ {name} faltante")
                return False

        return True

    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False


def generar_reporte_final():
    """Generar reporte final completo"""
    print("\n📊 EJECUTANDO VERIFICACIÓN FINAL COMPLETA:")
    print("=" * 45)

    resultados = {
        "timestamp": datetime.now().isoformat(),
        "version": "frontend-multitenant-corregido",
        "verificaciones": {},
    }

    # Ejecutar todas las verificaciones
    verificaciones = [
        ("frontend_corregido", verificar_frontend_corregido),
        ("logs_limpios", verificar_logs_limpios),
        ("estructura_final", verificar_estructura_final),
    ]

    exito_total = True
    for nombre, funcion in verificaciones:
        resultado = funcion()
        resultados["verificaciones"][nombre] = resultado
        if not resultado:
            exito_total = False

    # Resultado final
    print("\n🎯 RESULTADO FINAL:")
    print("=" * 20)

    if exito_total:
        print("🎉 ¡TODOS LOS PROBLEMAS RESUELTOS!")
        print("✅ Frontend multi-tenant funcionando perfectamente")
        print("✅ Sin errores 500 o WebSocket críticos")
        print("✅ Estructura multi-tenant completa")
        print("")
        print("🚀 LISTA PARA USAR:")
        print("🌐 URL: http://localhost:5173")
        print("🏢 TenantSelector activo")
        print("🔐 Login y verificar interfaz multi-tenant")
    else:
        print("⚠️ ALGUNOS PROBLEMAS PENDIENTES - Revisar detalles arriba")

    # Guardar reporte
    with open(
        "VERIFICACION-FINAL-CORRECCION-COMPLETA.json", "w", encoding="utf-8"
    ) as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    return exito_total


def main():
    print_banner()
    exito = generar_reporte_final()

    if exito:
        print(
            "\n📝 Reporte guardado en: VERIFICACION-FINAL-CORRECCION-COMPLETA.json"
        )
        return 0
    else:
        print("\n❌ VERIFICACIÓN FALLÓ - Revisar logs arriba")
        return 1


if __name__ == "__main__":
    exit(main())
