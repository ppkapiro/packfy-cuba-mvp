"""
No-op migration to linearize duplicate 0005 migrations.
This migration depends on 0005_envio_peso_optional and performs no operations.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("envios", "0005_envio_peso_optional"),
    ]

    run_before = [
        ("envios", "0006_envio_usuario_empresa"),
    ]

    operations = []
