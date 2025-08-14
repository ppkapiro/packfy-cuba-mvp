#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🇨🇺 PACKFY CUBA - Script para crear datos realistas de envíos cubanos
===============================================================
Crea envíos de ejemplo con nombres, direcciones y datos realistas de Cuba
"""

import os
import random
from datetime import datetime, timedelta

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.utils import timezone
from envios.models import Envio, HistorialEstado
from usuarios.models import Usuario

# ============================================================================
# 🇨🇺 DATOS REALISTAS CUBANOS
# ============================================================================

NOMBRES_CUBANOS = [
    # Nombres masculinos tradicionales cubanos
    "José",
    "Carlos",
    "Miguel",
    "Luis",
    "Francisco",
    "Manuel",
    "Antonio",
    "Rafael",
    "Jorge",
    "Pedro",
    "Roberto",
    "Ramón",
    "Eduardo",
    "Alberto",
    "Fernando",
    "Juan",
    "Mario",
    "Raúl",
    "Enrique",
    "Alejandro",
    "Ricardo",
    "Andrés",
    "Diego",
    "Pablo",
    # Nombres femeninos tradicionales cubanos
    "María",
    "Carmen",
    "Ana",
    "Rosa",
    "Isabel",
    "Teresa",
    "Esperanza",
    "Mercedes",
    "Caridad",
    "Zoila",
    "Miriam",
    "Olga",
    "Martha",
    "Gloria",
    "Lourdes",
    "Silvia",
    "Mayra",
    "Yolanda",
    "Dulce",
    "Carmelina",
    "Niurka",
    "Yanet",
    "Dianelys",
    "Yamilet",
]

APELLIDOS_CUBANOS = [
    "González",
    "Rodríguez",
    "Pérez",
    "Hernández",
    "García",
    "Martínez",
    "López",
    "Fernández",
    "Díaz",
    "Sánchez",
    "Ramírez",
    "Torres",
    "Flores",
    "Rivera",
    "Gómez",
    "Mendoza",
    "Vargas",
    "Castillo",
    "Jiménez",
    "Morales",
    "Herrera",
    "Medina",
    "Guerrero",
    "Ramos",
    "Cruz",
    "Moreno",
    "Domínguez",
    "Gutiérrez",
    "Vázquez",
    "Reyes",
    "Alvarez",
    "Ruiz",
    "Romero",
    "Castro",
    "Ortega",
    "Luna",
]

# Provincias y municipios reales de Cuba
DIRECCIONES_CUBA = [
    # La Habana
    {
        "provincia": "La Habana",
        "municipio": "Centro Habana",
        "direcciones": [
            "Calle 23 #512 entre L y M, El Vedado",
            "San Lázaro #863 apto 4, Centro Habana",
            "Malecón #107 e/ Genios y Crespo",
            "Línea #405 e/ E y F, El Vedado",
            "Carlos III #1205 e/ Reina y Estrella",
        ],
    },
    {
        "provincia": "La Habana",
        "municipio": "Habana Vieja",
        "direcciones": [
            "Obispo #315 e/ Habana y Aguiar",
            "Mercaderes #209 e/ Lamparilla y Amargura",
            "O'Reilly #524 e/ Monserrate y Villegas",
            "San Ignacio #74 e/ O'Reilly y Empedrado",
            "Tacón #12 e/ O'Reilly y Empedrado",
        ],
    },
    {
        "provincia": "La Habana",
        "municipio": "Playa",
        "direcciones": [
            "7ma Avenida #2804 e/ 28 y 30, Miramar",
            "5ta Avenida #7802 e/ 78 y 80, Playa",
            "Calle 70 #504 e/ 5ta y 7ma, Playa",
            "1era Avenida #1205 e/ 12 y 14, Miramar",
            "3ra Avenida #5607 e/ 56 y 58, Playa",
        ],
    },
    # Santiago de Cuba
    {
        "provincia": "Santiago de Cuba",
        "municipio": "Santiago de Cuba",
        "direcciones": [
            "José A. Saco #658 e/ Calvario y Carnicería",
            "Enramadas #503 e/ San Félix y San Germán",
            "Aguilera #406 e/ Reloj y San Félix",
            "Heredia #260 e/ Pío Rosado y Hartmann",
            "Corona #109 e/ San Basilio y Carnicería",
        ],
    },
    # Matanzas
    {
        "provincia": "Matanzas",
        "municipio": "Matanzas",
        "direcciones": [
            "Calle 85 #29020 e/ 290 y 292, Matanzas",
            "Jovellanos #28504 e/ 285 y 287",
            "Milanés #30112 e/ 301 y 303",
            "Magdalena #27208 e/ 272 y 274",
            "Contreras #28310 e/ 283 y 285",
        ],
    },
    # Villa Clara
    {
        "provincia": "Villa Clara",
        "municipio": "Santa Clara",
        "direcciones": [
            "Independencia #15 e/ Maceo y J.B. Zayas",
            "Marta Abreu #52 e/ Luis Estévez y Colón",
            "9 de Abril #8 e/ Maceo y J.B. Zayas",
            "Cuba #106 e/ Tristá y Unión",
            "Máximo Gómez #4 e/ Rafael Tristá y Unión",
        ],
    },
    # Holguín
    {
        "provincia": "Holguín",
        "municipio": "Holguín",
        "direcciones": [
            "Libertad #176 e/ Mártires y Luz Caballero",
            "Maceo #165 e/ Libertad y Mártires",
            "Frexes #190 e/ Libertad y Martí",
            "Martí #123 e/ Frexes y Maceo",
            "Cables #145 e/ Libertad y Mártires",
        ],
    },
    # Camagüey
    {
        "provincia": "Camagüey",
        "municipio": "Camagüey",
        "direcciones": [
            "República #403 e/ San Martín y General Gómez",
            "Independencia #256 e/ Avellaneda y Oscar Primelles",
            "Martí #67 e/ General Gómez y Honda",
            "Cisneros #342 e/ Padre Valencia y República",
            "Ignacio Agramonte #158 e/ Martí y República",
        ],
    },
]

PRODUCTOS_ENVIOS = [
    {
        "descripcion": "Medicamentos importados",
        "peso_min": 0.5,
        "peso_max": 2.0,
        "valor_min": 50,
        "valor_max": 300,
    },
    {
        "descripcion": "Productos electrónicos (teléfono móvil)",
        "peso_min": 0.3,
        "peso_max": 1.5,
        "valor_min": 200,
        "valor_max": 800,
    },
    {
        "descripcion": "Ropa y calzado",
        "peso_min": 1.0,
        "peso_max": 5.0,
        "valor_min": 30,
        "valor_max": 150,
    },
    {
        "descripcion": "Productos de higiene personal",
        "peso_min": 0.8,
        "peso_max": 3.0,
        "valor_min": 25,
        "valor_max": 80,
    },
    {
        "descripcion": "Suplementos alimentarios",
        "peso_min": 0.5,
        "peso_max": 2.5,
        "valor_min": 40,
        "valor_max": 120,
    },
    {
        "descripcion": "Repuestos de auto/moto",
        "peso_min": 2.0,
        "peso_max": 10.0,
        "valor_min": 80,
        "valor_max": 400,
    },
    {
        "descripcion": "Libros y material educativo",
        "peso_min": 0.5,
        "peso_max": 4.0,
        "valor_min": 15,
        "valor_max": 60,
    },
    {
        "descripcion": "Productos de belleza y cosméticos",
        "peso_min": 0.3,
        "peso_max": 2.0,
        "valor_min": 20,
        "valor_max": 100,
    },
    {
        "descripcion": "Herramientas de trabajo",
        "peso_min": 1.5,
        "peso_max": 8.0,
        "valor_min": 60,
        "valor_max": 250,
    },
    {
        "descripcion": "Alimentos no perecederos",
        "peso_min": 2.0,
        "peso_max": 15.0,
        "valor_min": 30,
        "valor_max": 100,
    },
]

TELEFONOS_CUBANOS = [
    # Números de celular cubanos (móvil)
    "+53 5",
    "+53 6",
    "+53 7",
]


def generar_telefono_cubano():
    """Genera un número de teléfono cubano realista"""
    prefijo = random.choice(TELEFONOS_CUBANOS)
    if prefijo in ["+53 5", "+53 6", "+53 7"]:  # Móvil
        numero = (
            f"{prefijo}{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        )
    else:  # Fijo
        numero = (
            f"{prefijo}{random.randint(10, 99)}-{random.randint(1000, 9999)}"
        )
    return numero


def generar_nombre_completo():
    """Genera un nombre completo cubano realista"""
    nombre = random.choice(NOMBRES_CUBANOS)
    apellido1 = random.choice(APELLIDOS_CUBANOS)
    apellido2 = random.choice(APELLIDOS_CUBANOS)
    return f"{nombre} {apellido1} {apellido2}"


def generar_direccion_cuba():
    """Genera una dirección cubana realista"""
    ubicacion = random.choice(DIRECCIONES_CUBA)
    direccion = random.choice(ubicacion["direcciones"])
    return f"{direccion}, {ubicacion['municipio']}, {ubicacion['provincia']}, Cuba"


def generar_email_opcional():
    """Genera un email opcional (no todos tienen)"""
    if random.random() < 0.4:  # 40% de probabilidad de tener email
        nombre = random.choice(NOMBRES_CUBANOS).lower()
        numero = random.randint(10, 99)
        dominios = ["nauta.cu", "gmail.com", "yahoo.com", "outlook.com"]
        return f"{nombre}{numero}@{random.choice(dominios)}"
    return None


def crear_envios_cubanos(cantidad=50):
    """
    Crea envíos con datos realistas cubanos
    """
    print(f"🇨🇺 CREANDO {cantidad} ENVÍOS CUBANOS REALISTAS")
    print("=" * 60)

    # Obtener un usuario para asignar como creador
    try:
        usuario_admin = Usuario.objects.filter(is_staff=True).first()
        if not usuario_admin:
            usuario_admin = Usuario.objects.first()

        if not usuario_admin:
            print("❌ No hay usuarios en el sistema. Creando usuario admin...")
            usuario_admin = Usuario.objects.create_superuser(
                email="admin@packfy.cu",
                password="admin123",
                first_name="Admin",
                last_name="Sistema",
            )
            print("✅ Usuario admin creado")

    except Exception as e:
        print(f"❌ Error obteniendo usuario: {e}")
        return

    envios_creados = 0
    estados_disponibles = [choice[0] for choice in Envio.EstadoChoices.choices]

    for i in range(cantidad):
        try:
            # Generar datos del envío
            producto = random.choice(PRODUCTOS_ENVIOS)
            peso = round(
                random.uniform(producto["peso_min"], producto["peso_max"]), 2
            )
            valor = round(
                random.uniform(producto["valor_min"], producto["valor_max"]), 2
            )

            # Generar personas
            remitente = generar_nombre_completo()
            destinatario = generar_nombre_completo()

            # Generar direcciones cubanas
            direccion_remitente = generar_direccion_cuba()
            direccion_destinatario = generar_direccion_cuba()

            # Generar contactos
            tel_remitente = generar_telefono_cubano()
            tel_destinatario = generar_telefono_cubano()
            email_remitente = generar_email_opcional()
            email_destinatario = generar_email_opcional()

            # Estado aleatorio con más probabilidad de estados activos
            estado_pesos = {
                "RECIBIDO": 0.25,
                "EN_TRANSITO": 0.35,
                "EN_REPARTO": 0.20,
                "ENTREGADO": 0.15,
                "DEVUELTO": 0.03,
                "CANCELADO": 0.02,
            }
            estado = random.choices(
                list(estado_pesos.keys()), weights=list(estado_pesos.values())
            )[0]

            # Fecha de creación (últimas 2 semanas)
            dias_atras = random.randint(0, 14)
            fecha_creacion = timezone.now() - timedelta(days=dias_atras)

            # Fecha estimada de entrega (3-10 días después de creación)
            fecha_estimada = fecha_creacion.date() + timedelta(
                days=random.randint(3, 10)
            )

            # Crear el envío
            envio = Envio.objects.create(
                descripcion=producto["descripcion"],
                peso=peso,
                valor_declarado=valor,
                estado_actual=estado,
                remitente_nombre=remitente,
                remitente_direccion=direccion_remitente,
                remitente_telefono=tel_remitente,
                remitente_email=email_remitente,
                destinatario_nombre=destinatario,
                destinatario_direccion=direccion_destinatario,
                destinatario_telefono=tel_destinatario,
                destinatario_email=email_destinatario,
                fecha_estimada_entrega=fecha_estimada,
                creado_por=usuario_admin,
                notas=f"Envío generado automáticamente - Producto cubano típico",
            )

            # Forzar la fecha de creación
            envio.fecha_creacion = fecha_creacion
            envio.save()

            # Crear historial de estados
            HistorialEstado.objects.create(
                envio=envio,
                estado="RECIBIDO",
                comentario="Paquete recibido en origen",
                ubicacion="Centro de distribución La Habana",
                registrado_por=usuario_admin,
            )

            # Si el estado actual no es RECIBIDO, crear estados intermedios
            if estado != "RECIBIDO":
                if estado in ["EN_TRANSITO", "EN_REPARTO", "ENTREGADO"]:
                    HistorialEstado.objects.create(
                        envio=envio,
                        estado="EN_TRANSITO",
                        comentario="En ruta hacia destino",
                        ubicacion="En tránsito",
                        registrado_por=usuario_admin,
                    )

                if estado in ["EN_REPARTO", "ENTREGADO"]:
                    HistorialEstado.objects.create(
                        envio=envio,
                        estado="EN_REPARTO",
                        comentario="Salió para entrega",
                        ubicacion="Centro de reparto local",
                        registrado_por=usuario_admin,
                    )

                if estado == "ENTREGADO":
                    HistorialEstado.objects.create(
                        envio=envio,
                        estado="ENTREGADO",
                        comentario="Entregado exitosamente",
                        ubicacion="Dirección del destinatario",
                        registrado_por=usuario_admin,
                    )

            envios_creados += 1
            print(
                f"✅ {envios_creados:2d}. Envío {envio.numero_guia} - {remitente} → {destinatario} ({estado})"
            )

        except Exception as e:
            print(f"❌ Error creando envío {i+1}: {e}")
            continue

    print("\n" + "=" * 60)
    print(f"🎉 PROCESO COMPLETADO")
    print(f"✅ {envios_creados} envíos cubanos creados exitosamente")
    print(f"📊 Total envíos en sistema: {Envio.objects.count()}")

    # Estadísticas por estado
    print("\n📈 ESTADÍSTICAS POR ESTADO:")
    for estado, nombre in Envio.EstadoChoices.choices:
        count = Envio.objects.filter(estado_actual=estado).count()
        if count > 0:
            print(f"   {nombre}: {count} envíos")


def mostrar_ejemplos():
    """Muestra algunos ejemplos de los envíos creados"""
    print("\n🔍 EJEMPLOS DE ENVÍOS CREADOS:")
    print("-" * 80)

    envios = Envio.objects.all()[:5]
    for envio in envios:
        print(f"\n📦 {envio.numero_guia} - {envio.estado_actual}")
        print(f"   📄 {envio.descripcion}")
        print(f"   📤 De: {envio.remitente_nombre}")
        print(f"      {envio.remitente_direccion}")
        print(f"   📥 Para: {envio.destinatario_nombre}")
        print(f"        {envio.destinatario_direccion}")
        print(
            f"   ⚖️  Peso: {envio.peso}kg | 💰 Valor: ${envio.valor_declarado}"
        )


if __name__ == "__main__":
    print("🇨🇺 PACKFY CUBA - GENERADOR DE DATOS REALISTAS")
    print("=" * 60)

    # Verificar estado actual
    total_actual = Envio.objects.count()
    total_usuarios = Usuario.objects.count()

    print(f"📊 Estado actual:")
    print(f"   - Envíos existentes: {total_actual}")
    print(f"   - Usuarios en sistema: {total_usuarios}")

    if total_actual > 0:
        respuesta = input(
            f"\n⚠️  Ya existen {total_actual} envíos. ¿Desea agregar más? (s/N): "
        )
        if respuesta.lower() not in ["s", "si", "sí", "y", "yes"]:
            print("❌ Operación cancelada")
            exit()

    # Preguntar cantidad
    try:
        cantidad = input(
            "\n🔢 ¿Cuántos envíos desea crear? (por defecto 30): "
        )
        cantidad = int(cantidad) if cantidad.strip() else 30

        if cantidad <= 0 or cantidad > 200:
            print("❌ Cantidad debe estar entre 1 y 200")
            exit()

    except ValueError:
        cantidad = 30
        print(f"✅ Usando cantidad por defecto: {cantidad}")

    # Crear envíos
    crear_envios_cubanos(cantidad)

    # Mostrar ejemplos
    mostrar_ejemplos()

    print(f"\n🎉 ¡Datos cubanos realistas creados exitosamente!")
    print(f"🌐 Revisa en: https://localhost:8443/admin/envios/envio/")
