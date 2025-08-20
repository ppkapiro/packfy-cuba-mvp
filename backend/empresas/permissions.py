"""
Sistema de permisos multi-tenant para Packfy Cuba MVP.
Proporciona decoradores y clases de permisos basados en empresa y rol.
"""

from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied

from .models import PerfilUsuario


def require_empresa(func):
    """
    Decorador que requiere que el usuario tenga una empresa asignada.
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, "tenant") or not request.tenant:
            return JsonResponse(
                {
                    "error": "Empresa requerida",
                    "detail": "Esta operación requiere contexto de empresa",
                },
                status=400,
            )
        return func(request, *args, **kwargs)

    return wrapper


def require_rol(*roles_permitidos):
    """
    Decorador que requiere que el usuario tenga uno de los roles especificados.

    Uso: @require_rol('dueno', 'operador_miami')
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if (
                not hasattr(request, "perfil_usuario")
                or not request.perfil_usuario
            ):
                return JsonResponse(
                    {
                        "error": "Acceso denegado",
                        "detail": "Usuario sin perfil de empresa",
                    },
                    status=403,
                )

            if request.perfil_usuario.rol not in roles_permitidos:
                return JsonResponse(
                    {
                        "error": "Permisos insuficientes",
                        "detail": f'Rol requerido: {", ".join(roles_permitidos)}',
                    },
                    status=403,
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_empresa_permission(permission_check):
    """
    Decorador genérico para verificar permisos basados en empresa.

    Uso: @require_empresa_permission(lambda perfil: perfil.puede_gestionar_empresa)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if (
                not hasattr(request, "perfil_usuario")
                or not request.perfil_usuario
            ):
                return JsonResponse(
                    {
                        "error": "Acceso denegado",
                        "detail": "Usuario sin perfil de empresa",
                    },
                    status=403,
                )

            if not permission_check(request.perfil_usuario):
                return JsonResponse(
                    {
                        "error": "Permisos insuficientes",
                        "detail": "No tiene permisos para esta operación",
                    },
                    status=403,
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class TenantPermission(permissions.BasePermission):
    """
    Permiso base para operaciones multi-tenant en DRF.
    Verifica que el usuario tenga una empresa asignada.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request, "tenant") or not request.tenant:
            return False

        return True


