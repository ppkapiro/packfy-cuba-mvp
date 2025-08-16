import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_test")
import django

django.setup()
from envios.models import Envio
from usuarios.models import Usuario

print("Envio fields:", [f.name for f in Envio._meta.get_fields()])
print("Usuario fields:", [f.name for f in Usuario._meta.get_fields()])
