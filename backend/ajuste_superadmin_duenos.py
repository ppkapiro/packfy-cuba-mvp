#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AJUSTE ESTRUCTURA - SUPERADMIN Y DUENOS
Configurar superadmin como super administrador global y duenos como admins de empresa
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Django imports after setup
from empresas.models import Empresa, PerfilUsuario  # noqa: E402
from usuarios.models import Usuario  # noqa: E402


def main():
    print("AJUSTE ESTRUCTURA - SUPERADMIN Y DUENOS")
    print("=" * 50)
    print("Objetivo: superadmin = super admin global, duenos = admin empresa")
    print("=" * 50)

    configurar_superadmin_global()
    configurar_duenos_como_admins()
    limpiar_admin_packfy_si_necesario()
    verificar_estructura_final()
    print("\nAJUSTE COMPLETADO")


def configurar_superadmin_global():
    """Configurar superadmin@packfy.com como super administrador global"""
    print("\nCONFIGURANDO SUPERADMIN GLOBAL")
    print("-" * 40)

    try:
        superadmin = Usuario.objects.get(email="superadmin@packfy.com")
        print(f"Configurando: {superadmin.email}")

        # Asegurar que es superuser
        superadmin.is_superuser = True
        superadmin.is_staff = True
        superadmin.save()
        print("   Permisos de superuser confirmados")

        # Verificar/crear perfiles en todas las empresas
        empresas = Empresa.objects.filter(activo=True)
        perfiles_actualizados = 0

        for empresa in empresas:
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=superadmin,
                empresa=empresa,
                defaults={"rol": "super_admin", "activo": True},
            )

            if not created:
                # Actualizar rol si ya existe
                if perfil.rol != "super_admin":
                    perfil.rol = "super_admin"
                    perfil.activo = True
                    perfil.save()
                    perfiles_actualizados += 1
                    print(f"   Actualizado en {empresa.nombre}")
                else:
                    print(f"   Ya configurado en {empresa.nombre}")
            else:
                perfiles_actualizados += 1
                print(f"   Creado perfil en {empresa.nombre}")

        print(f"   Total empresas accesibles: {empresas.count()}")

    except Usuario.DoesNotExist:
        print("ERROR: superadmin@packfy.com no existe")
        print("Recomendacion: Crear este usuario primero")


def configurar_duenos_como_admins():
    """Configurar dueños como administradores de sus empresas específicas"""
    print("\nCONFIGURANDO DUENOS COMO ADMINS DE EMPRESA")
    print("-" * 45)

    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        # Buscar el dueño actual de cada empresa
        duenos = PerfilUsuario.objects.filter(empresa=empresa, rol="dueno", activo=True)

        if duenos.count() == 1:
            dueno_perfil = duenos.first()
            dueno_usuario = dueno_perfil.usuario

            print(f"\n{empresa.nombre}:")
            print(f"   Dueño actual: {dueno_usuario.email}")

            # Configurar como admin de la empresa (staff local)
            dueno_perfil.rol = "admin_empresa"
            dueno_perfil.save()
            print(f"   Rol actualizado: dueno -> admin_empresa")

            # El usuario mantiene permisos básicos (no superuser global)
            if dueno_usuario.email != "superadmin@packfy.com":
                dueno_usuario.is_staff = True  # Puede acceder a admin si necesario
                dueno_usuario.is_superuser = False  # NO es superuser global
                dueno_usuario.save()
                print(f"   Permisos: staff=True, superuser=False")

        elif duenos.count() == 0:
            print(f"\n{empresa.nombre}: SIN DUENO ASIGNADO")
            print("   Recomendacion: Asignar un dueño manualmente")

        else:
            print(f"\n{empresa.nombre}: MULTIPLES DUENOS ({duenos.count()})")
            primer_dueno = duenos.first()
            print(f"   Manteniendo: {primer_dueno.usuario.email}")

            # Convertir extras a operadores
            for extra in duenos[1:]:
                extra.rol = "operador"
                extra.save()
                print(f"   Convertido a operador: {extra.usuario.email}")


def limpiar_admin_packfy_si_necesario():
    """Evaluar qué hacer con admin@packfy.com"""
    print("\nEVALUANDO admin@packfy.com")
    print("-" * 30)

    try:
        admin_user = Usuario.objects.get(email="admin@packfy.com")
        perfiles = PerfilUsuario.objects.filter(usuario=admin_user, activo=True)

        print(f"admin@packfy.com tiene {perfiles.count()} perfiles")

        # Opción 1: Convertir a operador general
        # Opción 2: Mantener como backup de superadmin
        # Opción 3: Desactivar

        print("   Opciones:")
        print("   1. Mantener como backup superadmin")
        print("   2. Convertir a operador general")
        print("   3. Desactivar temporalmente")
        print("   Accion: Manteniendo como backup (no cambios)")

    except Usuario.DoesNotExist:
        print("admin@packfy.com no existe")


def verificar_estructura_final():
    """Verificar la estructura después del ajuste"""
    print("\nESTRUCTURA FINAL")
    print("-" * 30)

    # Verificar superadmin
    try:
        superadmin = Usuario.objects.get(email="superadmin@packfy.com")
        perfiles_super = PerfilUsuario.objects.filter(usuario=superadmin, activo=True)
        print(f"SUPERADMIN: {superadmin.email}")
        print(f"   Empresas: {perfiles_super.count()}")
        print(f"   Superuser: {superadmin.is_superuser}")
        print(f"   Staff: {superadmin.is_staff}")
    except Usuario.DoesNotExist:
        print("SUPERADMIN: No configurado")

    print()

    # Verificar cada empresa
    empresas = Empresa.objects.filter(activo=True)
    for empresa in empresas:
        admins_empresa = PerfilUsuario.objects.filter(
            empresa=empresa, rol="admin_empresa", activo=True
        )

        print(f"{empresa.nombre}:")
        if admins_empresa.exists():
            for admin in admins_empresa:
                print(f"   Admin: {admin.usuario.email}")
        else:
            print("   Sin admin de empresa")


if __name__ == "__main__":
    main()
