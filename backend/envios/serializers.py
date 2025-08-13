import re

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from usuarios.serializers import UsuarioSerializer

from .models import Envio, HistorialEstado


class HistorialEstadoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo HistorialEstado
    """

    registrado_por = UsuarioSerializer(read_only=True)

    class Meta:
        model = HistorialEstado
        fields = [
            "id",
            "envio",
            "estado",
            "comentario",
            "ubicacion",
            "fecha",
            "registrado_por",
        ]
        read_only_fields = ["id", "fecha"]


class EnvioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Envio
    """

    historial = HistorialEstadoSerializer(many=True, read_only=True)
    creado_por = UsuarioSerializer(read_only=True)
    actualizado_por = UsuarioSerializer(read_only=True)
    estado_display = serializers.SerializerMethodField()

    def get_estado_display(self, obj):
        return obj.get_estado_actual_display()

    class Meta:
        model = Envio
        fields = [
            "id",
            "numero_guia",
            "estado_actual",
            "estado_display",
            "fecha_creacion",
            "fecha_estimada_entrega",
            "descripcion",
            "peso",
            "valor_declarado",
            "remitente_nombre",
            "remitente_direccion",
            "remitente_telefono",
            "remitente_email",
            "destinatario_nombre",
            "destinatario_direccion",
            "destinatario_telefono",
            "destinatario_email",
            "notas",
            "creado_por",
            "actualizado_por",
            "ultima_actualizacion",
            "historial",
        ]
        read_only_fields = [
            "id",
            "numero_guia",
            "fecha_creacion",
            "ultima_actualizacion",
            "creado_por",
            "actualizado_por",
            "historial",
        ]

    def validate_remitente_telefono(self, value):
        if not re.match(r"^\+?[0-9]{7,15}$", value):
            raise serializers.ValidationError(
                "El teléfono debe tener entre 7 y 15 dígitos, opcionalmente con prefijo '+'"
            )
        return value

    def validate_destinatario_telefono(self, value):
        if not re.match(r"^\+?[0-9]{7,15}$", value):
            raise serializers.ValidationError(
                "El teléfono debe tener entre 7 y 15 dígitos, opcionalmente con prefijo '+'"
            )
        return value

    def validate_remitente_email(self, value):
        if value:
            try:
                validate_email(value)
            except DjangoValidationError:
                raise serializers.ValidationError(
                    "El email del remitente no es válido"
                )
        return value

    def validate_peso(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El peso debe ser mayor que cero"
            )
        if value > 1000:  # Establecer un límite superior razonable (1000 kg)
            raise serializers.ValidationError(
                "El peso no puede exceder 1000 kg"
            )
        return value

    def validate_valor_declarado(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "El valor declarado no puede ser negativo"
            )
        return value

    def validate(self, data):
        """Validación a nivel de objeto para verificar datos consistentes"""
        if "fecha_estimada_entrega" in data and "fecha_creacion" in data:
            if data["fecha_estimada_entrega"] < data["fecha_creacion"]:
                raise serializers.ValidationError(
                    {
                        "fecha_estimada_entrega": "La fecha estimada de entrega no puede ser anterior a la fecha de creación"
                    }
                )
        return data
        #
        # def validate_valor_declarado(self, value):
        if value and value < 0:
            raise serializers.ValidationError(
                "El valor declarado no puede ser negativo"
            )
        return value


class CambioEstadoSerializer(serializers.Serializer):
    """
    Serializer para cambiar el estado de un envío y registrarlo en el historial
    """

    estado = serializers.ChoiceField(choices=Envio.EstadoChoices.choices)
    comentario = serializers.CharField(required=False, allow_blank=True)
    ubicacion = serializers.CharField(required=False, allow_blank=True)
