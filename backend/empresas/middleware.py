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
        Procesa cada request para configurar contexto básico.
        Solo se establece el tenant por header, la autenticación se maneja en process_view.
        """
        print(f"🚀 MIDDLEWARE process_request para {request.path}")

        # EXCLUIR RUTAS DEL ADMIN DJANGO - no requieren multitenancy
        admin_paths = ["/admin/", "/static/", "/media/"]
        if any(request.path.startswith(path) for path in admin_paths):
            print(f"🔓 ADMIN PATH - saltando multitenancy para {request.path}")
            request.tenant = None
            return None

        empresa = None

        # Método 1: Header X-Tenant-Slug (para APIs) - solo configurar empresa
        tenant_slug = request.META.get("HTTP_X_TENANT_SLUG")
        print(f"🔍 TENANT SLUG: {tenant_slug}")

        if tenant_slug:
            try:
                empresa = Empresa.objects.get(slug=tenant_slug, activo=True)
                logger.info(f"Empresa detectada por header: {empresa.nombre}")
            except Empresa.DoesNotExist:
                logger.warning(
                    f"Empresa no encontrada con slug: {tenant_slug}"
                )
                raise Http404(f"Empresa '{tenant_slug}' no encontrada")

        # Establecer contexto de empresa en el request
        request.tenant = empresa

        # Log del contexto establecido
        if empresa:
            logger.debug(
                f"Contexto tenant establecido: {empresa.nombre} (ID: {empresa.id})"
            )
        else:
            logger.debug("Sin contexto tenant - request sin empresa")

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Se ejecuta DESPUÉS de la autenticación DRF para configurar el perfil del usuario.
        """
        print(f"🎯 MIDDLEWARE process_view para {request.path}")
        print(
            f"🔍 USER EN PROCESS_VIEW: {getattr(request, 'user', 'NO USER')}"
        )

        # EXCLUIR RUTAS DEL ADMIN DJANGO - no requieren multitenancy
        admin_paths = ["/admin/", "/static/", "/media/"]
        if any(request.path.startswith(path) for path in admin_paths):
            print(f"🔓 ADMIN PATH - saltando process_view para {request.path}")
            return None

        # Solo procesar si hay una empresa y el usuario está autenticado
        if (
            hasattr(request, "tenant")
            and request.tenant
            and hasattr(request, "user")
            and request.user
            and request.user.is_authenticated
        ):

            try:
                perfil = (
                    PerfilUsuario.objects.select_related("empresa")
                    .filter(
                        usuario=request.user,
                        empresa=request.tenant,
                        activo=True,
                    )
                    .first()
                )

                if perfil:
                    request.perfil_usuario = perfil
                    print(
                        f"🎯 PERFIL CONFIGURADO: {perfil.rol} para {perfil.usuario.email}"
                    )
                else:
                    # Si no tiene perfil en esta empresa, buscar su perfil principal
                    perfil_principal = (
                        PerfilUsuario.objects.select_related("empresa")
                        .filter(
                            usuario=request.user,
                            activo=True,
                            empresa__activo=True,
                        )
                        .first()
                    )

                    if perfil_principal:
                        request.perfil_usuario = perfil_principal
                        # También actualizar el tenant si es diferente
                        if request.tenant != perfil_principal.empresa:
                            request.tenant = perfil_principal.empresa
                        print(
                            f"🎯 PERFIL PRINCIPAL: {perfil_principal.rol} para {perfil_principal.usuario.email}"
                        )
                    else:
                        print(
                            f"⚠️ SIN PERFIL: Usuario {request.user.username} sin perfil activo"
                        )

            except Exception as e:
                print(f"❌ ERROR PERFIL: {e}")
                logger.warning(f"Error configurando perfil del usuario: {e}")

        # No retornar nada para continuar con el procesamiento normal
        return None

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
