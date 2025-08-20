from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para obtener tokens JWT usando email en lugar de username.
    """

    username_field = "email"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo ya está configurado como email por el username_field
        # No necesitamos hacer pop de username

    def validate(self, attrs):
        """
        Validar las credenciales usando email en lugar de username.
        """
        # TokenObtainPairSerializer ya maneja la validación
        # Solo necesitamos asegurar que funcione con nuestro USERNAME_FIELD
        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT usando email.
    """

    serializer_class = CustomTokenObtainPairSerializer
