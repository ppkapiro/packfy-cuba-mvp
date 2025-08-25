#!/usr/bin/env python3
"""
🔍 AUDITORÍA COMPLETA DE BASE DE DATOS - MULTITENANCY
Packfy Cuba - Revisión completa antes de configurar dominios
"""

import os
import sys

import django

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from empresas.models import Empresa, PerfilUsuario
from envios.models import Envio
from usuarios.models import Usuario


def mostrar_separador(titulo):
    """Mostrar separador visual"""
    print("\n" + "=" * 80)
    print(f"🔍 {titulo}")
    print("=" * 80)


def auditar_usuarios():
    """Auditar todos los usuarios del sistema"""
    mostrar_separador("USUARIOS DEL SISTEMA")

    usuarios = Usuario.objects.all().order_by("id")
    print(f"📊 Total de usuarios: {usuarios.count()}")

    if usuarios.count() == 0:
        print("⚠️  No hay usuarios en el sistema")
        return

    print("\n🔍 LISTADO DETALLADO DE USUARIOS:")
    print("-" * 80)

    for usuario in usuarios:
        print(f"🆔 ID: {usuario.id}")
        print(f"📧 Email: {usuario.email}")
        print(f"👤 Nombre: {usuario.first_name} {usuario.last_name}")
        print(f"🔑 Username: {usuario.username}")
        print(f"✅ Activo: {'Sí' if usuario.is_active else 'No'}")
        print(f"👑 Staff: {'Sí' if usuario.is_staff else 'No'}")
        print(f"🏆 Superuser: {'Sí' if usuario.is_superuser else 'No'}")
        print(f"📅 Creado: {usuario.date_joined}")
        print(f"🕒 Último login: {usuario.last_login}")
        print("-" * 40)


def auditar_empresas():
    """Auditar todas las empresas del sistema"""
    mostrar_separador("EMPRESAS DEL SISTEMA")

    empresas = Empresa.objects.all().order_by("id")
    print(f"📊 Total de empresas: {empresas.count()}")

    if empresas.count() == 0:
        print("⚠️  No hay empresas en el sistema")
        return

    print("\n🔍 LISTADO DETALLADO DE EMPRESAS:")
    print("-" * 80)

    for empresa in empresas:
        print(f"🆔 ID: {empresa.id}")
        print(f"🏢 Nombre: {empresa.nombre}")
        print(
            f"🔗 Slug: {empresa.slug if hasattr(empresa, 'slug') and empresa.slug else '❌ SIN SLUG'}"
        )
        print(
            f"📝 Descripción: {empresa.descripcion if hasattr(empresa, 'descripcion') else 'N/A'}"
        )
        print(f"✅ Activo: {'Sí' if empresa.activo else 'No'}")
        print(f"📅 Fecha creación: {empresa.fecha_creacion}")

        # Mostrar configuración si existe
        if hasattr(empresa, "configuracion") and empresa.configuracion:
            print(f"⚙️  Configuración: {empresa.configuracion}")

        print("-" * 40)


def auditar_perfiles():
    """Auditar todos los perfiles de usuario"""
    mostrar_separador("PERFILES DE USUARIO")

    perfiles = PerfilUsuario.objects.all().order_by("empresa_id", "usuario_id")
    print(f"📊 Total de perfiles: {perfiles.count()}")

    if perfiles.count() == 0:
        print("⚠️  No hay perfiles en el sistema")
        return

    print("\n🔍 LISTADO DETALLADO DE PERFILES:")
    print("-" * 80)

    for perfil in perfiles:
        print(f"🆔 ID: {perfil.id}")
        print(f"👤 Usuario: {perfil.usuario.email} (ID: {perfil.usuario.id})")
        print(f"🏢 Empresa: {perfil.empresa.nombre} (ID: {perfil.empresa.id})")
        if hasattr(perfil.empresa, "slug") and perfil.empresa.slug:
            print(f"🔗 Slug empresa: {perfil.empresa.slug}")
        print(f"👔 Rol: {perfil.rol}")
        print(f"✅ Activo: {'Sí' if perfil.activo else 'No'}")
        print(f"📅 Fecha ingreso: {perfil.fecha_ingreso}")

        # Mostrar configuración del perfil si existe
        if hasattr(perfil, "configuracion") and perfil.configuracion:
            print(f"⚙️  Configuración perfil: {perfil.configuracion}")

        print("-" * 40)


def auditar_envios():
    """Auditar envíos para ver distribución por empresa"""
    mostrar_separador("ENVÍOS POR EMPRESA")

    envios = Envio.objects.all()
    print(f"📊 Total de envíos: {envios.count()}")

    if envios.count() == 0:
        print("⚠️  No hay envíos en el sistema")
        return

    # Agrupar por empresa
    empresas_con_envios = {}

    for envio in envios:
        empresa_id = envio.empresa.id if envio.empresa else "Sin empresa"
        empresa_nombre = (
            envio.empresa.nombre if envio.empresa else "Sin empresa"
        )

        if empresa_id not in empresas_con_envios:
            empresas_con_envios[empresa_id] = {
                "nombre": empresa_nombre,
                "count": 0,
                "envios": [],
            }

        empresas_con_envios[empresa_id]["count"] += 1
        empresas_con_envios[empresa_id]["envios"].append(
            {
                "id": envio.id,
                "numero_rastreo": envio.numero_rastreo,
                "estado": envio.estado,
                "fecha_creacion": envio.fecha_creacion,
            }
        )

    print("\n🔍 DISTRIBUCIÓN DE ENVÍOS POR EMPRESA:")
    print("-" * 80)

    for empresa_id, data in empresas_con_envios.items():
        print(f"🏢 {data['nombre']} (ID: {empresa_id})")
        print(f"📦 Envíos: {data['count']}")

        # Mostrar algunos envíos como ejemplo
        for i, envio in enumerate(data["envios"][:3]):  # Solo primeros 3
            print(
                f"   📋 {envio['numero_rastreo']} - {envio['estado']} - {envio['fecha_creacion']}"
            )

        if len(data["envios"]) > 3:
            print(f"   ... y {len(data['envios']) - 3} envíos más")

        print("-" * 40)


