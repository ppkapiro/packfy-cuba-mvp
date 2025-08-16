from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("envios", "0005_alter_envio_peso"),
        ("usuarios", "0003_usuario_empresa"),
        ("empresas", "0002_add_codigo_activa"),
    ]

    operations = [
        migrations.AddField(
            model_name="envio",
            name="usuario",
            field=models.ForeignKey(
                to="usuarios.usuario",
                on_delete=models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name="envios",
            ),
        ),
        migrations.AddField(
            model_name="envio",
            name="empresa",
            field=models.ForeignKey(
                to="empresas.empresa",
                on_delete=models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name="envios",
            ),
        ),
    ]
