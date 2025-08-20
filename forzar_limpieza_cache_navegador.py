#!/usr/bin/env python3
"""
🧹 FORZAR LIMPIEZA COMPLETA DEL CACHE DEL NAVEGADOR
==================================================
Script para generar URLs anti-cache y forzar carga de la nueva interfaz multi-tenant.
"""

import random
import string
import subprocess
import time


def print_banner():
    print("🧹 FORZAR LIMPIEZA COMPLETA DEL CACHE")
    print("=" * 40)
    print()


def generar_cache_busting_url():
    """Generar URL con parámetros anti-cache"""
    timestamp = int(time.time())
    random_str = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=8)
    )
    return f"http://localhost:5173?v={timestamp}&cache_bust={random_str}&force_reload=true"


def verificar_estructura_actual():
    """Verificar que la estructura multi-tenant esté en el container"""
    print("🔍 VERIFICANDO ESTRUCTURA ACTUAL EN CONTAINER:")
    print("-" * 45)

    try:
        # Verificar App.tsx actual
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "head",
                "-n",
                "15",
                "/app/src/App.tsx",
            ],
            capture_output=True,
            text=True,
        )

        if "TenantProvider" in result.stdout:
            print("✅ App.tsx con TenantProvider confirmado")
        else:
            print("❌ ERROR: App.tsx sin TenantProvider")
            return False

        # Verificar TenantSelector
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend",
                "ls",
                "-la",
                "/app/src/components/TenantSelector/",
            ],
            capture_output=True,
            text=True,
        )

        if "TenantSelector.tsx" in result.stdout:
            print("✅ TenantSelector.tsx presente")
        else:
            print("❌ ERROR: TenantSelector.tsx faltante")
            return False

        return True

    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False


def restart_frontend_service():
    """Reiniciar solo el servicio frontend"""
    print("\n🔄 REINICIANDO SERVICIO FRONTEND:")
    print("-" * 35)

    try:
        # Restart solo frontend
        print("🛑 Deteniendo frontend...")
        subprocess.run(["docker", "restart", "packfy-frontend"], check=True)

        print("⏳ Esperando reinicio...")
        time.sleep(10)

        # Verificar que esté ejecutándose
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

        if "Up" in result.stdout:
            print("✅ Frontend reiniciado correctamente")
            return True
        else:
            print("❌ ERROR: Frontend no se reinició")
            return False

    except Exception as e:
        print(f"❌ Error reiniciando frontend: {e}")
        return False


def main():
    print_banner()

    # Verificar estructura
    if not verificar_estructura_actual():
        print("❌ ESTRUCTURA INCORRECTA - Cancelando")
        return 1

    # Reiniciar frontend
    if not restart_frontend_service():
        print("❌ REINICIO FALLÓ - Cancelando")
        return 1

    # Generar URLs anti-cache
    print("\n🌐 URLS ANTI-CACHE GENERADAS:")
    print("-" * 30)

    for i in range(3):
        url = generar_cache_busting_url()
        print(f"🔗 URL {i+1}: {url}")

    print("\n🚀 INSTRUCCIONES DE LIMPIEZA MANUAL:")
    print("-" * 40)
    print("1. 🔄 Cerrar COMPLETAMENTE el navegador")
    print(
        "2. 🗑️ Abrir navegador > F12 > Aplicación > Borrar datos de almacenamiento"
    )
    print("3. 🌐 Abrir una de las URLs anti-cache de arriba")
    print("4. 🔄 Presionar Ctrl+Shift+R (forzar recarga)")
    print("5. 🏢 Verificar que aparezca TenantSelector")

    print("\n⚠️ SI AÚN NO FUNCIONA:")
    print("-" * 20)
    print("🧹 Modo Incógnito/Privado del navegador")
    print("🔄 O usar un navegador diferente")

    return 0


if __name__ == "__main__":
    exit(main())