def verificar_integridad_relaciones():
    """Verificar integridad de las relaciones entre modelos"""
    mostrar_separador("VERIFICACIÓN DE INTEGRIDAD")

    print("🔍 Verificando relaciones entre modelos...")

    # Verificar usuarios sin perfiles
    usuarios_sin_perfil = Usuario.objects.filter(perfilusuario__isnull=True)
    print(f"👤 Usuarios sin perfiles: {usuarios_sin_perfil.count()}")

    if usuarios_sin_perfil.count() > 0:
        print("   📋 Usuarios sin perfil:")
        for usuario in usuarios_sin_perfil:
            print(f"      • {usuario.email} (ID: {usuario.id})")

    # Verificar empresas sin usuarios
    empresas_sin_usuarios = Empresa.objects.filter(perfilusuario__isnull=True)
    print(f"🏢 Empresas sin usuarios: {empresas_sin_usuarios.count()}")

    if empresas_sin_usuarios.count() > 0:
        print("   📋 Empresas sin usuarios:")
        for empresa in empresas_sin_usuarios:
            print(f"      • {empresa.nombre} (ID: {empresa.id})")

    # Verificar empresas sin slug (crítico para dominios)
    empresas_sin_slug = Empresa.objects.filter(
        slug__isnull=True
    ) | Empresa.objects.filter(slug="")
    print(f"🔗 Empresas sin slug: {empresas_sin_slug.count()}")

    if empresas_sin_slug.count() > 0:
        print("   ⚠️  CRÍTICO: Empresas sin slug (necesario para dominios):")
        for empresa in empresas_sin_slug:
            print(f"      • {empresa.nombre} (ID: {empresa.id})")

    # Verificar slugs duplicados
    slugs_duplicados = (
        Empresa.objects.values("slug")
        .annotate(count=models.Count("slug"))
        .filter(count__gt=1)
    )
    print(f"🔄 Slugs duplicados: {len(slugs_duplicados)}")

    if len(slugs_duplicados) > 0:
        print("   ⚠️  CRÍTICO: Slugs duplicados encontrados:")
        for slug_data in slugs_duplicados:
            empresas_con_slug = Empresa.objects.filter(slug=slug_data["slug"])
            print(
                f"      • Slug '{slug_data['slug']}' usado por {slug_data['count']} empresas:"
            )
            for empresa in empresas_con_slug:
                print(f"        - {empresa.nombre} (ID: {empresa.id})")


def generar_recomendaciones():
    """Generar recomendaciones basadas en la auditoría"""
    mostrar_separador("RECOMENDACIONES")

    print("🎯 Basado en la auditoría, estas son las recomendaciones:")
    print()

    # Verificar si hay empresas sin slug
    empresas_sin_slug = Empresa.objects.filter(
        slug__isnull=True
    ) | Empresa.objects.filter(slug="")

    if empresas_sin_slug.count() > 0:
        print("🚨 ACCIÓN REQUERIDA:")
        print(
            "   1. Hay empresas sin slug - necesario para multitenancy por dominios"
        )
        print("   2. Ejecutar script de configuración para generar slugs")
        print()

    # Verificar usuarios sin perfiles
    usuarios_sin_perfil = Usuario.objects.filter(perfilusuario__isnull=True)

    if usuarios_sin_perfil.count() > 0:
        print("⚠️  ATENCIÓN:")
        print(f"   1. Hay {usuarios_sin_perfil.count()} usuarios sin perfiles")
        print("   2. Considerar crear perfiles o eliminar usuarios huérfanos")
        print()

    # Verificar envíos
    total_envios = Envio.objects.count()
    if total_envios > 0:
        print("📦 DATOS EXISTENTES:")
        print(f"   1. Hay {total_envios} envíos en el sistema")
        print("   2. Verificar que estén correctamente asociados a empresas")
        print()

    print("🎯 PASOS SIGUIENTES RECOMENDADOS:")
    print("   1. Revisar resultados de esta auditoría")
    print("   2. Corregir empresas sin slug si las hay")
    print("   3. Configurar dominios de desarrollo local")
    print("   4. Probar multitenancy por subdominios")
    print("   5. Crear datos de prueba si es necesario")


def main():
    """Función principal de auditoría"""
    print("🔍 INICIANDO AUDITORÍA COMPLETA DE BASE DE DATOS")
    print("🇨🇺 Packfy Cuba - Preparación para Multitenancy por Dominios")
    print("📅 Fecha:", timezone.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        # Ejecutar todas las auditorías
        auditar_usuarios()
        auditar_empresas()
        auditar_perfiles()
        auditar_envios()
        verificar_integridad_relaciones()
        generar_recomendaciones()

        mostrar_separador("AUDITORÍA COMPLETADA")
        print("✅ Auditoría completada exitosamente")
        print("📋 Revisa los resultados anteriores antes de proceder")

    except Exception as e:
        print(f"❌ Error durante la auditoría: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
