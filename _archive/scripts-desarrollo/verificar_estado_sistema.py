#!/usr/bin/env python
"""
Script para verificar el estado actual del sistema: empresas, usuarios y perfiles
"""

import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from empresas.models import Empresa, PerfilEmpresa


def main():
    print("=== ESTADO ACTUAL DEL SISTEMA ===")
    print()

    # Verificar empresas
    print("🏢 EMPRESAS:")
    empresas = Empresa.objects.all()
    if empresas.exists():
        for empresa in empresas:
            print(
                f"  ✅ {empresa.nombre} (slug: {empresa.slug}, activa: {empresa.activa})"
            )
    else:
        print("  ❌ No hay empresas en el sistema")

    print()

    # Verificar usuarios
    print("👥 USUARIOS:")
    User = get_user_model()
    usuarios = User.objects.all()
    if usuarios.exists():
        for user in usuarios[:5]:  # Solo los primeros 5
            print(
                f"  ✅ {user.email} (superuser: {user.is_superuser}, staff: {user.is_staff})"
            )
        if usuarios.count() > 5:
            print(f"  ... y {usuarios.count() - 5} usuarios más")
    else:
        print("  ❌ No hay usuarios en el sistema")

    print()

    # Verificar perfiles
    print("🎭 PERFILES EMPRESA:")
    perfiles = PerfilEmpresa.objects.all()
    if perfiles.exists():
        for perfil in perfiles[:5]:  # Solo los primeros 5
            print(
                f"  ✅ {perfil.usuario.email} → {perfil.rol} en {perfil.empresa.nombre}"
            )
        if perfiles.count() > 5:
            print(f"  ... y {perfiles.count() - 5} perfiles más")
    else:
        print("  ❌ No hay perfiles de empresa")

    print()
    print(
        f"📊 TOTALES: {empresas.count()} empresas, {usuarios.count()} usuarios, {perfiles.count()} perfiles"
    )


if __name__ == "__main__":
    main()
