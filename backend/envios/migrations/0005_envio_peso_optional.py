from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("envios", "0004_envio_stats_matview_index"),
    ]

    operations = [
        migrations.AlterField(
            model_name="envio",
            name="peso",
            field=models.DecimalField(
                max_digits=6,
                decimal_places=2,
                help_text="Peso en kg",
                null=True,
                blank=True,
            ),
        ),
    ]
