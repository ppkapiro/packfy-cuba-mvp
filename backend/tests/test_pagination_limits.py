import pytest
from django.test import Client

pytestmark = pytest.mark.django_db


def test_pagination_max_page_size(client: Client, django_user_model):
    user = django_user_model.objects.create_user(username="u1", password="p1")
    client.force_login(user)
    # Solicitar un page_size muy grande debe recortarse a 100
    r = client.get("/api/envios/?page_size=10000")
    assert r.status_code == 200
    data = r.json()
    assert data["page_size"] == 100


def test_pagination_fields_present(client: Client, django_user_model):
    user = django_user_model.objects.create_user(username="u2", password="p1")
    client.force_login(user)
    r = client.get("/api/envios/")
    assert r.status_code == 200
    data = r.json()
    assert {"count", "page", "page_size", "total_pages", "results"}.issubset(
        data.keys()
    )
