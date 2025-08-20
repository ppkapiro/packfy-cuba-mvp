#!/usr/bin/env python
"""
Script de inicialización completa del sistema multi-tenant
Resetea la base de datos y crea datos de prueba consistentes
"""

import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection, transaction
from empresas.models import Empresa, PerfilUsuario
from envios.models import Envio, HistorialEstado
from usuarios.models import Usuario


def reset_database():
    """Resetea completamente la base de datos"""
    print("🗃️ Reseteando base de datos...")

    with connection.cursor() as cursor:
        # Obtener todas las tablas
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%';
        """
        )
        tables = [row[0] for row in cursor.fetchall()]

        # Desactivar foreign key checks
        cursor.execute("PRAGMA foreign_keys = OFF;")

        # Limpiar todas las tablas
        for table in tables:
            cursor.execute(f"DELETE FROM {table};")
            print(f"  ✅ Tabla {table} limpiada")

        # Reactivar foreign key checks
        cursor.execute("PRAGMA foreign_keys = ON;")

    print("✅ Base de datos reseteada exitosamente")


def create_empresas():
    """Crear empresas de prueba"""
    print("🏢 Creando empresas de prueba...")

    empresas_data = [
        {
            "nombre": "Packfy Express Cuba",
            "slug": "packfy-express",
            "descripcion": "Empresa principal de paquetería rápida",
            "activo": True,
        },
        {
            "nombre": "Miami Shipping Co",
            "slug": "miami-shipping",
            "descripcion": "Operaciones en Miami, Florida",
            "activo": True,
        },
        {
            "nombre": "Habana Logistics",
            "slug": "habana-logistics",
            "descripcion": "Distribución local en La Habana",
            "activo": True,
        },
    ]

    empresas_creadas = []
    for empresa_data in empresas_data:
        empresa, created = Empresa.objects.get_or_create(
            slug=empresa_data["slug"], defaults=empresa_data
        )
        empresas_creadas.append(empresa)
        status = "creada" if created else "ya existía"
        print(f"  ✅ Empresa '{empresa.nombre}' {status}")

    return empresas_creadas


def create_usuarios_and_profiles(empresas):
    """Crear usuarios y sus perfiles en empresas"""
    print("👥 Creando usuarios y perfiles...")

    # Crear usuarios
    usuarios_data = [
        {
            "email": "admin@packfy.cu",
            "nombre": "Administrador Sistema",
            "telefono": "+53 5 123-4567",
            "is_staff": True,
            "is_superuser": True,
        },
        {
            "email": "operador.miami@packfy.cu",
            "nombre": "Juan Operador Miami",
            "telefono": "+1 305-123-4567",
        },
        {
            "email": "operador.cuba@packfy.cu",
            "nombre": "María Operadora Cuba",
            "telefono": "+53 5 234-5678",
        },
        {
            "email": "cliente1@ejemplo.cu",
            "nombre": "Carlos Cliente",
            "telefono": "+53 5 345-6789",
        },
    ]

    usuarios_creados = []
    for usuario_data in usuarios_data:
        email = usuario_data["email"]

        # Crear o obtener usuario
        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={
                **usuario_data,
                "password": "pbkdf2_sha256$720000$placeholder$hash",  # Contraseña temporal
            },
        )

        if created:
            usuario.set_password("password123")  # Contraseña de prueba
            usuario.save()

        usuarios_creados.append(usuario)
        status = "creado" if created else "ya existía"
        print(f"  ✅ Usuario '{usuario.email}' {status}")

    # Crear perfiles en empresas
    print("🎭 Asignando perfiles a empresas...")

    perfiles_asignaciones = [
        # Admin en todas las empresas como dueño
        (usuarios_creados[0], empresas[0], "dueno"),
        (usuarios_creados[0], empresas[1], "dueno"),
        (usuarios_creados[0], empresas[2], "dueno"),
        # Operador Miami
        (usuarios_creados[1], empresas[1], "operador_miami"),
        # Operador Cuba
        (usuarios_creados[2], empresas[0], "operador_cuba"),
        (usuarios_creados[2], empresas[2], "operador_cuba"),
        # Cliente en una empresa
        (usuarios_creados[3], empresas[0], "remitente"),
    ]

    for usuario, empresa, rol in perfiles_asignaciones:
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=usuario, empresa=empresa, defaults={"rol": rol}
        )
        status = "creado" if created else "ya existía"
        print(
            f"  ✅ Perfil {usuario.email} -> {empresa.slug} ({rol}) {status}"
        )

    return usuarios_creados


def create_envios_demo(empresas, usuarios):
    """Crear envíos de demostración"""
    print("📦 Creando envíos de demostración...")

    envios_data = [
        # Packfy Express Cuba
        {
            "empresa": empresas[0],
            "numero_guia": "PEC001",
            "estado_actual": "pendiente",
            "remitente_nombre": "Carlos Cliente",
            "remitente_telefono": "+53 5 345-6789",
            "remitente_direccion": "Calle 23 #456, Vedado, La Habana",
            "destinatario_nombre": "Ana Familia",
            "destinatario_telefono": "+53 5 987-6543",
            "destinatario_direccion": "Avenida 26 #123, Nuevo Vedado, La Habana",
            "descripcion": "Medicamentos y productos de higiene personal",
            "peso_kg": 2.5,
            "valor_declarado": 150.00,
        },
        {
            "empresa": empresas[0],
            "numero_guia": "PEC002",
            "estado_actual": "en_transito",
            "remitente_nombre": "Luis Sender",
            "remitente_telefono": "+1 305-456-7890",
            "remitente_direccion": "8250 NW 53rd St, Doral, FL 33166",
            "destinatario_nombre": "Rosa Pérez",
            "destinatario_telefono": "+53 5 111-2222",
            "destinatario_direccion": "Calle Real #45, Centro Habana",
            "descripcion": "Ropa y calzado",
            "peso_kg": 4.0,
            "valor_declarado": 200.00,
        },
        # Miami Shipping Co
        {
            "empresa": empresas[1],
            "numero_guia": "MSC001",
            "estado_actual": "entregado",
            "remitente_nombre": "Roberto Miami",
            "remitente_telefono": "+1 305-123-4567",
            "remitente_direccion": "1234 SW 8th St, Miami, FL 33135",
            "destinatario_nombre": "Elena Cuba",
            "destinatario_telefono": "+53 5 333-4444",
            "destinatario_direccion": "Malecón #678, La Habana Vieja",
            "descripcion": "Electrónicos y accesorios",
            "peso_kg": 3.2,
            "valor_declarado": 500.00,
        },
        # Habana Logistics
        {
            "empresa": empresas[2],
            "numero_guia": "HAB001",
            "estado_actual": "pendiente",
            "remitente_nombre": "Pedro Local",
            "remitente_telefono": "+53 5 555-6666",
            "remitente_direccion": "Infanta #234, Centro Habana",
            "destinatario_nombre": "Carmen Destinatario",
            "destinatario_telefono": "+53 5 777-8888",
            "destinatario_direccion": "Línea #89, Vedado, La Habana",
            "descripcion": "Documentos importantes",
            "peso_kg": 0.5,
            "valor_declarado": 50.00,
        },
    ]

    for envio_data in envios_data:
        numero_guia = envio_data["numero_guia"]
        envio, created = Envio.objects.get_or_create(
            numero_guia=numero_guia, defaults=envio_data
        )
        status = "creado" if created else "ya existía"
        print(
            f"  ✅ Envío '{numero_guia}' para {envio.empresa.nombre} {status}"
        )

        # Crear historial inicial
        if created:
            HistorialEstado.objects.create(
                envio=envio,
                estado_anterior="",
                estado_nuevo=envio.estado_actual,
                comentario=f"Envío creado en {envio.empresa.nombre}",
                usuario_responsable=f"Sistema - {envio.empresa.nombre}",
            )


def main():
    """Función principal de inicialización"""
    print("🚀 INICIALIZACIÓN COMPLETA DEL SISTEMA MULTI-TENANT")
    print("=" * 60)

    try:
        with transaction.atomic():
            # 1. Resetear base de datos
            reset_database()

            # 2. Crear empresas
            empresas = create_empresas()

            # 3. Crear usuarios y perfiles
            usuarios = create_usuarios_and_profiles(empresas)

            # 4. Crear envíos de demo
            create_envios_demo(empresas, usuarios)

        print("\n" + "=" * 60)
        print("✅ INICIALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("\n📋 RESUMEN:")
        print(f"   • {len(empresas)} empresas creadas")
        print(f"   • {len(usuarios)} usuarios creados")
        print(f"   • {Envio.objects.count()} envíos de demostración")

        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("   Email: admin@packfy.cu")
        print("   Contraseña: password123")
        print("   (Usuario administrador con acceso a todas las empresas)")

        print("\n🏢 EMPRESAS DISPONIBLES:")
        for empresa in empresas:
            print(f"   • {empresa.nombre} (slug: {empresa.slug})")

    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
