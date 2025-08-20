#!/usr/bin/env python3
"""
🔧 Script para corregir permisos de admin Django
El usuario Carlos (dueno@packfy.com) necesita permisos de staff y superuser
"""
import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.append("/app")
django.setup()

from django.contrib.auth.models import Permission
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def corregir_permisos_admin():
    """Corregir permisos de admin Django para usuarios"""

    print("=== 🔧 CORRIGIENDO PERMISOS ADMIN DJANGO ===")

    try:
        # 1. Encontrar al usuario Carlos (dueno@packfy.com)
        print("\n🔍 Buscando usuario Carlos...")
        try:
            carlos = Usuario.objects.get(email="dueno@packfy.com")
            print(
                f"✅ Usuario encontrado: {carlos.first_name} {carlos.last_name} ({carlos.email})"
            )
            print(
                f"   Estado actual: activo={carlos.is_active}, staff={carlos.is_staff}, superuser={carlos.is_superuser}"
            )
        except Usuario.DoesNotExist:
            print("❌ Usuario dueno@packfy.com no encontrado")
            return

        # 2. Corregir permisos de Carlos
        print("\n🔧 Corrigiendo permisos de Carlos...")

        # Activar el usuario
        carlos.is_active = True
        carlos.is_staff = True  # Necesario para acceder al admin
        carlos.is_superuser = True  # Acceso completo al admin
        carlos.save()

        print("✅ Carlos configurado como superuser y staff")

        # 3. Verificar otros usuarios importantes
        print("\n🔍 Verificando otros usuarios...")

        usuarios_admin = ["admin@packfy.cu", "superadmin@packfy.com"]

        for email in usuarios_admin:
            try:
                user = Usuario.objects.get(email=email)
                user.is_active = True
                user.is_staff = True
                user.is_superuser = True
                user.save()
                print(f"✅ {email}: configurado como superuser")
            except Usuario.DoesNotExist:
                print(f"⚠️ {email}: no encontrado")

        # 4. Crear superuser adicional si es necesario
        print("\n🔧 Verificando superuser principal...")

        superuser_email = "admin@packfy.cu"
        try:
            admin = Usuario.objects.get(email=superuser_email)
            print(f"✅ Superuser principal existe: {admin.email}")
        except Usuario.DoesNotExist:
            print("🔧 Creando superuser principal...")
            admin = Usuario.objects.create_superuser(
                email=superuser_email,
                password="admin123",
                first_name="Administrador",
                last_name="Principal",
            )
            print(f"✅ Superuser creado: {admin.email}")

        # 5. Verificar empresa y perfiles
        print("\n🔍 Verificando perfiles de empresa...")

        try:
            empresa = Empresa.objects.get(slug="packfy-express")
            print(f"✅ Empresa encontrada: {empresa.nombre}")

            # Asegurar que Carlos tiene perfil de dueño
            perfil_carlos, created = PerfilUsuario.objects.get_or_create(
                usuario=carlos, empresa=empresa, defaults={"rol": "dueno"}
            )

            if created:
                print("✅ Perfil de dueño creado para Carlos")
            else:
                print(f"✅ Carlos ya tiene perfil: {perfil_carlos.rol}")

        except Empresa.DoesNotExist:
            print("❌ Empresa packfy-express no encontrada")

        # 6. Mostrar resumen final
        print("\n=== 📋 RESUMEN FINAL ===")
        carlos.refresh_from_db()
        print(f"🎯 Carlos ({carlos.email}):")
        print(f"   • Activo: {carlos.is_active}")
        print(f"   • Staff (admin): {carlos.is_staff}")
        print(f"   • Superuser: {carlos.is_superuser}")

        print("\n✅ ¡Permisos de admin corregidos!")
        print("🔑 Carlos ahora puede acceder completamente al admin Django")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    corregir_permisos_admin()
