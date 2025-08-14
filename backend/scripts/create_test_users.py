#!/usr/bin/env python3
"""
Script para crear usuarios de prueba en Packfy Cuba MVP
"""

import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from usuarios.models import Usuario

User = get_user_model()


def create_test_users():
    """Crear usuarios de prueba"""
    try:
        # Crear usuario admin
        admin_user, created = Usuario.objects.get_or_create(
            email="admin@packfy.cu",
            defaults={
                "nombre": "Administrador",
                "apellidos": "Sistema",
                "es_administrador": True,
                "es_staff": True,
                "es_activo": True,
                "tipo_usuario": "ADMIN",
            },
        )

        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            print(f"✅ Usuario admin creado: {admin_user.email}")
        else:
            admin_user.set_password("admin123")
            admin_user.save()
            print(f"🔄 Usuario admin actualizado: {admin_user.email}")

        # Crear usuario empresa
        empresa_user, created = Usuario.objects.get_or_create(
            email="empresa@test.cu",
            defaults={
                "nombre": "Usuario",
                "apellidos": "Empresa",
                "es_administrador": False,
                "es_staff": False,
                "es_activo": True,
                "tipo_usuario": "EMPRESA",
            },
        )

        if created:
            empresa_user.set_password("empresa123")
            empresa_user.save()
            print(f"✅ Usuario empresa creado: {empresa_user.email}")
        else:
            empresa_user.set_password("empresa123")
            empresa_user.save()
            print(f"🔄 Usuario empresa actualizado: {empresa_user.email}")

        # Crear usuario cliente
        cliente_user, created = Usuario.objects.get_or_create(
            email="cliente@test.cu",
            defaults={
                "nombre": "Usuario",
                "apellidos": "Cliente",
                "es_administrador": False,
                "es_staff": False,
                "es_activo": True,
                "tipo_usuario": "CLIENTE",
            },
        )

        if created:
            cliente_user.set_password("cliente123")
            cliente_user.save()
            print(f"✅ Usuario cliente creado: {cliente_user.email}")
        else:
            cliente_user.set_password("cliente123")
            cliente_user.save()
            print(f"🔄 Usuario cliente actualizado: {cliente_user.email}")

        print("\n🎉 USUARIOS CREADOS/ACTUALIZADOS EXITOSAMENTE")
        print("=" * 50)
        print("Admin:   admin@packfy.cu   / admin123")
        print("Empresa: empresa@test.cu  / empresa123")
        print("Cliente: cliente@test.cu  / cliente123")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"❌ Error al crear usuarios: {e}")
        return False


if __name__ == "__main__":
    success = create_test_users()
    sys.exit(0 if success else 1)
