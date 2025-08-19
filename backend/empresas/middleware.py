import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class EmpresaContextMiddleware(MiddlewareMixin):
    """
    Middleware para manejar el contexto de la empresa actual.
    En la versión simplificada, este middleware es opcional.
    """

    def process_request(self, request):
        # Este middleware no hace nada actualmente en la versión simplificada
        pass
