from django.db import migrations

CREATE_INDEX_SQL = (
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_envio_estado_stats_estado "
    "ON envio_estado_stats(estado_actual);"
)
DROP_INDEX_SQL = "DROP INDEX IF EXISTS idx_envio_estado_stats_estado;"


def create_index(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        with schema_editor.connection.cursor() as cursor:
            cursor.execute(CREATE_INDEX_SQL)


def drop_index(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        with schema_editor.connection.cursor() as cursor:
            cursor.execute(DROP_INDEX_SQL)


class Migration(migrations.Migration):
    dependencies = [
        ("envios", "0003_envio_stats_matview"),
    ]

    operations = [
        migrations.RunPython(create_index, reverse_code=drop_index),
    ]
