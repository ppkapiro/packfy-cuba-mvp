import logging
import re

from django.http import Http404, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from .models import Empresa, PerfilUsuario

logger = logging.getLogger(__name__)


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware para manejar el contexto multi-tenant.
    Detecta la empresa actual por:
    1. Subdominio (empresa1.packfy.com)
    2. Header X-Tenant-Slug (para APIs)
    """

    def process_request(self, request):
        """
        Procesa cada request para configurar contexto básico.
        Prioriza detección por subdominio, fallback a header.
        """
        print(f"🚀 MIDDLEWARE process_request para {request.path}")
        print(f"🌐 HOST: {request.get_host()}")

        # EXCLUIR RUTAS DEL ADMIN DJANGO - no requieren multitenancy
        admin_paths = ["/admin/", "/static/", "/media/"]
        if any(request.path.startswith(path) for path in admin_paths):
            print(f"🔓 ADMIN PATH - saltando multitenancy para {request.path}")
            request.tenant = None
            return None

        empresa = None
        host = request.get_host()

        # Método 1: Detección por Subdominio (NUEVO - PRIORIDAD)
        empresa_slug = self._extract_tenant_from_subdomain(host)
        print(f"🏢 SUBDOMAIN SLUG: {empresa_slug}")

        if empresa_slug:
            try:
                empresa = Empresa.objects.get(slug=empresa_slug, activo=True)
                logger.info(f"Empresa detectada por subdominio: {empresa.nombre}")
                print(f"✅ EMPRESA POR SUBDOMAIN: {empresa.nombre}")
            except Empresa.DoesNotExist:
                logger.warning(f"Empresa no encontrada con slug: {empresa_slug}")
                # Para subdominios inválidos, redirigir a dominio principal
                if not self._is_main_domain(host):
                    main_domain = self._get_main_domain(host)
                    redirect_url = f"http://{main_domain}{request.get_full_path()}"
                    logger.info(f"Redirigiendo a dominio principal: {redirect_url}")
                    return HttpResponseRedirect(redirect_url)

        # Método 2: Header X-Tenant-Slug (para APIs) - fallback
        if not empresa:
            tenant_slug = request.META.get("HTTP_X_TENANT_SLUG")
            print(f"🔍 HEADER TENANT SLUG: {tenant_slug}")

            if tenant_slug:
                try:
                    empresa = Empresa.objects.get(slug=tenant_slug, activo=True)
                    logger.info(f"Empresa detectada por header: {empresa.nombre}")
                    print(f"✅ EMPRESA POR HEADER: {empresa.nombre}")
                except Empresa.DoesNotExist:
                    logger.warning(f"Empresa no encontrada con slug: {tenant_slug}")
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

    def _extract_tenant_from_subdomain(self, host):
        """
        Extrae el slug de la empresa del subdominio.

        Ejemplos:
        - empresa1.packfy.com → empresa1
        - empresa2.localhost:5173 → empresa2
        - app.packfy.com → None (dominio principal)
        - packfy.com → None (dominio principal)
        """
        # Limpiar puerto si existe
        host_clean = host.split(":")[0]

        # Patrones para detectar subdominios
        patterns = [
            r"^([^.]+)\.packfy\.com$",  # empresa1.packfy.com
            r"^([^.]+)\.localhost$",  # empresa1.localhost (desarrollo)
            r"^([^.]+)\.127\.0\.0\.1$",  # empresa1.127.0.0.1 (desarrollo)
        ]

        for pattern in patterns:
            match = re.match(pattern, host_clean)
            if match:
                subdomain = match.group(1)
                # Excluir subdominios principales/administrativos
                if subdomain not in ["app", "admin", "api", "www"]:
                    return subdomain

        return None

    def _is_main_domain(self, host):
        """
        Verifica si el host es un dominio principal
        (sin subdominio específico).
        """
        host_clean = host.split(":")[0]
        main_domains = [
            "packfy.com",
            "www.packfy.com",
            "app.packfy.com",
            "localhost",
            "127.0.0.1",
        ]
        return host_clean in main_domains

    def _get_main_domain(self, host):
        """
        Obtiene el dominio principal para redirección.
        """
        # En desarrollo, usar localhost
        if "localhost" in host or "127.0.0.1" in host:
            port = ":5173" if ":" in host else ""
            return f"localhost{port}"

        # En producción, usar app.packfy.com
        return "app.packfy.com"

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Se ejecuta DESPUÉS de la autenticación DRF para configurar
        el perfil del usuario.
        """
        print(f"🎯 MIDDLEWARE process_view para {request.path}")
        print(f"🔍 USER EN PROCESS_VIEW: {getattr(request, 'user', 'NO USER')}")

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
                        f"🎯 PERFIL CONFIGURADO: {perfil.rol} "
                        f"para {perfil.usuario.email}"
                    )
                else:
                    # Si no tiene perfil en esta empresa,
                    # buscar su perfil principal
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
                            f"🎯 PERFIL PRINCIPAL: {perfil_principal.rol} "
                            f"para {perfil_principal.usuario.email}"
                        )
                    else:
                        print(
                            f"⚠️ SIN PERFIL: Usuario "
                            f"{request.user.username} sin perfil activo"
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
            "EmpresaContextMiddleware is deprecated, " "use TenantMiddleware instead"
        )
        pass
