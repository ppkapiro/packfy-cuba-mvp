from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Empresa, PerfilUsuario
from .permissions import TenantPermission
from .serializers import EmpresaSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para empresas con soporte multi-tenant y
    restricciones por rol.
    """

    queryset = Empresa.objects.all()  # Queryset base (será filtrado por get_queryset)
    serializer_class = EmpresaSerializer

    def get_permissions(self):
        """
        Personalización de permisos por acción:
        - Lectura (list, retrieve, mi_empresa, mis_perfiles):
          Todos los usuarios
        - Modificación (update, partial_update): Solo dueño
        - Creación/eliminación: Solo dueño
        """
        if self.action in ["list", "retrieve", "mi_empresa", "mis_perfiles"]:
            # Lectura: Todos los usuarios autenticados con tenant
            permission_classes = [TenantPermission]
        elif self.action in ["create", "destroy", "update", "partial_update"]:
            # Escritura: Solo dueño
            from .permissions import EmpresaOwnerPermission

            permission_classes = [TenantPermission, EmpresaOwnerPermission]
        else:
            permission_classes = [TenantPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filtra empresas según el contexto multi-tenant:
        - Superusuarios ven todas las empresas
        - Usuarios normales solo ven la empresa actual
        """
        # Si el usuario es superusuario, mostrar todas las empresas
        if self.request.user.is_superuser:
            return Empresa.objects.all()

        # Si no hay empresa en el contexto, devolver queryset vacío
        if not hasattr(self.request, "tenant") or not self.request.tenant:
            return Empresa.objects.none()

        # Solo mostrar la empresa actual para usuarios normales
        return Empresa.objects.filter(id=self.request.tenant.id)

    @action(detail=False, methods=["get"])
    def mi_empresa(self, request):
        """
        Endpoint para obtener información de la empresa actual
        """
        if not hasattr(request, "tenant") or not request.tenant:
            return Response({"error": "No hay empresa en el contexto"}, status=400)

        serializer = self.get_serializer(request.tenant)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def mis_perfiles(self, request):
        """
        Endpoint para obtener los perfiles del usuario en la empresa actual
        """
        if not hasattr(request, "tenant") or not request.tenant:
            return Response({"error": "No hay empresa en el contexto"}, status=400)

        perfiles = PerfilUsuario.objects.filter(
            usuario=request.user, empresa=request.tenant, activo=True
        )

        data = [
            {
                "id": perfil.id,
                "rol": perfil.rol,
                "rol_display": perfil.get_rol_display(),
                "activo": perfil.activo,
                "fecha_vinculacion": perfil.fecha_vinculacion,
                "ultima_actividad": perfil.ultima_actividad,
                "telefono": perfil.telefono,
                "direccion": perfil.direccion,
                "empresa": {
                    "id": perfil.empresa.id,
                    "nombre": perfil.empresa.nombre,
                    "slug": perfil.empresa.slug,
                },
            }
            for perfil in perfiles
        ]

        return Response(data)
