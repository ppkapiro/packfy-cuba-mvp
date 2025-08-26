#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CONFIGURACION SIMPLE - SUPERADMIN Y DUENOS
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def configurar_estructura():
    print("=== CONFIGURANDO ESTRUCTURA DESEADA ===")

    # 1. superadmin@packfy.com = SUPER ADMIN GLOBAL
    try:
        superadmin = Usuario.objects.get(email="superadmin@packfy.com")
        print(f"1. Configurando {superadmin.email} como SUPER ADMIN GLOBAL")

        superadmin.is_superuser = True
        superadmin.is_staff = True
        superadmin.save()
        print("   Permisos globales: OK")

        empresas = Empresa.objects.filter(activo=True)
        for empresa in empresas:
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=superadmin,
                empresa=empresa,
                defaults={"rol": "super_admin", "activo": True},
            )
            if not created and perfil.rol != "super_admin":
                perfil.rol = "super_admin"
                perfil.save()
            print(f"   {empresa.nombre}: super_admin")

    except Usuario.DoesNotExist:
        print("ERROR: superadmin@packfy.com no existe")

    print()

    # 2. dueno@packfy.com = ADMIN de Packfy Express
    try:
        dueno = Usuario.objects.get(email="dueno@packfy.com")
        empresa_packfy = Empresa.objects.get(nombre="Packfy Express")

        print(f"2. Configurando {dueno.email} como ADMIN de Packfy Express")

        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=dueno,
            empresa=empresa_packfy,
            defaults={"rol": "admin_empresa", "activo": True},
        )
        if not created:
            perfil.rol = "admin_empresa"
            perfil.save()

        print(f"   {empresa_packfy.nombre}: admin_empresa")

    except Usuario.DoesNotExist:
        print("ERROR: dueno@packfy.com no existe")
    except Empresa.DoesNotExist:
        print("ERROR: Packfy Express no existe")

    print()

    # 3. consultor@packfy.com = ADMIN de otras empresas
    try:
        consultor = Usuario.objects.get(email="consultor@packfy.com")
        otras_empresas = Empresa.objects.filter(activo=True).exclude(
            nombre="Packfy Express"
        )

        print(f"3. Configurando {consultor.email} como ADMIN de otras empresas")

        for empresa in otras_empresas:
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=consultor,
                empresa=empresa,
                defaults={"rol": "admin_empresa", "activo": True},
            )
            if not created:
                perfil.rol = "admin_empresa"
                perfil.save()

            print(f"   {empresa.nombre}: admin_empresa")

    except Usuario.DoesNotExist:
        print("ERROR: consultor@packfy.com no existe")

    print()
    print("=== ESTRUCTURA CONFIGURADA ===")
    print("SUPER ADMIN GLOBAL:")
    print("  - superadmin@packfy.com (todas las empresas)")
    print()
    print("ADMINS DE EMPRESA:")
    print("  - dueno@packfy.com (Packfy Express)")
    print("  - consultor@packfy.com (otras 3 empresas)")


if __name__ == "__main__":
    configurar_estructura()
