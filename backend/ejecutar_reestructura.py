#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REESTRUCTURACION PASO A PASO
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def paso1_configurar_dominios():
    """PASO 1: Configurar dominios en empresas"""
    print("PASO 1: CONFIGURANDO DOMINIOS")
    print("=" * 30)

    mapeo = {
        "Cuba Express Cargo": "cubaexpress.com",
        "Habana Premium Logistics": "habanapremium.com",
        "Miami Shipping Express": "miamishipping.com",
        "Packfy Express": "packfy.com",
    }

    for nombre, dominio in mapeo.items():
        try:
            empresa = Empresa.objects.get(nombre=nombre, activo=True)
            empresa.dominio = dominio
            empresa.save()
            print(f"✅ {nombre} -> {dominio}")
        except Empresa.DoesNotExist:
            print(f"❌ {nombre} no encontrada")

    print("PASO 1 COMPLETADO\n")


def paso2_crear_admins():
    """PASO 2: Crear usuarios admin por dominio"""
    print("PASO 2: CREANDO ADMINS POR DOMINIO")
    print("=" * 35)

    empresas = Empresa.objects.filter(activo=True, dominio__isnull=False)

    for empresa in empresas:
        email = f"admin@{empresa.dominio}"

        # Crear usuario si no existe
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
            print(f"✅ Creado: {email}")
        else:
            print(f"ℹ️ Existe: {email}")

        # Crear perfil
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=usuario,
            empresa=empresa,
            defaults={"rol": "admin_empresa", "activo": True},
        )

        if created:
            print(f"   📋 Perfil admin_empresa creado")
        else:
            print(f"   📋 Perfil ya existía")

    print("PASO 2 COMPLETADO\n")


def paso3_configurar_superadmin():
    """PASO 3: Configurar superadmin único"""
    print("PASO 3: CONFIGURANDO SUPERADMIN ÚNICO")
    print("=" * 35)

    # Configurar superadmin@packfy.com
    try:
        superadmin = Usuario.objects.get(email="superadmin@packfy.com")
        superadmin.is_superuser = True
        superadmin.is_staff = True
        superadmin.save()
        print("✅ superadmin@packfy.com configurado")

        # Dar acceso a todas las empresas
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

        print(f"✅ Acceso a {empresas.count()} empresas")

    except Usuario.DoesNotExist:
        print("❌ superadmin@packfy.com no existe")

    # Remover superuser de otros
    otros = Usuario.objects.filter(is_superuser=True).exclude(
        email="superadmin@packfy.com"
    )

    for user in otros:
        user.is_superuser = False
        user.save()
        print(f"🔄 Removido superuser: {user.email}")

    print("PASO 3 COMPLETADO\n")


def verificar_resultado():
    """Verificar el resultado final"""
    print("VERIFICACIÓN FINAL")
    print("=" * 18)

    # Dominios
    print("DOMINIOS:")
    for empresa in Empresa.objects.filter(activo=True):
        print(f"  {empresa.nombre}: {empresa.dominio}")

    print("\nADMINS POR DOMINIO:")
    for empresa in Empresa.objects.filter(activo=True, dominio__isnull=False):
        email = f"admin@{empresa.dominio}"
        exists = Usuario.objects.filter(email=email).exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {email}")

    print("\nSUPERADMIN:")
    superusers = Usuario.objects.filter(is_superuser=True, is_active=True)
    for su in superusers:
        count = PerfilUsuario.objects.filter(usuario=su, activo=True).count()
        print(f"  {su.email}: {count} empresas")


if __name__ == "__main__":
    print("🚀 INICIANDO REESTRUCTURACIÓN DE DOMINIOS")
    print("=" * 45)
    print()

    paso1_configurar_dominios()
    paso2_crear_admins()
    paso3_configurar_superadmin()
    verificar_resultado()

    print("\n🎉 REESTRUCTURACIÓN COMPLETADA")
    print("\nCREDENCIALES CREADAS:")
    print("- admin@cubaexpress.com / admin123")
    print("- admin@habanapremium.com / admin123")
    print("- admin@miamishipping.com / admin123")
    print("- admin@packfy.com / admin123")
    print("\n⚠️ Cambiar passwords en producción")
