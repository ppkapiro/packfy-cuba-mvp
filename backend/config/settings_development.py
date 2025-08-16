# 🇨🇺 PACKFY CUBA - Configuración de Desarrollo v4.0
# Configuración específica para entorno de desarrollo

import os

from . import settings_base as base

# Re-exportar símbolos necesarios para Django (mantener nombres)
from .settings_base import *  # noqa

# 🔧 CONFIGURACIÓN DE DESARROLLO
DEBUG = True
ENVIRONMENT = "development"

# 🔒 SECURITY - Desarrollo
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "django-insecure-dev-key-v4-glassmorphism"
)

# 📱 ALLOWED_HOSTS - Móvil + PC
allowed_hosts_env = os.getenv(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0,backend"
)
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(",")]

# 🌐 CORS - Desarrollo permisivo + Móvil
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CORS origins desde variables de entorno
cors_origins_env = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,https://localhost:5173,http://127.0.0.1:5173,https://127.0.0.1:5173",
)
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in cors_origins_env.split(",")
]

# 📧 EMAIL - Mock para desarrollo
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# 🔧 LOGGING - Desarrollo detallado
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "development.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "packfy": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# 🚀 PERFORMANCE - Desarrollo sin optimizaciones
USE_TZ = True
USE_I18N = True
USE_L10N = True

# 📊 DEBUG TOOLBAR para desarrollo
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "usuarios.security_middleware.SecurityHeadersMiddleware",
        "usuarios.security_middleware.RateLimitMiddleware",
        "usuarios.security_middleware.RequestLoggingMiddleware",
        *MIDDLEWARE,  # base list
        "usuarios.security_middleware.SecurityMonitoringMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

# 🔧 CONFIGURACIONES ESPECÍFICAS DE DESARROLLO
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
