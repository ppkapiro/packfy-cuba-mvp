#!/usr/bin/env python
"""
Script simple para crear datos básicos de prueba
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def main():
    print("🚀 Creando datos básicos de prueba...")

    # Crear usuario administrador
    admin, created = Usuario.objects.get_or_create(
        email="admin@packfy.cu",
        defaults={
            "nombre": "Administrador Sistema",
            "telefono": "+53 5 123-4567",
            "password": make_password("password123"),
            "is_staff": True,
            "is_superuser": True,
        },
    )
    print(f'✅ Usuario admin: {"creado" if created else "ya existía"}')

    # Verificar empresas creadas por la migración
    empresas = Empresa.objects.all()
    print(f"🏢 Empresas disponibles: {empresas.count()}")
    for empresa in empresas:
        print(f"  - {empresa.nombre} (slug: {empresa.slug})")

        # Crear perfil de admin en cada empresa
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=admin, empresa=empresa, defaults={"rol": "dueno"}
        )
        print(f'    👤 Perfil admin: {"creado" if created else "ya existía"}')

    print("\n✅ Datos de prueba creados exitosamente")
    print("🔑 Credenciales de acceso:")
    print("   Email: admin@packfy.cu")
    print("   Contraseña: password123")


if __name__ == "__main__":
    main()
