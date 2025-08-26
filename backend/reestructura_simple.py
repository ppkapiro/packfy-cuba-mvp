#!/usr/bin/env python
import os
import sys

import django

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario

# PASO 1: Configurar dominios
print("PASO 1: Configurando dominios...")
mapeo = {
    "Cuba Express Cargo": "cubaexpress.com",
    "Habana Premium Logistics": "habanapremium.com",
    "Miami Shipping Express": "miamishipping.com",
    "Packfy Express": "packfy.com",
}

for nombre, dominio in mapeo.items():
    empresa = Empresa.objects.get(nombre=nombre, activo=True)
    empresa.dominio = dominio
    empresa.save()
    print(f"Configurado: {nombre} -> {dominio}")

print("\nPASO 2: Creando usuarios admin...")

# PASO 2: Crear usuarios admin
for empresa in Empresa.objects.filter(activo=True, dominio__isnull=False):
    email = f"admin@{empresa.dominio}"

    usuario, created = Usuario.objects.get_or_create(
        email=email,
        defaults={
            "username": email,
            "first_name": "Admin",
            "last_name": empresa.nombre,
            "is_active": True,
            "is_staff": True,
            "is_superuser": False,
            "password": make_password("admin123"),
        },
    )

    if created:
        print(f"Usuario creado: {email}")
    else:
        print(f"Usuario ya existe: {email}")

    # Crear perfil
    perfil, created = PerfilUsuario.objects.get_or_create(
        usuario=usuario,
        empresa=empresa,
        defaults={"rol": "admin_empresa", "activo": True},
    )

print("\nPASO 3: Configurando superadmin único...")

# PASO 3: Configurar superadmin
superadmin = Usuario.objects.get(email="superadmin@packfy.com")
superadmin.is_superuser = True
superadmin.is_staff = True
superadmin.save()

# Dar acceso a todas las empresas
for empresa in Empresa.objects.filter(activo=True):
    perfil, created = PerfilUsuario.objects.get_or_create(
        usuario=superadmin,
        empresa=empresa,
        defaults={"rol": "super_admin", "activo": True},
    )
    if not created and perfil.rol != "super_admin":
        perfil.rol = "super_admin"
        perfil.save()

# Remover superuser de otros
otros = Usuario.objects.filter(is_superuser=True).exclude(email="superadmin@packfy.com")
for user in otros:
    user.is_superuser = False
    user.save()
    print(f"Removido superuser de: {user.email}")

print("\nREESTRUCTURACIÓN COMPLETADA!")
print("\nCredenciales creadas:")
print("- admin@cubaexpress.com / admin123")
print("- admin@habanapremium.com / admin123")
print("- admin@miamishipping.com / admin123")
print("- admin@packfy.com / admin123")
print("\nSuperadmin único: superadmin@packfy.com")
