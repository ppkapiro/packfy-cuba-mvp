from .settings_base import *  # noqa

# Configuración específica para tests (rápidos y aislados)
DEBUG = False
SECRET_KEY = "test-secret-key-not-for-prod"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        # Usar archivo para permitir concurrencia entre hilos y aumentar timeout
        "NAME": os.path.join(BASE_DIR, "test.sqlite3"),
        "OPTIONS": {
            "timeout": 60,
            # Mejorar concurrencia en SQLite
            "init_command": "PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA busy_timeout=60000;",
        },
        "TEST": {"NAME": os.path.join(BASE_DIR, "test.sqlite3")},
    }
}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
}
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [  # type: ignore # noqa
    "usuarios.auth_security.SecureJWTAuthentication",
    "rest_framework.authentication.SessionAuthentication",
    "rest_framework.authentication.BasicAuthentication",
]
