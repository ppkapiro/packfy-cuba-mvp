#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VERIFICACION POST-REPARACION
Verificar que la estructura de usuarios funcione correctamente
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
    print("VERIFICACION POST-REPARACION")
    print("=" * 50)

    verificar_superusuarios_empresas()
    verificar_roles_por_empresa()
    generar_matriz_accesos()
    verificar_navegacion_dashboards()
    print("\nVERIFICACION COMPLETADA")


def verificar_superusuarios_empresas():
    """Verificar que superusuarios tengan acceso a todas las empresas"""
    print("\nSUPERUSUARIOS Y ACCESO A EMPRESAS")
    print("-" * 40)

    superusuarios = Usuario.objects.filter(is_superuser=True)
    empresas_total = Empresa.objects.filter(activo=True).count()

    for superuser in superusuarios:
        perfiles = PerfilUsuario.objects.filter(usuario=superuser, activo=True)
        empresas_acceso = perfiles.count()

        status = "OK" if empresas_acceso == empresas_total else "PROBLEMA"
        print(f"{superuser.email}: {empresas_acceso}/{empresas_total} [{status}]")

        if empresas_acceso != empresas_total:
            empresas_faltantes = Empresa.objects.filter(activo=True).exclude(
                id__in=perfiles.values("empresa_id")
            )
            print(
                f"   Empresas faltantes: {list(empresas_faltantes.values_list('nombre', flat=True))}"
            )


def verificar_roles_por_empresa():
    """Verificar que cada empresa tenga exactamente 1 dueño"""
    print("\nROLES POR EMPRESA")
    print("-" * 40)

    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        perfiles = PerfilUsuario.objects.filter(empresa=empresa, activo=True)

        roles_count = {}
        for rol in ["super_admin", "dueno", "operador_paquetes", "operador", "cliente"]:
            count = perfiles.filter(rol=rol).count()
            if count > 0:
                roles_count[rol] = count

        print(f"\n{empresa.nombre}:")
        for rol, count in roles_count.items():
            print(f"   {rol}: {count}")

        # Verificar problemas
        duenos = perfiles.filter(rol="dueno").count()
        if duenos != 1:
            print(f"   *** PROBLEMA: {duenos} duenos (deberia ser 1)")


def generar_matriz_accesos():
    """Generar matriz de usuarios vs empresas"""
    print("\nMATRIZ DE ACCESOS")
    print("-" * 40)

    usuarios = Usuario.objects.filter(is_active=True).order_by("email")
    empresas = Empresa.objects.filter(activo=True).order_by("nombre")

    # Header
    header = "Usuario".ljust(25)
    for empresa in empresas:
        header += empresa.nombre[:15].ljust(17)
    print(header)
    print("-" * len(header))

    # Filas
    for usuario in usuarios:
        fila = usuario.email[:24].ljust(25)

        for empresa in empresas:
            perfil = PerfilUsuario.objects.filter(
                usuario=usuario, empresa=empresa, activo=True
            ).first()

            if perfil:
                rol_short = perfil.rol[:15]
                fila += rol_short.ljust(17)
            else:
                fila += "---".ljust(17)

        print(fila)


def verificar_navegacion_dashboards():
    """Verificar qué dashboards deberían estar disponibles por rol"""
    print("\nNAVEGACION Y DASHBOARDS POR ROL")
    print("-" * 40)

    dashboard_mapping = {
        "super_admin": ["DashboardMain", "DashboardDueno", "Dashboard"],
        "dueno": ["DashboardDueno", "Dashboard"],
        "operador_paquetes": ["Dashboard"],
        "operador": ["Dashboard"],
        "cliente": ["Dashboard"],
    }

    usuarios = Usuario.objects.filter(is_active=True)

    for usuario in usuarios:
        perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)

        if perfiles.exists():
            print(f"\n{usuario.email}:")

            for perfil in perfiles[:3]:  # Mostrar solo primeros 3
                dashboards = dashboard_mapping.get(perfil.rol, ["Dashboard"])
                print(f"   {perfil.empresa.nombre} ({perfil.rol}): {dashboards}")

            if perfiles.count() > 3:
                print(f"   ... y {perfiles.count() - 3} empresas mas")


def verificar_casos_problematicos():
    """Verificar casos que podrían causar problemas de navegación"""
    print("\nCASOS PROBLEMATICOS")
    print("-" * 40)

    # Usuarios sin perfiles activos
    usuarios_sin_perfiles = Usuario.objects.filter(
        is_active=True, perfilusuario__isnull=True
    ).distinct()

    if usuarios_sin_perfiles.exists():
        print("Usuarios sin perfiles de empresa:")
        for usuario in usuarios_sin_perfiles:
            print(f"   {usuario.email}")

    # Usuarios con perfiles inactivos solamente
    usuarios_con_perfiles_inactivos = (
        Usuario.objects.filter(is_active=True, perfilusuario__activo=False)
        .exclude(perfilusuario__activo=True)
        .distinct()
    )

    if usuarios_con_perfiles_inactivos.exists():
        print("\nUsuarios solo con perfiles inactivos:")
        for usuario in usuarios_con_perfiles_inactivos:
            print(f"   {usuario.email}")

    # Empresas sin dueño
    empresas_sin_dueno = []
    for empresa in Empresa.objects.filter(activo=True):
        duenos = PerfilUsuario.objects.filter(
            empresa=empresa, rol="dueno", activo=True
        ).count()
        if duenos == 0:
            empresas_sin_dueno.append(empresa)

    if empresas_sin_dueno:
        print("\nEmpresas sin dueno:")
        for empresa in empresas_sin_dueno:
            print(f"   {empresa.nombre}")


if __name__ == "__main__":
    main()
    verificar_casos_problematicos()
