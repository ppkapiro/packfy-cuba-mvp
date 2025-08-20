from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Empresa, PerfilUsuario
from .permissions import TenantPermission, require_rol
from .serializers import EmpresaSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para empresas con soporte multi-tenant.
    """

    queryset = (
        Empresa.objects.all()
    )  # Queryset base (será filtrado por get_queryset)
    serializer_class = EmpresaSerializer
    permission_classes = [TenantPermission]

    def get_queryset(self):
        """
        Filtra empresas según el contexto multi-tenant:
        - Usuarios solo ven la empresa actual
        """
        # Si no hay empresa en el contexto, devolver queryset vacío
        if not hasattr(self.request, "tenant") or not self.request.tenant:
            return Empresa.objects.none()

        # Solo mostrar la empresa actual
        return Empresa.objects.filter(id=self.request.tenant.id)

    @action(detail=False, methods=["get"])
    def mi_empresa(self, request):
        """
        Endpoint para obtener información de la empresa actual
        """
        if not hasattr(request, "tenant") or not request.tenant:
            return Response(
                {"error": "No hay empresa en el contexto"}, status=400
            )

        serializer = self.get_serializer(request.tenant)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def mis_perfiles(self, request):
        """
        Endpoint para obtener los perfiles del usuario en la empresa actual
        """
        if not hasattr(request, "tenant") or not request.tenant:
            return Response(
                {"error": "No hay empresa en el contexto"}, status=400
            )

        perfiles = PerfilUsuario.objects.filter(
            usuario=request.user, empresa=request.tenant, activo=True
        )

        data = [
            {
                "rol": perfil.rol,
                "fecha_ingreso": perfil.fecha_ingreso,
                "configuracion": perfil.configuracion,
            }
            for perfil in perfiles
        ]

        return Response(data)
