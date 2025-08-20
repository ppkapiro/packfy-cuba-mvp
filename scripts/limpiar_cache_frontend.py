#!/usr/bin/env python
"""
Script para limpiar cache y forzar recarga del frontend moderno
"""
import time
import webbrowser

import requests


def limpiar_cache_frontend():
    """Limpia el cache y fuerza la recarga del frontend"""

    print("🧹 LIMPIEZA DE CACHE FRONTEND")
    print("=" * 50)

    # URLs con cache busting
    timestamp = str(int(time.time()))
    urls_cache_busting = [
        f"http://localhost:5173/?v={timestamp}",
        f"http://localhost:5173/?clear_cache={timestamp}",
        f"http://localhost:5173/?refresh={timestamp}",
    ]

    print("📋 Verificando estado del frontend...")
    try:
        response = requests.get("http://localhost:5173/", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend responde correctamente")

            # Verificar si el contenido es moderno
            content = response.text
            if "TenantSelector" in content or "react" in content.lower():
                print("✅ Contenido moderno detectado")
            else:
                print("⚠️  Contenido puede estar cacheado")

        else:
            print(f"❌ Frontend no responde: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return

    print("\n🔄 URLs para limpiar cache:")
    for i, url in enumerate(urls_cache_busting, 1):
        print(f"   {i}. {url}")

    print("\n💡 Instrucciones para limpiar cache manualmente:")
    print("   1. 🌐 Abre: http://localhost:5173")
    print("   2. 🔄 Presiona Ctrl+F5 (recarga fuerte)")
    print("   3. 🕵️ Abre modo incógnito/privado")
    print("   4. 🧹 Borra datos de navegador para localhost")
    print("   5. 🔧 F12 -> Network tab -> Disable cache")

    print("\n🎯 Características del frontend moderno:")
    print("   ✅ Login con email/password")
    print("   ✅ Dashboard con estadísticas")
    print("   ✅ Selector de empresa (multi-tenant)")
    print("   ✅ Gestión de envíos moderna")
    print("   ✅ Interfaz React con componentes TSX")

    print("\n🔍 Si sigues viendo contenido viejo:")
    print("   1. Verifica que no tienes otra app en puerto 5173")
    print("   2. Revisa extensiones de navegador")
    print("   3. Prueba con otro navegador")
    print("   4. Reinicia completamente Docker")

    # Abrir automáticamente con cache busting
    print("\n🚀 Abriendo frontend con cache busting...")
    try:
        webbrowser.open(urls_cache_busting[0])
        print(f"   🌐 Abierto: {urls_cache_busting[0]}")
    except:
        print("   ⚠️  No se pudo abrir automáticamente")


if __name__ == "__main__":
    limpiar_cache_frontend()
