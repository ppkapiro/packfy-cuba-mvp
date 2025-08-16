import pytest
from django.test import Client
from envios.models import Envio

pytestmark = pytest.mark.django_db


def test_rastrear_cache(client: Client):
    envio = Envio.objects.create(
        numero_guia="PKFTESTCACHE1",
        remitente_nombre="A",
        remitente_direccion="dir",
        remitente_telefono="123",
        destinatario_nombre="B",
        destinatario_direccion="dir2",
        destinatario_telefono="456",
        descripcion="desc",
        estado_actual="pendiente",
    )
    url = f"/api/envios/rastrear?numero_guia={envio.numero_guia}"
    r1 = client.get(url)
    assert r1.status_code == 200
    # Simular cambio en DB que no debería reflejarse hasta expirar cache
    envio.estado_actual = "transito"
    envio.save()
    r2 = client.get(url)
    assert r2.status_code == 200
    data2 = r2.json()
    # El estado debería seguir siendo el inicial (cacheado) si caching funciona
    assert data2["estado"] == "pendiente"
