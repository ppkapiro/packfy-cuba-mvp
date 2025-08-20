#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 PRUEBA DEL SISTEMA DE PROTECCIÓN
Demuestra cómo funciona la protección de BD
"""

import os

import django

from protector_bd import requiere_autorizacion

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from usuarios.models import Usuario


@requiere_autorizacion("CREAR USUARIO DE PRUEBA")
def crear_usuario_prueba():
    """
    Intenta crear un usuario de prueba
    Esta operación requiere autorización
    """
    print("👤 Creando usuario de prueba...")

    usuario = Usuario.objects.create_user(
        email="prueba@test.com",
        password="test123",
        username="prueba@test.com",
        first_name="Usuario",
        last_name="Prueba",
    )

    print(f"✅ Usuario creado: {usuario.email}")
    return usuario


@requiere_autorizacion("ELIMINAR USUARIOS DE PRUEBA")
def limpiar_usuarios_prueba():
    """
    Elimina usuarios de prueba
    Esta operación requiere autorización
    """
    print("🗑️ Eliminando usuarios de prueba...")

    usuarios_prueba = Usuario.objects.filter(email__contains="prueba")
    count = usuarios_prueba.count()
    usuarios_prueba.delete()

    print(f"✅ {count} usuarios de prueba eliminados")


def mostrar_usuarios_actuales():
    """
    Muestra usuarios actuales (sin protección)
    Esta operación NO requiere autorización
    """
    print("📋 Usuarios actuales:")
    usuarios = Usuario.objects.all().order_by("email")
    for user in usuarios:
        print(f"  - {user.email} ({user.first_name} {user.last_name})")
    print(f"Total: {usuarios.count()} usuarios")


def main():
    """Función principal de prueba"""
    print("🧪 PRUEBA DEL SISTEMA DE PROTECCIÓN")
    print("=" * 50)

    print("\n1️⃣ Operación SIN protección (consulta):")
    mostrar_usuarios_actuales()

    print("\n2️⃣ Operación CON protección (crear usuario):")
    print("⚠️  Esta operación requerirá autorización...")
    crear_usuario_prueba()

    print("\n3️⃣ Verificar si se creó:")
    mostrar_usuarios_actuales()

    print("\n4️⃣ Operación CON protección (limpiar):")
    print("⚠️  Esta operación requerirá autorización...")
    limpiar_usuarios_prueba()

    print("\n5️⃣ Verificar resultado final:")
    mostrar_usuarios_actuales()


if __name__ == "__main__":
    main()
