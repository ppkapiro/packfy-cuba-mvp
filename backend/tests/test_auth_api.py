import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from usuarios.models import Usuario


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def demo_user(db):
    email = "testuser@example.com"
    password = "testpass123"
    user = Usuario.objects.create_user(email=email, password=password)
    return {"user": user, "email": email, "password": password}


def test_login_success(api_client, demo_user):
    url = "/api/auth/login/"
    resp = api_client.post(
        url,
        {"email": demo_user["email"], "password": demo_user["password"]},
        format="json",
    )
    assert resp.status_code == status.HTTP_200_OK, resp.data
    data = resp.json()
    assert "access" in data and "refresh" in data
    # Optional user payload
    assert data.get("user", {}).get("email") == demo_user["email"]


def test_login_failure_wrong_password(api_client, demo_user):
    url = "/api/auth/login/"
    resp = api_client.post(
        url,
        {"email": demo_user["email"], "password": "wrong"},
        format="json",
    )
    assert resp.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_400_BAD_REQUEST,
    )


def test_refresh_success(api_client, demo_user):
    # Login primero
    login = api_client.post(
        "/api/auth/login/",
        {"email": demo_user["email"], "password": demo_user["password"]},
        format="json",
    )
    assert login.status_code == status.HTTP_200_OK
    refresh = login.json()["refresh"]

    # Refresh
    resp = api_client.post(
        "/api/auth/refresh/",
        {"refresh": refresh},
        format="json",
    )
    assert resp.status_code == status.HTTP_200_OK, resp.data
    assert "access" in resp.json()


def test_secure_logout_requires_auth(api_client, demo_user):
    # Login
    login = api_client.post(
        "/api/auth/login/",
        {"email": demo_user["email"], "password": demo_user["password"]},
        format="json",
    )
    assert login.status_code == status.HTTP_200_OK
    tokens = login.json()
    access = tokens["access"]
    refresh = tokens["refresh"]

    # Logout con token de acceso y refresh en cuerpo
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    resp = api_client.post(
        "/api/auth/logout/",
        {"refresh_token": refresh},
        format="json",
    )
    assert resp.status_code in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT)
