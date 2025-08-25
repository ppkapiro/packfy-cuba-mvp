#!/usr/bin/env python
"""
Script de reparación de migraciones multi-tenant
Crea empresas antes de que se apliquen las restricciones de foreign key
"""

import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import connection, transaction
from empresas.models import Empresa


def fix_migration_data():
    """Crear empresas necesarias para las migraciones existentes"""
    print("🔧 Reparando datos para migraciones multi-tenant...")

    # Crear las empresas que los envíos existentes necesitan
    empresas_necesarias = [
        {
            "id": 1,
            "nombre": "Packfy Express Cuba",
            "slug": "packfy-express",
            "descripcion": "Empresa principal de paquetería rápida",
            "activo": True,
        },
        {
            "id": 2,
            "nombre": "Miami Shipping Co",
            "slug": "miami-shipping",
            "descripcion": "Operaciones en Miami, Florida",
            "activo": True,
        },
        {
            "id": 3,
            "nombre": "Habana Logistics",
            "slug": "habana-logistics",
            "descripcion": "Distribución local en La Habana",
            "activo": True,
        },
    ]

    with transaction.atomic():
        for empresa_data in empresas_necesarias:
            empresa, created = Empresa.objects.get_or_create(
                id=empresa_data["id"], defaults=empresa_data
            )
            status = "creada" if created else "ya existía"
            print(
                f"  ✅ Empresa '{empresa.nombre}' (ID: {empresa.id}) {status}"
            )

    print("✅ Datos de migración reparados exitosamente")


if __name__ == "__main__":
    fix_migration_data()
