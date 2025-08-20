#!/usr/bin/env python3
"""
Script para listar todos los usuarios actuales y identificar cuáles sobran
"""

import os
import sys

import django

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from empresas.models import PerfilUsuario


def listar_usuarios_actuales():
    """Lista todos los usuarios actuales en la base de datos"""
    User = get_user_model()

    print("🔍 USUARIOS ACTUALES EN LA BASE DE DATOS")
    print("=" * 50)

    usuarios = User.objects.all().order_by("id")
    print(f"📊 Total de usuarios: {usuarios.count()}")
    print()

    for usuario in usuarios:
        try:
            perfil = PerfilUsuario.objects.get(usuario=usuario)
            empresa = (
                perfil.empresa.nombre if perfil.empresa else "Sin empresa"
            )
            rol = perfil.rol if perfil.rol else "Sin rol"
        except PerfilUsuario.DoesNotExist:
            empresa = "Sin perfil"
            rol = "Sin perfil"

        print(
            f"ID {usuario.id:2}: {usuario.email:25} | {usuario.nombre} {usuario.apellidos:15} | {empresa:15} | {rol}"
        )

    print()
    print(
        "🎯 USUARIOS ESPERADOS (según restaurar_estructura_20250820_095645.py):"
    )
    print("=" * 50)

    usuarios_esperados = [
        "1: superadmin@packfy.com         | Super Admin        | Packfy Express | dueno",
        "2: dueno@packfy.com              | Carlos Empresario  | Packfy Express | dueno",
        "3: miami@packfy.com              | Ana Miami          | Packfy Express | operador_miami",
        "4: cuba@packfy.com               | Jose Habana        | Packfy Express | operador_cuba",
        "5: remitente1@packfy.com         | Maria Rodriguez    | Packfy Express | remitente",
        "6: remitente2@packfy.com         | Pedro Gonzalez     | Packfy Express | remitente",
        "7: remitente3@packfy.com         | Luis Martinez      | Packfy Express | remitente",
        "8: destinatario1@cuba.cu         | Carmen Perez       | Packfy Express | destinatario",
        "9: destinatario2@cuba.cu         | Roberto Silva      | Packfy Express | destinatario",
        "10: destinatario3@cuba.cu        | Elena Fernandez    | Packfy Express | destinatario",
    ]

    for esperado in usuarios_esperados:
        print(f"   {esperado}")

    print()

    # Identificar usuarios extra
    emails_esperados = [
        "superadmin@packfy.com",
        "dueno@packfy.com",
        "miami@packfy.com",
        "cuba@packfy.com",
        "remitente1@packfy.com",
        "remitente2@packfy.com",
        "remitente3@packfy.com",
        "destinatario1@cuba.cu",
        "destinatario2@cuba.cu",
        "destinatario3@cuba.cu",
    ]

    usuarios_extra = []
    for usuario in usuarios:
        if usuario.email not in emails_esperados:
            usuarios_extra.append(usuario)

    if usuarios_extra:
        print("❌ USUARIOS QUE SOBRAN:")
        print("=" * 50)
        for usuario in usuarios_extra:
            print(
                f"❌ ID {usuario.id}: {usuario.email} - {usuario.nombre} {usuario.apellidos}"
            )
        print(f"\n🗑️  Se deben eliminar {len(usuarios_extra)} usuarios extras")
    else:
        print("✅ No hay usuarios extras - Base de datos correcta")


if __name__ == "__main__":
    listar_usuarios_actuales()
