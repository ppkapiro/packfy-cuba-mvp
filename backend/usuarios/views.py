from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import EsAdministrador, EsCreadorOAdministrador

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para usuarios.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_permissions(self):
        """
        Personalización de permisos:
        - Administradores pueden realizar todas las acciones
        - Usuarios solo pueden ver/editar su propio perfil
        """
        if self.action == 'me':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'destroy', 'list']:
            permission_classes = [EsAdministrador]
        else:
            permission_classes = [EsCreadorOAdministrador]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filtra los usuarios según los permisos del usuario actual:
        - Administradores ven todos los usuarios
        - Usuarios normales solo se ven a sí mismos
        """
        user = self.request.user
        # Verificar si el usuario está autenticado y tiene los atributos necesarios
        if user.is_authenticated and (user.is_staff or getattr(user, 'es_administrador_empresa', False)):
            return Usuario.objects.all()
        return Usuario.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Endpoint para obtener el perfil del usuario autenticado
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
