#!/usr/bin/env python
"""
🇨🇺 Script para crear envíos de prueba en PACKFY CUBA
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

from empresas.models import Empresa
from envios.models import Envio
from usuarios.models import Usuario


def main():
    print("🇨🇺 CREANDO DATOS DE PRUEBA PARA PACKFY CUBA")
    print("=" * 50)

    # Verificar usuarios
    usuarios = Usuario.objects.all()
    print(f"📊 Usuarios disponibles: {usuarios.count()}")
    for user in usuarios:
        print(f"  - {user.username} ({user.email})")

    if usuarios.count() == 0:
        print("❌ No hay usuarios en la base de datos")
        return

    admin = usuarios.first()
    print(f"\n✅ Usando usuario: {admin.username}")

    # Crear envíos de prueba
    nombres_cubanos = [
        "María José García Hernández",
        "Carlos Manuel Rodríguez López",
        "Ana Beatriz López Martínez",
        "José Antonio Pérez González",
        "Carmen Elena Sánchez Díaz",
        "Roberto Carlos Fernández Castro",
        "Yolanda María Torres Ruiz",
        "Miguel Ángel González Díaz",
        "Laura Isabel Herrera Morales",
        "Francisco Javier Jiménez Vargas",
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

    direcciones_cuba = [
        "Calle 23 #456, Vedado",
        "Avenida 26 #123, Nuevo Vedado",
        "Calle Real #89, Centro Habana",
        "Malecón #234, Habana Vieja",
        "Avenida 41 #567, Playa",
        "Calle L #890, Vedado",
        "Avenida de los Presidentes #345",
        "Calle San Lázaro #678",
        "Avenida Salvador Allende #234",
        "Calle Línea #567",
    ]

    # Limpiar envíos existentes
    envios_existentes = Envio.objects.count()
    if envios_existentes > 0:
        print(f"\n🗑️ Eliminando {envios_existentes} envíos existentes...")
        Envio.objects.all().delete()

    print(f"\n📦 Creando 10 envíos de prueba...")

    for i in range(10):
        try:
            origen_ciudad = random.choice(ciudades_cuba)
            destino_ciudad = random.choice(
                [c for c in ciudades_cuba if c != origen_ciudad]
            )

            envio = Envio.objects.create(
                remitente=admin,
                destinatario_nombre=nombres_cubanos[i],
                destinatario_telefono=f"+53 5{random.randint(1000000, 9999999)}",
                destinatario_email=f"cliente{i+1}@packfy.cu",
                destinatario_direccion=random.choice(direcciones_cuba),
                origen=f"{origen_ciudad}, Cuba",
                destino=f"{destino_ciudad}, Cuba",
                descripcion=f"Paquete #{i+1} - Productos varios para familia cubana",
                peso=Decimal(f"{random.uniform(0.5, 5.0):.2f}"),
                valor_declarado=Decimal(f"{random.uniform(10, 100):.2f}"),
                estado=random.choice(
                    ["pendiente", "en_transito", "entregado"]
                ),
                creado_por=admin,
                actualizado_por=admin,
            )

            print(
                f"  ✅ #{envio.numero_seguimiento}: {envio.destinatario_nombre}"
            )
            print(
                f"     {envio.origen} → {envio.destino} | {envio.peso}kg | ${envio.valor_declarado}"
            )

        except Exception as e:
            print(f"  ❌ Error creando envío {i+1}: {e}")

    # Estadísticas finales
    total_envios = Envio.objects.count()
    print(f"\n🎉 COMPLETADO!")
    print(f"📊 Total de envíos creados: {total_envios}")

    # Resumen por estado
    from django.db.models import Count

    estados = (
        Envio.objects.values("estado")
        .annotate(count=Count("estado"))
        .order_by("estado")
    )
    print(f"\n📈 Resumen por estado:")
    for estado in estados:
        print(f"  - {estado['estado']}: {estado['count']} envíos")


if __name__ == "__main__":
    main()
