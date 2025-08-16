#!/usr/bin/env python
"""
Script para crear datos de prueba - Envíos
"""
import os
import random
from datetime import datetime, timedelta

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_development")
django.setup()

from empresas.models import Empresa
from envios.models import Envio
from usuarios.models import Usuario


def crear_empresa_demo():
    """Crear empresa demo si no existe"""
    empresa, created = Empresa.objects.get_or_create(
        nombre="Packfy Cuba S.A.",
        defaults={
            "direccion": "Calle 23, Vedado, La Habana",
            "telefono": "+53 7 123-4567",
            "email": "info@packfy.cu",
            "activa": True,
        },
    )
    return empresa


def crear_envios_demo():
    """Crear envíos demo"""
    empresa = crear_empresa_demo()

    # Obtener usuario admin
    try:
        usuario = Usuario.objects.get(email="admin@packfy.cu")
    except Usuario.DoesNotExist:
        print("❌ Usuario admin no encontrado")
        return

    estados = [
        "REGISTRADO",
        "EN_TRANSITO",
        "EN_ALMACEN",
        "EN_RUTA",
        "ENTREGADO",
    ]
    ciudades_origen = [
        "La Habana",
        "Santiago de Cuba",
        "Santa Clara",
        "Camagüey",
        "Holguín",
    ]
    ciudades_destino = [
        "Matanzas",
        "Cienfuegos",
        "Pinar del Río",
        "Bayamo",
        "Trinidad",
    ]

    nombres_remitentes = [
        "José Martí",
        "Carlos Fernández",
        "María González",
        "Ana López",
        "Roberto Silva",
        "Carmen Herrera",
        "Luis Pérez",
        "Elena Castro",
        "Miguel Rodríguez",
        "Isabel Torres",
    ]

    nombres_destinatarios = [
        "Pedro García",
        "Yolanda Díaz",
        "Ramón Valdés",
        "Caridad Sánchez",
        "Alberto Ruiz",
        "Rosa Mendoza",
        "Ernesto Guevara",
        "Miriam Álvarez",
        "Raúl Jiménez",
        "Lourdes Vega",
    ]

    productos = [
        "Medicamentos",
        "Ropa y calzado",
        "Alimentos no perecederos",
        "Productos de aseo",
        "Electrónicos",
        "Libros y material escolar",
        "Artículos para el hogar",
        "Juguetes",
        "Productos de belleza",
        "Herramientas",
    ]

    envios_creados = 0

    for i in range(1, 21):  # Crear 20 envíos
        try:
            # Datos del envío
            numero_guia = f"PK{2025:04d}{i:04d}"
            fecha_creacion = datetime.now() - timedelta(
                days=random.randint(0, 30)
            )

            # Seleccionar aleatoriamente
            estado = random.choice(estados)
            ciudad_origen = random.choice(ciudades_origen)
            ciudad_destino = random.choice(ciudades_destino)
            remitente = random.choice(nombres_remitentes)
            destinatario = random.choice(nombres_destinatarios)
            producto = random.choice(productos)

            # Crear envío
            envio = Envio.objects.create(
                numero_guia=numero_guia,
                estado_actual=estado,
                fecha_creacion=fecha_creacion,
                fecha_estimada_entrega=fecha_creacion
                + timedelta(days=random.randint(3, 15)),
                # Remitente
                remitente_nombre=remitente,
                remitente_telefono=f"+53 5 {random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                remitente_direccion=f"Calle {random.randint(1, 100)}, {ciudad_origen}",
                remitente_ciudad=ciudad_origen,
                # Destinatario
                destinatario_nombre=destinatario,
                destinatario_telefono=f"+53 5 {random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                destinatario_direccion=f"Avenida {random.randint(1, 50)}, {ciudad_destino}",
                destinatario_ciudad=ciudad_destino,
                # Detalles del paquete
                descripcion=producto,
                peso=round(random.uniform(0.5, 10.0), 1),
                valor_declarado=round(random.uniform(20.0, 500.0), 2),
                # Asignaciones
                usuario_creador=usuario,
                empresa=empresa,
            )

            envios_creados += 1
            print(
                f"✅ Envío creado: {numero_guia} - {estado} ({remitente} → {destinatario})"
            )

        except Exception as e:
            print(f"❌ Error creando envío {i}: {e}")

    print(f"\n🎉 ¡{envios_creados} envíos creados exitosamente!")

    # Mostrar resumen
    total = Envio.objects.count()
    print(f"\n📊 Resumen de envíos en sistema:")
    print(f"Total: {total}")
    for estado in estados:
        count = Envio.objects.filter(estado_actual=estado).count()
        print(f"- {estado}: {count}")


if __name__ == "__main__":
    crear_envios_demo()
