#!/usr/bin/env python3
"""
🔍 PROBAR ENDPOINTS CON CONTEXTO DE TENANT
Usar header X-Tenant-Slug para acceder a los endpoints
"""

import json

import requests


def probar_con_tenant():
    print("=" * 60)
    print("🔍 PROBANDO ENDPOINTS CON CONTEXTO DE TENANT")
    print("=" * 60)

    base_url = "http://localhost:8000/api"

    # Login como superadmin
    login_response = requests.post(
        f"{base_url}/auth/login/",
        json={"email": "superadmin@packfy.com", "password": "super123!"},
    )

    if login_response.status_code != 200:
        print("❌ Error de login")
        return

    token = login_response.json()["access"]

    # Headers con tenant context
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-Slug": "packfy-express",  # Slug de la empresa
    }

    print("✅ Login exitoso como superadmin")
    print("🏢 Usando tenant: packfy-express")
    print("\n📡 PROBANDO ENDPOINTS CON CONTEXTO:")
    print("-" * 60)

    endpoints = [
        ("usuarios", "/usuarios/"),
        ("empresas", "/empresas/"),
        ("envios", "/envios/"),
        ("historial-estados", "/historial-estados/"),
    ]

    for nombre, endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            print(f"\n📂 {nombre.upper()}: {endpoint}")
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"   📊 Elementos: {len(data)}")
                    if data and len(data) > 0:
                        print(
                            f"   🔍 Ejemplo: {list(data[0].keys()) if isinstance(data[0], dict) else 'N/A'}"
                        )
                elif isinstance(data, dict):
                    if "results" in data:
                        print(f"   📊 Resultados: {len(data['results'])}")
                        print(f"   📄 Total: {data.get('count', 'N/A')}")
                        if data["results"]:
                            print(
                                f"   🔍 Campos: {list(data['results'][0].keys()) if data['results'] else 'N/A'}"
                            )
                    else:
                        print(f"   🔑 Keys: {list(data.keys())}")
            elif response.status_code == 403:
                print("   🔒 Sin permisos")
            elif response.status_code == 404:
                print("   ❌ No encontrado")
            else:
                print(f"   ⚠️ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   📄 Error: {error_data}")
                except:
                    print(f"   📄 Texto: {response.text[:100]}")

        except Exception as e:
            print(f"   💥 Excepción: {e}")

    # Probar endpoints específicos de empresas
    print("\n🏢 ENDPOINTS ESPECÍFICOS DE EMPRESAS:")
    print("-" * 60)

    empresa_endpoints = [
        ("mi_empresa", "/empresas/mi_empresa/"),
        ("mis_perfiles", "/empresas/mis_perfiles/"),
    ]

    for nombre, endpoint in empresa_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            print(f"\n📂 {nombre.upper()}: {endpoint}")
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   📄 Respuesta: {json.dumps(data, indent=2)}")
            else:
                print(f"   ❌ Error: {response.status_code}")

        except Exception as e:
            print(f"   💥 Excepción: {e}")


if __name__ == "__main__":
    probar_con_tenant()
