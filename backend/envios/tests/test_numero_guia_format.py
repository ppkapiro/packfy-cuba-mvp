import re

import pytest
from envios.models import Envio
from usuarios.models import Usuario


@pytest.mark.django_db
def test_formato_numero_guia():
    user = Usuario.objects.create_user(
        email="f@test.com", password="x", username="f"
    )
    envio = Envio.objects.create(
        descripcion="Test envio",
        peso=1.25,
        remitente_nombre="Remitente",
        remitente_direccion="Direccion R",
        remitente_telefono="5300000000",
        destinatario_nombre="Destinatario",
        destinatario_direccion="Direccion D",
        destinatario_telefono="5300000001",
        creado_por=user,
        actualizado_por=user,
    )
    assert re.fullmatch(
        r"PKF[0-9A-F]{10}", envio.numero_guia
    ), envio.numero_guia
