#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REESTRUCTURACIÓN DOMINIOS - PLAN DE MIGRACIÓN
Implementar estructura: 1 superadmin global + usuarios por dominio de empresa
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def main():
    print("🔄 REESTRUCTURACIÓN DE DOMINIOS - FASE 1")
    print("=" * 50)
    print("Objetivo: 1 superadmin global + usuarios por dominio empresa")
    print("=" * 50)

    # FASE 1: Configurar dominios en empresas
    configurar_dominios_empresas()

    # FASE 2: Crear usuarios por dominio
    crear_usuarios_por_dominio()

    # FASE 3: Limpiar estructura actual
    limpiar_usuarios_incorrectos()

    # FASE 4: Configurar superadmin único
    configurar_superadmin_unico()

    # FASE 5: Verificar resultado
    verificar_estructura_final()

    print("\n✅ REESTRUCTURACIÓN COMPLETADA")


def configurar_dominios_empresas():
    """Configurar dominios correctos en cada empresa"""
    print("\n🏢 CONFIGURANDO DOMINIOS DE EMPRESAS")
    print("-" * 40)

    mapeo_dominios = {
        "Cuba Express Cargo": "cubaexpress.com",
        "Habana Premium Logistics": "habanapremium.com",
        "Miami Shipping Express": "miamishipping.com",
        "Packfy Express": "packfy.com",
    }

    for nombre_empresa, dominio in mapeo_dominios.items():
        try:
            empresa = Empresa.objects.get(nombre=nombre_empresa, activo=True)
            empresa.dominio = dominio
            empresa.save()
            print(f"✅ {empresa.nombre} -> {dominio}")
        except Empresa.DoesNotExist:
            print(f"❌ No encontrada: {nombre_empresa}")


def crear_usuarios_por_dominio():
    """Crear usuarios administrativos por cada dominio de empresa"""
    print("\n👥 CREANDO USUARIOS POR DOMINIO")
    print("-" * 35)

    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        if not empresa.dominio:
            print(f"⚠️ {empresa.nombre} sin dominio configurado")
            continue

        # Crear admin de empresa
        email_admin = f"admin@{empresa.dominio}"

        try:
            # Verificar si ya existe
            usuario_admin = Usuario.objects.get(email=email_admin)
            print(f"✅ {email_admin} ya existe")
        except Usuario.DoesNotExist:
            # Crear nuevo usuario admin
            usuario_admin = Usuario.objects.create(
                email=email_admin,
                username=email_admin,
                first_name="Admin",
                last_name=empresa.nombre,
                is_active=True,
                is_staff=True,
                is_superuser=False,
                password=make_password("admin123"),  # Password temporal
            )
            print(f"✅ Creado: {email_admin}")

        # Crear/actualizar perfil de empresa
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=usuario_admin,
            empresa=empresa,
            defaults={"rol": "admin_empresa", "activo": True},
        )

        if not created:
            perfil.rol = "admin_empresa"
            perfil.activo = True
            perfil.save()

        print(f"   📋 Perfil admin_empresa en {empresa.nombre}")

        # Crear operador si no existe
        email_operador = f"operador@{empresa.dominio}"

        try:
            usuario_operador = Usuario.objects.get(email=email_operador)
            print(f"✅ {email_operador} ya existe")
        except Usuario.DoesNotExist:
            usuario_operador = Usuario.objects.create(
                email=email_operador,
                username=email_operador,
                first_name="Operador",
                last_name=empresa.nombre,
                is_active=True,
                is_staff=False,
                is_superuser=False,
                password=make_password("operador123"),
            )
            print(f"✅ Creado: {email_operador}")

        # Crear perfil operador
        perfil_op, created = PerfilUsuario.objects.get_or_create(
            usuario=usuario_operador,
            empresa=empresa,
            defaults={"rol": "operador", "activo": True},
        )

        print(f"   📋 Perfil operador en {empresa.nombre}")
        print()


