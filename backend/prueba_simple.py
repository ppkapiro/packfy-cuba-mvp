#!/usr/bin/env python
"""
Script de prueba simplificado para verificar conectividad
"""
import json

import requests

# Configuración
BASE_URL = "http://localhost:8000"
USUARIO_PRUEBA = {"email": "admin@packfy.com", "password": "admin123"}


def test_simple():
    print("🚀 PRUEBA SIMPLIFICADA MULTITENANCY")
    print("=" * 50)

    # 1. Probar backend básico
    print("\n1. Probando backend básico...")
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 401]:  # 401 es normal sin auth
            print("   ✅ Backend responde")
        else:
            print(f"   ❌ Backend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error conectando: {e}")
        return False

    # 2. Probar login
    print("\n2. Probando login...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json=USUARIO_PRUEBA,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")

        if response.status_code == 200:
            data = response.json()
            token = data.get("access")
            if token:
                print(f"   ✅ Login exitoso - Token: {token[:20]}...")
                return token

        print(f"   ❌ Login falló")
        return False

    except Exception as e:
        print(f"   ❌ Error en login: {e}")
        return False


if __name__ == "__main__":
    result = test_simple()
    print(f"\n🎯 Resultado final: {'✅ ÉXITO' if result else '❌ FALLÓ'}")
