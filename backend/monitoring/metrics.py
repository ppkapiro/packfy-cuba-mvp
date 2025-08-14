# 🇨🇺 PACKFY CUBA - Sistema de Métricas Django v4.0

import logging
import time
from functools import wraps
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from prometheus_client.django_utils import ExportToDjangoView

logger = logging.getLogger(__name__)

# ===============================
# MÉTRICAS DE APLICACIÓN
# ===============================

# Métricas HTTP
http_requests_total = Counter(
    "packfy_http_requests_total",
    "Total de peticiones HTTP",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "packfy_http_request_duration_seconds",
    "Duración de peticiones HTTP",
    ["method", "endpoint"],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

# Métricas de Base de Datos
db_connections_active = Gauge(
    "packfy_db_connections_active", "Conexiones activas a la base de datos"
)

db_query_duration_seconds = Histogram(
    "packfy_db_query_duration_seconds",
    "Duración de consultas a la base de datos",
    ["operation"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
)

# Métricas de Cache
cache_operations_total = Counter(
    "packfy_cache_operations_total",
    "Total de operaciones de cache",
    ["operation", "result"],
)

cache_hit_ratio = Gauge("packfy_cache_hit_ratio", "Ratio de aciertos en cache")

# ===============================
# MÉTRICAS DE NEGOCIO
# ===============================

# Métricas de Envíos
shipments_created_total = Counter(
    "packfy_shipments_created_total",
    "Total de envíos creados",
    ["empresa", "tipo"],
)

shipments_status_total = Gauge(
    "packfy_shipments_status_total", "Envíos por estado", ["estado", "empresa"]
)

shipments_pending_total = Gauge(
    "packfy_shipments_pending_total", "Total de envíos pendientes"
)

shipments_failed_total = Counter(
    "packfy_shipments_failed_total",
    "Total de envíos fallidos",
    ["error_type", "empresa"],
)

shipments_delivery_time = Histogram(
    "packfy_shipments_delivery_time_hours",
    "Tiempo de entrega de envíos en horas",
    ["empresa"],
    buckets=(1, 6, 12, 24, 48, 72, 168),  # 1h a 1 semana
)

# Métricas de Usuarios
user_sessions_active = Gauge(
    "packfy_user_sessions_active", "Sesiones de usuario activas"
)

login_attempts_total = Counter(
    "packfy_login_attempts_total",
    "Total de intentos de login",
    ["result", "empresa"],
)

login_attempts_failed_total = Counter(
    "packfy_login_attempts_failed_total",
    "Total de intentos de login fallidos",
    ["reason"],
)

# Métricas de API
api_requests_per_company = Counter(
    "packfy_api_requests_per_company_total",
    "Peticiones a la API por empresa",
    ["empresa", "endpoint"],
)

api_rate_limit_exceeded = Counter(
    "packfy_api_rate_limit_exceeded_total",
    "Rate limits excedidos",
    ["empresa", "endpoint"],
)

# ===============================
# MIDDLEWARE DE MÉTRICAS
# ===============================


class MetricsMiddleware:
    """Middleware para capturar métricas de peticiones HTTP"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Procesar petición
        response = self.get_response(request)

        # Calcular duración
        duration = time.time() - start_time

        # Extraer información de la petición
        method = request.method
        path = self._get_normalized_path(request.path)
        status = str(response.status_code)

        # Registrar métricas
        http_requests_total.labels(
            method=method, endpoint=path, status=status
        ).inc()

        http_request_duration_seconds.labels(
            method=method, endpoint=path
        ).observe(duration)

        # Métricas por empresa si está autenticado
        if hasattr(request, "user") and request.user.is_authenticated:
            empresa = getattr(request.user, "empresa", "unknown")
            if empresa:
                api_requests_per_company.labels(
                    empresa=(
                        empresa.codigo
                        if hasattr(empresa, "codigo")
                        else str(empresa)
                    ),
                    endpoint=path,
                ).inc()

        return response

    def _get_normalized_path(self, path: str) -> str:
        """Normalizar rutas para agrupar métricas"""
        # Remover IDs y parámetros dinámicos
        import re

        # Rutas comunes
        patterns = [
            (r"/api/v\d+/envios/\d+", "/api/v1/envios/{id}"),
            (r"/api/v\d+/empresas/\d+", "/api/v1/empresas/{id}"),
            (r"/api/v\d+/usuarios/\d+", "/api/v1/usuarios/{id}"),
            (r"/admin/\w+/\w+/\d+", "/admin/{app}/{model}/{id}"),
        ]

        for pattern, replacement in patterns:
            if re.search(pattern, path):
                return replacement

        return path


# ===============================
# COLECTOR DE MÉTRICAS DE NEGOCIO
# ===============================


class BusinessMetricsCollector:
    """Colector de métricas específicas del negocio"""

    @staticmethod
    def collect_shipment_metrics():
        """Recopilar métricas de envíos"""
        try:
            from empresas.models import Empresa
            from envios.models import Envio

            # Métricas por estado
            estados = Envio.objects.values(
                "estado_actual", "empresa__codigo"
            ).annotate(count=models.Count("id"))

            for estado_data in estados:
                shipments_status_total.labels(
                    estado=estado_data["estado_actual"],
                    empresa=estado_data["empresa__codigo"] or "unknown",
                ).set(estado_data["count"])

            # Total de envíos pendientes
            pendientes = Envio.objects.filter(
                estado_actual__in=["PENDIENTE", "EN_TRANSITO"]
            ).count()

            shipments_pending_total.set(pendientes)

        except Exception as e:
            logger.error(f"Error recopilando métricas de envíos: {e}")

    @staticmethod
    def collect_user_metrics():
        """Recopilar métricas de usuarios"""
        try:
            from django.contrib.sessions.models import Session
            from django.utils import timezone

            # Sesiones activas
            active_sessions = Session.objects.filter(
                expire_date__gt=timezone.now()
            ).count()

            user_sessions_active.set(active_sessions)

        except Exception as e:
            logger.error(f"Error recopilando métricas de usuarios: {e}")

    @staticmethod
    def collect_database_metrics():
        """Recopilar métricas de base de datos"""
        try:
            # Conexiones activas
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT count(*) as active_connections
                    FROM pg_stat_activity
                    WHERE state = 'active'
                """
                )
                result = cursor.fetchone()
                if result:
                    db_connections_active.set(result[0])

        except Exception as e:
            logger.error(f"Error recopilando métricas de base de datos: {e}")

    @staticmethod
    def collect_cache_metrics():
        """Recopilar métricas de cache"""
        try:
            from django.core.cache.utils import make_key

            # Obtener estadísticas de Redis
            if hasattr(cache, "_cache") and hasattr(cache._cache, "_client"):
                client = cache._cache._client
                info = client.info()

                if "keyspace_hits" in info and "keyspace_misses" in info:
                    hits = info["keyspace_hits"]
                    misses = info["keyspace_misses"]
                    total = hits + misses

                    if total > 0:
                        hit_ratio = hits / total
                        cache_hit_ratio.set(hit_ratio)

        except Exception as e:
            logger.error(f"Error recopilando métricas de cache: {e}")


# ===============================
# DECORADORES PARA MÉTRICAS
# ===============================


def track_db_query(operation: str):
    """Decorador para trackear consultas a la base de datos"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                db_query_duration_seconds.labels(operation=operation).observe(
                    duration
                )

        return wrapper

    return decorator


def track_cache_operation(operation: str):
    """Decorador para trackear operaciones de cache"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                cache_operations_total.labels(
                    operation=operation, result="hit" if result else "miss"
                ).inc()
                return result
            except Exception as e:
                cache_operations_total.labels(
                    operation=operation, result="error"
                ).inc()
                raise

        return wrapper

    return decorator


