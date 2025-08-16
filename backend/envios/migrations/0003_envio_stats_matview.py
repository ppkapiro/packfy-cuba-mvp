from django.db import migrations

MATVIEW_SQL = """
CREATE MATERIALIZED VIEW IF NOT EXISTS envio_estado_stats AS
SELECT estado_actual, count(*)::bigint AS total
FROM envios_envio
GROUP BY estado_actual;
"""
REFRESH_SQL = "REFRESH MATERIALIZED VIEW CONCURRENTLY envio_estado_stats;"
DROP_SQL = "DROP MATERIALIZED VIEW IF EXISTS envio_estado_stats;"


def create_matview(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        with schema_editor.connection.cursor() as cursor:
            cursor.execute(MATVIEW_SQL)


def drop_matview(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        with schema_editor.connection.cursor() as cursor:
            cursor.execute(DROP_SQL)


class Migration(migrations.Migration):
    dependencies = [
        ("envios", "0002_envio_indexes_uuidguide"),
        ("envios", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(create_matview, reverse_code=drop_matview),
    ]
