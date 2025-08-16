#!/usr/bin/env python
"""
Script para crear usuario admin
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_development")
django.setup()

from usuarios.models import Usuario

try:
    # Crear o actualizar usuario admin
    user, created = Usuario.objects.get_or_create(
        email="admin@packfy.cu",  # USERNAME_FIELD es email!
        defaults={
            "username": "admin",  # username separado
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )

    # Establecer contraseña
    user.set_password("admin123")
    user.save()

    print(
        f"✅ Usuario admin {'creado' if created else 'actualizado'} exitosamente"
    )
    print(f"Email (login): {user.email}")
    print(f"Username: {user.username}")
    print(f"Is Active: {user.is_active}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")

    # Listar todos los usuarios
    print("\n📋 Usuarios existentes:")
    for u in Usuario.objects.all():
        print(
            f"- Email: {u.email}, Username: {u.username} - Active: {u.is_active}"
        )

except Exception as e:
    print(f"❌ Error: {e}")
