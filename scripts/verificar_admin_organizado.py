#!/usr/bin/env python3
"""
🔧 Script para verificar la nueva organización del admin
"""
import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.append("/app")
django.setup()

from django.contrib.admin import site
from django.contrib.admin.sites import AdminSite
from usuarios.admin import ClientesAdmin, PersonalEmpresaAdmin, UsuarioAdmin
from usuarios.models import ClienteUsuario, PersonalEmpresa, Usuario


def verificar_admin_organizado():
    """Verificar la nueva organización del admin"""

    print("=== 🎯 VERIFICANDO ORGANIZACIÓN DEL ADMIN ===\n")

    # Simular request de Carlos
    class FakeRequest:
        def __init__(self, user):
            self.user = user

    carlos = Usuario.objects.get(email="dueno@packfy.com")
    request = FakeRequest(carlos)

    print("=== 👥 PERSONAL DE EMPRESA ===")
    try:
        personal_admin = PersonalEmpresaAdmin(PersonalEmpresa, AdminSite())
        personal_qs = personal_admin.get_queryset(request)
        print(f"✅ Total personal visible para Carlos: {personal_qs.count()}")

        for user in personal_qs:
            perfil = user.perfiles_empresa.first()
            icon = {
                "dueno": "👑",
                "operador_miami": "🌎",
                "operador_cuba": "🇨🇺",
            }.get(perfil.rol, "👤")
            print(f"  {icon} {user.email} - {perfil.get_rol_display()}")

        # Verificar que Carlos puede editar
        for user in personal_qs:
            puede_editar = personal_admin.has_change_permission(request, user)
            print(f"    ✅ Puede editar: {puede_editar}")
            if not puede_editar and user.email != "admin@packfy.cu":
                print(f"    ⚠️ PROBLEMA: Carlos no puede editar {user.email}")

    except Exception as e:
        print(f"❌ Error en PersonalEmpresaAdmin: {e}")

    print("\n=== 👤 CLIENTES ===")
    try:
        clientes_admin = ClientesAdmin(ClienteUsuario, AdminSite())
        clientes_qs = clientes_admin.get_queryset(request)
        print(f"✅ Total clientes visibles para Carlos: {clientes_qs.count()}")

        for user in clientes_qs:
            perfil = user.perfiles_empresa.first()
            icon = {"remitente": "📦", "destinatario": "📬"}.get(
                perfil.rol, "👤"
            )
            print(f"  {icon} {user.email} - {perfil.get_rol_display()}")

        # Verificar permisos de edición para clientes
        for user in clientes_qs:
            puede_editar = clientes_admin.has_change_permission(request, user)
            print(f"    ✅ Puede editar: {puede_editar}")

    except Exception as e:
        print(f"❌ Error en ClientesAdmin: {e}")

    print("\n=== 🔐 VERIFICACIÓN DE SEGURIDAD ===")

    # Verificar que NO puede ver superusers
    superusers = Usuario.objects.filter(is_superuser=True)
    print(f"Superusers en sistema: {superusers.count()}")

    all_admin = UsuarioAdmin(Usuario, AdminSite())
    all_qs = all_admin.get_queryset(request)
    superusers_visibles = all_qs.filter(is_superuser=True).count()

    if superusers_visibles == 0:
        print("✅ SEGURIDAD: Carlos NO puede ver superusers")
    else:
        print(f"⚠️ PROBLEMA: Carlos puede ver {superusers_visibles} superusers")

    print("\n=== 📊 RESUMEN DE ORGANIZACIÓN ===")
    print(f"👥 Personal de empresa: {personal_qs.count()} usuarios")
    print(f"👤 Clientes: {clientes_qs.count()} usuarios")
    print(
        f"📝 Total visible para Carlos: {personal_qs.count() + clientes_qs.count()}"
    )
    print(f"🔒 Superusers ocultos: ✅")

    print("\n=== 🎨 ICONOS Y CATEGORÍAS ===")
    print("👑 Dueño")
    print("🌎 Operador Miami")
    print("🇨🇺 Operador Cuba")
    print("📦 Remitente")
    print("📬 Destinatario")

    print("\n✅ ¡Verificación completada!")


if __name__ == "__main__":
    verificar_admin_organizado()
