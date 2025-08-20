#!/usr/bin/env python3
"""
🔧 Script para corregir permisos de usuarios
Basado en la imagen del panel de administración
"""
import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.append("/app")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def corregir_permisos_usuarios():
    """Corregir permisos basado en la imagen del admin"""

    print("=== 🔧 CORRIGIENDO PERMISOS DE USUARIOS ===")

    try:
        # Obtener la empresa
        empresa = Empresa.objects.get(slug="packfy-express")
        print(f"✅ Empresa encontrada: {empresa.nombre}")

        # 1. Corregir cuba@packfy.com - debe ser OPERADOR_CUBA
        print("\n🔧 Corrigiendo cuba@packfy.com...")
        try:
            user_cuba = Usuario.objects.get(email="cuba@packfy.com")

            # Activar el usuario si no está activo
            if not user_cuba.is_active:
                user_cuba.is_active = True
                user_cuba.save()
                print("✅ Usuario cuba@packfy.com activado")

            # Verificar/crear perfil de empresa
            perfil_cuba, created = PerfilUsuario.objects.get_or_create(
                usuario=user_cuba,
                empresa=empresa,
                defaults={"rol": "operador_cuba"},
            )

            if created:
                print(
                    "✅ Perfil creado para cuba@packfy.com como OPERADOR_CUBA"
                )
            else:
                print(
                    f"✅ Perfil existente para cuba@packfy.com: {perfil_cuba.rol}"
                )

        except Usuario.DoesNotExist:
            print("❌ Usuario cuba@packfy.com no encontrado")

        # 2. Verificar dueno@packfy.com
        print("\n🔧 Verificando dueno@packfy.com...")
        try:
            user_dueno = Usuario.objects.get(email="dueno@packfy.com")

            # Asegurar que es staff y superuser
            if not user_dueno.is_staff:
                user_dueno.is_staff = True
                user_dueno.save()
                print("✅ dueno@packfy.com configurado como staff")

            # Verificar perfil
            perfil_dueno, created = PerfilUsuario.objects.get_or_create(
                usuario=user_dueno, empresa=empresa, defaults={"rol": "dueno"}
            )

            if created:
                print("✅ Perfil creado para dueno@packfy.com como DUEÑO")
            else:
                print(
                    f"✅ Perfil existente para dueno@packfy.com: {perfil_dueno.rol}"
                )

        except Usuario.DoesNotExist:
            print("❌ Usuario dueno@packfy.com no encontrado")

        # 3. Verificar miami@packfy.com
        print("\n🔧 Verificando miami@packfy.com...")
        try:
            user_miami = Usuario.objects.get(email="miami@packfy.com")

            # Verificar perfil
            perfil_miami, created = PerfilUsuario.objects.get_or_create(
                usuario=user_miami,
                empresa=empresa,
                defaults={"rol": "operador_miami"},
            )

            if created:
                print(
                    "✅ Perfil creado para miami@packfy.com como OPERADOR_MIAMI"
                )
            else:
                print(
                    f"✅ Perfil existente para miami@packfy.com: {perfil_miami.rol}"
                )

        except Usuario.DoesNotExist:
            print("❌ Usuario miami@packfy.com no encontrado")

        # 4. Crear admin@packfy.cu si no existe
        print("\n🔧 Verificando admin@packfy.cu...")
        user_admin, created = Usuario.objects.get_or_create(
            email="admin@packfy.cu",
            defaults={
                "username": "admin@packfy.cu",
                "first_name": "Administrador",
                "last_name": "Packfy",
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            user_admin.set_password("admin123")
            user_admin.save()
            print("✅ Usuario admin@packfy.cu creado")
        else:
            # Asegurar que tiene los permisos correctos
            user_admin.is_active = True
            user_admin.is_staff = True
            user_admin.is_superuser = True
            user_admin.save()
            print("✅ Usuario admin@packfy.cu corregido")

        # Crear perfil de empresa para admin
        perfil_admin, created = PerfilUsuario.objects.get_or_create(
            usuario=user_admin, empresa=empresa, defaults={"rol": "dueno"}
        )

        if created:
            print("✅ Perfil creado para admin@packfy.cu como DUEÑO")

        # 5. Mostrar resumen final
        print("\n=== 📋 RESUMEN FINAL ===")
        for perfil in PerfilUsuario.objects.filter(empresa=empresa):
            user = perfil.usuario
            print(
                f"• {user.email}: {perfil.rol} (activo: {user.is_active}, staff: {user.is_staff})"
            )

        print("\n✅ ¡Permisos corregidos exitosamente!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    corregir_permisos_usuarios()
