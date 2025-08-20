#!/usr/bin/env python
"""
Script de debugging para verificar qué está pasando con los permisos
"""

import os
import sys

import django

sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def debug_perfil_usuario():
    print("=== DEBUG PERFIL USUARIO ===")

    # Obtener el dueño
    try:
        usuario_dueno = Usuario.objects.get(email="dueno@packfy.com")
        print(f"Usuario encontrado: {usuario_dueno.email}")

        # Obtener empresa
        empresa = Empresa.objects.get(slug="packfy-express")
        print(f"Empresa encontrada: {empresa.nombre}")

        # Obtener perfil
        perfil = PerfilUsuario.objects.filter(
            usuario=usuario_dueno, empresa=empresa, activo=True
        ).first()

        if perfil:
            print(f"✅ Perfil encontrado:")
            print(f"   Rol: {perfil.rol}")
            print(f"   Activo: {perfil.activo}")
            print(f"   es_dueno: {perfil.es_dueno}")
            print(
                f"   puede_gestionar_envios: {perfil.puede_gestionar_envios}"
            )
        else:
            print("❌ Perfil NO encontrado")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    debug_perfil_usuario()
