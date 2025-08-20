#!/usr/bin/env python3
"""
Script para eliminar los 3 usuarios extras y dejar exactamente 10 usuarios
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model


def eliminar_usuarios_extras():
    """Eliminar exactamente los 3 usuarios que sobran"""

    User = get_user_model()

    print("🗑️ ELIMINANDO USUARIOS EXTRAS...")

    # Lista de usuarios que NO deben existir
    usuarios_a_eliminar = [
        "admin@packfy.cu",
        "empresa@test.cu",
        "cliente@test.cu",
    ]

    eliminados = 0
    for email in usuarios_a_eliminar:
        try:
            usuario = User.objects.get(email=email)
            print(f"❌ Eliminando: {usuario.id} - {usuario.email}")
            usuario.delete()
            eliminados += 1
        except User.DoesNotExist:
            print(f"ℹ️ Usuario {email} no existe")

    total_usuarios = User.objects.count()
    print(f"✅ Usuarios eliminados: {eliminados}")
    print(f"📊 Total usuarios restantes: {total_usuarios}")

    if total_usuarios == 10:
        print("🎉 ¡PERFECTO! Ahora tenemos exactamente 10 usuarios")
        print("\n👥 USUARIOS FINALES:")
        for u in User.objects.all().order_by("id"):
            print(f"   {u.id}: {u.email}")
    else:
        print(
            f"⚠️ ADVERTENCIA: Se esperaban 10 usuarios, pero hay {total_usuarios}"
        )


if __name__ == "__main__":
    eliminar_usuarios_extras()
