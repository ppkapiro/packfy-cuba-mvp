from rest_framework import serializers

from .models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Empresa
    """

    class Meta:
        model = Empresa
        fields = [
            "id",
            "slug",
            "nombre",
            "ruc",
            "direccion",
            "telefono",
            "email",
            "logo",
            "activo",
            "dominio",
            "fecha_creacion",
            "ultima_actualizacion",
        ]
        read_only_fields = [
            "id",
            "slug",
            "fecha_creacion",
            "ultima_actualizacion",
        ]
