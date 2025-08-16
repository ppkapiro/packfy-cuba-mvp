from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0002_alter_usuario_managers"),
        ("empresas", "0002_add_codigo_activa"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="empresa",
            field=models.ForeignKey(
                to="empresas.empresa",
                on_delete=models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name="usuarios",
            ),
        )
    ]
