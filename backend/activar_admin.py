#!/usr/b# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')/env python
"""
Script para activar usuario admin
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "packfy_cuba_mvp.settings")
django.setup()

from django.contrib.auth.models import User


def activar_admin():
    try:
        user = User.objects.get(email="admin@packfy.com")
        user.is_active = True
        user.save()
        print(f"✅ Usuario {user.email} activado exitosamente")
        print(f"   is_active: {user.is_active}")
        print(f"   is_staff: {user.is_staff}")
        print(f"   is_superuser: {user.is_superuser}")
        return True
    except User.DoesNotExist:
        print("❌ Usuario admin@packfy.com no encontrado")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("🔧 ACTIVANDO USUARIO ADMIN")
    print("=" * 30)
    activar_admin()
