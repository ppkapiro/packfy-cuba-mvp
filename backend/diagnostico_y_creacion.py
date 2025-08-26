#!/usr/bin/env python
"""
Diagnóstico y creación directa de envíos
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import random
from decimal import Decimal

from empresas.models import Empresa
from envios.models import Envio


def diagnosticar_datos():
    """Diagnóstico completo del sistema"""
    print("🔍 DIAGNÓSTICO COMPLETO")
    print("=" * 40)

    print("\n1. EMPRESAS:")
    empresas = Empresa.objects.all()
    for empresa in empresas:
        print(
            f"   - ID: {empresa.id} | Slug: {empresa.slug} | Nombre: {empresa.nombre}"
        )

    print(f"\n2. ENVÍOS TOTALES: {Envio.objects.count()}")

    print("\n3. ENVÍOS POR EMPRESA:")
    for empresa in empresas:
        count = Envio.objects.filter(empresa=empresa).count()
        print(f"   - {empresa.slug}: {count} envíos")

    print("\n4. ENVÍOS SIN EMPRESA:")
    sin_empresa = Envio.objects.filter(empresa__isnull=True).count()
    print(f"   - Sin empresa: {sin_empresa}")

    print("\n5. MUESTRA DE ENVÍOS:")
    for envio in Envio.objects.all()[:3]:
        empresa_name = envio.empresa.slug if envio.empresa else "None"
        print(f"   - {envio.numero_guia} → Empresa: {empresa_name}")


def crear_envios_correctos():
    """Crear envíos con las cantidades correctas"""
    print("\n📦 CREANDO ENVÍOS CORRECTOS")
    print("=" * 40)

    # Limpiar todos los envíos existentes
    count_deleted = Envio.objects.all().count()
    Envio.objects.all().delete()
    print(f"🗑️ Eliminados {count_deleted} envíos existentes")

    # Configuración correcta
    config = {
        "cuba-express": 45,
        "habana-premium": 26,
        "miami-shipping": 44,
        "packfy-express": 55,
    }

    total_creados = 0

    for slug, cantidad in config.items():
        try:
            empresa = Empresa.objects.get(slug=slug)
            print(f"\n🏢 {empresa.nombre} ({slug})")

            for i in range(1, cantidad + 1):
                Envio.objects.create(
                    numero_guia=f"{slug.upper()[:3]}{i:04d}",
                    codigo_rastreo=f"{slug.upper()[:3]}-{i:06d}",
                    empresa=empresa,
                    remitente_nombre=f"Remitente {i}",
                    remitente_direccion="Miami, FL",
                    remitente_telefono="+1305123456",
                    destinatario_nombre=f"Destinatario {i}",
                    destinatario_direccion="La Habana",
                    destinatario_telefono="+5371234567",
                    peso=Decimal("1.5"),
                    valor_declarado=Decimal("100.00"),
                    estado_actual="RECIBIDO",
                )

            print(f"   ✅ Creados {cantidad} envíos")
            total_creados += cantidad

        except Empresa.DoesNotExist:
            print(f"   ❌ Empresa {slug} no encontrada")

    print(f"\n🎯 Total creados: {total_creados} envíos")


def verificar_resultado():
    """Verificar el resultado final"""
    print("\n✅ VERIFICACIÓN FINAL")
    print("=" * 30)

    for empresa in Empresa.objects.all():
        count = Envio.objects.filter(empresa=empresa).count()
        print(f"   - {empresa.slug}: {count} envíos")

    print(f"\n📊 Total: {Envio.objects.count()} envíos")


if __name__ == "__main__":
    diagnosticar_datos()
    crear_envios_correctos()
    verificar_resultado()
    print("\n🎉 ¡PROCESO COMPLETADO!")
