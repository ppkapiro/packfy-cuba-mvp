#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ VERIFICAR ESTADO BLINDADO

Script simple para verificar que la estructura blindada está funcionando.
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def verificar_estructura():
    print("🔍 VERIFICANDO ESTRUCTURA BLINDADA...")
    print("=" * 50)

    # Contar registros
    total_usuarios = Usuario.objects.count()
    total_empresas = Empresa.objects.count()
    total_perfiles = PerfilUsuario.objects.count()

    print(f"📊 Estadísticas:")
    print(f"   Usuarios: {total_usuarios}")
    print(f"   Empresas: {total_empresas}")
    print(f"   Perfiles: {total_perfiles}")
    print()

    # Verificar usuarios clave
    print("👥 Usuarios clave:")

    try:
        superadmin = Usuario.objects.get(email="superadmin@packfy.com")
        print(
            f"   ✅ Superadmin: {superadmin.email} (staff: {superadmin.is_staff}, super: {superadmin.is_superuser})"
        )
    except Usuario.DoesNotExist:
        print("   ❌ Superadmin no encontrado")

    try:
        dueno = Usuario.objects.get(email="dueno@packfy.com")
        print(f"   ✅ Dueño: {dueno.email} (staff: {dueno.is_staff})")
    except Usuario.DoesNotExist:
        print("   ❌ Dueño no encontrado")

    try:
        miami = Usuario.objects.get(email="miami@packfy.com")
        print(f"   ✅ Operador Miami: {miami.email}")
    except Usuario.DoesNotExist:
        print("   ❌ Operador Miami no encontrado")

    print()

    # Verificar empresa
    print("🏢 Empresa:")
    try:
        empresa = Empresa.objects.get(slug="packfy-express")
        print(f"   ✅ {empresa.nombre} (activo: {empresa.activo})")
    except Empresa.DoesNotExist:
        print("   ❌ Empresa Packfy Express no encontrada")

    print()

    # Verificar perfiles
    print("🔗 Perfiles de usuario:")
    perfiles_activos = PerfilUsuario.objects.filter(activo=True).count()
    print(f"   Perfiles activos: {perfiles_activos}")

    print()
    print("=" * 50)

    if total_usuarios >= 10 and total_empresas >= 1 and total_perfiles >= 9:
        print("✅ ESTRUCTURA BLINDADA VERIFICADA - TODO OK")
        return True
    else:
        print("❌ ESTRUCTURA INCOMPLETA - NECESITA RESTAURACIÓN")
        return False


if __name__ == "__main__":
    verificar_estructura()
