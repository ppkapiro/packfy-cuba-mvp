#!/usr/bin/env python3
"""
Prueba simple de restricciones de roles
"""

import os

import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from empresas.models import Empresa, PerfilUsuario


def main():
    print("🚀 PRUEBA SIMPLE DE RESTRICCIONES DE ROLES")
    print("=" * 50)

    # Obtener empresa y usuarios
    empresa = Empresa.objects.get(slug="packfy-express")
    dueno = (
        PerfilUsuario.objects.filter(empresa=empresa, rol="dueno")
        .first()
        .usuario
    )
    operador = (
        PerfilUsuario.objects.filter(empresa=empresa, rol="operador_miami")
        .first()
        .usuario
    )

    print(f"🏢 Empresa: {empresa.nombre}")
    print(f"👤 Dueño: {dueno.get_full_name()}")
    print(f"👤 Operador: {operador.get_full_name()}")

    # Intentar autenticación
    print("\n🔐 Probando autenticación...")

    # Login del dueño
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        {"username": dueno.username, "password": "packfy123"},
    )

    if response.status_code == 200:
        token_dueno = response.json()["access"]
        print(f"✅ Login dueño exitoso")

        # Probar acceso a envíos
        headers = {
            "Authorization": f"Bearer {token_dueno}",
            "X-Tenant-Slug": empresa.slug,
        }

        response = requests.get(
            "http://localhost:8000/api/envios/", headers=headers
        )
        if response.status_code == 200:
            envios = response.json()
            count = (
                len(envios["results"]) if "results" in envios else len(envios)
            )
            print(f"✅ Dueño ve {count} envíos")
        else:
            print(f"❌ Error acceso envíos: {response.status_code}")

    else:
        print(f"❌ Error login dueño: {response.status_code}")
        print(response.text)

    print("\n✅ Prueba básica completada")


if __name__ == "__main__":
    main()
