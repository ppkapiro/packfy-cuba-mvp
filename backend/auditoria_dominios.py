#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AUDITORIA PROFUNDA - DOMINIOS Y USUARIOS
Analizar la discrepancia entre usuarios y dominios de empresas
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario  # noqa: E402
from usuarios.models import Usuario  # noqa: E402


def main():
    print("🔍 AUDITORIA PROFUNDA - DOMINIOS Y USUARIOS")
    print("=" * 60)
    print("Objetivo: Analizar discrepancia entre emails y dominios")
    print("=" * 60)

    analizar_empresas_y_dominios()
    analizar_usuarios_por_dominio()
    identificar_problemas_estructura()
    proponer_reestructuracion()
    print("\n📋 AUDITORIA COMPLETADA")


def analizar_empresas_y_dominios():
    """Analizar empresas y sus dominios configurados"""
    print("\n🏢 EMPRESAS Y SUS DOMINIOS")
    print("-" * 40)

    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        print(f"\n{empresa.nombre}:")
        print(f"   ID: {empresa.id}")

        # Verificar si tiene dominio configurado
        dominio = getattr(empresa, "dominio", None)
        if dominio:
            print(f"   Dominio: {dominio}")
        else:
            print("   Dominio: NO CONFIGURADO")

        # Extraer dominio probable del nombre
        dominio_probable = generar_dominio_desde_nombre(empresa.nombre)
        print(f"   Dominio probable: {dominio_probable}")

        # Contar usuarios asociados
        usuarios_empresa = PerfilUsuario.objects.filter(empresa=empresa, activo=True)
        print(f"   Usuarios: {usuarios_empresa.count()}")


def generar_dominio_desde_nombre(nombre_empresa):
    """Generar dominio probable basado en el nombre de empresa"""
    # Limpiar y convertir nombre a dominio
    nombre_limpio = nombre_empresa.lower()
    nombre_limpio = nombre_limpio.replace(" ", "")
    nombre_limpio = nombre_limpio.replace("-", "")

    # Mapeo específico conocido
    mapeo_dominios = {
        "cubaexpresscargo": "cubaexpress.com",
        "habanapremiumlogistics": "habanapremium.com",
        "miamishippingexpress": "miamishipping.com",
        "packfyexpress": "packfy.com",
    }

    return mapeo_dominios.get(nombre_limpio, f"{nombre_limpio}.com")


def analizar_usuarios_por_dominio():
    """Analizar usuarios y verificar coherencia con dominios"""
    print("\n👥 USUARIOS Y DOMINIOS DE EMAIL")
    print("-" * 40)

    usuarios = Usuario.objects.filter(is_active=True).order_by("email")

    dominio_count = {}
    problemas = []

    for usuario in usuarios:
        email = usuario.email
        dominio_email = email.split("@")[1] if "@" in email else "SIN_DOMINIO"

        print(f"\n{email}:")
        print(f"   Dominio email: {dominio_email}")

        # Contar dominios
        dominio_count[dominio_email] = dominio_count.get(dominio_email, 0) + 1

        # Verificar perfiles de empresa
        perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)

        if perfiles.exists():
            for perfil in perfiles:
                empresa = perfil.empresa
                dominio_empresa = generar_dominio_desde_nombre(empresa.nombre)

                coherente = dominio_email == dominio_empresa
                status = "✅" if coherente else "❌"

                print(f"   {status} {empresa.nombre} ({perfil.rol})")
                print(f"       Esperado: @{dominio_empresa}")

                if not coherente and usuario.email != "superadmin@packfy.com":
                    problemas.append(
                        {
                            "usuario": email,
                            "empresa": empresa.nombre,
                            "dominio_actual": dominio_email,
                            "dominio_esperado": dominio_empresa,
                            "rol": perfil.rol,
                        }
                    )
        else:
            print("   Sin perfiles de empresa")

    print(f"\n📊 RESUMEN POR DOMINIO:")
    for dominio, count in sorted(dominio_count.items()):
        print(f"   {dominio}: {count} usuarios")

    return problemas


