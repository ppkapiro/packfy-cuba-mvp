"""
Configuración Django para VS Code Pylance
Este archivo ayuda a VS Code a entender la estructura de Django
"""

import os

import django

# Configurar Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Importar modelos para que Pylance los reconozca
try:
    from empresas.models import Empresa  # noqa: F401
    from envios.models import Envio, HistorialEstado  # noqa: F401
    from usuarios.models import Usuario  # noqa: F401
except ImportError:
    pass
