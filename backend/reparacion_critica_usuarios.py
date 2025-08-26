#!/usr/bin/env python
"""
🔧 REPARACIÓN CRÍTICA - ESTRUCTURA DE USUARIOS
Solución a problemas críticos de superusuarios sin empresas y roles duplicados
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Django imports after setup
from empresas.models import Empresa, PerfilUsuario  # noqa: E402
from usuarios.models import Usuario  # noqa: E402


def main():
    print("🔧 REPARACIÓN CRÍTICA - ESTRUCTURA DE USUARIOS")
    print("=" * 60)
    print("🎯 Objetivo: Solucionar superusuarios sin empresas")
    print("=" * 60)

    reparar_superusuarios()
    limpiar_roles_duplicados()
    verificar_estructura_final()
    print("\n✅ REPARACIÓN COMPLETADA")


def reparar_superusuarios():
    """Asignar empresas a superusuarios para que puedan acceder al sistema"""
    print("\n🔧 REPARANDO SUPERUSUARIOS")
    print("-" * 40)

    superusuarios = Usuario.objects.filter(is_superuser=True)
    empresas = Empresa.objects.filter(activo=True)

    print(f"👑 Superusuarios encontrados: {superusuarios.count()}")
    print(f"🏢 Empresas disponibles: {empresas.count()}")

    for superuser in superusuarios:
        print(f"\n🔄 Procesando: {superuser.email}")

        # Verificar si ya tiene perfiles
        perfiles_existentes = PerfilUsuario.objects.filter(
            usuario=superuser, activo=True
        )

        if perfiles_existentes.exists():
            count = perfiles_existentes.count()
            print(f"   ✅ Ya tiene {count} empresa(s) asignada(s)")
            continue

        # Asignar a TODAS las empresas con rol especial
        perfiles_creados = 0
        for empresa in empresas:
            # Verificar si ya existe el perfil
            perfil_existente = PerfilUsuario.objects.filter(
                usuario=superuser, empresa=empresa
            ).first()

            if not perfil_existente:
                # Crear perfil con rol super_admin
                PerfilUsuario.objects.create(
                    usuario=superuser, empresa=empresa, rol="super_admin", activo=True
                )
                perfiles_creados += 1
                print(f"   ✅ Creado perfil en {empresa.nombre} (super_admin)")
            else:
                # Actualizar perfil existente
                perfil_existente.rol = "super_admin"
                perfil_existente.activo = True
                perfil_existente.save()
                perfiles_creados += 1
                empresa_nombre = empresa.nombre
                msg = f"   🔄 Actualizado perfil en {empresa_nombre}"
                print(f"{msg} (super_admin)")

        print(f"   📊 Total perfiles: {perfiles_creados}")


def limpiar_roles_duplicados():
    """Limpiar roles duplicados de 'dueno' por empresa"""
    print("\n🧹 LIMPIANDO ROLES DUPLICADOS")
    print("-" * 40)

    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        # Buscar múltiples dueños
        duenos = PerfilUsuario.objects.filter(
            empresa=empresa, rol="dueno", activo=True
        ).order_by("fecha_creacion")

        if duenos.count() > 1:
            print(f"\n🚨 {empresa.nombre}: {duenos.count()} dueños encontrados")

            # Mantener el primero como dueño, convertir el resto
            primer_dueno = duenos.first()
            print(f"   ✅ Mantener como dueño: {primer_dueno.usuario.email}")

            for dueno_extra in duenos[1:]:
                # Convertir a operador
                dueno_extra.rol = "operador"
                dueno_extra.save()
                email = dueno_extra.usuario.email
                print(f"   🔄 Convertido a operador: {email}")

        elif duenos.count() == 1:
            print(f"✅ {empresa.nombre}: 1 dueño (correcto)")

        else:
            print(f"⚠️ {empresa.nombre}: Sin dueño asignado")


def verificar_estructura_final():
    """Verificar que la estructura esté correcta después de la reparación"""
    print("\n📊 VERIFICACIÓN FINAL")
    print("-" * 40)

    # Verificar superusuarios
    superusuarios = Usuario.objects.filter(is_superuser=True)

    for superuser in superusuarios:
        perfiles = PerfilUsuario.objects.filter(usuario=superuser, activo=True)
        empresas_acceso = perfiles.count()
        print(f"👑 {superuser.email}: {empresas_acceso} empresas")

    # Verificar empresas
    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        perfiles = PerfilUsuario.objects.filter(empresa=empresa, activo=True)
        duenos = perfiles.filter(rol="dueno")
        super_admins = perfiles.filter(rol="super_admin")
        operadores = perfiles.filter(rol__contains="operador")

        print(f"\n🏢 {empresa.nombre}:")
        print(f"   👑 Super admins: {super_admins.count()}")
        print(f"   🏢 Dueños: {duenos.count()}")
        print(f"   👥 Operadores: {operadores.count()}")
        print(f"   📊 Total usuarios: {perfiles.count()}")

        if duenos.count() != 1:
            print("   ⚠️ PROBLEMA: Debería tener exactamente 1 dueño")


def crear_usuario_administrador_si_no_existe():
    """Crear usuario administrador principal si no existe"""
    print("\n🔧 VERIFICANDO USUARIO ADMINISTRADOR PRINCIPAL")
    print("-" * 50)

    try:
        admin_user = Usuario.objects.get(email="admin@packfy.com")
        print("✅ Usuario admin@packfy.com ya existe")
        print(f"   👑 Superuser: {admin_user.is_superuser}")
        print(f"   🔧 Staff: {admin_user.is_staff}")

        # Asegurar que tenga permisos de superuser
        if not admin_user.is_superuser:
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            print("   🔄 Permisos de superuser activados")

    except Usuario.DoesNotExist:
        print("❌ Usuario admin@packfy.com no existe")
        print("   📝 Recomendación: Crear manualmente desde Django admin")


if __name__ == "__main__":
    main()
    crear_usuario_administrador_si_no_existe()
