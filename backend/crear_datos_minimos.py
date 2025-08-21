#!/usr/bin/env python
"""
Script para crear datos básicos: empresa y usuario dueño
"""

import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from empresas.models import Empresa, PerfilEmpresa

User = get_user_model()


def main():
    print("🚀 CREANDO DATOS BÁSICOS DEL SISTEMA...")
    print()

    # 1. Crear empresa principal
    print("🏢 Creando empresa principal...")
    empresa, created = Empresa.objects.get_or_create(
        slug="packfy-express-cuba",
        defaults={
            "nombre": "PackFy Express Cuba",
            "activa": True,
            "telefono": "+53 5 123-4567",
            "direccion": "La Habana, Cuba",
        },
    )

    if created:
        print(f"✅ Empresa creada: {empresa.nombre}")
    else:
        print(f"ℹ️ Empresa ya existía: {empresa.nombre}")

    # 2. Crear usuario dueño
    print("👤 Creando usuario dueño...")
    usuario, created = User.objects.get_or_create(
        email="dueno@packfy.com",
        defaults={
            "nombre": "Carlos",
            "apellido": "Rodriguez",
            "telefono": "+53 5 123-4567",
            "password": make_password("dueno123!"),
            "is_staff": True,
            "is_superuser": True,
        },
    )

    if created:
        print(f"✅ Usuario creado: {usuario.email}")
    else:
        print(f"ℹ️ Usuario ya existía: {usuario.email}")

    # 3. Crear perfil de empresa para el dueño
    print("🎭 Creando perfil de empresa...")
    perfil, created = PerfilEmpresa.objects.get_or_create(
        usuario=usuario,
        empresa=empresa,
        defaults={"rol": "dueno", "activo": True},
    )

    if created:
        print(f"✅ Perfil creado: {perfil.rol} en {perfil.empresa.nombre}")
    else:
        print(f"ℹ️ Perfil ya existía: {perfil.rol} en {perfil.empresa.nombre}")

    print()
    print("🎉 DATOS BÁSICOS CREADOS EXITOSAMENTE!")
    print()
    print("📋 RESUMEN:")
    print(f"   🏢 Empresa: {empresa.nombre} (slug: {empresa.slug})")
    print(f"   👤 Usuario: {usuario.email}")
    print(f"   🎭 Rol: {perfil.rol}")
    print()
    print("🔑 CREDENCIALES DE ACCESO:")
    print(f"   Email: {usuario.email}")
    print(f"   Password: dueno123!")
    print()


if __name__ == "__main__":
    main()
