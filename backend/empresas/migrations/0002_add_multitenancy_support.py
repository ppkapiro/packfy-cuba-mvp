# Generated manually for multitenancy support

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("empresas", "0001_initial"),
    ]

    operations = [
        # Actualizar modelo Empresa para multitenancy
        migrations.AlterModelOptions(
            name="empresa",
            options={
                "verbose_name": "Empresa",
                "verbose_name_plural": "Empresas",
                "ordering": ["nombre"],
            },
        ),
        migrations.RemoveField(
            model_name="empresa",
            name="id",
        ),
        migrations.AddField(
            model_name="empresa",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AddField(
            model_name="empresa",
            name="slug",
            field=models.SlugField(
                max_length=100,
                unique=True,
                help_text="Identificador único para URLs",
            ),
        ),
        migrations.AddField(
            model_name="empresa",
            name="configuracion",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="Configuraciones específicas de la empresa",
            ),
        ),
        migrations.AlterField(
            model_name="empresa",
            name="activo",
            field=models.BooleanField(
                default=True, help_text="Empresa activa en el sistema"
            ),
        ),
        migrations.AlterField(
            model_name="empresa",
            name="dominio",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                help_text="Dominio personalizado (futuro)",
            ),
        ),
        # Crear modelo PerfilUsuario
        migrations.CreateModel(
            name="PerfilUsuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rol",
                    models.CharField(
                        choices=[
                            ("dueno", "Dueño"),
                            ("operador_miami", "Operador Miami"),
                            ("operador_cuba", "Operador Cuba"),
                            ("remitente", "Remitente"),
                            ("destinatario", "Destinatario"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "activo",
                    models.BooleanField(
                        default=True, help_text="Usuario activo en la empresa"
                    ),
                ),
                (
                    "telefono",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("direccion", models.TextField(blank=True, null=True)),
                ("fecha_vinculacion", models.DateTimeField(auto_now_add=True)),
                ("ultima_actividad", models.DateTimeField(auto_now=True)),
                (
                    "empresa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usuarios",
                        to="empresas.empresa",
                    ),
                ),
                (
                    "usuario",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="perfil",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Perfil de Usuario",
                "verbose_name_plural": "Perfiles de Usuarios",
                "ordering": ["empresa__nombre", "rol", "usuario__first_name"],
            },
        ),
        migrations.AlterUniqueTogether(
            name="perfilusuario",
            unique_together={("usuario", "empresa")},
        ),
    ]
