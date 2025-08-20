#!/usr/bin/env python3
"""
🧹 VERIFICACIÓN LIMPIEZA COMPLETA - OPCIÓN A
===============================================
Script para verificar que la limpieza y consolidación multi-tenant se completó correctamente.
"""

import json
import subprocess
import sys
import time
from datetime import datetime

import requests


def print_banner():
    print("🧹 VERIFICACIÓN LIMPIEZA COMPLETA - OPCIÓN A")
    print("=" * 50)
    print()


def verificar_archivos_legacy():
    """Verificar que no existan archivos legacy"""
    print("📂 VERIFICANDO ELIMINACIÓN DE ARCHIVOS LEGACY:")
    print("-" * 45)

    try:
        # Verificar App.clean.tsx
        try:
            subprocess.run(
                ["type", "frontend\\src\\App.clean.tsx"],
                check=True,
                shell=True,
                capture_output=True,
            )
            print("❌ ERROR: App.clean.tsx aún existe")
            return False
        except subprocess.CalledProcessError:
            print("✅ App.clean.tsx eliminado correctamente")

        # Verificar App-new.tsx
        try:
            subprocess.run(
                ["type", "frontend\\src\\App-new.tsx"],
                check=True,
                shell=True,
                capture_output=True,
            )
            print("❌ ERROR: App-new.tsx aún existe")
            return False
        except subprocess.CalledProcessError:
            print("✅ App-new.tsx eliminado correctamente")

        # Verificar que solo existe App.tsx
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                "Get-ChildItem frontend\\src\\App*.tsx | Select-Object Name",
            ],
            capture_output=True,
            text=True,
            shell=True,
        )

        if result.returncode == 0:
            files = result.stdout.strip()
            print(f"📋 Archivos App existentes:\n{files}")

            if "App.clean.tsx" in files or "App-new.tsx" in files:
                print("❌ ERROR: Archivos legacy aún presentes")
                return False
            elif "App.tsx" in files:
                print("✅ Solo App.tsx multi-tenant presente")
                return True

        return False

    except Exception as e:
        print(f"❌ Error verificando archivos: {e}")
        return False


def verificar_estructura_container():
    """Verificar estructura en container Docker"""
    print("\n🐳 VERIFICANDO ESTRUCTURA EN CONTAINER:")
    print("-" * 40)

    try:
        # Verificar App.tsx en container
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "find",
                "/app/src",
                "-name",
                "App*.tsx",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            files = result.stdout.strip().split("\n")
            print("📋 Archivos App en container:")
            for file in files:
                if file:
                    print(f"   📄 {file}")

            # Verificar que solo existe App.tsx (y App.test.tsx)
            app_files = [
                f
                for f in files
                if f.endswith("App.tsx") and "__tests__" not in f
            ]
            if len(app_files) == 1 and "/app/src/App.tsx" in app_files:
                print("✅ Solo App.tsx multi-tenant en container")
                return True
            else:
                print("❌ ERROR: Estructura incorrecta en container")
                return False
        else:
            print("❌ ERROR: No se pudo verificar container")
            return False

    except Exception as e:
        print(f"❌ Error verificando container: {e}")
        return False


def verificar_componentes_multitenant():
    """Verificar que componentes multi-tenant están presentes"""
    print("\n🏢 VERIFICANDO COMPONENTES MULTI-TENANT:")
    print("-" * 42)

    try:
        # Verificar TenantContext
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "find",
                "/app/src",
                "-name",
                "TenantContext*",
            ],
            capture_output=True,
            text=True,
        )

        if "TenantContext.tsx" in result.stdout:
            print("✅ TenantContext.tsx presente")
        else:
            print("❌ TenantContext.tsx faltante")
            return False

        # Verificar TenantSelector
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "find",
                "/app/src",
                "-name",
                "TenantSelector*",
            ],
            capture_output=True,
            text=True,
        )

        if "TenantSelector.tsx" in result.stdout:
            print("✅ TenantSelector.tsx presente")
        else:
            print("❌ TenantSelector.tsx faltante")
            return False

        # Verificar contenido de App.tsx
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "head",
                "-n",
                "10",
                "/app/src/App.tsx",
            ],
            capture_output=True,
            text=True,
        )

        if "TenantProvider" in result.stdout:
            print("✅ App.tsx contiene TenantProvider")
            return True
        else:
            print("❌ App.tsx no contiene TenantProvider")
            return False

    except Exception as e:
        print(f"❌ Error verificando componentes: {e}")
        return False


def verificar_acceso_frontend():
    """Verificar acceso al frontend"""
    print("\n🌐 VERIFICANDO ACCESO AL FRONTEND:")
    print("-" * 35)

    try:
        # Esperar a que el container esté ready
        print("⏳ Esperando container frontend...")
        time.sleep(5)

        # Verificar salud del container
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                "name=packfy-frontend",
                "--format",
                "table {{.Status}}",
            ],
            capture_output=True,
            text=True,
        )

        if "healthy" in result.stdout.lower() or "up" in result.stdout.lower():
            print("✅ Container frontend saludable")
        else:
            print("⚠️ Container frontend en estado intermedio")

        # Verificar acceso HTTP
        try:
            response = requests.get("http://localhost:5173", timeout=10)
            if response.status_code == 200:
                print("✅ Frontend accesible en http://localhost:5173")
                return True
            else:
                print(f"⚠️ Frontend responde con código {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Frontend no accesible aún: {e}")
            return False

    except Exception as e:
        print(f"❌ Error verificando acceso: {e}")
        return False


def generar_reporte():
    """Generar reporte final de verificación"""
    print("\n📊 EJECUTANDO VERIFICACIÓN COMPLETA:")
    print("=" * 40)

    resultados = {
        "timestamp": datetime.now().isoformat(),
        "verificaciones": {},
    }

    # Ejecutar verificaciones
    verificaciones = [
        ("archivos_legacy", verificar_archivos_legacy),
        ("estructura_container", verificar_estructura_container),
        ("componentes_multitenant", verificar_componentes_multitenant),
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
        print("🎉 ¡LIMPIEZA COMPLETADA EXITOSAMENTE!")
        print("✅ Sistema multi-tenant exclusivo activo")
        print("🌐 Frontend accesible en: http://localhost:5173")
        print("🏢 Estructura multi-tenant consolidada")
    else:
        print("⚠️ VERIFICACIÓN PARCIAL - Revisar detalles arriba")

    # Guardar reporte
    with open(
        "VERIFICACION-LIMPIEZA-COMPLETADA.json", "w", encoding="utf-8"
    ) as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    return exito_total


def main():
    print_banner()
    exito = generar_reporte()

    if exito:
        print("\n🚀 PRÓXIMOS PASOS:")
        print("-" * 15)
        print("1. 🌐 Acceder a http://localhost:5173")
        print("2. 🔐 Hacer login con cualquier usuario")
        print("3. 🏢 Verificar que aparezca TenantSelector")
        print("4. ✅ Confirmar interfaz multi-tenant")
        print(
            "\n📝 Reporte guardado en: VERIFICACION-LIMPIEZA-COMPLETADA.json"
        )
        return 0
    else:
        print("\n❌ VERIFICACIÓN FALLÓ - Revisar logs arriba")
        return 1


if __name__ == "__main__":
    sys.exit(main())
