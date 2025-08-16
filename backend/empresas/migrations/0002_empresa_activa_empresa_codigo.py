"""
No-op migration to linearize duplicate 0002 migrations.
This migration depends on 0002_add_codigo_activa and performs no operations.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("empresas", "0002_add_codigo_activa"),
    ]

    operations = []
