from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("empresas", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="empresa",
            name="codigo",
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
        migrations.AddField(
            model_name="empresa",
            name="activa",
            field=models.BooleanField(default=True),
        ),
    ]
