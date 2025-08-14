#!/usr/bin/env python3
"""
Script simple para crear envíos de prueba en PACKFY CUBA
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_development")
django.setup()

import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from envios.models import Envio

print("🇨🇺 PACKFY CUBA - Creando datos de prueba...")

Usuario = get_user_model()

# Obtener primer usuario
usuario = Usuario.objects.first()
print(f"👤 Usuario: {usuario.username}")

# Datos cubanos realistas
nombres_cubanos = [
    "María García Rodríguez",
    "Carlos Pérez Martínez",
    "Ana López Fernández",
    "José Martínez González",
    "Carmen Díaz Herrera",
    "Luis Rodríguez Suárez",
    "Elena Fernández Castro",
    "Miguel Ángel Pérez",
    "Isabel Martín Jiménez",
    "Roberto Carlos Mendoza",
    "Yolanda Herrera López",
    "Francisco Javier Cruz",
    "Marisol Vega Morales",
    "Antonio Ramírez Silva",
    "Caridad Sánchez Pérez",
    "Pedro Pablo García",
    "Miriam González Díaz",
    "Rafael Martínez López",
    "Esperanza Cruz Herrera",
    "Ramón Alberto Suárez",
]

direcciones_habana = [
    "Calle 23 #456, Vedado, La Habana",
    "Ave 26 #789, Nuevo Vedado, La Habana",
    "Calle 21 #234, Miramar, La Habana",
    "Calle L #567, Vedado, La Habana",
    "Ave 5ta #890, Playa, La Habana",
    "Calle 17 #123, Vedado, La Habana",
    "Ave Boyeros #456, Plaza, La Habana",
    "Calle San Lázaro #789, Centro Habana",
    "Ave Salvador Allende #234, Cerro, La Habana",
    "Calle Infanta #567, Centro Habana",
    "Malecón #123, Centro Habana",
    "Calle Obispo #456, Habana Vieja",
    "Ave Rancho Boyeros #789, Cerro",
    "Calle Monte #234, Centro Habana",
    "Ave Carlos III #567, Centro Habana",
]

productos_tipicos = [
    "Medicamentos para hipertensión",
    "Ropa y zapatos de marca",
    "iPhone 14 Pro Max",
    "Cosméticos Mary Kay",
    "Laptop Dell Inspiron 15",
    "Vitaminas y suplementos",
    "Perfumes Chanel y Dior",
    "Tablet Samsung Galaxy",
    "Repuestos de carro (filtros)",
    "Productos de limpieza Tide",
    "Ropa de bebé Carter's",
    "Auriculares AirPods Pro",
    "Medicamentos especializados",
    "Herramientas de trabajo",
    "Monitor Dell 24 pulgadas",
    "Cremas anti-edad Olay",
    "Zapatos Nike Air Max",
    "Multivitamínicos Centrum",
    "Maquillaje MAC",
    "Aceite de motor Mobil 1",
]

estados = ["pendiente", "en_transito", "entregado", "en_aduana"]
tipos = ["estandar", "express", "premium"]

print("🧹 Limpiando envíos antiguos...")
# Limpiar envíos de prueba anteriores
Envio.objects.filter(numero_tracking__startswith="PKY2025").delete()

print("📦 Creando 20 envíos realistas...")

for i in range(20):
    # Seleccionar datos aleatorios
    estado = random.choice(estados)
    tipo = random.choice(tipos)
    peso = round(random.uniform(0.5, 5.0), 1)
    valor = round(random.uniform(50, 1000), 2)

    # Calcular costo basado en peso y tipo
    if tipo == "estandar":
        costo_base = 20
    elif tipo == "express":
        costo_base = 35
    else:  # premium
        costo_base = 50

    costo = round(costo_base + (peso * 5), 2)

    # Fecha aleatoria en los últimos 30 días
    fecha_envio = datetime.now() - timedelta(days=random.randint(1, 30))

    # Crear envío
    envio = Envio.objects.create(
        numero_tracking=f"PKY2025{i+1:03d}",
        usuario=usuario,
        nombre_destinatario=random.choice(nombres_cubanos),
        direccion_destinatario=random.choice(direcciones_habana),
        telefono_destinatario=f"+5353{random.randint(1000000, 9999999)}",
        descripcion=random.choice(productos_tipicos),
        peso=Decimal(str(peso)),
        valor_declarado=Decimal(str(valor)),
        costo_envio=Decimal(str(costo)),
        ciudad_origen="Miami, FL",
        estado=estado,
        tipo_envio=tipo,
        fecha_envio=fecha_envio,
    )

    print(
        f"✅ {envio.numero_tracking} - {envio.nombre_destinatario} - {envio.estado}"
    )

# Estadísticas finales
total = Envio.objects.count()
por_estado = {}
for estado in estados:
    por_estado[estado] = Envio.objects.filter(estado=estado).count()

print(f"\n🎉 COMPLETADO!")
print(f"📊 Total envíos: {total}")
print("📈 Por estado:")
for estado, cantidad in por_estado.items():
    print(f"   • {estado}: {cantidad}")

print("\n💡 Puedes ver los envíos en: https://localhost:5173")
print("🔐 Usuario admin: admin@packfy.cu")
