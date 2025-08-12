"""
Configuración Django para VS Code Pylance
Este archivo ayuda a VS Code a entender la estructura de Django
"""

import os

import django
from django.conf import settings

# Configurar Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import AbstractUser

# Esto permite que Pylance entienda los modelos Django
from django.db import models
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Importar modelos para que Pylance los reconozca
try:
    from empresas.models import Empresa
    from envios.models import Envio, HistorialEstado
    from usuarios.models import Usuario
except ImportError:
    pass