def limpiar_usuarios_incorrectos():
    """Limpiar usuarios que están en empresas con dominios incorrectos"""
    print("\n🧹 LIMPIANDO USUARIOS INCORRECTOS")
    print("-" * 35)

    print("NOTA: Esta fase solo reporta, no elimina automáticamente")
    print("Se requiere decisión manual para migrar/eliminar datos\n")

    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        if not empresa.dominio:
            continue

        print(f"{empresa.nombre} (@{empresa.dominio}):")

        # Usuarios con dominios incorrectos
        perfiles = PerfilUsuario.objects.filter(empresa=empresa, activo=True)

        usuarios_incorrectos = []
        for perfil in perfiles:
            email_domain = perfil.usuario.email.split("@")[1]
            # Permitir superadmin@packfy.com en todas
            if (
                email_domain != empresa.dominio
                and perfil.usuario.email != "superadmin@packfy.com"
            ):
                usuarios_incorrectos.append(perfil)

        if usuarios_incorrectos:
            print("   ❌ Usuarios con dominio incorrecto:")
            for perfil in usuarios_incorrectos:
                print(f"     - {perfil.usuario.email} ({perfil.rol})")
                # AQUÍ se podría implementar migración de datos
                # Por ahora solo reportamos
        else:
            print("   ✅ Todos los usuarios tienen dominio correcto")
        print()


def configurar_superadmin_unico():
    """Configurar superadmin@packfy.com como único superusuario global"""
    print("\n👑 CONFIGURANDO SUPERADMIN ÚNICO")
    print("-" * 35)

    # 1. Asegurar que superadmin@packfy.com existe y es único superuser
    try:
        superadmin = Usuario.objects.get(email="superadmin@packfy.com")
        superadmin.is_superuser = True
        superadmin.is_staff = True
        superadmin.save()
        print("✅ superadmin@packfy.com configurado como superuser")
    except Usuario.DoesNotExist:
        print("❌ superadmin@packfy.com no existe - DEBE CREARSE")
        return

    # 2. Remover permisos de superuser de otros usuarios
    otros_superusers = Usuario.objects.filter(is_superuser=True).exclude(
        email="superadmin@packfy.com"
    )

    if otros_superusers.exists():
        print("🔄 Removiendo permisos de superuser de otros usuarios:")
        for user in otros_superusers:
            user.is_superuser = False
            # Mantener is_staff si es admin de empresa
            if not user.email.startswith("admin@"):
                user.is_staff = False
            user.save()
            print(f"   - {user.email}: superuser=False")

    # 3. Asegurar que superadmin tiene acceso a todas las empresas
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

    print(f"✅ superadmin tiene acceso a {empresas.count()} empresas")


def verificar_estructura_final():
    """Verificar la estructura después de la reestructuración"""
    print("\n📊 VERIFICACIÓN ESTRUCTURA FINAL")
    print("-" * 40)

    print("1. SUPERUSUARIO ÚNICO:")
    superusers = Usuario.objects.filter(is_superuser=True, is_active=True)
    for user in superusers:
        empresas_acceso = PerfilUsuario.objects.filter(
            usuario=user, activo=True
        ).count()
        print(f"   👑 {user.email}: {empresas_acceso} empresas")

    print("\n2. ESTRUCTURA POR EMPRESA:")
    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        print(f"\n   🏢 {empresa.nombre} (@{empresa.dominio or 'SIN_DOMINIO'}):")

        # Admins de la empresa
        admins = PerfilUsuario.objects.filter(
            empresa=empresa, rol="admin_empresa", activo=True
        )
        print(f"     👤 Admins: {admins.count()}")
        for admin in admins:
            print(f"       - {admin.usuario.email}")

        # Operadores
        operadores = PerfilUsuario.objects.filter(
            empresa=empresa, rol="operador", activo=True
        )
        print(f"     🔧 Operadores: {operadores.count()}")

        # Total usuarios
        total = PerfilUsuario.objects.filter(empresa=empresa, activo=True)
        print(f"     📊 Total usuarios: {total.count()}")


def generar_credenciales():
    """Generar resumen de credenciales creadas"""
    print("\n🔑 CREDENCIALES GENERADAS")
    print("-" * 25)

    empresas = Empresa.objects.filter(activo=True)

    print("ACCESO DE ADMINISTRACIÓN:")
    print("- superadmin@packfy.com / [password existente]")
    print()

    print("ACCESO POR EMPRESA:")
    for empresa in empresas:
        if empresa.dominio:
            print(f"- admin@{empresa.dominio} / admin123")
            print(f"- operador@{empresa.dominio} / operador123")

    print("\n⚠️ CAMBIAR PASSWORDS EN PRODUCCIÓN")


if __name__ == "__main__":
    main()
    generar_credenciales()
