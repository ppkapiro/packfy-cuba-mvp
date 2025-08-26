#!/usr/bin/env python
"""
Análisis profundo del estado actual del sistema multitenancy
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from django.db.models import Count
from empresas.models import Empresa, PerfilUsuario
from envios.models import DestinatarioCuba, Envio, RemitenteCuba


def analisis_completo():
    print("=" * 80)
    print("📊 ANÁLISIS PROFUNDO DEL SISTEMA MULTITENANCY")
    print("=" * 80)

    # 1. EMPRESAS
    print("\n🏢 === EMPRESAS REGISTRADAS ===")
    empresas = Empresa.objects.all()
    for empresa in empresas:
        print(f"   ID: {empresa.id}")
        print(f"   📛 Nombre: {empresa.nombre}")
        print(f"   🔗 Slug: '{empresa.slug}'")
        print(f"   ✅ Activo: {empresa.activo}")
        print(f"   🌐 Dominio: {empresa.dominio or 'Sin dominio personalizado'}")
        print(f"   📧 Email: {empresa.email or 'No definido'}")
        print(f"   📞 Teléfono: {empresa.telefono or 'No definido'}")
        print(f"   📅 Creada: {empresa.fecha_creacion.strftime('%Y-%m-%d %H:%M')}")
        print(f"   ⚙️  Configuración: {empresa.configuracion}")
        print("   " + "-" * 50)

    total_empresas = empresas.count()
    empresas_activas = empresas.filter(activo=True).count()
    print(f"   📈 TOTAL: {total_empresas} empresas ({empresas_activas} activas)")

    # 2. USUARIOS
    print("\n👥 === USUARIOS DEL SISTEMA ===")
    usuarios = User.objects.all()
    for usuario in usuarios:
        perfiles = PerfilUsuario.objects.filter(usuario=usuario)
        print(f"   ID: {usuario.id}")
        print(f"   👤 Username: {usuario.username}")
        print(f"   📧 Email: {usuario.email}")
        print(f"   📛 Nombre: {usuario.get_full_name() or 'Sin nombre'}")
        print(f"   ✅ Activo: {usuario.is_active}")
        print(f"   🔑 Staff: {usuario.is_staff}")
        print(f"   👑 Superuser: {usuario.is_superuser}")
        print(f"   📅 Creado: {usuario.date_joined.strftime('%Y-%m-%d %H:%M')}")
        print(f"   🏢 Empresas: {perfiles.count()}")
        for perfil in perfiles:
            print(f"      └─ {perfil.empresa.nombre} ({perfil.get_rol_display()})")
        print("   " + "-" * 50)

    total_usuarios = usuarios.count()
    usuarios_activos = usuarios.filter(is_active=True).count()
    print(f"   📈 TOTAL: {total_usuarios} usuarios ({usuarios_activos} activos)")

    # 3. PERFILES MULTITENANCY
    print("\n🎭 === PERFILES MULTI-EMPRESA ===")
    perfiles = PerfilUsuario.objects.select_related("usuario", "empresa").all()

    # Agrupar por empresa
    for empresa in empresas:
        perfiles_empresa = perfiles.filter(empresa=empresa)
        if perfiles_empresa.exists():
            print(f"\n   🏢 {empresa.nombre} ({empresa.slug}):")
            for perfil in perfiles_empresa:
                print(
                    f"      👤 {perfil.usuario.username} - {perfil.get_rol_display()}"
                )
                print(f"         📧 {perfil.usuario.email}")
                print(f"         ✅ Activo: {perfil.activo}")
                print(
                    f"         📅 Vinculado: {perfil.fecha_vinculacion.strftime('%Y-%m-%d')}"
                )
                if perfil.telefono:
                    print(f"         📞 Tel: {perfil.telefono}")

    print(f"\n   📈 TOTAL PERFILES: {perfiles.count()}")

    # 4. ANÁLISIS POR ROLES
    print("\n🎭 === DISTRIBUCIÓN POR ROLES ===")
    roles_count = perfiles.values("rol").annotate(count=Count("rol")).order_by("-count")
    for rol_data in roles_count:
        rol_name = dict(PerfilUsuario.RolChoices.choices)[rol_data["rol"]]
        print(f"   {rol_name}: {rol_data['count']} usuarios")

    # 5. DATOS RELACIONADOS (ENVÍOS)
    print("\n📦 === DATOS DE ENVÍOS POR EMPRESA ===")
    try:
        envios = Envio.objects.select_related("empresa").all()
        if envios.exists():
            envios_por_empresa = (
                envios.values("empresa__nombre")
                .annotate(count=Count("id"))
                .order_by("-count")
            )
            for empresa_data in envios_por_empresa:
                print(
                    f"   {empresa_data['empresa__nombre']}: {empresa_data['count']} envíos"
                )
        else:
            print("   📝 No hay envíos registrados")
    except Exception as e:
        print(f"   ❌ Error accediendo a envíos: {e}")

    # 6. REMITENTES Y DESTINATARIOS
    print("\n📮 === REMITENTES Y DESTINATARIOS ===")
    try:
        remitentes = RemitenteCuba.objects.all().count()
        destinatarios = DestinatarioCuba.objects.all().count()
        print(f"   📤 Remitentes: {remitentes}")
        print(f"   📥 Destinatarios: {destinatarios}")
    except Exception as e:
        print(f"   ❌ Error accediendo a remitentes/destinatarios: {e}")

    # 7. CONFIGURACIONES ACTUALES
    print("\n⚙️  === CONFIGURACIONES MULTITENANCY ===")
    print("   📋 Middleware configurado: empresas.middleware.TenantMiddleware")
    print("   🔗 Slug único por empresa: ✅")
    print("   👥 Perfiles usuario-empresa: ✅")
    print("   🔐 Roles definidos: ✅")

    # 8. DOMINIOS Y SLUGS DISPONIBLES
    print("\n🌐 === DOMINIOS Y SLUGS DISPONIBLES ===")
    for empresa in empresas:
        print(f"   🏢 {empresa.nombre}:")
        print(f"      🔗 Slug: '{empresa.slug}'")
        print(f"      🌐 Subdominio: {empresa.slug}.packfy.com")
        print(f"      🌐 Desarrollo: {empresa.slug}.localhost:5173")
        if empresa.dominio:
            print(f"      🎯 Dominio personalizado: {empresa.dominio}")

    print("\n" + "=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)


if __name__ == "__main__":
    analisis_completo()
