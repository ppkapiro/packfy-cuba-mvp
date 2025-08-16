import pytest
from django.test import Client
from envios.models import Envio

pytestmark = pytest.mark.django_db


def test_estadisticas_endpoint(client: Client, django_user_model):
    # Crear usuario y loguear
    user = django_user_model.objects.create_user(username="u1", password="p1")
    client.force_login(user)
    # Crear envíos con distintos estados
    Envio.objects.create(
        numero_guia="PKFEST1",
        remitente_nombre="R1",
        remitente_direccion="d",
        remitente_telefono="t",
        destinatario_nombre="D1",
        destinatario_direccion="d2",
        destinatario_telefono="t2",
        descripcion="desc",
        estado_actual="RECIBIDO",
        creado_por=user,
        actualizado_por=user,
    )
    Envio.objects.create(
        numero_guia="PKFEST2",
        remitente_nombre="R2",
        remitente_direccion="d",
        remitente_telefono="t",
        destinatario_nombre="D2",
        destinatario_direccion="d2",
        destinatario_telefono="t2",
        descripcion="desc",
        estado_actual="EN_TRANSITO",
        creado_por=user,
        actualizado_por=user,
    )

    r = client.get("/api/envios/estadisticas/")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 2
    assert "RECIBIDO" in data["por_estado"]
    assert data["origen"] in {"matview", "query"}
