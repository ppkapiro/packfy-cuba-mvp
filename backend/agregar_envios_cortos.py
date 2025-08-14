#!/usr/bin/env python
"""
🇨🇺 Script para agregar más envíos con remitentes de nombres cortos
"""
import os
import sys

import django

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import random
from decimal import Decimal

from envios.models import Envio
from usuarios.models import Usuario


def main():
    print("🇨🇺 AGREGANDO 10 ENVÍOS CON NOMBRES CORTOS Y CREATIVOS")
    print("=" * 60)

    # Obtener admin para creado_por y actualizado_por
    admin = Usuario.objects.first()

    # Remitentes con nombres más cortos y creativos
    remitentes_cortos = [
        {
            "nombre": "Luis Torres",
            "direccion": "Calle 42 #789, Miramar, La Habana",
            "telefono": "+53 76543210",
            "email": "luis.torres@nauta.cu",
        },
        {
            "nombre": "Carmen Vega",
            "direccion": "Avenida Boyeros #156, Plaza, La Habana",
            "telefono": "+53 72345678",
            "email": "carmen.vega@nauta.cu",
        },
        {
            "nombre": "Pedro Silva",
            "direccion": "Calle 10 #234, Vedado, La Habana",
            "telefono": "+53 78901234",
            "email": "pedro.silva@nauta.cu",
        },
        {
            "nombre": "Rosa Méndez",
            "direccion": "Malecón #567, Habana Vieja, La Habana",
            "telefono": "+53 75678901",
            "email": "rosa.mendez@nauta.cu",
        },
        {
            "nombre": "Jorge Ruiz",
            "direccion": "Avenida 23 #345, Vedado, La Habana",
            "telefono": "+53 73456789",
            "email": "jorge.ruiz@nauta.cu",
        },
        {
            "nombre": "Elena Castro",
            "direccion": "Calle L #678, Vedado, La Habana",
            "telefono": "+53 77890123",
            "email": "elena.castro@nauta.cu",
        },
        {
            "nombre": "Raúl Díaz",
            "direccion": "Avenida 31 #890, Playa, La Habana",
            "telefono": "+53 74567890",
            "email": "raul.diaz@nauta.cu",
        },
        {
            "nombre": "Sofía Moreno",
            "direccion": "Calle Real #123, Centro Habana",
            "telefono": "+53 78234567",
            "email": "sofia.moreno@nauta.cu",
        },
        {
            "nombre": "Daniel López",
            "direccion": "Avenida de los Presidentes #456, Vedado",
            "telefono": "+53 76789012",
            "email": "daniel.lopez@nauta.cu",
        },
        {
            "nombre": "Isabel Ramos",
            "direccion": "Calle San Lázaro #789, Centro Habana",
            "telefono": "+53 75432109",
            "email": "isabel.ramos@nauta.cu",
        },
    ]

    # Destinatarios también con nombres cortos
    destinatarios_cortos = [
        "Mario Pérez",
        "Lina García",
        "Tomás Ruiz",
        "Eva Morales",
        "Alex Herrera",
        "Sara Jiménez",
        "Hugo Vargas",
        "Nora Delgado",
        "Iván Ortega",
        "Celia Mendoza",
    ]

    ciudades_cuba = [
        "La Habana",
        "Santiago de Cuba",
        "Holguín",
        "Santa Clara",
        "Matanzas",
        "Camagüey",
        "Cienfuegos",
        "Pinar del Río",
        "Bayamo",
        "Ciego de Ávila",
    ]

    direcciones_destino = [
        "Calle 5 #234, Reparto Sueño",
        "Avenida Central #567, Vista Alegre",
        "Calle Principal #890, El Cerro",
        "Malecón Norte #123, Costa Verde",
        "Avenida Libertad #456, Nuevo Mundo",
        "Calle Martí #789, Centro Ciudad",
        "Boulevard #345, Las Flores",
        "Avenida Revolución #678, La Victoria",
        "Calle Independencia #901, El Progreso",
        "Paseo #234, Bella Vista",
    ]

    print(f"📦 Creando 10 nuevos envíos con nombres cortos...")

    for i in range(10):
        try:
            # Seleccionar remitente y destinatario
            remitente = remitentes_cortos[i]
            destinatario = destinatarios_cortos[i]

            # Ciudades diferentes para origen y destino
            origen_ciudad = random.choice(ciudades_cuba)
            destino_ciudad = random.choice(
                [c for c in ciudades_cuba if c != origen_ciudad]
            )

            # Generar número de guía único
            numero_guia = f"PK{random.randint(100000, 999999)}"

            # Crear el envío
            envio = Envio.objects.create(
                numero_guia=numero_guia,
                remitente_nombre=remitente["nombre"],
                remitente_direccion=remitente["direccion"],
                remitente_telefono=remitente["telefono"],
                remitente_email=remitente["email"],
                destinatario_nombre=destinatario,
                destinatario_telefono=f"+53 5{random.randint(1000000, 9999999)}",
                destinatario_email=f"{destinatario.lower().replace(' ', '.')}@gmail.com",
                destinatario_direccion=f"{random.choice(direcciones_destino)}, {destino_ciudad}, Cuba",
                descripcion=f"Encomienda familiar #{i+1} - Productos básicos",
                peso=Decimal(f"{random.uniform(0.3, 4.5):.2f}"),
                valor_declarado=Decimal(f"{random.uniform(5, 80):.2f}"),
                estado_actual=random.choice(
                    ["pendiente", "en_transito", "entregado", "retenido"]
                ),
                creado_por=admin,
                actualizado_por=admin,
            )

            print(
                f"  ✅ #{envio.numero_guia}: {remitente['nombre']} → {destinatario}"
            )
            print(
                f"     📍 {origen_ciudad} → {destino_ciudad} | {envio.peso}kg | ${envio.valor_declarado}"
            )

        except Exception as e:
            print(f"  ❌ Error creando envío {i+1}: {e}")

    # Estadísticas finales
    total_envios = Envio.objects.count()
    print(f"\n🎉 ¡ENVÍOS AGREGADOS EXITOSAMENTE!")
    print(f"📊 Total de envíos en la base de datos: {total_envios}")

    # Mostrar resumen por estado
    from django.db.models import Count

    estados = (
        Envio.objects.values("estado_actual")
        .annotate(count=Count("estado_actual"))
        .order_by("estado_actual")
    )
    print(f"\n📈 Resumen por estado:")
    for estado in estados:
        print(f"  - {estado['estado_actual']}: {estado['count']} envíos")

    # Mostrar algunos remitentes con nombres cortos
    print(f"\n👥 Algunos remitentes con nombres cortos:")
    remitentes_cortos_db = (
        Envio.objects.filter(remitente_nombre__regex=r"^[A-Za-z]+ [A-Za-z]+$")
        .values("remitente_nombre")
        .distinct()[:8]
    )

    for rem in remitentes_cortos_db:
        count = Envio.objects.filter(
            remitente_nombre=rem["remitente_nombre"]
        ).count()
        print(f"  - {rem['remitente_nombre']}: {count} envío(s)")


if __name__ == "__main__":
    main()
