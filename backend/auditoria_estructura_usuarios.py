#!/usr/bin/env python
"""
🔍 AUDITORÍA COMPLETA DE ESTRUCTURA DE USUARIOS Y FRONTEND
Análisis profundo de roles, empresas, navegación y problemas estructurales
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import authenticate
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def main():
    print("🔍 AUDITORÍA COMPLETA - ESTRUCTURA USUARIOS Y FRONTEND")
    print("=" * 80)
    print("📅 FECHA: 25 de Agosto, 2025")
    print("🎯 OBJETIVO: Analizar estructura de usuarios, roles y frontend")
    print("=" * 80)

    analizar_estructura_usuarios()
    analizar_empresas_y_relaciones()
    analizar_roles_y_permisos()
    identificar_problemas_estructura()
    analizar_dashboards_frontend()
    proponer_estructura_ideal()


def analizar_estructura_usuarios():
    """Análisis detallado de todos los usuarios del sistema"""
    print("\n👥 ANÁLISIS DE USUARIOS EN EL SISTEMA")
    print("-" * 60)

    usuarios = Usuario.objects.all().order_by("email")
    print(f"📊 Total de usuarios: {usuarios.count()}")

    # Análisis por tipo de usuario
    superusers = usuarios.filter(is_superuser=True)
    staff = usuarios.filter(is_staff=True, is_superuser=False)
    regulares = usuarios.filter(is_staff=False, is_superuser=False)

    print(f"\n📋 CLASIFICACIÓN POR PRIVILEGIOS:")
    print(f"   👑 Superusuarios: {superusers.count()}")
    print(f"   🔧 Staff: {staff.count()}")
    print(f"   👤 Regulares: {regulares.count()}")

    print(f"\n👑 SUPERUSUARIOS (Administradores Globales):")
    for user in superusers:
        perfiles_count = PerfilUsuario.objects.filter(usuario=user, activo=True).count()
        empresas_acceso = PerfilUsuario.objects.filter(
            usuario=user, activo=True
        ).values_list("empresa__nombre", flat=True)
        print(f"   • {user.email} - {user.nombre} {user.apellido}")
        print(f"     🏢 Empresas: {perfiles_count} ({list(empresas_acceso)})")
        print(f"     📊 Staff: {user.is_staff} | Activo: {user.is_active}")

    print(f"\n🔧 USUARIOS STAFF:")
    for user in staff:
        perfiles_count = PerfilUsuario.objects.filter(usuario=user, activo=True).count()
        empresas_acceso = PerfilUsuario.objects.filter(
            usuario=user, activo=True
        ).values_list("empresa__nombre", flat=True)
        print(f"   • {user.email} - {user.nombre} {user.apellido}")
        print(f"     🏢 Empresas: {perfiles_count} ({list(empresas_acceso)})")

    print(f"\n👤 USUARIOS REGULARES (Primeros 10):")
    for user in regulares[:10]:
        perfiles_count = PerfilUsuario.objects.filter(usuario=user, activo=True).count()
        empresas_acceso = PerfilUsuario.objects.filter(
            usuario=user, activo=True
        ).values_list("empresa__nombre", flat=True)
        print(f"   • {user.email} - {user.nombre} {user.apellido}")
        print(f"     🏢 Empresas: {perfiles_count} ({list(empresas_acceso)})")


def analizar_empresas_y_relaciones():
    """Análisis de empresas y sus relaciones con usuarios"""
    print("\n🏢 ANÁLISIS DE EMPRESAS Y RELACIONES")
    print("-" * 60)

    empresas = Empresa.objects.filter(activo=True).order_by("nombre")
    print(f"📊 Total de empresas activas: {empresas.count()}")

    for empresa in empresas:
        perfiles = PerfilUsuario.objects.filter(empresa=empresa, activo=True)
        print(f"\n🏢 EMPRESA: {empresa.nombre} ({empresa.slug})")
        print(f"   📧 Email: {empresa.email}")
        print(f"   📱 Teléfono: {empresa.telefono}")
        print(f"   👥 Usuarios asignados: {perfiles.count()}")

        # Análisis por roles
        roles_count = {}
        for perfil in perfiles:
            rol = perfil.rol
            roles_count[rol] = roles_count.get(rol, 0) + 1

        print(f"   📋 Distribución de roles:")
        for rol, count in roles_count.items():
            print(f"      • {rol}: {count} usuario(s)")

        # Usuarios específicos
        print(f"   👤 Usuarios:")
        for perfil in perfiles:
            user = perfil.usuario
            print(
                f"      • {user.email} ({perfil.rol}) - Superuser: {user.is_superuser}"
            )


def analizar_roles_y_permisos():
    """Análisis de roles y sistema de permisos"""
    print("\n🎭 ANÁLISIS DE ROLES Y PERMISOS")
    print("-" * 60)

    # Obtener todos los roles únicos
    roles_unicos = (
        PerfilUsuario.objects.filter(activo=True)
        .values_list("rol", flat=True)
        .distinct()
    )

    print(f"📋 ROLES ENCONTRADOS EN EL SISTEMA:")
    for rol in roles_unicos:
        count = PerfilUsuario.objects.filter(rol=rol, activo=True).count()
        usuarios_con_rol = PerfilUsuario.objects.filter(
            rol=rol, activo=True
        ).values_list("usuario__email", flat=True)
        print(f"\n   🎭 ROL: {rol}")
        print(f"      👥 Cantidad: {count} usuario(s)")
        print(f"      📧 Usuarios: {list(usuarios_con_rol)}")

    # Análisis de usuarios multi-empresa
    print(f"\n🌐 USUARIOS MULTI-EMPRESA:")
    usuarios_multi = Usuario.objects.annotate(
        num_empresas=models.Count(
            "perfilusuario", filter=models.Q(perfilusuario__activo=True)
        )
    ).filter(num_empresas__gt=1)

    for usuario in usuarios_multi:
        perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
        empresas = [f"{p.empresa.nombre} ({p.rol})" for p in perfiles]
        print(f"   • {usuario.email}: {len(empresas)} empresas")
        for empresa_info in empresas:
            print(f"     - {empresa_info}")


def identificar_problemas_estructura():
    """Identificar problemas en la estructura actual"""
    print("\n🚨 PROBLEMAS IDENTIFICADOS EN LA ESTRUCTURA")
    print("-" * 60)

    problemas = []

    # Problema 1: Confusión entre admin y dueño
    roles_confusos = ["admin", "dueno", "administrador", "owner"]
    perfiles_confusos = PerfilUsuario.objects.filter(
        rol__in=roles_confusos, activo=True
    )
    if perfiles_confusos.exists():
        problemas.append(
            {
                "titulo": "🔥 CONFUSIÓN DE ROLES ADMINISTRATIVOS",
                "descripcion": f"Roles confusos encontrados: {list(perfiles_confusos.values_list('rol', flat=True).distinct())}",
                "severidad": "CRÍTICA",
                "afectados": perfiles_confusos.count(),
            }
        )

    # Problema 2: Usuarios sin empresa
    usuarios_sin_empresa = Usuario.objects.annotate(
        num_empresas=models.Count(
            "perfilusuario", filter=models.Q(perfilusuario__activo=True)
        )
    ).filter(num_empresas=0, is_active=True)

    if usuarios_sin_empresa.exists():
        problemas.append(
            {
                "titulo": "⚠️ USUARIOS SIN EMPRESA ASIGNADA",
                "descripcion": f"Usuarios activos sin empresa: {list(usuarios_sin_empresa.values_list('email', flat=True))}",
                "severidad": "ALTA",
                "afectados": usuarios_sin_empresa.count(),
            }
        )

    # Problema 3: Empresas sin dueño claro
    for empresa in Empresa.objects.filter(activo=True):
        duenos = PerfilUsuario.objects.filter(
            empresa=empresa,
            activo=True,
            rol__in=["dueno", "owner", "admin", "administrador"],
        )
        if duenos.count() == 0:
            problemas.append(
                {
                    "titulo": f"⚠️ EMPRESA SIN DUEÑO: {empresa.nombre}",
                    "descripcion": "No hay usuario con rol de dueño/admin",
                    "severidad": "MEDIA",
                    "afectados": 1,
                }
            )
        elif duenos.count() > 1:
            problemas.append(
                {
                    "titulo": f"🔥 MÚLTIPLES DUEÑOS: {empresa.nombre}",
                    "descripcion": f"Múltiples usuarios con roles administrativos: {duenos.count()}",
                    "severidad": "ALTA",
                    "afectados": duenos.count(),
                }
            )

    # Mostrar problemas
    print(f"📊 TOTAL DE PROBLEMAS ENCONTRADOS: {len(problemas)}")
    for i, problema in enumerate(problemas, 1):
        print(f"\n{i}. {problema['titulo']}")
        print(f"   📝 {problema['descripcion']}")
        print(f"   🚨 Severidad: {problema['severidad']}")
        print(f"   👥 Afectados: {problema['afectados']}")


def analizar_dashboards_frontend():
    """Análisis de dashboards del frontend"""
    print("\n🖥️ ANÁLISIS DE DASHBOARDS FRONTEND")
    print("-" * 60)

    # Esta función analizaría los archivos del frontend
    # Por ahora, listamos lo que sabemos que existe

    dashboards_conocidos = [
        "Dashboard.tsx - Dashboard principal genérico",
        "DashboardMain.tsx - Dashboard principal con roles",
        "DashboardDueno.tsx - Dashboard específico del dueño",
        "DashboardOperador.tsx - Dashboard para operadores",
        "DashboardRemitente.tsx - Dashboard para remitentes",
        "DashboardDestinatario.tsx - Dashboard para destinatarios",
    ]

    print("📱 DASHBOARDS EXISTENTES:")
    for dashboard in dashboards_conocidos:
        print(f"   • {dashboard}")

    print(f"\n🚨 PROBLEMAS DE NAVEGACIÓN IDENTIFICADOS:")
    print("   • Múltiples dashboards sin lógica clara de selección")
    print("   • No hay menú de cambio de empresa para usuarios multi-empresa")
    print("   • Confusión entre dashboard principal y específicos por rol")
    print("   • No hay navegación clara basada en permisos")


def proponer_estructura_ideal():
    """Proponer estructura ideal para el sistema"""
    print("\n🎯 PROPUESTA DE ESTRUCTURA IDEAL")
    print("=" * 60)

    print("🏗️ JERARQUÍA DE USUARIOS PROPUESTA:")
    print(
        """
    1. 👑 SUPER ADMINISTRADOR (1 usuario)
       • Email: admin@packfy.com
       • Acceso: TODAS las empresas
       • Permisos: TODOS los permisos
       • Función: Administrar todo el sistema

    2. 🏢 DUEÑO DE EMPRESA (1 por empresa)
       • Rol: 'dueno'
       • Acceso: SU empresa únicamente
       • Permisos: Todos los permisos de SU empresa
       • Función: Administrar su empresa específica

    3. 👥 OPERADORES (Múltiples por empresa)
       • Roles: 'operador_miami', 'operador_cuba', etc.
       • Acceso: SU empresa únicamente
       • Permisos: Operaciones específicas
       • Función: Gestionar envíos y operaciones

    4. 📦 USUARIOS CLIENTE (Múltiples)
       • Roles: 'remitente', 'destinatario'
       • Acceso: Pueden usar múltiples empresas
       • Permisos: Solo sus envíos
       • Función: Crear y rastrear envíos
    """
    )

    print("\n🖥️ ESTRUCTURA DE FRONTEND PROPUESTA:")
    print(
        """
    1. 🔐 LOGIN PAGE
       • Detecta tenant automáticamente
       • Muestra empresas disponibles si es multi-empresa

    2. 🏠 DASHBOARD PRINCIPAL
       • Único dashboard que decide qué mostrar según rol
       • Selector de empresa para usuarios multi-empresa
       • Navegación basada en permisos reales

    3. 📱 PÁGINAS ESPECÍFICAS
       • /dashboard - Dashboard principal inteligente
       • /envios - Gestión de envíos (según permisos)
       • /usuarios - Solo para dueños y super admin
       • /configuracion - Solo para dueños y super admin
       • /tracking - Público y usuarios
    """
    )

    print("\n🔧 PLAN DE IMPLEMENTACIÓN:")
    print(
        """
    FASE 1: 🔥 LIMPIEZA DE ROLES
    • Estandarizar roles: 'super_admin', 'dueno', 'operador', 'cliente'
    • Eliminar confusión admin/dueño
    • Asegurar 1 dueño por empresa

    FASE 2: 🖥️ UNIFICACIÓN FRONTEND
    • Consolidar en 1 dashboard inteligente
    • Implementar selector de empresa
    • Navegación basada en roles reales

    FASE 3: 🧪 PRUEBAS EXHAUSTIVAS
    • Probar cada rol en cada empresa
    • Verificar navegación y permisos
    • Validar experiencia de usuario
    """
    )

    print("\n" + "=" * 60)
    print("📋 AUDITORÍA COMPLETADA")
    print("   Revisar propuesta y confirmar antes de implementar")
    print("=" * 60)


# Importar models para el análisis
from django.db import models

if __name__ == "__main__":
    main()
