#!/usr/bin/env python3
"""
🔍 Script para verificar usuarios existentes y sus contraseñas
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


def verificar_usuarios():
    """Verificar usuarios existentes y resetear contraseñas conocidas"""

    print("=== 🔍 VERIFICANDO USUARIOS EXISTENTES ===")

    try:
        # Mostrar todos los usuarios
        usuarios = Usuario.objects.all()
        print(f"\n📋 Total usuarios: {usuarios.count()}")

        for user in usuarios:
            print(
                f"• {user.email}: activo={user.is_active}, staff={user.is_staff}, superuser={user.is_superuser}"
            )

        # Resetear contraseñas conocidas
        print("\n🔧 Reseteando contraseñas...")

        # Lista de usuarios con contraseñas conocidas
        usuarios_passwords = [
            ("admin@packfy.cu", "admin123"),
            ("dueno@packfy.com", "dueno123"),
            ("cuba@packfy.com", "cuba123"),
            ("miami@packfy.com", "miami123"),
            ("superadmin@packfy.com", "super123"),
            ("remitente1@packfy.com", "remitente123"),
            ("destinatario1@cuba.cu", "destinatario123"),
        ]

        for email, password in usuarios_passwords:
            try:
                user = Usuario.objects.get(email=email)
                user.set_password(password)
                user.is_active = True  # Asegurar que esté activo
                user.save()
                print(f"✅ {email}: contraseña actualizada a '{password}'")
            except Usuario.DoesNotExist:
                print(f"❌ {email}: usuario no encontrado")

        print("\n📋 CREDENCIALES ACTUALIZADAS:")
        print("• admin@packfy.cu / admin123")
        print("• dueno@packfy.com / dueno123")
        print("• cuba@packfy.com / cuba123")
        print("• miami@packfy.com / miami123")
        print("• superadmin@packfy.com / super123")
        print("• remitente1@packfy.com / remitente123")
        print("• destinatario1@cuba.cu / destinatario123")

        print("\n=== ✅ VERIFICACIÓN COMPLETA ===")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    verificar_usuarios()
