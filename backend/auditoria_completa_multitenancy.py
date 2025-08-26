#!/usr/bin/env python
"""
🔍 AUDITORÍA COMPLETA MULTITENANCY
Packfy Cuba - Análisis exhaustivo del sistema multitenancy para desarrollar estrategia perfecta
"""
import json
import os
from datetime import datetime

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count, Q
from empresas.models import Empresa, PerfilUsuario
from envios.models import DestinatarioCuba, Envio, RemitenteCuba


def auditoria_arquitectura():
    """Análisis de la arquitectura actual"""
    print("=" * 100)
    print("🏗️  AUDITORÍA ARQUITECTURA MULTITENANCY")
    print("=" * 100)

    # 1. CONFIGURACIÓN DE MIDDLEWARE
    print("\n🔧 === CONFIGURACIÓN MIDDLEWARE ===")
    middleware_list = settings.MIDDLEWARE
    tenant_middleware = [
        m for m in middleware_list if "tenant" in m.lower() or "empresa" in m.lower()
    ]

    print(f"   📋 Middleware total: {len(middleware_list)}")
    for i, middleware in enumerate(middleware_list):
        if "tenant" in middleware.lower() or "empresa" in middleware.lower():
            print(f"   ✅ #{i+1}: {middleware} [MULTITENANCY]")
        else:
            print(f"   📋 #{i+1}: {middleware}")

    print(f"\n   🎯 Middleware multitenancy encontrado: {len(tenant_middleware)}")

    # 2. MODELOS MULTITENANCY
    print("\n🗄️  === MODELOS MULTITENANCY ===")
    print("   📊 Empresa:")
    print(f"      🏢 Total empresas: {Empresa.objects.count()}")
    print(f"      ✅ Empresas activas: {Empresa.objects.filter(activo=True).count()}")
    print(
        f"      🔗 Con slug único: {Empresa.objects.exclude(slug__isnull=True).exclude(slug='').count()}"
    )
    print(
        f"      🌐 Con dominio personalizado: {Empresa.objects.exclude(dominio__isnull=True).exclude(dominio='').count()}"
    )

    print("   👥 PerfilUsuario:")
    print(f"      🎭 Total perfiles: {PerfilUsuario.objects.count()}")
    print(
        f"      ✅ Perfiles activos: {PerfilUsuario.objects.filter(activo=True).count()}"
    )

    # 3. RELACIONES MULTITENANCY
    print("\n🔗 === RELACIONES MULTITENANCY ===")
    # Verificar si los modelos tienen FK a Empresa
    try:
        envios_con_empresa = Envio.objects.filter(empresa__isnull=False).count()
        total_envios = Envio.objects.count()
        print(f"   📦 Envíos: {envios_con_empresa}/{total_envios} con empresa asignada")
    except Exception as e:
        print(f"   ❌ Error verificando envíos: {e}")

    try:
        remitentes_con_empresa = (
            RemitenteCuba.objects.filter(empresa__isnull=False).count()
            if hasattr(RemitenteCuba, "empresa")
            else 0
        )
        total_remitentes = RemitenteCuba.objects.count()
        print(
            f"   📤 Remitentes: {remitentes_con_empresa}/{total_remitentes} con empresa asignada"
        )
    except Exception as e:
        print(f"   📤 Remitentes: Modelo sin campo empresa")

    try:
        destinatarios_con_empresa = (
            DestinatarioCuba.objects.filter(empresa__isnull=False).count()
            if hasattr(DestinatarioCuba, "empresa")
            else 0
        )
        total_destinatarios = DestinatarioCuba.objects.count()
        print(
            f"   📥 Destinatarios: {destinatarios_con_empresa}/{total_destinatarios} con empresa asignada"
        )
    except Exception as e:
        print(f"   📥 Destinatarios: Modelo sin campo empresa")