def identificar_problemas_estructura():
    """Identificar problemas específicos en la estructura actual"""
    print("\n⚠️ PROBLEMAS IDENTIFICADOS")
    print("-" * 40)

    problemas = []

    # Problema 1: Usuarios con @packfy.com en múltiples empresas
    usuarios_packfy = Usuario.objects.filter(
        email__endswith="@packfy.com", is_active=True
    )

    for usuario in usuarios_packfy:
        if usuario.email == "superadmin@packfy.com":
            continue  # Este debe ser global

        perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
        empresas_no_packfy = perfiles.exclude(empresa__nombre="Packfy Express").count()

        if empresas_no_packfy > 0:
            problemas.append(
                f"❌ {usuario.email} tiene acceso a empresas "
                f"que no son Packfy Express"
            )

    # Problema 2: Empresas sin usuarios de su dominio
    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        if empresa.nombre == "Packfy Express":
            continue  # Esta puede tener @packfy.com

        dominio_esperado = generar_dominio_desde_nombre(empresa.nombre)
        usuarios_dominio = Usuario.objects.filter(
            email__endswith=f"@{dominio_esperado}", is_active=True
        )

        if not usuarios_dominio.exists():
            problemas.append(
                f"❌ {empresa.nombre} no tiene usuarios " f"@{dominio_esperado}"
            )

    # Problema 3: Múltiples superusuarios
    superusuarios = Usuario.objects.filter(is_superuser=True, is_active=True)
    if superusuarios.count() > 1:
        problemas.append(
            f"❌ Hay {superusuarios.count()} superusuarios " f"(debería ser solo 1)"
        )

    if problemas:
        for problema in problemas:
            print(f"   {problema}")
    else:
        print("   ✅ No se encontraron problemas críticos")


def proponer_reestructuracion():
    """Proponer nueva estructura de usuarios por dominio"""
    print("\n🎯 PROPUESTA DE REESTRUCTURACIÓN")
    print("-" * 45)

    print("ESTRUCTURA IDEAL:")
    print()

    # Superusuario global
    print("👑 SUPERUSUARIO GLOBAL:")
    print("   superadmin@packfy.com")
    print("   - Acceso a todas las empresas")
    print("   - Rol: super_admin en todas")
    print()

    # Usuarios por empresa con sus dominios
    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        dominio = generar_dominio_desde_nombre(empresa.nombre)
        print(f"🏢 {empresa.nombre.upper()}:")
        print(f"   Dominio: @{dominio}")
        print(f"   Usuarios necesarios:")
        print(f"   - admin@{dominio} (admin_empresa)")
        print(f"   - operador@{dominio} (operador)")
        print(f"   - cliente@{dominio} (cliente)")
        print()

    print("📝 ACCIONES REQUERIDAS:")
    print("1. Crear usuarios con dominios correctos")
    print("2. Migrar datos de usuarios existentes")
    print("3. Actualizar configuración de empresas")
    print("4. Establecer superadmin@packfy.com como único global")


def generar_plan_migracion():
    """Generar plan detallado de migración"""
    print("\n📋 PLAN DE MIGRACIÓN")
    print("-" * 30)

    print("FASE 1 - PREPARACIÓN:")
    print("- Backup de usuarios actuales")
    print("- Configurar dominios en modelo Empresa")
    print("- Crear script de migración")
    print()

    print("FASE 2 - CREACIÓN:")
    print("- Crear usuarios con dominios correctos")
    print("- Asignar roles apropiados")
    print("- Configurar perfiles de empresa")
    print()

    print("FASE 3 - MIGRACIÓN:")
    print("- Migrar datos críticos (envíos, clientes)")
    print("- Actualizar referencias de usuarios")
    print("- Desactivar usuarios obsoletos")
    print()

    print("FASE 4 - VERIFICACIÓN:")
    print("- Probar login por dominio")
    print("- Verificar permisos")
    print("- Validar navegación")


if __name__ == "__main__":
    main()
    generar_plan_migracion()