class EmpresaOwnerPermission(permissions.BasePermission):
    """
    Permiso para dueños de empresa.
    Solo los dueños pueden realizar ciertas operaciones.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Configurar perfil_usuario si no existe
        if (
            not hasattr(request, "perfil_usuario")
            or not request.perfil_usuario
        ):
            self._setup_user_profile(request)

        if (
            not hasattr(request, "perfil_usuario")
            or not request.perfil_usuario
        ):
            return False

        return request.perfil_usuario.es_dueno

    def _setup_user_profile(self, request):
        """
        Configura el perfil del usuario basado en el tenant y usuario autenticado.
        """
        try:
            print(f"🔧 CONFIGURANDO PERFIL para {request.user.email}")

            # Obtener empresa del tenant
            empresa = getattr(request, "tenant", None)

            if empresa:
                # Buscar perfil específico para esta empresa
                perfil = (
                    PerfilUsuario.objects.select_related("empresa")
                    .filter(
                        usuario=request.user,
                        empresa=empresa,
                        activo=True,
                    )
                    .first()
                )

                if perfil:
                    request.perfil_usuario = perfil
                    print(
                        f"✅ PERFIL CONFIGURADO: {perfil.rol} para {perfil.usuario.email}"
                    )
                    return

            # Fallback: buscar cualquier perfil activo del usuario
            perfil = (
                PerfilUsuario.objects.select_related("empresa")
                .filter(
                    usuario=request.user, activo=True, empresa__activo=True
                )
                .first()
            )

            if perfil:
                request.perfil_usuario = perfil
                # También actualizar el tenant si no estaba configurado
                if not hasattr(request, "tenant") or not request.tenant:
                    request.tenant = perfil.empresa
                print(
                    f"✅ PERFIL FALLBACK: {perfil.rol} para {perfil.usuario.email}"
                )
            else:
                print(
                    f"❌ SIN PERFIL: Usuario {request.user.email} sin perfil activo"
                )

        except Exception as e:
            print(f"❌ ERROR CONFIGURANDO PERFIL: {e}")


class EmpresaOperatorPermission(permissions.BasePermission):
    """
    Permiso para operadores de empresa.
    Dueños y operadores pueden realizar estas operaciones.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Configurar perfil_usuario si no existe
        if (
            not hasattr(request, "perfil_usuario")
            or not request.perfil_usuario
        ):
            self._setup_user_profile(request)

        if (
            not hasattr(request, "perfil_usuario")
            or not request.perfil_usuario
        ):
            return False

        return request.perfil_usuario.puede_gestionar_envios

    def _setup_user_profile(self, request):
        """
        Configura el perfil del usuario basado en el tenant y usuario autenticado.
        """
        try:
            print(f"🔧 CONFIGURANDO PERFIL OPERATOR para {request.user.email}")

            # Obtener empresa del tenant
            empresa = getattr(request, "tenant", None)

            if empresa:
                # Buscar perfil específico para esta empresa
                perfil = (
                    PerfilUsuario.objects.select_related("empresa")
                    .filter(
                        usuario=request.user,
                        empresa=empresa,
                        activo=True,
                    )
                    .first()
                )

                if perfil:
                    request.perfil_usuario = perfil
                    print(
                        f"✅ PERFIL OPERATOR CONFIGURADO: {perfil.rol} para {perfil.usuario.email}"
                    )
                    return

            # Fallback: buscar cualquier perfil activo del usuario
            perfil = (
                PerfilUsuario.objects.select_related("empresa")
                .filter(
                    usuario=request.user, activo=True, empresa__activo=True
                )
                .first()
            )

            if perfil:
                request.perfil_usuario = perfil
                # También actualizar el tenant si no estaba configurado
                if not hasattr(request, "tenant") or not request.tenant:
                    request.tenant = perfil.empresa
                print(
                    f"✅ PERFIL OPERATOR FALLBACK: {perfil.rol} para {perfil.usuario.email}"
                )
            else:
                print(
                    f"❌ SIN PERFIL OPERATOR: Usuario {request.user.email} sin perfil activo"
                )

        except Exception as e:
            print(f"❌ ERROR CONFIGURANDO PERFIL OPERATOR: {e}")


class EmpresaClientPermission(permissions.BasePermission):
    """
    Permiso para clientes de empresa.
    Cualquier usuario de la empresa puede realizar estas operaciones.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if (
            not hasattr(request, "perfil_usuario")
            or not request.perfil_usuario
        ):
            return False

        return request.perfil_usuario.activo


class EmpresaSpecificPermission(permissions.BasePermission):
    """
    Permiso para verificar que el objeto pertenece a la empresa del usuario.
    """

    def has_object_permission(self, request, view, obj):
        if not hasattr(request, "tenant") or not request.tenant:
            return False

        # Verificar que el objeto pertenece a la empresa del usuario
        if hasattr(obj, "empresa"):
            return obj.empresa == request.tenant

        # Si el objeto no tiene empresa directa, buscar relaciones
        if hasattr(obj, "remitente") and hasattr(obj.remitente, "empresa"):
            return obj.remitente.empresa == request.tenant

        if hasattr(obj, "destinatario") and hasattr(
            obj.destinatario, "empresa"
        ):
            return obj.destinatario.empresa == request.tenant

        return False


# Decoradores de conveniencia
require_dueno = require_rol(PerfilUsuario.RolChoices.DUENO)
require_operador = require_rol(
    PerfilUsuario.RolChoices.DUENO,
    PerfilUsuario.RolChoices.OPERADOR_MIAMI,
    PerfilUsuario.RolChoices.OPERADOR_CUBA,
)
require_operador_miami = require_rol(
    PerfilUsuario.RolChoices.DUENO, PerfilUsuario.RolChoices.OPERADOR_MIAMI
)
require_operador_cuba = require_rol(
    PerfilUsuario.RolChoices.DUENO, PerfilUsuario.RolChoices.OPERADOR_CUBA
)
require_cliente = require_rol(
    PerfilUsuario.RolChoices.DUENO,
    PerfilUsuario.RolChoices.OPERADOR_MIAMI,
    PerfilUsuario.RolChoices.OPERADOR_CUBA,
    PerfilUsuario.RolChoices.REMITENTE,
    PerfilUsuario.RolChoices.DESTINATARIO,
)
