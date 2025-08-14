# 🇨🇺 PACKFY CUBA - Configuración de Staging v4.0
# Configuración específica para entorno de staging/testing

import os

from .settings import *

# 🔧 CONFIGURACIÓN DE STAGING
DEBUG = False  # Producción simulada
ENVIRONMENT = "staging"

# 🔒 SECURITY - Staging semi-estricto
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY_STAGING", "django-staging-key-v4-secure"
)
ALLOWED_HOSTS = ["staging.packfy.cu", "test.packfy.cu", "localhost"]

# 🌐 CORS - Staging controlado
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://staging.packfy.cu",
    "https://test.packfy.cu",
    "http://localhost:5173",
    "https://localhost:5173",
]

# 🔒 CONFIGURACIONES DE SEGURIDAD MEDIAS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 3600  # 1 hora para staging
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"

# 🍪 COOKIES SEMI-SEGURAS
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

# 📧 EMAIL - Mock mejorado para staging
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "logs" / "emails"

# 🔧 LOGGING - Staging detallado
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
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "staging.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 3,
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

# 🚀 PERFORMANCE - Staging balanceado
USE_TZ = True
USE_I18N = True
USE_L10N = True

# 📊 CACHE - Simple para staging
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "packfy-staging-cache",
        "TIMEOUT": 300,
        "OPTIONS": {
            "MAX_ENTRIES": 1000,
        },
    }
}

# 📁 STATIC FILES - Staging
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# 🔧 ADMINISTRACIÓN HABILITADA EN STAGING
ADMIN_ENABLED = True
