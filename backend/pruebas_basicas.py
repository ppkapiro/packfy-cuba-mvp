#!/usr/bin/env python
"""
🧪 PRUEBAS BÁSICAS MULTITENANCY
Verificación rápida del sistema
"""
import json
from datetime import datetime

import requests


def test_backend_health():
    """Prueba básica de conectividad del backend"""
    print("🔍 Probando backend...")
    try:
        response = requests.get("http://localhost:8000/api/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Backend responde correctamente")
            return True
        else:
            print(f"   ❌ Backend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_frontend_health():
    """Prueba básica de conectividad del frontend"""
    print("🌐 Probando frontend...")
    try:
        response = requests.get("http://localhost:5173", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Frontend responde correctamente")
            return True
        else:
            print(f"   ❌ Frontend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    print("🚀 PRUEBAS BÁSICAS MULTITENANCY")
    print("=" * 40)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Pruebas básicas
    backend_ok = test_backend_health()
    frontend_ok = test_frontend_health()

    print("\n" + "=" * 40)
    print("📊 RESUMEN:")
    print(f"Backend:  {'✅' if backend_ok else '❌'}")
    print(f"Frontend: {'✅' if frontend_ok else '❌'}")

    if backend_ok and frontend_ok:
        print("\n🎉 Sistema básico funcionando!")
        print("🔗 URLs disponibles:")
        print("   Backend:  http://localhost:8000/api/")
        print("   Frontend: http://localhost:5173")
    else:
        print("\n⚠️ Hay problemas en el sistema")


if __name__ == "__main__":
    main()
