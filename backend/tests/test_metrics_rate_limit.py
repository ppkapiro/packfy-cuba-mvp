import os
import time

import pytest
from django.test import Client

pytestmark = pytest.mark.django_db


def test_metrics_endpoint(client: Client):
    resp = client.get("/api/metrics/")
    assert resp.status_code == 200
    # Debe contener nombres de métricas registradas si hay peticiones previas
    assert (
        b"packfy_request_total" in resp.content
        or b"packfy_request_latency_seconds" in resp.content
    )


def test_rate_limit_applies(client: Client, settings):
    # Reducir límites para prueba rápida
    os.environ["RATE_LIMIT_WINDOW"] = "5"
    os.environ["RATE_LIMIT_MAX"] = "3"
    # Hacemos 4 peticiones a un endpoint monitoreado (usar rastrear) simulando misma IP
    hit_url = "/api/envios/rastrear?code=TEST123"
    for i in range(3):
        r = client.get(hit_url, REMOTE_ADDR="1.2.3.4")
        # Permitimos 404 u otro código pero no 429 hasta superar
        assert r.status_code != 429
    r = client.get(hit_url, REMOTE_ADDR="1.2.3.4")
    assert r.status_code == 429
    data = r.json()
    assert "retry_after" in data
