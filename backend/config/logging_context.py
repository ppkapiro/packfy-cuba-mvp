"""Middleware para enriquecer registros con request_id, path y status.
Añade atributos a LogRecord mediante un filtro global ligero.
"""

import logging
import time

from django.utils.deprecation import MiddlewareMixin

_logger = logging.getLogger(__name__)


class LoggingContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._log_start = time.perf_counter()  # type: ignore[attr-defined]

    def process_response(self, request, response):
        # Insertar campos en record via LoggerAdapter pattern usando atributos globales
        duration_ms = None
        start = getattr(request, "_log_start", None)
        if start:
            duration_ms = (time.perf_counter() - start) * 1000
        # Guardar en objeto request para que formato JSON (que espera record.*) no falle
        # Usamos logging.setLogRecordFactory? Simplicidad: añadimos a logging.Logger mediante extra en un mensaje debug
        extra = {
            "request_id": getattr(request, "request_id", "-"),
            "request_path": request.path,
            "status_code": response.status_code,
            "latency_ms": round(duration_ms, 2) if duration_ms else None,
        }
        # Emite trazas muy ligeras sólo si excede umbral
        if duration_ms and duration_ms > 1000:
            _logger.warning(
                "request lento", extra=extra
            )  # Formato JSON incluirá campos
        else:
            _logger.info("request", extra=extra)
        return response
