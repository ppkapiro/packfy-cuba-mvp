import logging
import re

import pytest
from django.test import Client

pytestmark = pytest.mark.django_db


class CaptureHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


def test_request_id_and_logging(client: Client, settings):
    handler = CaptureHandler()
    logger = logging.getLogger("config.logging_context")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    resp = client.get("/health/")
    assert resp.status_code == 200
    rid = resp.headers.get("X-Request-ID") or resp.headers.get("x-request-id")
    assert rid and re.match(r"^[a-f0-9\-]{16,36}$", rid)

    # Debe haberse logueado al menos un record con esos extras
    assert any(getattr(r, "request_id", None) == rid for r in handler.records)
    # Status code registrado
    assert any(
        getattr(r, "status_code", None) == resp.status_code
        for r in handler.records
    )

    logger.removeHandler(handler)
