# Generated manually for multi-tenant support

import django.db.models.deletion
from django.db import migrations, models


def create_default_empresas(apps, schema_editor):
    """Crear empresas por defecto antes de agregar el campo"""
    Empresa = apps.get_model("empresas", "Empresa")

    empresas_default = [
        {
            "id": 1,
            "nombre": "Packfy Express Cuba",
            "slug": "packfy-express",
            "activo": True,
        },
        {
            "id": 2,
            "nombre": "Miami Shipping Co",
            "slug": "miami-shipping",
            "activo": True,
        },
        {
            "id": 3,
            "nombre": "Habana Logistics",
            "slug": "habana-logistics",
            "activo": True,
        },
    ]

    for empresa_data in empresas_default:
        # Intentar crear, si ya existe con ese slug, actualizar
        try:
            empresa, created = Empresa.objects.get_or_create(
                slug=empresa_data["slug"], defaults=empresa_data
            )
            if not created:
                # Si ya existe, asegurarse de que tenga el ID correcto
                if empresa.id != empresa_data["id"]:
                    # Si existe con diferente ID, crear uno nuevo sin slug único
                    empresa_data_no_slug = empresa_data.copy()
                    empresa_data_no_slug["slug"] = (
                        f"{empresa_data['slug']}-{empresa_data['id']}"
                    )
                    Empresa.objects.update_or_create(
                        id=empresa_data["id"], defaults=empresa_data_no_slug
                    )
        except Exception:
            # Si hay cualquier error, crear por ID
            Empresa.objects.update_or_create(
                id=empresa_data["id"],
                defaults={
                    "nombre": empresa_data["nombre"],
                    "slug": f"{empresa_data['slug']}-{empresa_data['id']}",
                    "activo": empresa_data["activo"],
                },
            )


def reverse_create_empresas(apps, schema_editor):
    """Reversar la creación de empresas"""
    pass  # No necesitamos hacer nada al reversar


class Migration(migrations.Migration):

    dependencies = [
        ("empresas", "0003_fix_usuario_relation"),
        ("envios", "0002_initial"),
    ]

    operations = [
        # Primero crear las empresas por defecto
        migrations.RunPython(create_default_empresas, reverse_create_empresas),
        # Luego agregar el campo con el valor por defecto
        migrations.AddField(
            model_name="envio",
            name="empresa",
            field=models.ForeignKey(
                help_text="Empresa propietaria del envío",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="envios",
                to="empresas.empresa",
                default=1,  # Empresa por defecto
            ),
        ),
    ]
