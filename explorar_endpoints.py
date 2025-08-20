#!/usr/bin/env python3
"""
🔍 EXPLORACIÓN COMPLETA DE ENDPOINTS
Verificar todas las funcionalidades disponibles en el backend
"""

import json

import requests


def explorar_endpoints():
    print("=" * 60)
    print("🔍 EXPLORACIÓN COMPLETA DE ENDPOINTS")
    print("=" * 60)

    base_url = "http://localhost:8000/api"

    # Login como superadmin para tener acceso completo
    login_response = requests.post(
        f"{base_url}/auth/login/",
        json={"email": "superadmin@packfy.com", "password": "super123!"},
    )

    if login_response.status_code != 200:
        print("❌ Error de login")
        return

    token = login_response.json()["access"]
    headers = {"Authorization": f"Bearer {token}"}

    print("✅ Login exitoso como superadmin")
    print("\n📡 EXPLORANDO ENDPOINTS DISPONIBLES:")
    print("-" * 60)

    # Obtener endpoints desde la API root
    try:
        api_root = requests.get(f"{base_url}/", headers=headers)
        if api_root.status_code == 200:
            endpoints = api_root.json()
            print("\n🌐 ENDPOINTS DESDE API ROOT:")
            for key, url in endpoints.items():
                print(f"   📍 {key}: {url}")

        # Probar endpoints específicos
        endpoints_a_probar = [
            ("usuarios", "/usuarios/"),
            ("empresas", "/empresas/"),
            ("envios", "/envios/"),
            ("historial-estados", "/historial-estados/"),
            ("sistema-info", "/sistema-info/"),
        ]

        print("\n🧪 PROBANDO ENDPOINTS ESPECÍFICOS:")
        print("-" * 60)

        for nombre, endpoint in endpoints_a_probar:
            try:
                response = requests.get(
                    f"{base_url}{endpoint}", headers=headers
                )
                print(f"\n📂 {nombre.upper()}: {endpoint}")
                print(f"   Status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"   📊 Elementos: {len(data)}")
                        if data and len(data) > 0:
                            print(
                                f"   🔍 Primer elemento: {list(data[0].keys()) if isinstance(data[0], dict) else 'N/A'}"
                            )
                    elif isinstance(data, dict):
                        if "results" in data:
                            print(f"   📊 Resultados: {len(data['results'])}")
                            print(f"   📄 Total: {data.get('count', 'N/A')}")
                        else:
                            print(f"   🔑 Keys: {list(data.keys())}")
                elif response.status_code == 404:
                    print("   ❌ Endpoint no encontrado")
                elif response.status_code == 403:
                    print("   🔒 Sin permisos")
                else:
                    print(f"   ⚠️ Error: {response.status_code}")

            except Exception as e:
                print(f"   💥 Excepción: {e}")

        # Información del sistema
        print("\n🔧 INFORMACIÓN DEL SISTEMA:")
        print("-" * 60)
        try:
            sistema_response = requests.get(
                f"{base_url}/sistema-info/", headers=headers
            )
            if sistema_response.status_code == 200:
                sistema_info = sistema_response.json()
                for key, value in sistema_info.items():
                    print(f"   📋 {key}: {value}")
            else:
                print(
                    f"   ❌ No se pudo obtener info del sistema: {sistema_response.status_code}"
                )
        except Exception as e:
            print(f"   💥 Error: {e}")

    except Exception as e:
        print(f"💥 Error general: {e}")


if __name__ == "__main__":
    explorar_endpoints()
