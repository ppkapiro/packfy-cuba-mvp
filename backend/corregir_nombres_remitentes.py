#!/usr/bin/env python3
"""
Corrección rápida: Actualizar nombres de remitentes para que sean cubanos viviendo en Miami
"""

import os
import random

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa
from envios.models import Envio


def main():
    print("🔧 CORRIGIENDO NOMBRES DE REMITENTES...")

    # Nombres cubanos en Miami (los que realmente envían)
    nombres_cubanos_miami = [
        "Rafael Hernández",
        "Yolanda Pérez",
        "Orlando García",
        "Marisol Rodríguez",
        "Ramón Fernández",
        "Caridad Martínez",
        "Alejandro López",
        "Miriam Sánchez",
        "Fernando Díaz",
        "Teresa González",
        "Armando Cruz",
        "Esperanza Ruiz",
        "Carlos Alberto Vega",
        "Lourdes Herrera",
        "Roberto Castellanos",
    ]

    empresa = Empresa.objects.get(slug="packfy-express")
    envios = Envio.objects.filter(empresa=empresa)

    print(f"📦 Actualizando {envios.count()} envíos...")

    count = 0
    for envio in envios:
        # Solo actualizar si tiene nombre en inglés
        if any(
            nombre in envio.remitente_nombre
            for nombre in [
                "Robert",
                "Jennifer",
                "Michael",
                "Jessica",
                "David",
                "Ashley",
            ]
        ):
            envio.remitente_nombre = random.choice(nombres_cubanos_miami)
            envio.save(update_fields=["remitente_nombre"])
            count += 1

    print(f"✅ Actualizados {count} remitentes")
    print(
        "🎯 Ahora los envíos son realistas: cubanos en Miami → familia en Cuba"
    )


if __name__ == "__main__":
    main()
