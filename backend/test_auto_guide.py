#!/usr/bin/env python3
import os
import sys

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from envios.models import Envio

# Crear un envío de prueba sin numero_guia
envio = Envio.objects.create(
    descripcion="Paquete de prueba para testing de numero automatico",
    peso=2.5,
    valor_declarado=100.00,
    remitente_nombre="Juan Perez",
    remitente_direccion="Miami, FL",
    remitente_telefono="+1234567890",
    remitente_email="juan@test.com",
    destinatario_nombre="Maria Garcia",
    destinatario_direccion="La Habana, Cuba",
    destinatario_telefono="+53512345678",
    destinatario_email="maria@test.com",
)

print(f"✅ Envío creado exitosamente!")
print(f"📋 ID: {envio.id}")
print(f"🔢 Número de guía generado automáticamente: {envio.numero_guia}")
print(f"📊 Estado: {envio.estado_actual}")
print(f"📅 Fecha creación: {envio.fecha_creacion}")

# Verificar que otros envíos también tienen números automáticos
total_envios = Envio.objects.count()
print(f"\n📦 Total de envíos en la base de datos: {total_envios}")

if total_envios > 1:
    print("\n📋 Últimos envíos:")
    for e in Envio.objects.order_by("-id")[:3]:
        print(f"  - ID {e.id}: {e.numero_guia} ({e.destinatario_nombre})")
