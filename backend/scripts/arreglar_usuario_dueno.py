#!/usr/bin/env python3
"""
🔧 Script para arreglar permisos y datos del usuario dueño
"""

import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.append("/app")
django.setup()

from django.contrib.auth import get_user_model
from empresas.models import Empresa, PerfilEmpresa
from envios.models import Envio


def arreglar_usuario_dueno():
    User = get_user_model()

    print("🔧 Arreglando usuario dueño...")

    # 1. Buscar o crear usuario dueño
    try:
        dueno = User.objects.get(email="dueno@packfy.com")
        print(f"✅ Usuario encontrado: {dueno.email}")
    except User.DoesNotExist:
        print("❌ Usuario dueño no existe")
        return

    # 2. Hacer que sea superuser para tener acceso completo
    if not dueno.is_superuser:
        dueno.is_superuser = True
        dueno.is_staff = True
        dueno.save()
        print("✅ Usuario convertido a superuser")

    # 3. Buscar o crear empresa
    empresa, created = Empresa.objects.get_or_create(
        nombre="Packfy Express Cuba",
        defaults={
            "descripcion": "Empresa principal de Packfy",
            "activa": True,
            "tipo_empresa": "paqueteria",
            "telefono": "+53 5 123 4567",
            "email": "info@packfy.com",
        },
    )

    if created:
        print(f"✅ Empresa creada: {empresa.nombre}")
    else:
        print(f"✅ Empresa encontrada: {empresa.nombre}")

    # 4. Crear o actualizar perfil de dueño
    perfil, created = PerfilEmpresa.objects.get_or_create(
        usuario=dueno,
        empresa=empresa,
        defaults={
            "rol": "dueno",
            "activo": True,
            "fecha_ingreso": "2024-01-01",
        },
    )

    if created:
        print(f"✅ Perfil creado: {perfil.rol} en {perfil.empresa.nombre}")
    else:
        perfil.rol = "dueno"
        perfil.activo = True
        perfil.save()
        print(
            f"✅ Perfil actualizado: {perfil.rol} en {perfil.empresa.nombre}"
        )

    # 5. Crear algunos envíos de prueba si no existen
    envios_count = Envio.objects.count()
    if envios_count == 0:
        print("📦 Creando envíos de prueba...")

        # Crear remitente y destinatario
        remitente, _ = User.objects.get_or_create(
            email="remitente@test.com",
            defaults={
                "username": "remitente",
                "first_name": "Juan",
                "last_name": "Pérez",
            },
        )

        destinatario, _ = User.objects.get_or_create(
            email="destinatario@test.com",
            defaults={
                "username": "destinatario",
                "first_name": "María",
                "last_name": "González",
            },
        )

        # Crear envíos
        for i in range(1, 6):
            Envio.objects.create(
                numero_guia=f"PKF{i:04d}",
                descripcion=f"Paquete de prueba {i}",
                peso=2.5,
                estado_actual="RECIBIDO",
                remitente=remitente,
                destinatario=destinatario,
                empresa=empresa,
                valor_declarado=50.0,
            )

        print("✅ 5 envíos de prueba creados")
    else:
        print(f"✅ Ya existen {envios_count} envíos")

    print("\n🎯 VERIFICACIÓN FINAL:")
    print(f"Usuario: {dueno.email}")
    print(f"Superuser: {dueno.is_superuser}")
    print(f"Staff: {dueno.is_staff}")
    print(f"Empresa: {empresa.nombre}")
    print(f"Perfil: {perfil.rol}")
    print(f"Envíos: {Envio.objects.count()}")

    print("\n✅ ¡Usuario dueño configurado correctamente!")


if __name__ == "__main__":
    arreglar_usuario_dueno()
