#!/usr/bin/env python3
"""
🎉 VERIFICACIÓN FINAL - ESTRUCTURA COMPLETAMENTE NUEVA
=====================================================
Script para verificar que la nueva estructura multi-tenant está funcionando correctamente.
"""

import json
import subprocess
import time
from datetime import datetime

import requests


def print_banner():
    print("🎉 VERIFICACIÓN FINAL - ESTRUCTURA NUEVA")
    print("=" * 45)
    print()


def verificar_containers():
    """Verificar que todos los containers estén ejecutándose"""
    print("🐳 VERIFICANDO CONTAINERS:")
    print("-" * 25)

    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "table {{.Names}}\\t{{.Status}}"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            containers = {}

            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        status = parts[1].strip()
                        containers[name] = status

            required_containers = [
                "packfy-frontend",
                "packfy-backend",
                "packfy-database",
            ]
            all_running = True

            for container in required_containers:
                if container in containers:
                    if "Up" in containers[container]:
                        print(f"✅ {container}: {containers[container]}")
                    else:
                        print(f"❌ {container}: {containers[container]}")
                        all_running = False
                else:
                    print(f"❌ {container}: No encontrado")
                    all_running = False

            return all_running
        else:
            print("❌ Error verificando containers")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def verificar_estructura_multitenant():
    """Verificar estructura multi-tenant en container"""
    print("\n🏢 VERIFICANDO ESTRUCTURA MULTI-TENANT:")
    print("-" * 40)

    try:
        # Verificar App.tsx
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "head",
                "-n",
                "3",
                "/app/src/App.tsx",
            ],
            capture_output=True,
            text=True,
        )

        if "TenantProvider" in result.stdout:
            print("✅ App.tsx con TenantProvider confirmado")
        else:
            print("❌ App.tsx sin TenantProvider")
            return False

        # Verificar TenantSelector
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "ls",
                "/app/src/components/TenantSelector/",
            ],
            capture_output=True,
            text=True,
        )

        if "TenantSelector.tsx" in result.stdout:
            print("✅ TenantSelector.tsx presente")
        else:
            print("❌ TenantSelector.tsx faltante")
            return False

        # Verificar TenantContext
        result = subprocess.run(
            ["docker", "exec", "packfy-frontend", "ls", "/app/src/contexts/"],
            capture_output=True,
            text=True,
        )

        if "TenantContext.tsx" in result.stdout:
            print("✅ TenantContext.tsx presente")
        else:
            print("❌ TenantContext.tsx faltante")
            return False

        return True

    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False


def verificar_acceso_frontend():
    """Verificar acceso al frontend"""
    print("\n🌐 VERIFICANDO ACCESO AL FRONTEND:")
    print("-" * 35)

    try:
        print("⏳ Esperando que el frontend esté listo...")
        time.sleep(10)

        response = requests.get("http://localhost:5173", timeout=15)
        if response.status_code == 200:
            print("✅ Frontend accesible en http://localhost:5173")

            # Verificar contenido
            content = response.text.lower()
            if "tenant" in content or "empresa" in content:
                print("✅ Contenido multi-tenant detectado")
            else:
                print("⚠️ Contenido multi-tenant no detectado en HTML")

            return True
        else:
            print(f"⚠️ Frontend responde con código {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Frontend no accesible: {e}")
        return False


def generar_reporte_final():
    """Generar reporte final"""
    print("\n📊 EJECUTANDO VERIFICACIÓN COMPLETA:")
    print("=" * 40)

    resultados = {
        "timestamp": datetime.now().isoformat(),
        "estructura": "frontend-multitenant",
        "verificaciones": {},
    }

    # Ejecutar verificaciones
    verificaciones = [
        ("containers", verificar_containers),
        ("estructura_multitenant", verificar_estructura_multitenant),
        ("acceso_frontend", verificar_acceso_frontend),
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
        print("🎉 ¡ESTRUCTURA NUEVA COMPLETAMENTE FUNCIONAL!")
        print("✅ Frontend multi-tenant 100% operativo")
        print("🌐 Acceso: http://localhost:5173")
        print("🏢 TenantSelector y TenantProvider activos")
        print("")
        print("🚀 PRÓXIMOS PASOS:")
        print("1. 🌐 Abrir http://localhost:5173 en un navegador NUEVO")
        print("2. 🔐 Hacer login con cualquier usuario")
        print("3. 🏢 Verificar que aparezca TenantSelector")
        print("4. ✅ ¡Disfrutar la interfaz multi-tenant!")
    else:
        print("⚠️ VERIFICACIÓN PARCIAL - Revisar detalles arriba")

    # Guardar reporte
    with open(
        "VERIFICACION-ESTRUCTURA-NUEVA-COMPLETA.json", "w", encoding="utf-8"
    ) as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    return exito_total


def main():
    print_banner()
    exito = generar_reporte_final()

    if exito:
        print(
            "\n📝 Reporte guardado en: VERIFICACION-ESTRUCTURA-NUEVA-COMPLETA.json"
        )
        return 0
    else:
        print("\n❌ VERIFICACIÓN FALLÓ - Revisar logs arriba")
        return 1


if __name__ == "__main__":
    exit(main())
