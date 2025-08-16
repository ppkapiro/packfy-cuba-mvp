"""Middleware y utilidades de métricas y rate limiting.

Incluye:
 - RequestMetricsMiddleware: mide latencia y expone contadores Prometheus.
 - RateLimitMiddleware: limitación básica por IP+path (Redis si disponible; fallback memoria).
"""

import os
import threading
import time
from collections import defaultdict, deque
from typing import Deque, Tuple

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

try:
    from prometheus_client import Counter, Histogram
except ImportError:  # pragma: no cover
    Counter = None  # type: ignore
    Histogram = None  # type: ignore

REQUEST_COUNT = (
    Counter(
        "packfy_request_total",
        "Total peticiones",
        ["method", "path", "status"],
    )
    if Counter
    else None
)
REQUEST_LATENCY = (
    Histogram(
        "packfy_request_latency_seconds",
        "Latencia requests",
        ["method", "path"],
        buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5),
    )
    if Histogram
    else None
)

# Contadores adicionales
AUTH_FAILURES = (
    Counter(
        "packfy_auth_failure_total",
        "Fallos de autenticación (401/403)",
        ["path"],
    )
    if Counter
    else None
)
REQUEST_STATUS_CLASS = (
    Counter(
        "packfy_request_status_class_total",
        "Peticiones por clase de estado (2xx/3xx/4xx/5xx)",
        ["method", "path", "class"],
    )
    if Counter
    else None
)
RATE_LIMIT_REJECTS = (
    Counter(
        "packfy_rate_limit_reject_total",
        "Peticiones rechazadas por rate limit",
        ["path"],
    )
    if Counter
    else None
)


class RequestMetricsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request._metrics_start = time.perf_counter()  # type: ignore[attr-defined]

    def process_response(self, request, response):
        start = getattr(request, "_metrics_start", None)
        if start and REQUEST_LATENCY:
            elapsed = time.perf_counter() - start
            path = request.path.split("?")[0]
            REQUEST_LATENCY.labels(request.method, path).observe(elapsed)
            if REQUEST_COUNT:
                REQUEST_COUNT.labels(
                    request.method, path, response.status_code
                ).inc()
            # Clase de estado 2xx/3xx/4xx/5xx
            if REQUEST_STATUS_CLASS:
                try:
                    status_class = f"{int(response.status_code) // 100}xx"
                except Exception:  # pragma: no cover (defensivo)
                    status_class = "naxx"
                REQUEST_STATUS_CLASS.labels(
                    request.method, path, status_class
                ).inc()
            # Fallos de autenticación
            if AUTH_FAILURES and int(getattr(response, "status_code", 0)) in (
                401,
                403,
            ):
                AUTH_FAILURES.labels(path).inc()
        return response


class RateLimitBackend:
    def __init__(self):
        # Valores por defecto; se recalculan por verificación desde entorno
        self.window = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
        self.max_requests = int(os.getenv("RATE_LIMIT_MAX", "100"))
        self._lock = threading.Lock()
        self._buckets = defaultdict(deque)
        self._use_redis = False
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            try:  # pragma: no cover - best effort
                import redis

                self._redis = redis.from_url(redis_url)
                self._use_redis = True
            except Exception:  # noqa
                self._use_redis = False

    def check(self, key: str) -> Tuple[bool, int]:
        # Leer límites actuales desde el entorno en cada verificación (útil en tests)
        try:
            window = int(os.getenv("RATE_LIMIT_WINDOW", str(self.window)))
        except Exception:
            window = self.window
        try:
            max_requests = int(
                os.getenv("RATE_LIMIT_MAX", str(self.max_requests))
            )
        except Exception:
            max_requests = self.max_requests

        now = time.time()
        if self._use_redis:
            pipe = self._redis.pipeline()  # type: ignore[attr-defined]
            window_key = f"rl:{key}"
            pipe.zremrangebyscore(window_key, 0, now - window)
            pipe.zadd(window_key, {str(now): now})
            pipe.zcard(window_key)
            pipe.expire(window_key, window)
            _, _, count, _ = pipe.execute()
            remaining = max_requests - count
            return (count <= max_requests, remaining)
        # In-memory
        with self._lock:
            dq = self._buckets[key]
            # Purge timestamps fuera de ventana
            while dq and dq[0] < now - window:
                dq.popleft()
            dq.append(now)
            remaining = max_requests - len(dq)
            return (len(dq) <= max_requests, remaining)


rate_backend = RateLimitBackend()


class RateLimitMiddleware(MiddlewareMixin):
    SAFE_PATH_PREFIXES = (
        "/api/envios/rastrear",
        "/api/envios/buscar_por_remitente",
        "/api/envios/buscar_por_destinatario",
        "/api/health",
    )

    def process_request(self, request):
        path = request.path
        if not any(path.startswith(p) for p in self.SAFE_PATH_PREFIXES):
            return None
        ip = request.META.get("REMOTE_ADDR", "unknown")
        key = f"{ip}:{path.split('?')[0]}"
        allowed, remaining = rate_backend.check(key)
        if not allowed:
            if RATE_LIMIT_REJECTS:
                RATE_LIMIT_REJECTS.labels(path.split("?")[0]).inc()
            return JsonResponse(
                {
                    "detail": "Rate limit excedido",
                    "retry_after": int(os.getenv("RATE_LIMIT_WINDOW", "60")),
                },
                status=429,
            )
        request.rate_remaining = remaining  # type: ignore[attr-defined]
        return None