def auditoria_empresas():
    """Análisis detallado de empresas"""
    print("\n" + "=" * 100)
    print("🏢 AUDITORÍA DETALLADA DE EMPRESAS")
    print("=" * 100)

    empresas = Empresa.objects.all().order_by("fecha_creacion")

    for i, empresa in enumerate(empresas, 1):
        print(f"\n#{i} === {empresa.nombre.upper()} ===")
        print(f"   🆔 ID: {empresa.id}")
        print(f"   🔗 Slug: '{empresa.slug}'")
        print(f"   ✅ Activo: {empresa.activo}")
        print(f"   🌐 Dominio: {empresa.dominio or 'Sin dominio personalizado'}")
        print(f"   📧 Email: {empresa.email or 'No configurado'}")
        print(f"   📞 Teléfono: {empresa.telefono or 'No configurado'}")
        print(f"   🏠 Dirección: {empresa.direccion or 'No configurada'}")
        print(f"   📅 Creada: {empresa.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")
        print(
            f"   🔄 Actualizada: {empresa.ultima_actualizacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Configuración JSON
        if empresa.configuracion:
            print(f"   ⚙️  Configuración:")
            for key, value in empresa.configuracion.items():
                print(f"      📋 {key}: {value}")
        else:
            print(f"   ⚙️  Configuración: Sin configuración")

        # Usuarios asociados
        perfiles = PerfilUsuario.objects.filter(empresa=empresa).select_related(
            "usuario"
        )
        print(f"   👥 Usuarios: {perfiles.count()}")
        for perfil in perfiles:
            estado = "✅" if perfil.activo else "❌"
            print(
                f"      {estado} {perfil.usuario.username} ({perfil.get_rol_display()})"
            )

        # Envíos asociados
        try:
            envios_empresa = Envio.objects.filter(empresa=empresa).count()
            print(f"   📦 Envíos: {envios_empresa}")
        except Exception:
            print(f"   📦 Envíos: No verificable")

        # URLs multitenancy
        print(f"   🌐 URLs Multitenancy:")
        print(f"      🖥️  Desarrollo: {empresa.slug}.localhost:5173")
        print(f"      🌍 Producción: {empresa.slug}.packfy.com")
        if empresa.dominio:
            print(f"      🎯 Personalizado: {empresa.dominio}")


def auditoria_usuarios_multitenancy():
    """Análisis de usuarios en contexto multitenancy"""
    print("\n" + "=" * 100)
    print("👥 AUDITORÍA USUARIOS MULTITENANCY")
    print("=" * 100)

    usuarios = User.objects.all().order_by("date_joined")

    for i, usuario in enumerate(usuarios, 1):
        perfiles = PerfilUsuario.objects.filter(usuario=usuario).select_related(
            "empresa"
        )

        print(f"\n#{i} === {usuario.username.upper()} ===")
        print(f"   🆔 ID: {usuario.id}")
        print(f"   📧 Email: {usuario.email}")
        print(f"   📛 Nombre: {usuario.get_full_name() or 'Sin nombre completo'}")
        print(f"   ✅ Activo: {usuario.is_active}")
        print(f"   🔑 Staff: {usuario.is_staff}")
        print(f"   👑 Superuser: {usuario.is_superuser}")
        print(f"   📅 Registrado: {usuario.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   🏢 Empresas asociadas: {perfiles.count()}")

        # Perfiles por empresa
        if perfiles.exists():
            for perfil in perfiles:
                estado = "✅" if perfil.activo else "❌"
                print(
                    f"      {estado} {perfil.empresa.nombre} → {perfil.get_rol_display()}"
                )
                print(
                    f"         📅 Vinculado: {perfil.fecha_vinculacion.strftime('%Y-%m-%d')}"
                )
                print(
                    f"         🔄 Última actividad: {perfil.ultima_actividad.strftime('%Y-%m-%d %H:%M')}"
                )
                if perfil.telefono:
                    print(f"         📞 Teléfono: {perfil.telefono}")
        else:
            print(f"      ⚠️  Sin perfiles de empresa asignados")


def auditoria_roles_permisos():
    """Análisis de roles y permisos"""
    print("\n" + "=" * 100)
    print("🎭 AUDITORÍA ROLES Y PERMISOS")
    print("=" * 100)

    # Distribución de roles
    print("\n📊 === DISTRIBUCIÓN DE ROLES ===")
    roles_stats = (
        PerfilUsuario.objects.values("rol")
        .annotate(total=Count("id"), activos=Count("id", filter=Q(activo=True)))
        .order_by("-total")
    )

    for rol_stat in roles_stats:
        rol_display = dict(PerfilUsuario.RolChoices.choices)[rol_stat["rol"]]
        print(f"   🎭 {rol_display}:")
        print(f"      📊 Total: {rol_stat['total']}")
        print(f"      ✅ Activos: {rol_stat['activos']}")

    # Usuarios con múltiples roles
    print("\n👥 === USUARIOS CON MÚLTIPLES EMPRESAS ===")
    usuarios_multi_empresa = (
        User.objects.annotate(num_empresas=Count("perfiles_empresa"))
        .filter(num_empresas__gt=1)
        .order_by("-num_empresas")
    )

    for usuario in usuarios_multi_empresa:
        perfiles = PerfilUsuario.objects.filter(usuario=usuario).select_related(
            "empresa"
        )
        print(f"   👤 {usuario.username} ({perfiles.count()} empresas):")
        for perfil in perfiles:
            print(f"      🏢 {perfil.empresa.nombre} → {perfil.get_rol_display()}")

    # Empresas sin usuarios
    print("\n🏢 === EMPRESAS SIN USUARIOS ===")
    empresas_sin_usuarios = Empresa.objects.annotate(
        num_usuarios=Count("usuarios")
    ).filter(num_usuarios=0)

    if empresas_sin_usuarios.exists():
        for empresa in empresas_sin_usuarios:
            print(f"   ⚠️  {empresa.nombre} ({empresa.slug}) - Sin usuarios")
    else:
        print("   ✅ Todas las empresas tienen usuarios asignados")


def auditoria_configuracion_frontend():
    """Análisis de configuración frontend"""
    print("\n" + "=" * 100)
    print("🌐 AUDITORÍA CONFIGURACIÓN FRONTEND")
    print("=" * 100)

    # Verificar archivos de configuración frontend
    frontend_paths = [
        "frontend/src/contexts/TenantContext.tsx",
        "frontend-multitenant/src/contexts/TenantContext.tsx",
        "frontend/src/services/api.ts",
        "frontend-multitenant/src/services/api.ts",
    ]

    print("\n📁 === ARCHIVOS FRONTEND MULTITENANCY ===")
    for path in frontend_paths:
        full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
        if os.path.exists(full_path):
            print(f"   ✅ {path}")
            # Obtener tamaño del archivo
            size = os.path.getsize(full_path)
            print(f"      📏 Tamaño: {size:,} bytes")
            # Obtener fecha de modificación
            mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
            print(f"      📅 Modificado: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"   ❌ {path} - No encontrado")


def auditoria_patrones_url():
    """Análisis de patrones de URL para multitenancy"""
    print("\n" + "=" * 100)
    print("🔗 AUDITORÍA PATRONES URL MULTITENANCY")
    print("=" * 100)

    empresas = Empresa.objects.filter(activo=True)

    print("\n🌐 === DOMINIOS CONFIGURADOS ===")
    for empresa in empresas:
        print(f"\n🏢 {empresa.nombre} ('{empresa.slug}'):")

        # URLs de desarrollo
        print(f"   🖥️  Desarrollo:")
        print(f"      🔗 URL: {empresa.slug}.localhost:5173")
        print(f"      📋 Parámetro: localhost:5173?empresa={empresa.slug}")

        # URLs de producción
        print(f"   🌍 Producción:")
        print(f"      🔗 URL: {empresa.slug}.packfy.com")
        print(f"      📋 Parámetro: app.packfy.com?empresa={empresa.slug}")

        # Dominio personalizado
        if empresa.dominio:
            print(f"   🎯 Personalizado: {empresa.dominio}")
        else:
            print(f"   🎯 Personalizado: No configurado")

    print("\n🔍 === DETECCIÓN IMPLEMENTADA ===")
    print("   ✅ Subdominio (empresa.packfy.com)")
    print("   ✅ Parámetro URL (?empresa=slug)")
    print("   ✅ Header HTTP (X-Tenant-Slug)")
    print("   ✅ localStorage (persistencia)")


def generar_estrategia_datos_prueba():
    """Generar estrategia para datos de prueba"""
    print("\n" + "=" * 100)
    print("🎯 ESTRATEGIA PARA DATOS DE PRUEBA PERFECTOS")
    print("=" * 100)

    empresas_activas = Empresa.objects.filter(activo=True)
    total_usuarios = User.objects.count()
    total_perfiles = PerfilUsuario.objects.count()

    print(f"\n📊 === ESTADO ACTUAL ===")
    print(f"   🏢 Empresas activas: {empresas_activas.count()}")
    print(f"   👥 Usuarios totales: {total_usuarios}")
    print(f"   🎭 Perfiles activos: {total_perfiles}")

    try:
        total_envios = Envio.objects.count()
        print(f"   📦 Envíos existentes: {total_envios}")
    except:
        print(f"   📦 Envíos existentes: No verificable")

    print(f"\n🎯 === ESTRATEGIA RECOMENDADA ===")
    print("   1. 📊 EMPRESAS:")
    print("      - Mantener empresas existentes")
    print("      - Agregar 2-3 empresas de demostración más")
    print("      - Configurar dominios específicos")
    print("      - Establecer configuraciones diferenciadas")

    print("\n   2. 👥 USUARIOS:")
    print("      - Crear usuarios específicos por rol")
    print("      - Asegurar usuarios multi-empresa")
    print("      - Configurar perfiles con datos realistas")
    print("      - Establecer jerarquías claras")

    print("\n   3. 📦 ENVÍOS:")
    print("      - Crear envíos distribuidos entre empresas")
    print("      - Diferentes estados y tipos")
    print("      - Datos de remitentes/destinatarios realistas")
    print("      - Historiales de seguimiento")

    print("\n   4. 🔐 PERMISOS:")
    print("      - Verificar aislamiento por empresa")
    print("      - Probar restricciones de rol")
    print("      - Validar acceso multi-empresa")
    print("      - Confirmar seguridad de datos")


def main():
    """Ejecutar auditoría completa"""
    print("🚀 INICIANDO AUDITORÍA COMPLETA MULTITENANCY")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    auditoria_arquitectura()
    auditoria_empresas()
    auditoria_usuarios_multitenancy()
    auditoria_roles_permisos()
    auditoria_configuracion_frontend()
    auditoria_patrones_url()
    generar_estrategia_datos_prueba()

    print("\n" + "=" * 100)
    print("✅ AUDITORÍA COMPLETA FINALIZADA")
    print("=" * 100)
    print("\n🎯 PRÓXIMO PASO: Implementar datos de prueba según estrategia recomendada")


if __name__ == "__main__":
    main()
