"""🇨🇺 PACKFY CUBA - Settings base unificados
No incluye secretos ni flags de entorno. Extender en settings_development / settings_production.
"""

import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Core
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or "dev-only-insecure-key--replace"
DEBUG = False  # Override en dev
# En producción se debe definir DJANGO_SECRET_KEY. Para forzar validación, exportar ENFORCE_SECURE_SECRET=1
if os.getenv("ENFORCE_SECURE_SECRET") == "1" and SECRET_KEY.startswith(
    "dev-only-insecure-key"
):
    raise RuntimeError(
        "SECRET_KEY inseguro detectado (ENFORCE_SECURE_SECRET=1). Defina DJANGO_SECRET_KEY."
    )
ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "usuarios",
    "empresas",
    "envios",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # 🔒 SEGURIDAD AVANZADA v4.1
    "config.security_middleware.SecurityHeadersMiddleware",
    "config.security_middleware.AdvancedRateLimitMiddleware",
    "config.security_middleware.InputSanitizationMiddleware",
    "config.security_middleware.SecurityAuditMiddleware",
    # Middleware existente
    "config.middleware.RequestIDMiddleware",
    "config.metrics.RequestMetricsMiddleware",
    "config.metrics.RateLimitMiddleware",  # Mantener como backup
    "config.logging_context.LoggingContextMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "packfy"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "database"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

AUTH_USER_MODEL = "usuarios.Usuario"
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Havana"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "config.pagination.SafePageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # JWT para APIs y SessionAuthentication para compatibilidad con tests/Client
        "usuarios.auth_security.SecureJWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# CORS (estricto por defecto, abierto sólo en dev override)
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS: list[str] = []
CORS_ALLOW_CREDENTIALS = True

# Health flag
APPLICATION_NAME = "packfy-cuba"
APPLICATION_VERSION = os.getenv("APP_VERSION", "4.0")
