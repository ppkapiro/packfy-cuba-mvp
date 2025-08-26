import logging

from django.contrib.auth import authenticate
from empresas.models import Empresa, PerfilUsuario
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from usuarios.models import Usuario

logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Obtener el tenant del header
        request = self.context.get("request")
        tenant_slug = request.META.get("HTTP_X_TENANT_SLUG", "packfy-express")

        logger.info(
            f"Login attempt - Email: {attrs.get('email')}, Tenant: {tenant_slug}"
        )

        # Validar que el tenant existe
        try:
            empresa = Empresa.objects.get(slug=tenant_slug, activo=True)
            logger.info(f"Empresa found: {empresa.nombre}")
        except Empresa.DoesNotExist:
            logger.error(f"Empresa not found for slug: {tenant_slug}")
            raise serializers.ValidationError("Tenant no válido")

        # Usar el email como username para autenticación
        username = attrs.get("email")
        password = attrs.get("password")

        # Autenticar usuario
        user = authenticate(username=username, password=password)
        if not user:
            logger.error(f"Authentication failed for user: {username}")
            raise serializers.ValidationError("Credenciales inválidas")

        logger.info(f"User authenticated: {user.email}")

        # Verificar que el usuario tiene acceso a esta empresa
        perfil = PerfilUsuario.objects.filter(
            usuario=user, empresa=empresa, activo=True
        ).first()

        if not perfil and not user.is_superuser:
            logger.error(f"User {user.email} has no access to empresa {empresa.nombre}")
            raise serializers.ValidationError("No tiene acceso a esta empresa")

        # Generar tokens
        data = super().validate(attrs)

        # Agregar información adicional
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "empresa_actual": {
                "id": empresa.id,
                "nombre": empresa.nombre,
                "slug": empresa.slug,
            },
        }

        if perfil:
            data["user"]["rol"] = perfil.rol

        logger.info(f"Login successful for {user.email} in {empresa.nombre}")
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        logger.info(f"Login request received from {request.META.get('REMOTE_ADDR')}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Body: {request.data}")

        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f"Login response: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HealthCheckView(APIView):
    """Vista simple para verificar que el API está funcionando"""

    def get(self, request):
        return Response(
            {
                "status": "OK",
                "message": "API funcionando correctamente",
                "tenant_slug": request.META.get("HTTP_X_TENANT_SLUG", "none"),
                "timestamp": request.META.get("HTTP_DATE", "none"),
            }
        )
