# 🇨🇺 PACKFY CUBA - Middleware de Seguridad Avanzado v4.0

import hashlib
import json
import logging
import secrets
import time

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("packfy.security")


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para agregar headers de seguridad esenciales
    """

    def process_response(self, request, response):
        """Agregar headers de seguridad a todas las respuestas"""

        # Content Security Policy
        if not settings.DEBUG:
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: blob: https:; "
                "connect-src 'self' https://api.packfy.cu; "
                "frame-ancestors 'none';"
            )
            response["Content-Security-Policy"] = csp

        # Otros headers de seguridad
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        # Para APIs
        if request.path.startswith("/api/"):
            response["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response["Pragma"] = "no-cache"

        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware de rate limiting avanzado
    """

    # Configuraciones de rate limiting
    RATE_LIMITS = {
        "default": {"requests": 100, "window": 3600},  # 100 req/hora
        "auth": {"requests": 10, "window": 900},  # 10 req/15min
        "api": {"requests": 1000, "window": 3600},  # 1000 req/hora
        "upload": {"requests": 20, "window": 3600},  # 20 uploads/hora
    }

    def process_request(self, request):
        """Verificar rate limits antes de procesar la request"""

        # Determinar tipo de endpoint
        endpoint_type = self._get_endpoint_type(request)

        # Obtener configuración de rate limit
        limit_config = self.RATE_LIMITS.get(
            endpoint_type, self.RATE_LIMITS["default"]
        )

        # Verificar rate limit
        if not self._check_rate_limit(request, endpoint_type, limit_config):
            logger.warning(
                f"Rate limit exceeded for {self._get_client_ip(request)} "
                f"on endpoint type: {endpoint_type}"
            )
            return JsonResponse(
                {
                    "error": "Rate limit exceeded",
                    "detail": f"Too many requests. Try again later.",
                    "retry_after": limit_config["window"],
                },
                status=429,
            )

        return None

    def _get_endpoint_type(self, request):
        """Determinar el tipo de endpoint para aplicar rate limit específico"""
        path = request.path.lower()

        if any(
            auth_path in path for auth_path in ["/login", "/token", "/refresh"]
        ):
            return "auth"
        elif path.startswith("/api/"):
            return "api"
        elif "upload" in path or request.method == "POST":
            return "upload"
        else:
            return "default"

    def _check_rate_limit(self, request, endpoint_type, config):
        """Verificar si la request está dentro del rate limit"""
        ip = self._get_client_ip(request)
        # Verificar si el usuario está autenticado de forma segura
        user_id = "anonymous"
        if (
            hasattr(request, "user")
            and hasattr(request.user, "id")
            and request.user.is_authenticated
        ):
            user_id = getattr(request.user, "id", "anonymous")

        # Crear clave única por IP y usuario
        cache_key = f"rate_limit:{endpoint_type}:{ip}:{user_id}"

        # Obtener contador actual
        current_count = cache.get(cache_key, 0)

        # Verificar límite
        if current_count >= config["requests"]:
            return False

        # Incrementar contador
        cache.set(cache_key, current_count + 1, config["window"])

        return True

    def _get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return ip


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware para logging detallado de requests
    """

    # Rutas sensibles que requieren logging especial
    SENSITIVE_PATHS = ["/api/auth/", "/admin/", "/api/envios/"]

    def process_request(self, request):
        """Logging de request entrante"""
        request._start_time = time.time()

        # Log detallado para rutas sensibles
        if any(path in request.path for path in self.SENSITIVE_PATHS):
            self._log_sensitive_request(request)

    def process_response(self, request, response):
        """Logging de response"""

        # Calcular tiempo de procesamiento
        if hasattr(request, "_start_time"):
            duration = time.time() - request._start_time
            response["X-Processing-Time"] = f"{duration:.3f}s"

            # Log de performance si es lento
            if duration > 2.0:  # Más de 2 segundos
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {duration:.3f}s"
                )

        # Log de errores
        if response.status_code >= 400:
            self._log_error_response(request, response)

        return response

    def _log_sensitive_request(self, request):
        """Log detallado para requests sensibles"""
        log_data = {
            "timestamp": time.time(),
            "method": request.method,
            "path": request.path,
            "ip": self._get_client_ip(request),
            "user_agent": request.META.get("HTTP_USER_AGENT", "")[:200],
            "user": (
                str(request.user) if hasattr(request, "user") else "Anonymous"
            ),
            "content_type": request.META.get("CONTENT_TYPE", ""),
        }

        logger.info(f"Sensitive request: {json.dumps(log_data)}")

    def _log_error_response(self, request, response):
        """Log de respuestas de error"""
        log_data = {
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "ip": self._get_client_ip(request),
            "user": (
                str(request.user) if hasattr(request, "user") else "Anonymous"
            ),
        }

        logger.warning(f"Error response: {json.dumps(log_data)}")

    def _get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return ip


class CSRFSecurityMiddleware(MiddlewareMixin):
    """
    Middleware adicional de protección CSRF
    """

    def process_request(self, request):
        """Verificaciones adicionales de CSRF"""

        # Para APIs REST, verificar headers adicionales
        if request.path.startswith("/api/") and request.method in [
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ]:

            # Verificar X-Requested-With para AJAX
            if not request.META.get("HTTP_X_REQUESTED_WITH"):
                # En producción, esto sería más estricto
                if settings.ENVIRONMENT == "production":
                    logger.warning(
                        "API request without X-Requested-With header"
                    )

            # Verificar Content-Type para JSON APIs
            content_type = request.META.get("CONTENT_TYPE", "")
            if (
                "application/json" not in content_type
                and request.method != "GET"
            ):
                logger.info(f"Non-JSON API request: {content_type}")

        return None


class SecurityMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware para detectar patrones de ataque
    """

    # Patrones sospechosos en URLs
    SUSPICIOUS_PATTERNS = [
        "wp-admin",
        "phpmyadmin",
        ".env",
        "config.php",
        "sql",
        "admin.php",
        "wp-login",
        "shell",
        "../",
        "..\\",
        "passwd",
        "etc/passwd",
    ]

    def process_request(self, request):
        """Detectar patrones de ataque"""

        path = request.path.lower()
        query = request.META.get("QUERY_STRING", "").lower()

        # Detectar patrones sospechosos
        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern in path or pattern in query:
                self._log_suspicious_activity(request, pattern)

                # En producción, podríamos bloquear
                if settings.ENVIRONMENT == "production":
                    return JsonResponse(
                        {
                            "error": "Forbidden",
                            "detail": "Suspicious activity detected",
                        },
                        status=403,
                    )

        return None

    def _log_suspicious_activity(self, request, pattern):
        """Log de actividad sospechosa"""
        log_data = {
            "timestamp": time.time(),
            "ip": self._get_client_ip(request),
            "path": request.path,
            "pattern": pattern,
            "user_agent": request.META.get("HTTP_USER_AGENT", "")[:200],
            "method": request.method,
        }

        logger.error(f"Suspicious activity detected: {json.dumps(log_data)}")

    def _get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return ip
