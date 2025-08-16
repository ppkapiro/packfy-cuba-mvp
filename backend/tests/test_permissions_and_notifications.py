import pytest
from django.contrib.auth import get_user_model
from envios.models import Envio
from envios.notifications import enviar_notificacion_estado
from rest_framework.test import APIRequestFactory
from usuarios.permissions import EsCreadorOAdministrador


@pytest.mark.django_db
def test_es_creador_o_admin_allows_creator_object_permission():
    User = get_user_model()
    user = User.objects.create_user(username="u1", password="p1")
    other = User.objects.create_user(username="u2", password="p2")
    envio = Envio.objects.create(
        numero_guia="G-1",
        remitente_nombre="R",
        remitente_direccion="",
        remitente_telefono="",
        remitente_email="r@example.com",
        destinatario_nombre="D",
        destinatario_direccion="",
        destinatario_telefono="",
        destinatario_email="d@example.com",
        creado_por=user,
        actualizado_por=user,
        usuario=user,
    )
    perm = EsCreadorOAdministrador()
    factory = APIRequestFactory()
    request = factory.get("/api/envios/")
    request.user = user
    assert perm.has_object_permission(request, None, envio) is True

    request.user = other
    assert perm.has_object_permission(request, None, envio) is False


@pytest.mark.django_db
def test_enviar_notificacion_estado_no_recipients_returns_false(settings):
    User = get_user_model()
    user = User.objects.create_user(username="u1", password="p1")
    envio = Envio.objects.create(
        numero_guia="G-2",
        remitente_nombre="R",
        remitente_direccion="",
        remitente_telefono="",
        remitente_email="",
        destinatario_nombre="D",
        destinatario_direccion="",
        destinatario_telefono="",
        destinatario_email="",
        creado_por=user,
        actualizado_por=user,
        usuario=user,
    )
    assert enviar_notificacion_estado(envio) is False


@pytest.mark.django_db
def test_enviar_notificacion_estado_sends_to_valid_emails(
    monkeypatch, settings
):
    sent = {"count": 0}

    def fake_send_mail(*args, **kwargs):
        sent["count"] += 1
        return 1

    import envios.notifications as notif

    monkeypatch.setattr(notif, "send_mail", fake_send_mail)
    User = get_user_model()
    user = User.objects.create_user(username="u1", password="p1")
    envio = Envio.objects.create(
        numero_guia="G-3",
        remitente_nombre="R",
        remitente_direccion="",
        remitente_telefono="",
        remitente_email="r@example.com",
        destinatario_nombre="D",
        destinatario_direccion="",
        destinatario_telefono="",
        destinatario_email="d@example.com",
        creado_por=user,
        actualizado_por=user,
        usuario=user,
    )

    assert enviar_notificacion_estado(envio) is True
    assert sent["count"] == 2
