"""🇨🇺 PACKFY CUBA - Comando Django para crear datos de prueba

Actualizado para el modelo actual de `Envio` (usa numero_guia autogenerado y campos remitente/destinatario).
"""

import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from envios.models import Envio

Usuario = get_user_model()


REMITENTES = [
    "Carlos Rodríguez",
    "Ana Gómez",
    "Luis Pérez",
    "María Fernández",
    "Jorge Díaz",
    "Elena Suárez",
    "Raúl Martínez",
    "Lucía Romero",
    "Pedro Alonso",
    "Sonia Herrera",
]

DESTINATARIOS = [
    "Yoandry López",
    "Yanelis Cruz",
    "Michel González",
    "Isabel Pardo",
    "Reinier Peña",
    "Claudia Ramos",
    "Roberto Linares",
    "Giselle Blanco",
    "Armando Guerra",
    "Dunia Del Río",
]

DIRECCIONES = [
    "Vedado, La Habana",
    "Centro Habana, La Habana",
    "Playa, La Habana",
    "Habana Vieja, La Habana",
    "Santiago de Cuba",
    "Camagüey",
    "Holguín",
    "Santa Clara",
    "Matanzas",
    "Cienfuegos",
]

DESCRIPCIONES = [
    "Ropa y textiles",
    "Electrónica pequeña",
    "Medicamentos básicos",
    "Accesorios móviles",
    "Zapatos deportivos",
    "Alimentos no perecederos",
    "Artículos de higiene",
    "Juguetes infantiles",
    "Herramientas manuales",
    "Libros y papelería",
]


class Command(BaseCommand):
    help = "Crea 20 envíos de prueba con datos variados (numero_guia autogenerado)"

    def handle(self, *args, **options):
        self.stdout.write("🇨🇺 Generando envíos de prueba...")

        usuario, _ = Usuario.objects.get_or_create(
            email="demo@packfy.cu",
            defaults={"username": "demo", "password": "demo12345"},
        )

        creados = []
        for i in range(20):
            envio = Envio.objects.create(
                descripcion=random.choice(DESCRIPCIONES),
                peso=Decimal(str(round(random.uniform(0.3, 8.0), 2))),
                remitente_nombre=random.choice(REMITENTES),
                remitente_direccion=random.choice(DIRECCIONES),
                remitente_telefono=f"53{random.randint(50000000, 59999999)}",
                destinatario_nombre=random.choice(DESTINATARIOS),
                destinatario_direccion=random.choice(DIRECCIONES),
                destinatario_telefono=f"53{random.randint(30000000, 39999999)}",
                creado_por=usuario,
                actualizado_por=usuario,
            )
            creados.append(envio.numero_guia)
            self.stdout.write(
                f"  ✅ {envio.numero_guia} - {envio.destinatario_nombre} ({envio.peso}kg)"
            )

        self.stdout.write(f"\n🎉 {len(creados)} envíos creados correctamente.")

        # Estadísticas
        estadisticas = {}
        for estado in estados_posibles:
            count = len([e for e in envios_creados if e.estado == estado])
            estadisticas[estado] = count

        self.stdout.write("\n📊 ESTADÍSTICAS DE LOS ENVÍOS CREADOS:")
        for estado, count in estadisticas.items():
            self.stdout.write(f"  📦 {estado.upper()}: {count} envíos")

        peso_total = sum([float(e.peso) for e in envios_creados])
        valor_total = sum([float(e.valor_declarado) for e in envios_creados])
        costo_total = sum([float(e.costo_envio) for e in envios_creados])

        self.stdout.write(f"\n💰 TOTALES:")
        self.stdout.write(f"  ⚖️ Peso total: {peso_total:.2f} kg")
        self.stdout.write(f"  💎 Valor declarado total: ${valor_total:,.2f}")
        self.stdout.write(f"  💵 Costo envío total: ${costo_total:,.2f}")

        self.stdout.write(
            self.style.SUCCESS("\n✅ Proceso completado exitosamente!")
        )
