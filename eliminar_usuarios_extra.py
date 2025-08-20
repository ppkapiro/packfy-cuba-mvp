#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eliminar usuarios extra que no están en el script de restauración
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from protector_bd import requiere_autorizacion, ProtectorBaseDatos

from usuarios.models import Usuario


@requiere_autorizacion("ELIMINAR USUARIOS")
def eliminar_usuarios_extra():
    print("🗑️ ELIMINANDO USUARIOS EXTRA...")

    # Usuarios que NO deben existir según el script de restauración
    usuarios_a_eliminar = [
        "admin@packfy.cu",
        "cliente@test.cu",
        "empresa@test.cu",
    ]

    # Verificar usuarios actuales
    print("📋 Usuarios actuales:")
    todos_usuarios = Usuario.objects.all()
    for user in todos_usuarios:
        print(f"  - {user.email} ({user.first_name} {user.last_name})")

    print(f"\n🔍 Total usuarios antes: {todos_usuarios.count()}")

    # Eliminar usuarios extra
    eliminados = 0
    for email in usuarios_a_eliminar:
        try:
            usuario = Usuario.objects.get(email=email)
            print(
                f"❌ Eliminando: {usuario.email} ({usuario.first_name} {usuario.last_name})"
            )
            usuario.delete()
            eliminados += 1
        except Usuario.DoesNotExist:
            print(f"⚠️  Usuario {email} no existe")

    # Verificar resultado final
    usuarios_finales = Usuario.objects.all()
    print(f"\n✅ Usuarios después: {usuarios_finales.count()}")
    print(f"🗑️ Usuarios eliminados: {eliminados}")

    print("\n📋 Usuarios restantes:")
    for user in usuarios_finales:
        print(f"  - {user.email} ({user.first_name} {user.last_name})")



# 🛡️ VERIFICACIÓN DE PROTECCIÓN
if __name__ == "__main__":
    protector = ProtectorBaseDatos()
    if not protector.esta_protegida():
        print("⚠️  ADVERTENCIA: Base de datos no protegida")
        respuesta = input("¿Activar protección antes de continuar? (si/no): ")
        if respuesta.lower() in ['si', 'sí', 's']:
            protector.activar_proteccion()

if __name__ == "__main__":
    eliminar_usuarios_extra()
