import logging

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin

from .models import Empresa, PerfilUsuario

logger = logging.getLogger(__name__)


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware para manejar el contexto multi-tenant.
    Detecta la empresa actual y proporciona contexto para toda la aplicación.
    """

    def process_request(self, request):
        """
        Procesa cada request para determinar la empresa actual.
        Métodos de detección:
        1. Header X-Tenant-Slug (para APIs)
        2. Subdomain (futuro)
        3. Usuario autenticado (fallback)
        """
        empresa = None

        # Método 1: Header X-Tenant-Slug (para APIs)
        tenant_slug = request.META.get("HTTP_X_TENANT_SLUG")
        if tenant_slug:
            try:
                empresa = Empresa.objects.get(slug=tenant_slug, activo=True)
                logger.info(f"Empresa detectada por header: {empresa.nombre}")
            except Empresa.DoesNotExist:
                logger.warning(
                    f"Empresa no encontrada con slug: {tenant_slug}"
                )
                raise Http404(f"Empresa '{tenant_slug}' no encontrada")

        # Método 2: Usuario autenticado (fallback)
        elif request.user.is_authenticated:
            try:
                perfil = PerfilUsuario.objects.select_related("empresa").get(
                    usuario=request.user, activo=True, empresa__activo=True
                )
                empresa = perfil.empresa
                logger.info(f"Empresa detectada por usuario: {empresa.nombre}")

                # Agregar perfil al request para fácil acceso
                request.perfil_usuario = perfil

            except PerfilUsuario.DoesNotExist:
                logger.warning(
                    f"Usuario {request.user.username} sin empresa asignada"
                )
                # Para usuarios sin empresa (superuser, etc), continuar sin empresa

        # Método 3: Empresa por defecto para requests no autenticados (opcional)
        # Puedes descomentar esto si necesitas una empresa por defecto
        # elif not empresa:
        #     empresa = Empresa.objects.filter(activo=True).first()

        # Establecer contexto de empresa en el request
        request.tenant = empresa

        # Log del contexto establecido
        if empresa:
            logger.debug(
                f"Contexto tenant establecido: {empresa.nombre} (ID: {empresa.id})"
            )
        else:
            logger.debug("Sin contexto tenant - request sin empresa")

    def process_response(self, request, response):
        """
        Procesa la respuesta para agregar headers informativos.
        """
        if hasattr(request, "tenant") and request.tenant:
            response["X-Tenant-Name"] = request.tenant.nombre
            response["X-Tenant-Slug"] = request.tenant.slug

        return response


class EmpresaContextMiddleware(MiddlewareMixin):
    """
    Middleware legacy para compatibilidad.
    Redirige al nuevo TenantMiddleware.
    """

    def process_request(self, request):
        # Compatibilidad con versión anterior
        logger.warning(
            "EmpresaContextMiddleware is deprecated, use TenantMiddleware instead"
        )
        pass
