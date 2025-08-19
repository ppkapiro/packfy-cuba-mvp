"""
Utilidades para el sistema multi-tenant.
Proporciona funciones helper para trabajar con empresas y usuarios.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Empresa, PerfilUsuario

User = get_user_model()


class TenantUtils:
    """
    Clase con utilidades para manejo de multi-tenancy.
    """

    @staticmethod
    def crear_empresa_con_dueno(
        nombre_empresa,
        email_dueno,
        password_dueno,
        nombre_dueno=None,
        apellido_dueno=None,
    ):
        """
        Crea una nueva empresa junto con su usuario dueño.

        Args:
            nombre_empresa (str): Nombre de la empresa
            email_dueno (str): Email del dueño
            password_dueno (str): Password del dueño
            nombre_dueno (str, optional): Nombre del dueño
            apellido_dueno (str, optional): Apellido del dueño

        Returns:
            tuple: (empresa, usuario, perfil)
        """
        with transaction.atomic():
            # Crear empresa
            empresa = Empresa.objects.create(nombre=nombre_empresa)

            # Crear usuario dueño
            usuario = User.objects.create_user(
                username=email_dueno,
                email=email_dueno,
                password=password_dueno,
                first_name=nombre_dueno or "",
                last_name=apellido_dueno or "",
            )

            # Crear perfil de dueño
            perfil = PerfilUsuario.objects.create(
                usuario=usuario,
                empresa=empresa,
                rol=PerfilUsuario.RolChoices.DUENO,
            )

            return empresa, usuario, perfil

    @staticmethod
    def agregar_usuario_a_empresa(
        empresa, email_usuario, rol, password=None, nombre=None, apellido=None
    ):
        """
        Agrega un usuario existente o nuevo a una empresa con un rol específico.

        Args:
            empresa (Empresa): La empresa a la que agregar el usuario
            email_usuario (str): Email del usuario
            rol (str): Rol del usuario (usar PerfilUsuario.RolChoices)
            password (str, optional): Password si es usuario nuevo
            nombre (str, optional): Nombre del usuario
            apellido (str, optional): Apellido del usuario

        Returns:
            tuple: (usuario, perfil, es_nuevo_usuario)
        """
        with transaction.atomic():
            # Buscar usuario existente
            try:
                usuario = User.objects.get(email=email_usuario)
                es_nuevo_usuario = False

                # Verificar si ya tiene perfil en esta empresa
                if PerfilUsuario.objects.filter(
                    usuario=usuario, empresa=empresa
                ).exists():
                    raise ValidationError(
                        f"El usuario ya pertenece a la empresa {empresa.nombre}"
                    )

            except User.DoesNotExist:
                # Crear nuevo usuario
                if not password:
                    raise ValidationError(
                        "Password requerido para usuario nuevo"
                    )

                usuario = User.objects.create_user(
                    username=email_usuario,
                    email=email_usuario,
                    password=password,
                    first_name=nombre or "",
                    last_name=apellido or "",
                )
                es_nuevo_usuario = True

            # Crear perfil en la empresa
            perfil = PerfilUsuario.objects.create(
                usuario=usuario, empresa=empresa, rol=rol
            )

            return usuario, perfil, es_nuevo_usuario

    @staticmethod
    def cambiar_rol_usuario(usuario, empresa, nuevo_rol):
        """
        Cambia el rol de un usuario en una empresa específica.

        Args:
            usuario (User): El usuario
            empresa (Empresa): La empresa
            nuevo_rol (str): El nuevo rol

        Returns:
            PerfilUsuario: El perfil actualizado
        """
        try:
            perfil = PerfilUsuario.objects.get(
                usuario=usuario, empresa=empresa
            )
            perfil.rol = nuevo_rol
            perfil.save()
            return perfil
        except PerfilUsuario.DoesNotExist:
            raise ValidationError(
                f"El usuario no pertenece a la empresa {empresa.nombre}"
            )

    @staticmethod
    def obtener_empresas_usuario(usuario):
        """
        Obtiene todas las empresas a las que pertenece un usuario.

        Args:
            usuario (User): El usuario

        Returns:
            QuerySet: Empresas del usuario con sus roles
        """
        return PerfilUsuario.objects.filter(
            usuario=usuario, activo=True, empresa__activo=True
        ).select_related("empresa")

    @staticmethod
    def obtener_usuarios_empresa(empresa, rol=None):
        """
        Obtiene todos los usuarios de una empresa, opcionalmente filtrado por rol.

        Args:
            empresa (Empresa): La empresa
            rol (str, optional): Filtrar por rol específico

        Returns:
            QuerySet: Perfiles de usuarios de la empresa
        """
        queryset = PerfilUsuario.objects.filter(
            empresa=empresa, activo=True
        ).select_related("usuario")

        if rol:
            queryset = queryset.filter(rol=rol)

        return queryset

    @staticmethod
    def transferir_usuario_empresa(
        usuario, empresa_origen, empresa_destino, nuevo_rol=None
    ):
        """
        Transfiere un usuario de una empresa a otra.

        Args:
            usuario (User): El usuario a transferir
            empresa_origen (Empresa): Empresa actual
            empresa_destino (Empresa): Nueva empresa
            nuevo_rol (str, optional): Nuevo rol (mantiene el actual si no se especifica)

        Returns:
            PerfilUsuario: El nuevo perfil en la empresa destino
        """
        with transaction.atomic():
            # Obtener perfil actual
            try:
                perfil_origen = PerfilUsuario.objects.get(
                    usuario=usuario, empresa=empresa_origen
                )
            except PerfilUsuario.DoesNotExist:
                raise ValidationError(
                    f"El usuario no pertenece a {empresa_origen.nombre}"
                )

            # Determinar rol para nueva empresa
            rol_final = nuevo_rol or perfil_origen.rol

            # Desactivar perfil en empresa origen
            perfil_origen.activo = False
            perfil_origen.save()

            # Crear o activar perfil en empresa destino
            perfil_destino, created = PerfilUsuario.objects.get_or_create(
                usuario=usuario,
                empresa=empresa_destino,
                defaults={"rol": rol_final, "activo": True},
            )

            if not created:
                perfil_destino.rol = rol_final
                perfil_destino.activo = True
                perfil_destino.save()

            return perfil_destino

    @staticmethod
    def obtener_estadisticas_empresa(empresa):
        """
        Obtiene estadísticas básicas de una empresa.

        Args:
            empresa (Empresa): La empresa

        Returns:
            dict: Estadísticas de la empresa
        """
        perfiles = PerfilUsuario.objects.filter(empresa=empresa, activo=True)

        return {
            "total_usuarios": perfiles.count(),
            "duenos": perfiles.filter(
                rol=PerfilUsuario.RolChoices.DUENO
            ).count(),
            "operadores_miami": perfiles.filter(
                rol=PerfilUsuario.RolChoices.OPERADOR_MIAMI
            ).count(),
            "operadores_cuba": perfiles.filter(
                rol=PerfilUsuario.RolChoices.OPERADOR_CUBA
            ).count(),
            "remitentes": perfiles.filter(
                rol=PerfilUsuario.RolChoices.REMITENTE
            ).count(),
            "destinatarios": perfiles.filter(
                rol=PerfilUsuario.RolChoices.DESTINATARIO
            ).count(),
        }
