#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SCRIPT PROTEGIDO - Flush de Base de Datos
Requiere autorización antes de limpiar la BD
"""

import os
import sys

import django

from protector_bd import ProtectorBaseDatos, requiere_autorizacion

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command


@requiere_autorizacion("FLUSH COMPLETO DE BASE DE DATOS")
def flush_base_datos():
    """
    Limpia completamente la base de datos
    ⚠️ OPERACIÓN DESTRUCTIVA - Requiere autorización
    """
    print("🗑️ Ejecutando flush de base de datos...")
    call_command("flush", "--noinput")
    print("✅ Base de datos limpiada")


@requiere_autorizacion("EJECUTAR MIGRACIONES")
def ejecutar_migraciones():
    """
    Ejecuta todas las migraciones pendientes
    """
    print("📊 Ejecutando migraciones...")
    call_command("migrate")
    print("✅ Migraciones completadas")


@requiere_autorizacion("RESTAURAR ESTRUCTURA BLINDADA")
def restaurar_estructura():
    """
    Restaura la estructura blindada de usuarios
    """
    print("🔄 Restaurando estructura blindada...")

    # Importar y ejecutar la restauración
    exec(open("restaurar_estructura_20250820_095645.py").read())

    print("✅ Estructura restaurada")


def main():
    """Función principal con menú de opciones"""
    protector = ProtectorBaseDatos()

    print("🛡️ GESTIÓN PROTEGIDA DE BASE DE DATOS")
    print("=" * 50)

    # Verificar estado de protección
    if protector.esta_protegida():
        print("🛡️ Estado: BASE DE DATOS PROTEGIDA")
        print(f"📊 Datos: {protector.obtener_estado_bd()}")
    else:
        print("⚠️  Estado: BASE DE DATOS NO PROTEGIDA")
        respuesta = (
            input("¿Desea activar la protección? (si/no): ").strip().lower()
        )
        if respuesta in ["si", "sí", "s"]:
            protector.activar_proteccion()

    print("\nOpciones disponibles:")
    print("1. 🗑️  Limpiar base de datos (flush)")
    print("2. 📊 Ejecutar migraciones")
    print("3. 🔄 Restaurar estructura blindada")
    print("4. 🛡️ Gestionar protección")
    print("5. 📋 Ver estado actual")
    print("0. ❌ Salir")

    while True:
        try:
            opcion = input("\nSeleccione una opción (0-5): ").strip()

            if opcion == "1":
                flush_base_datos()
            elif opcion == "2":
                ejecutar_migraciones()
            elif opcion == "3":
                restaurar_estructura()
            elif opcion == "4":
                gestionar_proteccion()
            elif opcion == "5":
                mostrar_estado()
            elif opcion == "0":
                print("👋 Saliendo...")
                break
            else:
                print("❓ Opción no válida")

        except KeyboardInterrupt:
            print("\n👋 Saliendo...")
            break


def gestionar_proteccion():
    """Gestiona el estado de protección"""
    protector = ProtectorBaseDatos()

    if protector.esta_protegida():
        print("🛡️ La protección está ACTIVA")
        respuesta = input("¿Desea desactivarla? (si/no): ").strip().lower()
        if respuesta in ["si", "sí", "s"]:
            protector.desactivar_proteccion()
    else:
        print("⚠️  La protección está INACTIVA")
        respuesta = input("¿Desea activarla? (si/no): ").strip().lower()
        if respuesta in ["si", "sí", "s"]:
            protector.activar_proteccion()


def mostrar_estado():
    """Muestra el estado actual del sistema"""
    try:
        from empresas.models import Empresa, PerfilUsuario
        from usuarios.models import Usuario

        print("\n📊 ESTADO ACTUAL DEL SISTEMA:")
        print(f"👥 Usuarios: {Usuario.objects.count()}")
        print(f"🏢 Empresas: {Empresa.objects.count()}")
        print(f"👤 Perfiles: {PerfilUsuario.objects.count()}")

        print("\n📋 Usuarios registrados:")
        for user in Usuario.objects.all().order_by("email"):
            print(f"  - {user.email} ({user.first_name} {user.last_name})")

    except Exception as e:
        print(f"❌ Error al obtener estado: {e}")


if __name__ == "__main__":
    main()