def track_business_event(event_type: str, **labels):
    """Decorador para trackear eventos de negocio"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

                # Incrementar contador específico según el evento
                if event_type == "shipment_created":
                    empresa = labels.get("empresa", "unknown")
                    tipo = labels.get("tipo", "standard")
                    shipments_created_total.labels(
                        empresa=empresa, tipo=tipo
                    ).inc()

                elif event_type == "login_attempt":
                    result_label = "success" if result else "failed"
                    empresa = labels.get("empresa", "unknown")
                    login_attempts_total.labels(
                        result=result_label, empresa=empresa
                    ).inc()

                    if not result:
                        reason = labels.get("reason", "invalid_credentials")
                        login_attempts_failed_total.labels(reason=reason).inc()

                return result
            except Exception as e:
                if event_type == "shipment_created":
                    error_type = type(e).__name__
                    empresa = labels.get("empresa", "unknown")
                    shipments_failed_total.labels(
                        error_type=error_type, empresa=empresa
                    ).inc()
                raise

        return wrapper

    return decorator


# ===============================
# VISTA DE MÉTRICAS
# ===============================


def metrics_view(request):
    """Vista para exponer métricas de Prometheus"""
    # Recopilar métricas en tiempo real
    BusinessMetricsCollector.collect_shipment_metrics()
    BusinessMetricsCollector.collect_user_metrics()
    BusinessMetricsCollector.collect_database_metrics()
    BusinessMetricsCollector.collect_cache_metrics()

    # Generar métricas en formato Prometheus
    return ExportToDjangoView()(request)


def business_metrics_view(request):
    """Vista para métricas específicas del negocio"""
    from django.http import HttpResponse

    # Recopilar solo métricas de negocio
    BusinessMetricsCollector.collect_shipment_metrics()
    BusinessMetricsCollector.collect_user_metrics()

    # Crear registro específico para métricas de negocio
    business_registry = CollectorRegistry()

    # Registrar solo métricas de negocio
    for metric in [
        shipments_created_total,
        shipments_status_total,
        shipments_pending_total,
        shipments_failed_total,
        shipments_delivery_time,
        user_sessions_active,
        login_attempts_total,
        login_attempts_failed_total,
    ]:
        business_registry.register(metric)

    # Generar output
    output = generate_latest(business_registry)
    return HttpResponse(output, content_type=CONTENT_TYPE_LATEST)
