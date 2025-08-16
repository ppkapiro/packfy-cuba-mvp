# 🇨🇺 PACKFY CUBA - Configuración de Testing v4.0
# Configuración específica para entorno de testing

import os
import tempfile

from .settings import *

# 🔧 CONFIGURACIÓN DE TESTING
DEBUG = False  # Testing debe simular producción
ENVIRONMENT = "testing"

# 🔒 SECURITY - Testing con datos seguros
SECRET_KEY = "django-testing-key-v4-secure-but-not-production"
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

# 🗄️ BASE DE DATOS - SQLite en archivo (persistente entre procesos para E2E)
_TEST_DB_PATH = os.path.join(BASE_DIR, "test_e2e.sqlite3")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": _TEST_DB_PATH,
        "OPTIONS": {
            "timeout": 60,
            # Mejorar concurrencia en SQLite
            "init_command": "PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA busy_timeout=60000;",
        },
        "TEST": {
            "NAME": _TEST_DB_PATH,
        },
    }
}

# 📊 CACHE - Dummy cache para testing
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "sessions": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "persistent": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}

# 📧 EMAIL - Testing backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# 🔄 SESSIONS - Testing
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# 🌐 CORS - Permisivo para testing
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# 📁 MEDIA Y STATIC - Temporal
MEDIA_ROOT = tempfile.mkdtemp()
STATIC_ROOT = tempfile.mkdtemp()

# 🔒 PASSWORD VALIDATORS - Simplificados para testing
AUTH_PASSWORD_VALIDATORS = []

# 🚀 PERFORMANCE - Optimizado para testing
USE_TZ = True
USE_I18N = False  # Deshabilitado para velocidad
USE_L10N = False

# 🔧 LOGGING - Mínimo para testing
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "packfy": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# 🧪 CONFIGURACIONES ESPECÍFICAS DE TESTING
TEST_RUNNER = "django.test.runner.DiscoverRunner"


# Deshabilitar migraciones para velocidad
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


if "test" in sys.argv or "pytest" in sys.modules:
    MIGRATION_MODULES = DisableMigrations()

# 📊 JWT - Configuración para testing
SIMPLE_JWT.update(
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(
            minutes=5
        ),  # Más corto para testing
        "REFRESH_TOKEN_LIFETIME": timedelta(minutes=10),
        "ROTATE_REFRESH_TOKENS": False,  # Simplificar para tests
    }
)

# 🔧 MIDDLEWARE - Mínimo para testing
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# 🚫 Deshabilitar throttling en tests
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {}

# 📱 PWA - Deshabilitar para testing
PWA_SERVICE_WORKER_PATH = None
