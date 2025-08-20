#!/usr/bin/env python3
"""
Script de restauración simplificado para 10 usuarios exactos
Para ser ejecutado durante la construcción del contenedor Docker
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from empresas.models import Empresa, PerfilUsuario


def restaurar_10_usuarios():
    """Crear exactamente 10 usuarios según especificación"""

    User = get_user_model()

    print("🔄 CREANDO ESTRUCTURA CON 10 USUARIOS EXACTOS...")

    # 1. Limpiar datos actuales
    print("🗑️ Limpiando datos actuales...")
    PerfilUsuario.objects.all().delete()
    User.objects.all().delete()
    Empresa.objects.all().delete()

    # 2. Crear empresa base
    print("🏢 Creando empresa...")
    empresa = Empresa.objects.create(
        nombre="Packfy Express", slug="packfy-express", activo=True
    )

    # 3. Crear superadministrador
    print("👑 Creando superadministrador...")
    superadmin = User.objects.create_user(
        email="superadmin@packfy.com",
        password="super123!",
        username="superadmin@packfy.com",
        first_name="Super",
        last_name="Administrador",
        is_active=True,
        is_staff=True,
        is_superuser=True,
        es_administrador_empresa=True,
    )

    # 4. Crear dueño de empresa
    print("👔 Creando dueño...")
    dueno = User.objects.create_user(
        email="dueno@packfy.com",
        password="dueno123!",
        username="dueno@packfy.com",
        first_name="Carlos",
        last_name="Empresario",
        is_active=True,
        is_staff=True,
        es_administrador_empresa=True,
    )

    PerfilUsuario.objects.create(
        usuario=dueno, empresa=empresa, rol="dueno", activo=True
    )

    # 5. Crear operadores
    print("🌴 Creando operadores...")
    miami = User.objects.create_user(
        email="miami@packfy.com",
        password="miami123!",
        username="miami@packfy.com",
        first_name="Ana",
        last_name="Miami",
        is_active=True,
        es_administrador_empresa=True,
    )

    PerfilUsuario.objects.create(
        usuario=miami, empresa=empresa, rol="operador_miami", activo=True
    )

    cuba = User.objects.create_user(
        email="cuba@packfy.com",
        password="cuba123!",
        username="cuba@packfy.com",
        first_name="Jose",
        last_name="Habana",
        is_active=True,
        es_administrador_empresa=True,
    )

    PerfilUsuario.objects.create(
        usuario=cuba, empresa=empresa, rol="operador_cuba", activo=True
    )

    # 6. Crear remitentes
    print("📦 Creando remitentes...")
    remitentes = [
        ("remitente1@packfy.com", "Maria", "Rodriguez"),
        ("remitente2@packfy.com", "Pedro", "Gonzalez"),
        ("remitente3@packfy.com", "Luis", "Martinez"),
    ]

    for email, nombre, apellido in remitentes:
        user = User.objects.create_user(
            email=email,
            password="remitente123!",
            username=email,
            first_name=nombre,
            last_name=apellido,
            is_active=True,
        )

        PerfilUsuario.objects.create(
            usuario=user, empresa=empresa, rol="remitente", activo=True
        )

    # 7. Crear destinatarios
    print("🎯 Creando destinatarios...")
    destinatarios = [
        ("destinatario1@cuba.cu", "Carmen", "Perez"),
        ("destinatario2@cuba.cu", "Roberto", "Silva"),
        ("destinatario3@cuba.cu", "Elena", "Fernandez"),
    ]

    for email, nombre, apellido in destinatarios:
        user = User.objects.create_user(
            email=email,
            password="destinatario123!",
            username=email,
            first_name=nombre,
            last_name=apellido,
            is_active=True,
        )

        PerfilUsuario.objects.create(
            usuario=user, empresa=empresa, rol="destinatario", activo=True
        )

    print(f"✅ ESTRUCTURA CREADA - 10 USUARIOS EXACTOS")
    print(f"Usuarios: {User.objects.count()}")
    print(f"Empresas: {Empresa.objects.count()}")
    print(f"Perfiles: {PerfilUsuario.objects.count()}")


if __name__ == "__main__":
    restaurar_10_usuarios()
