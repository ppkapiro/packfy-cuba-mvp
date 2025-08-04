from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class EmpresaContextMiddleware(MiddlewareMixin):
    """
    Middleware para manejar el contexto de la empresa actual.
    En la versión simplificada, este middleware no hace nada especial.
    Se mantiene como placeholder para futuras implementaciones.
    """
    def process_request(self, request):
        # Este middleware no hace nada actualmente en la versión simplificada
        # Será utilizado en el futuro para la funcionalidad multi-tenant
        pass
