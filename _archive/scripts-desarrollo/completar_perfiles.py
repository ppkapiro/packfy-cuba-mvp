#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 REPARAR TODOS LOS PERFILES RESTANTES

Ahora que sabemos que funciona, vamos a crear todos los perfiles que faltan.
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario

print("🔧 CREANDO TODOS LOS PERFILES RESTANTES...")
print("=" * 60)

# Obtener la empresa
try:
    empresa = Empresa.objects.get(slug="packfy-express")
    print(f"✅ Empresa encontrada: {empresa.nombre}")
except Empresa.DoesNotExist:
    print("❌ Empresa no encontrada")
    exit(1)

# Lista de usuarios y sus roles
usuarios_roles = [
    ("miami@packfy.com", "operador_miami"),
    ("cuba@packfy.com", "operador_cuba"),
    ("remitente1@packfy.com", "remitente"),
    ("remitente2@packfy.com", "remitente"),
    ("remitente3@packfy.com", "remitente"),
    ("destinatario1@cuba.cu", "destinatario"),
    ("destinatario2@cuba.cu", "destinatario"),
    ("destinatario3@cuba.cu", "destinatario"),
]

perfiles_creados = 0
perfiles_existentes = 0

for email, rol in usuarios_roles:
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
            perfiles_creados += 1
        else:
            print(f"ℹ️ Perfil existente: {email} -> {perfil_existente.rol}")
            perfiles_existentes += 1

    except Usuario.DoesNotExist:
        print(f"❌ Usuario no encontrado: {email}")

print(f"\n📊 RESUMEN:")
print(f"   Perfiles creados: {perfiles_creados}")
print(f"   Perfiles existentes: {perfiles_existentes}")
print(f"   Total perfiles: {PerfilUsuario.objects.count()}")

print(f"\n👥 TODOS LOS PERFILES:")
for perfil in PerfilUsuario.objects.all().select_related("usuario", "empresa"):
    print(
        f"   ✅ {perfil.usuario.email} -> {perfil.empresa.nombre} ({perfil.rol})"
    )

print(f"\n🎉 ¡PERFILES COMPLETADOS!")
print(
    f"Ahora todos los usuarios deberían tener acceso a sus funcionalidades correspondientes."
)
