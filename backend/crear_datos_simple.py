import os
import sys

import django

# Add the project directory to Python path
sys.path.append("/app")

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_development")
django.setup()

from datetime import datetime, timedelta

from empresas.models import Empresa
from envios.models import Envio
from usuarios.models import Usuario

print("🚀 Iniciando creación de datos demo...")

# Verificar usuario admin
try:
    admin_user = Usuario.objects.get(email="admin@packfy.cu")
    print(f"✅ Usuario admin encontrado: {admin_user.email}")
except Usuario.DoesNotExist:
    print("❌ Usuario admin no encontrado")
    sys.exit(1)

# Crear/obtener empresa
empresa, created = Empresa.objects.get_or_create(
    nombre="Packfy Cuba Demo",
    defaults={
        "direccion": "La Habana, Cuba",
        "telefono": "+53 7 123-4567",
        "email": "demo@packfy.cu",
        "activa": True,
    },
)
print(f"✅ Empresa: {empresa.nombre} ({'creada' if created else 'existente'})")

# Crear envíos
envios_data = [
    {
        "numero_guia": "PK20250001",
        "estado_actual": "REGISTRADO",
        "remitente_nombre": "José Martí",
        "destinatario_nombre": "Carlos Fernández",
        "descripcion": "Paquete de medicamentos",
        "peso": 2.5,
        "valor_declarado": 150.00,
    },
    {
        "numero_guia": "PK20250002",
        "estado_actual": "EN_TRANSITO",
        "remitente_nombre": "María González",
        "destinatario_nombre": "Ana López",
        "descripcion": "Ropa y calzado",
        "peso": 3.2,
        "valor_declarado": 200.00,
    },
    {
        "numero_guia": "PK20250003",
        "estado_actual": "EN_ALMACEN",
        "remitente_nombre": "Roberto Silva",
        "destinatario_nombre": "Carmen Herrera",
        "descripcion": "Productos electrónicos",
        "peso": 1.8,
        "valor_declarado": 350.00,
    },
    {
        "numero_guia": "PK20250004",
        "estado_actual": "EN_RUTA",
        "remitente_nombre": "Luis Pérez",
        "destinatario_nombre": "Elena Castro",
        "descripcion": "Alimentos no perecederos",
        "peso": 4.1,
        "valor_declarado": 75.00,
    },
    {
        "numero_guia": "PK20250005",
        "estado_actual": "ENTREGADO",
        "remitente_nombre": "Miguel Rodríguez",
        "destinatario_nombre": "Isabel Torres",
        "descripcion": "Libros y material escolar",
        "peso": 2.9,
        "valor_declarado": 120.00,
    },
]

envios_creados = 0
for data in envios_data:
    try:
        # Verificar si ya existe
        if Envio.objects.filter(numero_guia=data["numero_guia"]).exists():
            print(f"⚠️ Envío {data['numero_guia']} ya existe")
            continue

        envio = Envio.objects.create(
            numero_guia=data["numero_guia"],
            estado_actual=data["estado_actual"],
            # Fechas
            fecha_creacion=datetime.now() - timedelta(days=envios_creados),
            fecha_estimada_entrega=datetime.now() + timedelta(days=5),
            # Remitente
            remitente_nombre=data["remitente_nombre"],
            remitente_telefono="+53 5 1234-5678",
            remitente_direccion="La Habana, Cuba",
            remitente_ciudad="La Habana",
            # Destinatario
            destinatario_nombre=data["destinatario_nombre"],
            destinatario_telefono="+53 5 8765-4321",
            destinatario_direccion="Santiago de Cuba, Cuba",
            destinatario_ciudad="Santiago de Cuba",
            # Paquete
            descripcion=data["descripcion"],
            peso=data["peso"],
            valor_declarado=data["valor_declarado"],
            # Relaciones
            usuario_creador=admin_user,
            empresa=empresa,
        )

        envios_creados += 1
        print(f"✅ Envío creado: {envio.numero_guia} - {envio.estado_actual}")

    except Exception as e:
        print(f"❌ Error creando envío {data['numero_guia']}: {e}")

print(f"\n🎉 Proceso completado!")
print(f"Envíos creados: {envios_creados}")
print(f"Total en sistema: {Envio.objects.count()}")
