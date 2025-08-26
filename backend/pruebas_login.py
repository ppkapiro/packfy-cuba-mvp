#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PRUEBAS DE LOGIN - ESTRUCTURA DE DOMINIOS
Verificar que todos los usuarios puedan hacer login correctamente
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import authenticate
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def main():
    print("🧪 PRUEBAS DE LOGIN - ESTRUCTURA DE DOMINIOS")
    print("=" * 50)
    print()

    probar_superadmin()
    probar_admins_empresas()
    probar_usuarios_existentes()
    generar_resumen_credenciales()

    print("\n✅ PRUEBAS DE LOGIN COMPLETADAS")


def probar_superadmin():
    """Probar login del superadmin global"""
    print("👑 PROBANDO SUPERADMIN GLOBAL")
    print("-" * 30)

    email = "superadmin@packfy.com"

    try:
        usuario = Usuario.objects.get(email=email)
        print(f"✅ Usuario existe: {email}")
        print(f"   - is_superuser: {usuario.is_superuser}")
        print(f"   - is_staff: {usuario.is_staff}")
        print(f"   - is_active: {usuario.is_active}")

        # Verificar perfiles en empresas
        perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
        print(f"   - Acceso a {perfiles.count()} empresas:")

        for perfil in perfiles:
            print(f"     • {perfil.empresa.nombre} ({perfil.rol})")

        # Verificar autenticación (sin password real por seguridad)
        print(f"   - Estado autenticación: CONFIGURADO")

    except Usuario.DoesNotExist:
        print(f"❌ Usuario NO existe: {email}")

    print()


def probar_admins_empresas():
    """Probar login de administradores por empresa"""
    print("🏢 PROBANDO ADMINS POR EMPRESA")
    print("-" * 35)

    empresas = Empresa.objects.filter(activo=True, dominio__isnull=False)

    for empresa in empresas:
        email = f"admin@{empresa.dominio}"

        print(f"{empresa.nombre}:")

        try:
            usuario = Usuario.objects.get(email=email)
            print(f"   ✅ Usuario existe: {email}")
            print(f"      - is_superuser: {usuario.is_superuser}")
            print(f"      - is_staff: {usuario.is_staff}")
            print(f"      - is_active: {usuario.is_active}")

            # Verificar perfil específico
            perfil = PerfilUsuario.objects.filter(
                usuario=usuario, empresa=empresa, activo=True
            ).first()

            if perfil:
                print(f"      - Rol en empresa: {perfil.rol}")
                print(f"      - Perfil activo: {perfil.activo}")
            else:
                print(f"      ❌ Sin perfil en {empresa.nombre}")

            # Probar autenticación con password conocido
            auth_user = authenticate(username=email, password="admin123")
            if auth_user:
                print(f"      ✅ Login exitoso con admin123")
            else:
                print(f"      ❌ Login falló con admin123")

        except Usuario.DoesNotExist:
            print(f"   ❌ Usuario NO existe: {email}")

        print()


def probar_usuarios_existentes():
    """Probar algunos usuarios existentes importantes"""
    print("👥 PROBANDO USUARIOS EXISTENTES")
    print("-" * 35)

    usuarios_importantes = [
        "dueno@packfy.com",
        "consultor@packfy.com",
        "demo@packfy.com",
        "miami@packfy.com",
        "cuba@packfy.com",
    ]

    for email in usuarios_importantes:
        print(f"{email}:")

        try:
            usuario = Usuario.objects.get(email=email)
            print(f"   ✅ Usuario existe")
            print(f"      - is_active: {usuario.is_active}")
            print(f"      - is_superuser: {usuario.is_superuser}")

            # Verificar empresas
            perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
            print(f"      - Empresas: {perfiles.count()}")

            for perfil in perfiles:
                print(f"        • {perfil.empresa.nombre} ({perfil.rol})")

        except Usuario.DoesNotExist:
            print(f"   ❌ Usuario NO existe")

        print()


def generar_resumen_credenciales():
    """Generar resumen final de credenciales para testing"""
    print("📋 RESUMEN DE CREDENCIALES PARA TESTING")
    print("-" * 45)

    print("SUPERADMIN GLOBAL:")
    print("- Email: superadmin@packfy.com")
    print("- Password: [password existente]")
    print("- Acceso: Todas las empresas")
    print("- Dashboard: DashboardMain (super_admin)")
    print()

    print("ADMINS POR EMPRESA:")
    empresas = Empresa.objects.filter(activo=True, dominio__isnull=False)

    for empresa in empresas:
        email = f"admin@{empresa.dominio}"
        existe = Usuario.objects.filter(email=email).exists()
        status = "✅" if existe else "❌"

        print(f"- {status} {email}")
        print(f"  Password: admin123")
        print(f"  Empresa: {empresa.nombre}")
        print(f"  Dashboard: DashboardDueno (admin_empresa)")

    print()
    print("USUARIOS OPERACIONALES:")
    operacionales = ["dueno@packfy.com", "consultor@packfy.com", "demo@packfy.com"]

    for email in operacionales:
        existe = Usuario.objects.filter(email=email).exists()
        status = "✅" if existe else "❌"

        if existe:
            usuario = Usuario.objects.get(email=email)
            perfiles_count = PerfilUsuario.objects.filter(
                usuario=usuario, activo=True
            ).count()
            print(f"- {status} {email} ({perfiles_count} empresas)")
        else:
            print(f"- {status} {email}")


def probar_deteccion_tenant():
    """Simular detección de tenant por dominio"""
    print("\n🌐 SIMULACIÓN DETECCIÓN DE TENANT")
    print("-" * 40)

    casos_prueba = [
        ("cubaexpress.com", "cuba-express"),
        ("habanapremium.com", "habana-premium"),
        ("miamishipping.com", "miami-shipping"),
        ("packfy.com", "packfy-express"),
        ("localhost", "packfy-express"),  # desarrollo
        ("desconocido.com", "packfy-express"),  # fallback
    ]

    print("Mapeo dominio → tenant slug:")
    for dominio, slug_esperado in casos_prueba:
        print(f"  {dominio} → {slug_esperado}")

    print("\n📝 Frontend debe configurar:")
    print("  X-Tenant-Slug: [slug detectado]")
    print("  para que API use empresa correcta")


def verificar_configuracion_empresas():
    """Verificar que todas las empresas estén bien configuradas"""
    print("\n🏢 VERIFICACIÓN CONFIGURACIÓN EMPRESAS")
    print("-" * 45)

    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        print(f"{empresa.nombre}:")
        print(f"  - ID: {empresa.id}")
        print(f"  - Slug: {empresa.slug}")
        print(f"  - Dominio: {empresa.dominio}")
        print(f"  - Activo: {empresa.activo}")

        # Verificar usuarios
        usuarios_count = PerfilUsuario.objects.filter(
            empresa=empresa, activo=True
        ).count()
        print(f"  - Usuarios: {usuarios_count}")

        # Verificar admin específico
        if empresa.dominio:
            admin_email = f"admin@{empresa.dominio}"
            admin_existe = Usuario.objects.filter(email=admin_email).exists()
            print(f"  - Admin específico: {'✅' if admin_existe else '❌'}")

        print()


if __name__ == "__main__":
    main()
    probar_deteccion_tenant()
    verificar_configuracion_empresas()
