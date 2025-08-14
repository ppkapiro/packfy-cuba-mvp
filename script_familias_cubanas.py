#!/usr/bin/env python3
"""
Script mejorado para crear envíos con remitentes y destinatarios relacionados
para PACKFY CUBA - Relaciones familiares auténticas
"""

import os
import random
from datetime import date, datetime, timedelta
from decimal import Decimal

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from envios.models import Envio


def crear_datos_con_familias():
    print("🇨🇺 CREANDO ENVÍOS CON FAMILIAS CUBANAS REALISTAS...")
    print("👨‍👩‍👧‍👦 Remitentes en Miami → Familiares en La Habana")

    Usuario = get_user_model()

    # Obtener usuario admin
    try:
        usuario = Usuario.objects.get(id=1)
        print(f"✅ Usuario administrador: {usuario.username}")
    except Usuario.DoesNotExist:
        print("❌ No se encontró usuario admin")
        return

    # Familias cubanas con relaciones reales
    familias_cubanas = [
        {
            "apellido": "García Rodríguez",
            "remitente": {
                "nombre": "Roberto García Pérez",
                "direccion": "1234 SW 8th Street, Miami, FL 33135",
                "telefono": "+13053451234",
                "email": "roberto.garcia.miami@gmail.com",
            },
            "destinatarios": [
                {
                    "nombre": "María García Rodríguez",
                    "direccion": "Calle 23 #456, Vedado, La Habana",
                    "telefono": "+5353123456",
                    "email": "maria.garcia.habana@nauta.cu",
                    "relacion": "hermana",
                },
                {
                    "nombre": "Carmen García Rodríguez",
                    "direccion": "Calle 23 #456, Vedado, La Habana",
                    "telefono": "+5353123457",
                    "email": "carmen.garcia.habana@nauta.cu",
                    "relacion": "madre",
                },
            ],
        },
        {
            "apellido": "Pérez Martínez",
            "remitente": {
                "nombre": "Carlos Pérez Silva",
                "direccion": "5678 Coral Way, Miami, FL 33155",
                "telefono": "+13054567890",
                "email": "carlos.perez.miami@hotmail.com",
            },
            "destinatarios": [
                {
                    "nombre": "Ana Pérez Martínez",
                    "direccion": "Ave 26 #789, Nuevo Vedado, La Habana",
                    "telefono": "+5353234567",
                    "email": "ana.perez.habana@nauta.cu",
                    "relacion": "hija",
                },
                {
                    "nombre": "José Pérez Martínez",
                    "direccion": "Ave 26 #789, Nuevo Vedado, La Habana",
                    "telefono": "+5353234568",
                    "email": "jose.perez.habana@nauta.cu",
                    "relacion": "hijo",
                },
            ],
        },
        {
            "apellido": "López Fernández",
            "remitente": {
                "nombre": "Elena López Castro",
                "direccion": "9012 Flagler Street, Miami, FL 33174",
                "telefono": "+13056789012",
                "email": "elena.lopez.miami@yahoo.com",
            },
            "destinatarios": [
                {
                    "nombre": "Miguel López Fernández",
                    "direccion": "Calle 21 #234, Miramar, La Habana",
                    "telefono": "+5353345678",
                    "email": "miguel.lopez.habana@nauta.cu",
                    "relacion": "esposo",
                },
                {
                    "nombre": "Sofía López Fernández",
                    "direccion": "Calle 21 #234, Miramar, La Habana",
                    "telefono": "+5353345679",
                    "email": "sofia.lopez.habana@nauta.cu",
                    "relacion": "hija",
                },
            ],
        },
        {
            "apellido": "Martínez González",
            "remitente": {
                "nombre": "Rosa Martínez Díaz",
                "direccion": "3456 NW 7th Street, Miami, FL 33126",
                "telefono": "+13057890123",
                "email": "rosa.martinez.miami@gmail.com",
            },
            "destinatarios": [
                {
                    "nombre": "Luis Martínez González",
                    "direccion": "Calle L #567, Vedado, La Habana",
                    "telefono": "+5353456789",
                    "email": "luis.martinez.habana@nauta.cu",
                    "relacion": "hermano",
                },
                {
                    "nombre": "Isabel Martínez González",
                    "direccion": "Calle L #567, Vedado, La Habana",
                    "telefono": "+5353456788",
                    "email": "isabel.martinez.habana@nauta.cu",
                    "relacion": "madre",
                },
            ],
        },
        {
            "apellido": "Hernández Castro",
            "remitente": {
                "nombre": "Francisco Hernández López",
                "direccion": "7890 SW 40th Street, Miami, FL 33155",
                "telefono": "+13059012345",
                "email": "francisco.hernandez.miami@outlook.com",
            },
            "destinatarios": [
                {
                    "nombre": "Carmen Hernández Castro",
                    "direccion": "Ave 5ta #890, Playa, La Habana",
                    "telefono": "+5353567890",
                    "email": "carmen.hernandez.habana@nauta.cu",
                    "relacion": "prima",
                },
                {
                    "nombre": "Roberto Hernández Castro",
                    "direccion": "Ave 5ta #890, Playa, La Habana",
                    "telefono": "+5353567891",
                    "email": "roberto.hernandez.habana@nauta.cu",
                    "relacion": "tío",
                },
            ],
        },
        {
            "apellido": "Rodríguez Silva",
            "remitente": {
                "nombre": "Yolanda Rodríguez Morales",
                "direccion": "2468 Biscayne Blvd, Miami, FL 33137",
                "telefono": "+13051234567",
                "email": "yolanda.rodriguez.miami@gmail.com",
            },
            "destinatarios": [
                {
                    "nombre": "Antonio Rodríguez Silva",
                    "direccion": "Calle 17 #123, Vedado, La Habana",
                    "telefono": "+5353678901",
                    "email": "antonio.rodriguez.habana@nauta.cu",
                    "relacion": "padre",
                },
                {
                    "nombre": "Mercedes Rodríguez Silva",
                    "direccion": "Calle 17 #123, Vedado, La Habana",
                    "telefono": "+5353678902",
                    "email": "mercedes.rodriguez.habana@nauta.cu",
                    "relacion": "hermana",
                },
            ],
        },
    ]

    # Productos típicos que envían desde Miami
    productos_miami_cuba = [
        "Medicamentos para la diabetes (Metformina)",
        "Ropa de marca (Nike, Adidas)",
        "iPhone 15 Pro Max con accesorios",
        "Cosméticos Mary Kay y Avon",
        "Laptop Dell para estudios",
        "Medicamentos para hipertensión (Losartán)",
        "Productos de higiene personal (Dove, Pantene)",
        "Tablet Samsung para nietos",
        "Repuestos de carro (filtros, aceite)",
        "Vitaminas Centrum y Omega-3",
        "Ropa para niños (Carter's, Gap Kids)",
        "Auriculares Apple AirPods",
        "Perfumes (Chanel, Dior, Victoria's Secret)",
        "Herramientas de trabajo (Dewalt, Black & Decker)",
        "Productos para el cabello (L'Oréal, Pantene)",
        "Medicamentos especializados para el corazón",
        "Zapatos deportivos (Nike Air Max, Adidas)",
        "Suplementos nutricionales",
        "Maquillaje (MAC, Maybelline, Revlon)",
        "Electrodomésticos pequeños (licuadora, plancha)",
    ]

    estados_posibles = list(Envio.EstadoChoices.values)

    print(f"🗑️ Limpiando envíos anteriores...")
    Envio.objects.filter(numero_guia__startswith="PKY").delete()

    print(f"📦 Creando envíos con relaciones familiares...")

    contador_envio = 1

    for familia in familias_cubanas:
        remitente = familia["remitente"]

        for destinatario in familia["destinatarios"]:
            # Entre 1-4 envíos por destinatario
            num_envios = random.randint(1, 4)

            for i in range(num_envios):
                numero_guia = f"PKY2025{contador_envio:03d}"

                # Seleccionar producto y calcular peso/valor realistas
                producto = random.choice(productos_miami_cuba)

                # Pesos y valores más realistas según el producto
                if "iPhone" in producto or "Laptop" in producto:
                    peso = round(random.uniform(0.8, 2.5), 2)
                    valor = round(random.uniform(500, 1200), 2)
                elif "Medicamentos" in producto:
                    peso = round(random.uniform(0.2, 1.0), 2)
                    valor = round(random.uniform(80, 300), 2)
                elif "Ropa" in producto:
                    peso = round(random.uniform(1.0, 3.0), 2)
                    valor = round(random.uniform(100, 400), 2)
                else:
                    peso = round(random.uniform(0.5, 4.0), 2)
                    valor = round(random.uniform(50, 600), 2)

                estado = random.choice(estados_posibles)

                # Crear envío
                envio = Envio.objects.create(
                    numero_guia=numero_guia,
                    estado_actual=estado,
                    descripcion=producto,
                    peso=Decimal(str(peso)),
                    valor_declarado=Decimal(str(valor)),
                    # Datos del remitente (familiar en Miami)
                    remitente_nombre=remitente["nombre"],
                    remitente_direccion=remitente["direccion"],
                    remitente_telefono=remitente["telefono"],
                    remitente_email=remitente["email"],
                    # Datos del destinatario (familiar en Cuba)
                    destinatario_nombre=destinatario["nombre"],
                    destinatario_direccion=destinatario["direccion"],
                    destinatario_telefono=destinatario["telefono"],
                    destinatario_email=destinatario["email"],
                    # Metadata
                    notas=f"Envío familiar: {remitente['nombre']} → {destinatario['nombre']} ({destinatario['relacion']})",
                    creado_por=usuario,
                    actualizado_por=usuario,
                    fecha_estimada_entrega=date.today()
                    + timedelta(days=random.randint(3, 21)),
                )

                print(
                    f"✅ {numero_guia} | {remitente['nombre']} → {destinatario['nombre']} ({destinatario['relacion']}) | {producto[:40]}..."
                )
                contador_envio += 1

    # Estadísticas finales
    total_envios = Envio.objects.count()
    print(f"\n🎉 COMPLETADO!")
    print(f"📊 Total de envíos creados: {total_envios}")
    print(f"👨‍👩‍👧‍👦 Familias representadas: {len(familias_cubanas)}")

    # Mostrar estadísticas por estado
    print(f"\n📈 Distribución por estado:")
    for estado in estados_posibles:
        cantidad = Envio.objects.filter(estado_actual=estado).count()
        print(f"   • {estado}: {cantidad} envíos")

    print(f"\n💡 Accede al sistema en: https://localhost:5173")
    print(f"🔐 Usuario admin: {usuario.username}")


if __name__ == "__main__":
    crear_datos_con_familias()
