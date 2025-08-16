"""Wrapper legacy: importa settings_base.
Mantener para compatibilidad si DJANGO_SETTINGS_MODULE apunta a config.settings.
"""

from .settings_base import *  # noqa

CORS_ALLOW_CREDENTIALS = True
