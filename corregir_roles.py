#!/usr/bin/env python
# Script para corregir roles de usuario

import os
import sys

import django

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def corregir_roles():
    print("🔧 CORRIGIENDO ROLES DE USUARIO...")

    # Buscar usuario dueño
    try:
        usuario = Usuario.objects.get(email="dueno@packfy.com")
        print(f"✅ Usuario encontrado: {usuario.email}")
    except Usuario.DoesNotExist:
        print("❌ Usuario dueno@packfy.com no encontrado")
        return

    # Ver todas las empresas
    empresas = Empresa.objects.all()
    print(f"📋 Empresas encontradas: {empresas.count()}")
    for empresa in empresas:
        print(f"   - {empresa.nombre} (ID: {empresa.id})")

    # Ver perfiles actuales
    perfiles = PerfilUsuario.objects.filter(usuario=usuario)
    print(f"👤 Perfiles del usuario: {perfiles.count()}")
    for perfil in perfiles:
        print(f"   - {perfil.empresa.nombre}: rol='{perfil.rol}'")

    # Corregir rol en PackFy Express (ID: 3)
    try:
        packfy_empresa = Empresa.objects.get(id=3)
        perfil_packfy, created = PerfilUsuario.objects.get_or_create(
            usuario=usuario,
            empresa=packfy_empresa,
            defaults={"rol": "dueno", "activo": True},
        )

        if created:
            print(
                f"✅ Perfil creado para {packfy_empresa.nombre} con rol 'dueno'"
            )
        else:
            perfil_packfy.rol = "dueno"
            perfil_packfy.activo = True
            perfil_packfy.save()
            print(f"✅ Rol actualizado a 'dueno' en {packfy_empresa.nombre}")

    except Empresa.DoesNotExist:
        print("❌ Empresa PackFy Express (ID: 3) no encontrada")

    # Verificar cambios
    perfiles_final = PerfilUsuario.objects.filter(usuario=usuario)
    print(f"\n🎯 RESULTADO FINAL:")
    for perfil in perfiles_final:
        print(
            f"   - {perfil.empresa.nombre}: rol='{perfil.rol}' (activo: {perfil.activo})"
        )


if __name__ == "__main__":
    corregir_roles()
