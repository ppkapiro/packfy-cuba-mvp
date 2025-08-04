from rest_framework import permissions

class EsAdministrador(permissions.BasePermission):
    """
    Permiso que verifica si el usuario es administrador del sistema o de una empresa.
    """
    
    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            return False
        
        # Permitir acceso a administradores del sistema
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Permitir acceso a administradores de empresa
        return request.user.es_administrador_empresa


class EsCreadorOAdministrador(permissions.BasePermission):
    """
    Permiso que verifica si el usuario es el creador del objeto o un administrador.
    """
    
    def has_permission(self, request, view):
        # Para crear registros, verificar si es administrador
        if view.action == 'create':
            return request.user.is_authenticated and (
                request.user.is_staff or 
                request.user.is_superuser or 
                request.user.es_administrador_empresa
            )
        return True
        
    def has_object_permission(self, request, view, obj):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            return False
        
        # Permitir acceso a administradores
        if request.user.is_staff or request.user.is_superuser or request.user.es_administrador_empresa:
            return True
        
        # Verificar si el usuario es el creador del objeto
        if hasattr(obj, 'creado_por') and obj.creado_por == request.user:
            return True
        
        return False
