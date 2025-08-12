"""
Middleware para proteger usuarios demo en Packfy Cuba
Previene modificaciones accidentales de usuarios de prueba
"""
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import logging

Usuario = get_user_model()

class ProteccionUsuariosDemoMiddleware:
    """
    Middleware que protege usuarios demo de modificaciones
    """
    
    USUARIOS_PROTEGIDOS = [
        'admin@packfy.cu',
        'empresa@test.cu', 
        'cliente@test.cu'
    ]
    
    RUTAS_PROTEGIDAS = [
        '/api/usuarios/',
        '/admin/usuarios/',
        '/api/auth/register/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
    
    def __call__(self, request):
        # Verificar si es una ruta protegida
        if any(ruta in request.path for ruta in self.RUTAS_PROTEGIDAS):
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                # Verificar si intenta modificar usuarios protegidos
                if self._es_modificacion_usuario_protegido(request):
                    return JsonResponse({
                        'error': 'Usuario demo protegido',
                        'message': 'Los usuarios de demostración no pueden ser modificados',
                        'protected_users': self.USUARIOS_PROTEGIDOS
                    }, status=403)
        
        response = self.get_response(request)
        return response
    
    def _es_modificacion_usuario_protegido(self, request):
        """Verificar si la petición intenta modificar un usuario protegido"""
        try:
            # Verificar en URL params
            if 'email' in request.GET:
                email = request.GET.get('email')
                if email in self.USUARIOS_PROTEGIDOS:
                    return True
            
            # Verificar en body de la petición
            if hasattr(request, 'data') and isinstance(request.data, dict):
                email = request.data.get('email')
                if email in self.USUARIOS_PROTEGIDOS:
                    return True
            
            # Verificar por ID en la URL
            import re
            user_id_match = re.search(r'/usuarios/(\d+)/', request.path)
            if user_id_match:
                user_id = int(user_id_match.group(1))
                try:
                    usuario = Usuario.objects.get(id=user_id)
                    if usuario.email in self.USUARIOS_PROTEGIDOS:
                        return True
                except Usuario.DoesNotExist:
                    pass
            
            return False
            
        except Exception as e:
            self.logger.warning(f"Error verificando protección de usuario: {e}")
            return False
