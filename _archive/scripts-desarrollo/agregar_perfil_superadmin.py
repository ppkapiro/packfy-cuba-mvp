#!/usr/bin/env python3
"""
Agregar perfil al superadmin
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def agregar_perfil_superadmin():
    print("🔧 AGREGANDO PERFIL AL SUPERADMIN...")

    try:
        # Obtener superadmin
        superadmin = Usuario.objects.get(email="superadmin@packfy.com")
        print(f"👤 Superadmin encontrado: {superadmin.email}")

        # Obtener empresa
        empresa = Empresa.objects.first()
        print(f"🏢 Empresa encontrada: {empresa.nombre}")

        # Verificar si ya tiene perfil
        perfil_existe = PerfilUsuario.objects.filter(
            usuario=superadmin, empresa=empresa
        ).exists()

        if perfil_existe:
            print("✅ El superadmin ya tiene perfil")
        else:
            # Crear perfil
            perfil = PerfilUsuario.objects.create(
                usuario=superadmin,
                empresa=empresa,
                rol="superadmin",
                activo=True,
            )
            print(f"✅ Perfil creado: {perfil.rol} en {perfil.empresa.nombre}")

        # Verificar resultado
        perfiles = PerfilUsuario.objects.filter(usuario=superadmin)
        print(f"📋 Total perfiles del superadmin: {perfiles.count()}")

        for p in perfiles:
            print(f"  - {p.rol} en {p.empresa.nombre} (activo: {p.activo})")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    agregar_perfil_superadmin()
