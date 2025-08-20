#!/usr/bin/env python3
"""
🔍 PASO 2: PROBAR FUNCIONALIDADES POR ROL
Verificar permisos y funcionalidades de cada tipo de usuario
"""

import json

import requests


def probar_por_roles():
    print("=" * 70)
    print("🔍 PASO 2: PROBANDO FUNCIONALIDADES POR ROL")
    print("=" * 70)

    base_url = "http://localhost:8000/api"

    # Lista de usuarios por rol
    usuarios_por_rol = [
        ("SUPERADMIN", "superadmin@packfy.com", "super123!"),
        ("DUEÑO", "dueno@packfy.com", "dueno123!"),
        ("OPERADOR MIAMI", "miami@packfy.com", "miami123!"),
        ("OPERADOR CUBA", "cuba@packfy.com", "cuba123!"),
        ("REMITENTE", "remitente1@packfy.com", "remitente123!"),
        ("DESTINATARIO", "destinatario1@cuba.cu", "destinatario123!"),
    ]

    # Endpoints a probar
    endpoints_prueba = [
        ("usuarios", "/usuarios/"),
        ("empresas", "/empresas/"),
        ("mi_empresa", "/empresas/mi_empresa/"),
        ("mis_perfiles", "/empresas/mis_perfiles/"),
        ("envios", "/envios/"),
    ]

    print("📋 PROBANDO ACCESO POR ROL:")
    print("-" * 70)

    for rol, email, password in usuarios_por_rol:
        print(f"\n👤 **{rol}**: {email}")
        print("=" * 40)

        # Login
        login_response = requests.post(
            f"{base_url}/auth/login/",
            json={"email": email, "password": password},
        )

        if login_response.status_code != 200:
            print(f"   ❌ Error de login: {login_response.status_code}")
            continue

        token = login_response.json()["access"]

        # Headers con contexto tenant
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Tenant-Slug": "packfy-express",
        }

        print("   ✅ Login exitoso")

        # Probar cada endpoint
        for nombre, endpoint in endpoints_prueba:
            try:
                response = requests.get(
                    f"{base_url}{endpoint}", headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        count = len(data)
                    elif isinstance(data, dict) and "results" in data:
                        count = len(data["results"])
                    else:
                        count = "obj"

                    print(f"   ✅ {nombre}: {count} elementos")

                elif response.status_code == 403:
                    print(f"   🔒 {nombre}: Sin permisos")
                elif response.status_code == 404:
                    print(f"   ❌ {nombre}: No encontrado")
                else:
                    print(f"   ⚠️ {nombre}: Error {response.status_code}")

            except Exception as e:
                print(f"   💥 {nombre}: Excepción {e}")

        # Información específica del usuario
        try:
            me_response = requests.get(
                f"{base_url}/usuarios/me/", headers=headers
            )
            if me_response.status_code == 200:
                me_data = me_response.json()
                perfiles = me_data.get("perfiles_usuario", [])
                if perfiles:
                    perfil = perfiles[0]
                    print(f"   📋 Rol en sistema: {perfil['rol']}")
                    print(f"   🏢 Empresa: {perfil['empresa']['nombre']}")
                else:
                    print("   ⚠️ Sin perfiles asignados")
        except:
            print("   💥 Error obteniendo perfil")


if __name__ == "__main__":
    probar_por_roles()
