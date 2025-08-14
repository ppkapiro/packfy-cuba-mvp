#!/usr/bin/env python
"""
🇨🇺 Script para actualizar remitentes con datos simulados realistas
"""
import os
import sys

import django

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import random

from envios.models import Envio


def main():
    print("🇨🇺 ACTUALIZANDO REMITENTES CON DATOS REALISTAS")
    print("=" * 50)

    # Remitentes simulados realistas cubanos
    remitentes_cubanos = [
        {
            "nombre": "María Elena Rodríguez Pérez",
            "direccion": "Calle 17 #304, Vedado, La Habana, Cuba",
            "telefono": "+53 78451236",
            "email": "maria.rodriguez@nauta.cu",
        },
        {
            "nombre": "Carlos Alberto González Martínez",
            "direccion": "Avenida 31 #2456, Playa, La Habana, Cuba",
            "telefono": "+53 72847593",
            "email": "carlos.gonzalez@nauta.cu",
        },
        {
            "nombre": "Ana Beatriz López Fernández",
            "direccion": "Calle San Lázaro #567, Centro Habana, Cuba",
            "telefono": "+53 78934521",
            "email": "ana.lopez@nauta.cu",
        },
        {
            "nombre": "José Manuel Herrera Castro",
            "direccion": "Malecón #123, Habana Vieja, La Habana, Cuba",
            "telefono": "+53 72156389",
            "email": "jose.herrera@nauta.cu",
        },
        {
            "nombre": "Carmen Rosa Díaz Torres",
            "direccion": "Avenida de los Presidentes #789, Vedado, La Habana, Cuba",
            "telefono": "+53 78567234",
            "email": "carmen.diaz@nauta.cu",
        },
        {
            "nombre": "Roberto Carlos Sánchez Ruiz",
            "direccion": "Calle L #345, Vedado, La Habana, Cuba",
            "telefono": "+53 76234578",
            "email": "roberto.sanchez@nauta.cu",
        },
        {
            "nombre": "Yolanda María Jiménez Vargas",
            "direccion": "Avenida 26 #678, Nuevo Vedado, La Habana, Cuba",
            "telefono": "+53 78345629",
            "email": "yolanda.jimenez@nauta.cu",
        },
        {
            "nombre": "Miguel Ángel Morales Delgado",
            "direccion": "Calle 23 #891, Vedado, La Habana, Cuba",
            "telefono": "+53 75674523",
            "email": "miguel.morales@nauta.cu",
        },
        {
            "nombre": "Laura Isabel Ramírez Ortega",
            "direccion": "Avenida 41 #234, Playa, La Habana, Cuba",
            "telefono": "+53 78923456",
            "email": "laura.ramirez@nauta.cu",
        },
        {
            "nombre": "Francisco Javier Mendoza García",
            "direccion": "Calle Real #456, Centro Habana, La Habana, Cuba",
            "telefono": "+53 76785432",
            "email": "francisco.mendoza@nauta.cu",
        },
    ]

    # Obtener todos los envíos
    envios = Envio.objects.all().order_by("id")
    print(f"📦 Encontrados {envios.count()} envíos para actualizar")

    if envios.count() == 0:
        print("❌ No hay envíos en la base de datos")
        return

    print("\n🔄 Actualizando remitentes...")

    for i, envio in enumerate(envios):
        # Asignar remitente de forma cíclica
        remitente = remitentes_cubanos[i % len(remitentes_cubanos)]

        # Actualizar campos del remitente
        envio.remitente_nombre = remitente["nombre"]
        envio.remitente_direccion = remitente["direccion"]
        envio.remitente_telefono = remitente["telefono"]
        envio.remitente_email = remitente["email"]

        envio.save()

        print(f"  ✅ #{envio.numero_guia}: {remitente['nombre']}")
        print(f"     📧 {remitente['email']} | 📞 {remitente['telefono']}")
        print(f"     📍 {remitente['direccion']}")
        print()

    print("🎉 ¡ACTUALIZACIÓN COMPLETADA!")
    print(f"📊 {envios.count()} envíos actualizados con remitentes realistas")

    # Mostrar resumen
    print("\n📋 RESUMEN DE REMITENTES:")
    remitentes_unicos = set()
    for envio in Envio.objects.all():
        remitentes_unicos.add(envio.remitente_nombre)

    for remitente in sorted(remitentes_unicos):
        count = Envio.objects.filter(remitente_nombre=remitente).count()
        print(f"  - {remitente}: {count} envío(s)")


if __name__ == "__main__":
    main()
