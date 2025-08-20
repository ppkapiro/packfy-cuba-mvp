#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 REPARACIÓN URGENTE: PERFILES Y PERMISOS

Arregla los perfiles de empresa y permisos que no se crearon correctamente.
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario

print("🔧 REPARANDO PERFILES Y PERMISOS...")
print("=" * 50)

# 1. Verificar estado actual
print("📊 Estado actual:")
print(f"  Usuarios: {Usuario.objects.count()}")
print(f"  Empresas: {Empresa.objects.count()}")
print(f"  PerfilUsuario: {PerfilUsuario.objects.count()}")

# 2. Arreglar superadmin
print("\n👑 Arreglando superadmin...")
try:
    superadmin = Usuario.objects.get(email="superadmin@packfy.com")
    superadmin.is_staff = True
    superadmin.is_superuser = True
    superadmin.save()
    print(
        f"✅ Superadmin configurado: staff={superadmin.is_staff}, super={superadmin.is_superuser}"
    )
except Usuario.DoesNotExist:
    print("❌ Superadmin no encontrado")

# 3. Crear empresa si no existe
print("\n🏢 Verificando empresa...")
empresa, created = Empresa.objects.get_or_create(
    slug="packfy-express",
    defaults={"nombre": "Packfy Express", "activo": True},
)

if created:
    print(f"✅ Empresa creada: {empresa.nombre}")
else:
    print(f"ℹ️ Empresa existente: {empresa.nombre}")

# 4. Crear perfiles que faltan
print("\n📋 Creando perfiles de usuario...")

perfiles_config = [
    ("dueno@packfy.com", "dueno"),
    ("miami@packfy.com", "operador_miami"),
    ("cuba@packfy.com", "operador_cuba"),
    ("remitente1@packfy.com", "remitente"),
    ("remitente2@packfy.com", "remitente"),
    ("remitente3@packfy.com", "remitente"),
    ("destinatario1@cuba.cu", "destinatario"),
    ("destinatario2@cuba.cu", "destinatario"),
    ("destinatario3@cuba.cu", "destinatario"),
]

for email, rol in perfiles_config:
    try:
        usuario = Usuario.objects.get(email=email)

        # Verificar si ya existe el perfil
        perfil_existente = PerfilUsuario.objects.filter(
            usuario=usuario, empresa=empresa
        ).first()

        if not perfil_existente:
            PerfilUsuario.objects.create(
                usuario=usuario, empresa=empresa, rol=rol, activo=True
            )
            print(f"✅ Perfil creado: {email} -> {rol}")
        else:
            print(f"ℹ️ Perfil existente: {email} -> {perfil_existente.rol}")

    except Usuario.DoesNotExist:
        print(f"❌ Usuario no encontrado: {email}")

# 5. Verificar resultado final
print("\n📊 Estado final:")
print(f"  Usuarios: {Usuario.objects.count()}")
print(f"  Empresas: {Empresa.objects.count()}")
print(f"  PerfilUsuario: {PerfilUsuario.objects.count()}")

print("\n👥 Perfiles por usuario:")
for usuario in Usuario.objects.all():
    perfiles = PerfilUsuario.objects.filter(usuario=usuario)
    if perfiles.exists():
        for perfil in perfiles:
            print(
                f"  ✅ {usuario.email} -> {perfil.empresa.nombre} ({perfil.rol})"
            )
    else:
        if usuario.is_superuser:
            print(
                f"  👑 {usuario.email} -> SUPERUSUARIO (sin perfiles de empresa)"
            )
        else:
            print(f"  ⚠️ {usuario.email} -> SIN PERFILES")

print("\n🎉 ¡REPARACIÓN COMPLETADA!")
print("Ahora todos los usuarios deberían tener sus perfiles correctos.")
