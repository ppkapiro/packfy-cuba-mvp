"""
🔒 PACKFY CUBA - Middleware de Seguridad Avanzada v4.1
Protección empresarial contra ataques comunes
"""

import hashlib
import logging
import time
from collections import defaultdict

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.utils.cache import add_never_cache_headers
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware que añade headers de seguridad críticos
    """

    def process_response(self, request, response):
        # Security Headers críticos
        security_headers = {
            # XSS Protection
            "X-XSS-Protection": "1; mode=block",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https:; "
                "frame-ancestors 'none';"
            ),
            # HSTS (solo si HTTPS)
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
            # Referrer Policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # Permissions Policy
            "Permissions-Policy": (
                "geolocation=(), microphone=(), camera=(), "
                "payment=(), usb=(), magnetometer=(), gyroscope=()"
            ),
        }

        for header, value in security_headers.items():
            response[header] = value

        # Remover headers que exponen información
        headers_to_remove = ["Server", "X-Powered-By", "X-AspNet-Version"]
        for header in headers_to_remove:
            if header in response:
                del response[header]

        return response


class AdvancedRateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting avanzado con diferentes límites por endpoint
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Configuración de rate limits por endpoint
        self.rate_limits = {
            # Endpoints críticos - muy restrictivos
            "/api/auth/login/": {
                "requests": 5,
                "window": 300,
            },  # 5 intentos por 5min
            "/api/auth/register/": {
                "requests": 3,
                "window": 3600,
            },  # 3 por hora
            "/api/auth/password-reset/": {"requests": 3, "window": 3600},
            # API general - moderado
            "/api/": {"requests": 100, "window": 300},  # 100 por 5min
            # Endpoints públicos - más permisivo
            "/api/envios/rastrear/": {
                "requests": 20,
                "window": 60,
            },  # 20 por minuto
            # Default
            "default": {"requests": 60, "window": 60},  # 60 por minuto
        }

    def get_client_ip(self, request):
        """Obtener IP real del cliente considerando proxies"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def get_rate_limit_config(self, path):
        """Obtener configuración de rate limit para un path"""
        for pattern, config in self.rate_limits.items():
            if pattern != "default" and path.startswith(pattern):
                return config
        return self.rate_limits["default"]

    def process_request(self, request):
        client_ip = self.get_client_ip(request)
        path = request.path

        # Configuración para este endpoint
        config = self.get_rate_limit_config(path)

        # Clave de cache única
        cache_key = f"rate_limit:{client_ip}:{path}"

        # Obtener contador actual
        current_requests = cache.get(cache_key, 0)

        if current_requests >= config["requests"]:
            logger.warning(
                f"Rate limit exceeded for IP {client_ip} on {path}. "
                f"Requests: {current_requests}/{config['requests']}"
            )

            return JsonResponse(
                {
                    "error": "Demasiadas solicitudes. Intente de nuevo más tarde.",
                    "retry_after": config["window"],
                },
                status=429,
            )

        # Incrementar contador
        cache.set(cache_key, current_requests + 1, config["window"])

        return None


class InputSanitizationMiddleware(MiddlewareMixin):
    """
    Middleware para sanitizar inputs y detectar ataques
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Patrones sospechosos
        self.suspicious_patterns = [
            # SQL Injection
            r"(\bunion\s+select\b)|(\bdrop\s+table\b)|(\binsert\s+into\b)",
            # XSS
            r"(<script[^>]*>.*?</script>)|(<iframe[^>]*>)",
            # Command Injection
            r"(\$\(.*\))|(\beval\s*\()|(\bexec\s*\()",
            # Path Traversal
            r"(\.\./)|(\.\\\.)|(\/etc\/passwd)|(\/windows\/system32)",
        ]

    def is_suspicious_input(self, data):
        """Detectar input sospechoso"""
        if not isinstance(data, str):
            return False

        data_lower = data.lower()
        for pattern in self.suspicious_patterns:
            import re

            if re.search(pattern, data_lower, re.IGNORECASE):
                return True
        return False

    def scan_data(self, data, path=""):
        """Escanear datos recursivamente"""
        if isinstance(data, dict):
            for key, value in data.items():
                if self.scan_data(value, f"{path}.{key}"):
                    return True
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if self.scan_data(item, f"{path}[{i}]"):
                    return True
        elif isinstance(data, str):
            return self.is_suspicious_input(data)

        return False

    def process_request(self, request):
        client_ip = self.get_client_ip(request)

        # Escanear datos POST/PUT
        if hasattr(request, "body") and request.body:
            try:
                import json

                if request.content_type == "application/json":
                    data = json.loads(request.body)
                    if self.scan_data(data):
                        logger.critical(
                            f"Suspicious input detected from IP {client_ip}: {request.path}"
                        )
                        return JsonResponse(
                            {"error": "Input no válido detectado"}, status=400
                        )
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        # Escanear parámetros GET
        for param, value in request.GET.items():
            if self.is_suspicious_input(value):
                logger.critical(
                    f"Suspicious GET parameter from IP {client_ip}: {param}={value}"
                )
                return JsonResponse(
                    {"error": "Parámetros no válidos"}, status=400
                )

        return None

    def get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class SecurityAuditMiddleware(MiddlewareMixin):
    """
    Middleware para auditoría de seguridad
    """

    def process_request(self, request):
        # Log de requests sensibles
        sensitive_paths = ["/api/auth/", "/api/admin/", "/admin/"]

        for path in sensitive_paths:
            if request.path.startswith(path):
                # Verificar si el usuario está disponible de forma segura
                user_info = "Anonymous"
                if hasattr(request, "user") and hasattr(
                    request.user, "username"
                ):
                    try:
                        user_info = getattr(
                            request.user, "username", "Anonymous"
                        )
                    except AttributeError:
                        user_info = "Anonymous"

                logger.info(
                    f"Sensitive endpoint access: {request.path} "
                    f"from {self.get_client_ip(request)} "
                    f"User: {user_info}"
                )
                break

        return None

    def get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
