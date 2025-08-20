from empresas.models import PerfilUsuario
from empresas.permissions import TenantPermission
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Usuario
from .permissions import EsAdministrador, EsCreadorOAdministrador
from .serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para usuarios.
    """

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        """
        Personalización de permisos multi-tenant:
        - Requiere permisos de empresa para todas las acciones
        - El endpoint 'me' solo requiere autenticación
        """
        if self.action == "me":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [TenantPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filtra los usuarios por empresa actual (multi-tenant):
        - Solo muestra usuarios que pertenecen a la empresa del contexto
        """
        # Si no hay empresa en el contexto, devolver queryset vacío
        if not hasattr(self.request, "tenant") or not self.request.tenant:
            return Usuario.objects.none()

        # Obtener usuarios que tienen perfil en la empresa actual
        usuarios_empresa = PerfilUsuario.objects.filter(
            empresa=self.request.tenant, activo=True
        ).values_list("usuario_id", flat=True)

        return Usuario.objects.filter(id__in=usuarios_empresa)

    @action(detail=False, methods=["get"])
    def me(self, request):
        """
        Endpoint para obtener el perfil del usuario autenticado
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
