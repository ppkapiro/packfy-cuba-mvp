#!/usr/bin/env python3
"""
Script para crear datos de prueba CORRECTOS para PACKFY CUBA
Basado en el modelo real de envios_envio
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


def crear_datos_prueba():
    print("🇨🇺 CREANDO DATOS DE PRUEBA PARA PACKFY CUBA...")
    print("📊 Usando modelo correcto: envios_envio")

    Usuario = get_user_model()

    # Obtener usuario existente
    try:
        usuario = Usuario.objects.get(id=1)  # admin@packfy.cu
        print(f"✅ Usuario encontrado: {usuario.username}")
    except Usuario.DoesNotExist:
        print("❌ No se encontró usuario admin")
        return

    # Datos cubanos realistas
    nombres_cubanos = [
        "María García Rodríguez",
        "Carlos Pérez Martínez",
        "Ana López Fernández",
        "José Martínez González",
        "Carmen Díaz Herrera",
        "Luis Hernández Castro",
        "Rosa Fernández Morales",
        "Miguel Rodríguez Silva",
        "Elena Castro Pérez",
        "Roberto González López",
        "Isabel Morales García",
        "Francisco Silva Hernández",
        "Yolanda Pérez Rodríguez",
        "Antonio Castro González",
        "Mercedes López Silva",
        "Rafael Hernández Morales",
        "Teresa González Fernández",
        "Osvaldo Martínez Díaz",
        "Esperanza Silva Castro",
        "Ramón Rodríguez Morales",
    ]

    direcciones_habana = [
        "Calle 23 #456, Vedado, La Habana",
        "Ave 26 #789, Nuevo Vedado, La Habana",
        "Calle 21 #234, Miramar, La Habana",
        "Calle L #567, Vedado, La Habana",
        "Ave 5ta #890, Playa, La Habana",
        "Calle 17 #123, Vedado, La Habana",
        "Ave 41 #456, Playa, La Habana",
        "Calle G #789, Vedado, La Habana",
        "Ave 7ma #234, Miramar, La Habana",
        "Calle 19 #567, Vedado, La Habana",
        "Ave 1ra #890, Miramar, La Habana",
        "Calle 15 #123, Vedado, La Habana",
        "Ave 3ra #456, Miramar, La Habana",
        "Calle M #789, Vedado, La Habana",
        "Ave 31 #234, Playa, La Habana",
        "Calle 13 #567, Vedado, La Habana",
        "Ave 9na #890, Miramar, La Habana",
        "Calle N #123, Vedado, La Habana",
        "Ave 43 #456, Playa, La Habana",
        "Calle 25 #789, Vedado, La Habana",
    ]

    productos_tipicos = [
        "Medicamentos para la diabetes",
        "Ropa y zapatos Nike",
        "iPhone 15 Pro Max",
        "Cosméticos Mary Kay",
        "Laptop Dell Inspiron 15",
        "Medicamentos para hipertensión",
        "Productos de higiene personal",
        "Tablet Samsung Galaxy",
        "Repuestos para carro",
        "Vitaminas y suplementos",
        "Ropa para niños",
        "Productos electrónicos",
        "Perfumes y colonias",
        "Herramientas de trabajo",
        "Productos para el cabello",
        "Medicamentos para el corazón",
        "Artículos deportivos",
        "Productos para bebé",
        "Electrodomésticos pequeños",
        "Artículos de cocina",
    ]

    direcciones_miami = [
        "1234 SW 8th Street, Miami, FL 33135",
        "5678 Biscayne Blvd, Miami, FL 33137",
        "9012 Coral Way, Miami, FL 33155",
        "3456 NW 7th Street, Miami, FL 33126",
        "7890 SW 40th Street, Miami, FL 33155",
        "2468 Flagler Street, Miami, FL 33135",
        "1357 Lincoln Road, Miami Beach, FL 33139",
        "8024 SW 24th Street, Miami, FL 33155",
        "4680 NE 2nd Avenue, Miami, FL 33137",
        "9753 West Flagler, Miami, FL 33174",
    ]

    estados_posibles = list(Envio.EstadoChoices.values)

    print(f"🗑️ Limpiando envíos existentes...")
    Envio.objects.filter(numero_guia__startswith="PKY").delete()

    print(f"📦 Creando 20 envíos...")

    for i in range(20):
        numero_guia = f"PKY2025{i+1:03d}"

        # Datos aleatorios pero realistas
        nombre_destinatario = random.choice(nombres_cubanos)
        direccion_destinatario = random.choice(direcciones_habana)
        producto = random.choice(productos_tipicos)
        direccion_remitente = random.choice(direcciones_miami)
        estado = random.choice(estados_posibles)
        peso = round(random.uniform(0.5, 8.0), 2)
        valor = round(random.uniform(50, 1000), 2)

        # Crear envío con TODOS los campos requeridos
        envio = Envio.objects.create(
            numero_guia=numero_guia,
            estado_actual=estado,
            descripcion=producto,
            peso=Decimal(str(peso)),
            valor_declarado=Decimal(str(valor)),
            # Datos del remitente (REQUERIDOS)
            remitente_nombre=f"Familiar de {nombre_destinatario.split()[0]}",
            remitente_direccion=direccion_remitente,
            remitente_telefono="+1305" + str(random.randint(1000000, 9999999)),
            remitente_email=f"remitente{i+1}@gmail.com",
            # Datos del destinatario
            destinatario_nombre=nombre_destinatario,
            destinatario_direccion=direccion_destinatario,
            destinatario_telefono="+5353"
            + str(random.randint(1000000, 9999999)),
            destinatario_email=f"destinatario{i+1}@nauta.cu",
            # Metadata
            notas=f"Envío de prueba #{i+1} - {producto}",
            creado_por=usuario,
            actualizado_por=usuario,
            fecha_estimada_entrega=date.today()
            + timedelta(days=random.randint(3, 15)),
        )

        print(
            f"✅ Envío {numero_guia} creado - {estado} - {nombre_destinatario}"
        )

    # Verificar creación
    total_envios = Envio.objects.count()
    print(f"\n🎉 COMPLETADO!")
    print(f"📊 Total de envíos en base de datos: {total_envios}")

    # Mostrar algunos ejemplos
    print(f"\n📋 Ejemplos creados:")
    for envio in Envio.objects.all()[:5]:
        print(
            f"   • {envio.numero_guia} - {envio.estado_actual} - {envio.destinatario_nombre}"
        )


if __name__ == "__main__":
    crear_datos_prueba()
