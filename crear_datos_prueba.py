import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from envios.models import Envio
from usuarios.models import Usuario

admin = Usuario.objects.first()

# Crear envíos adicionales para testing
envios_prueba = [
    (
        "TEST003",
        "RECIBIDO",
        "Carlos Rodriguez",
        "Ana Martinez",
        "Paquete electrónicos",
    ),
    (
        "TEST004",
        "EN_REPARTO",
        "Maria Garcia",
        "Pedro Lopez",
        "Documentos importantes",
    ),
    ("TEST005", "ENTREGADO", "Juan Perez", "Carmen Silva", "Medicamentos"),
    (
        "TEST006",
        "EN_TRANSITO",
        "Ana Lopez",
        "Maria Rodriguez",
        "Libros académicos",
    ),
]

for guia, estado, remitente, destinatario, descripcion in envios_prueba:
    if not Envio.objects.filter(numero_guia=guia).exists():
        Envio.objects.create(
            numero_guia=guia,
            estado_actual=estado,
            descripcion=descripcion,
            peso=1.0,
            valor_declarado=25.00,
            remitente_nombre=remitente,
            remitente_direccion="Direccion de prueba",
            remitente_telefono="53111111",
            destinatario_nombre=destinatario,
            destinatario_direccion="Direccion destino de prueba",
            destinatario_telefono="53222222",
            creado_por=admin,
        )
        print(f"Creado: {guia} - {remitente} -> {destinatario}")

print(f"Total envios: {Envio.objects.count()}")
