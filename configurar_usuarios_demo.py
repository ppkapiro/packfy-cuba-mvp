#!/usr/bin/env python
"""
Script para crear usuarios de prueba con diferentes roles en el sistema multi-tenant
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from protector_bd import requiere_autorizacion, ProtectorBaseDatos

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from empresas.models import Empresa, PerfilUsuario
from envios.models import Envio, HistorialEstado
from usuarios.models import Usuario


@requiere_autorizacion("CREAR USUARIOS")
def crear_usuarios_prueba():
    """Crear usuarios de prueba con diferentes roles"""
    print("👥 Creando usuarios de prueba...")

    usuarios_data = [
        {
            "email": "admin@packfy.cu",
            "nombre": "Administrador Sistema",
            "telefono": "+53 5 123-4567",
            "password": "password123",
            "is_staff": True,
            "is_superuser": True,
            "descripcion": "Administrador principal del sistema",
        },
        {
            "email": "gerente.miami@packfy.cu",
            "nombre": "Roberto García",
            "telefono": "+1 305-555-0101",
            "password": "miami123",
            "descripcion": "Gerente de operaciones en Miami",
        },
        {
            "email": "operador.cuba@packfy.cu",
            "nombre": "María González",
            "telefono": "+53 5 234-5678",
            "password": "cuba123",
            "descripcion": "Operadora en La Habana",
        },
        {
            "email": "cliente1@ejemplo.cu",
            "nombre": "Carlos Cliente",
            "telefono": "+53 5 345-6789",
            "password": "cliente123",
            "descripcion": "Cliente frecuente",
        },
        {
            "email": "cliente2@ejemplo.com",
            "nombre": "Ana Remitente",
            "telefono": "+1 786-555-0202",
            "password": "cliente123",
            "descripcion": "Cliente desde Miami",
        },
    ]

    usuarios_creados = []
    for usuario_data in usuarios_data:
        email = usuario_data["email"]
        password = usuario_data.pop("password")

        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={**usuario_data, "password": make_password(password)},
        )

        if created:
            usuario.set_password(password)
            usuario.save()

        usuarios_creados.append((usuario, password))
        status = "✅ creado" if created else "ℹ️ ya existía"
        print(f"  {status}: {usuario.email} - {usuario.nombre}")

    return usuarios_creados


def asignar_perfiles_empresas(usuarios_creados):
    """Asignar perfiles de usuarios a diferentes empresas"""
    print("\n🏢 Asignando perfiles a empresas...")

    # Obtener empresas
    empresas = {
        "packfy": Empresa.objects.filter(slug__icontains="packfy").first(),
        "miami": Empresa.objects.filter(slug__icontains="miami").first(),
        "habana": Empresa.objects.filter(slug__icontains="habana").first(),
    }

    print(f"Empresas encontradas: {list(empresas.keys())}")

    # Definir asignaciones de perfiles
    asignaciones = [
        # Admin en todas las empresas como dueño
        (usuarios_creados[0][0], empresas["packfy"], "dueno"),
        (usuarios_creados[0][0], empresas["miami"], "dueno"),
        (usuarios_creados[0][0], empresas["habana"], "dueno"),
        # Gerente Miami - operador en Miami y Packfy
        (usuarios_creados[1][0], empresas["miami"], "operador_miami"),
        (usuarios_creados[1][0], empresas["packfy"], "operador_miami"),
        # Operador Cuba - operador en Packfy y Habana
        (usuarios_creados[2][0], empresas["packfy"], "operador_cuba"),
        (usuarios_creados[2][0], empresas["habana"], "operador_cuba"),
        # Cliente 1 - remitente en Packfy
        (usuarios_creados[3][0], empresas["packfy"], "remitente"),
        # Cliente 2 - remitente en Miami
        (usuarios_creados[4][0], empresas["miami"], "remitente"),
    ]

    for usuario, empresa, rol in asignaciones:
        if empresa:  # Solo si la empresa existe
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=usuario, empresa=empresa, defaults={"rol": rol}
            )
            status = "✅ creado" if created else "ℹ️ ya existía"
            print(f"  {status}: {usuario.email} → {empresa.nombre} ({rol})")


def crear_envios_demo(usuarios_creados):
    """Crear envíos de demostración para cada empresa"""
    print("\n📦 Creando envíos de demostración...")

    empresas = list(Empresa.objects.all())

    envios_demo = [
        {
            "empresa": empresas[0],
            "numero_guia": "PKF001",
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
            "empresa": empresas[1] if len(empresas) > 1 else empresas[0],
            "numero_guia": "MIA001",
            "estado_actual": "en_transito",
            "remitente_nombre": "Ana Remitente",
            "remitente_telefono": "+1 786-555-0202",
            "remitente_direccion": "8250 NW 53rd St, Doral, FL 33166",
            "destinatario_nombre": "Rosa Pérez",
            "destinatario_telefono": "+53 5 111-2222",
            "destinatario_direccion": "Calle Real #45, Centro Habana",
            "descripcion": "Ropa y calzado",
            "peso_kg": 4.0,
            "valor_declarado": 200.00,
        },
        {
            "empresa": empresas[2] if len(empresas) > 2 else empresas[0],
            "numero_guia": "HAB001",
            "estado_actual": "entregado",
            "remitente_nombre": "Roberto García",
            "remitente_telefono": "+1 305-555-0101",
            "remitente_direccion": "1234 SW 8th St, Miami, FL 33135",
            "destinatario_nombre": "Elena Cuba",
            "destinatario_telefono": "+53 5 333-4444",
            "destinatario_direccion": "Malecón #678, La Habana Vieja",
            "descripcion": "Electrónicos y accesorios",
            "peso_kg": 3.2,
            "valor_declarado": 500.00,
        },
    ]

    for envio_data in envios_demo:
        numero_guia = envio_data["numero_guia"]
        envio, created = Envio.objects.get_or_create(
            numero_guia=numero_guia, defaults=envio_data
        )
        status = "✅ creado" if created else "ℹ️ ya existía"
        print(f"  {status}: {numero_guia} para {envio.empresa.nombre}")

        # Crear historial inicial si es nuevo
        if created:
            HistorialEstado.objects.create(
                envio=envio,
                estado_anterior="",
                estado_nuevo=envio.estado_actual,
                comentario=f"Envío creado en {envio.empresa.nombre}",
                usuario_responsable=f"Sistema - {envio.empresa.nombre}",
                fecha_cambio=timezone.now(),
            )


def mostrar_resumen():
    """Mostrar resumen del sistema creado"""
    print("\n" + "=" * 60)
    print("🎉 SISTEMA MULTI-TENANT CONFIGURADO EXITOSAMENTE")
    print("=" * 60)

    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Empresas: {Empresa.objects.count()}")
    print(f"   • Usuarios: {Usuario.objects.count()}")
    print(f"   • Perfiles: {PerfilUsuario.objects.count()}")
    print(f"   • Envíos: {Envio.objects.count()}")

    print(f"\n🏢 EMPRESAS DISPONIBLES:")
    for empresa in Empresa.objects.all():
        print(f"   • {empresa.nombre} (slug: {empresa.slug})")

    print(f"\n🔑 USUARIOS DE PRUEBA:")
    usuarios_passwords = [
        ("admin@packfy.cu", "password123", "Administrador"),
        ("gerente.miami@packfy.cu", "miami123", "Gerente Miami"),
        ("operador.cuba@packfy.cu", "cuba123", "Operador Cuba"),
        ("cliente1@ejemplo.cu", "cliente123", "Cliente Cuba"),
        ("cliente2@ejemplo.com", "cliente123", "Cliente Miami"),
    ]

    for email, password, descripcion in usuarios_passwords:
        print(f"   • {email:<25} | {password:<12} | {descripcion}")

    print(f"\n🌐 ACCESO AL SISTEMA:")
    print(f"   • Frontend: http://localhost:5173")
    print(f"   • Backend API: http://localhost:8000/api/")
    print(f"   • Swagger Docs: http://localhost:8000/api/swagger/")

    print(f"\n🚀 PRÓXIMOS PASOS:")
    print(f"   1. Accede al frontend en http://localhost:5173")
    print(f"   2. Inicia sesión con cualquiera de los usuarios de prueba")
    print(f"   3. Prueba el cambio entre empresas con el selector")
    print(f"   4. Verifica que cada empresa muestra solo sus datos")


def main():
    """Función principal"""
    print("🚀 CONFIGURACIÓN COMPLETA DEL SISTEMA MULTI-TENANT")
    print("=" * 60)

    try:
        # 1. Crear usuarios de prueba
        usuarios_creados = crear_usuarios_prueba()

        # 2. Asignar perfiles a empresas
        asignar_perfiles_empresas(usuarios_creados)

        # 3. Crear envíos de demostración
        crear_envios_demo(usuarios_creados)

        # 4. Mostrar resumen
        mostrar_resumen()

    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        import traceback

        traceback.print_exc()



# 🛡️ VERIFICACIÓN DE PROTECCIÓN
if __name__ == "__main__":
    protector = ProtectorBaseDatos()
    if not protector.esta_protegida():
        print("⚠️  ADVERTENCIA: Base de datos no protegida")
        respuesta = input("¿Activar protección antes de continuar? (si/no): ")
        if respuesta.lower() in ['si', 'sí', 's']:
            protector.activar_proteccion()

if __name__ == "__main__":
    main()
