from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("envios", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="envio",
            name="numero_guia",
            field=models.CharField(max_length=20, unique=True, db_index=True),
        ),
        migrations.AddIndex(
            model_name="envio",
            index=models.Index(
                fields=["estado_actual", "fecha_creacion"],
                name="envio_estado_fecha_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="envio",
            index=models.Index(
                fields=["remitente_nombre"], name="envio_remitente_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="envio",
            index=models.Index(
                fields=["destinatario_nombre"], name="envio_destinatario_idx"
            ),
        ),
    ]
