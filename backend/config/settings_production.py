# 🇨🇺 PACKFY CUBA - Configuración de Producción v4.0
# Configuración específica para entorno de producción

import os
from urllib.parse import urlparse

from .settings import *

# 🔧 CONFIGURACIÓN DE PRODUCCIÓN
DEBUG = False
ENVIRONMENT = "production"

# 🔒 SECURITY - Producción estricta
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY_PROD")
if not SECRET_KEY:
    raise ValueError(
        "DJANGO_SECRET_KEY_PROD debe estar definida en producción"
    )

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
if not ALLOWED_HOSTS or ALLOWED_HOSTS == [""]:
    ALLOWED_HOSTS = [
        "api.packfy.cu",
        "www.packfy.cu",
        "packfy.cu",
        "localhost",
        "127.0.0.1",
    ]

# Database para producción
if "DATABASE_URL" in os.environ:
    import dj_database_url

    DATABASES["default"] = dj_database_url.parse(os.environ["DATABASE_URL"])

# Static files para producción
STATIC_ROOT = "/app/staticfiles"
STATIC_URL = "/static/"

MEDIA_ROOT = "/app/media"
MEDIA_URL = "/media/"

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# CORS para producción
CORS_ALLOWED_ORIGINS = [
    "https://packfy.cu",
    "https://www.packfy.cu",
]

CORS_ALLOW_CREDENTIALS = True

# 📊 CACHE - Redis optimizado para producción
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "retry_on_timeout": True,
                "socket_keepalive": True,
                "socket_keepalive_options": {},
            },
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": True,  # No fallar si Redis está caído
        },
        "KEY_PREFIX": "packfy_prod",
        "TIMEOUT": 300,  # 5 minutos por defecto
    },
    # Caché secundario para sesiones
    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/2"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "packfy_sessions",
        "TIMEOUT": 3600,  # 1 hora para sesiones
    },
    # Caché para datos de larga duración
    "persistent": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/3"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "packfy_persistent",
        "TIMEOUT": 86400,  # 24 horas
    },
}

# 🔄 SESSION ENGINE - Redis para sesiones
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "sessions"
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True

# Email configuración (para notificaciones)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# Logging para producción
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/app/logs/django.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
