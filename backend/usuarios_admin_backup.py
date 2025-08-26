from django.contrib import admi            empresas_del_usuario = request.user.perfiles_empresa.filter(
                rol="admin_empresa"rom django.contrib.auth.admin import UserAdmin
from django.db import models
from django.utils.html import format_html

from .models import ClienteUsuario, PersonalEmpresa, Usuario


# Inline para mostrar perfiles de empresa en el admin de usuario
class PerfilEmpresaInline(admin.TabularInline):
    """
    Inline para gestionar perfiles de empresa desde el usuario
    """

    from empresas.models import PerfilUsuario

    model = PerfilUsuario
    extra = 1
    fields = ("empresa", "rol", "activo", "telefono", "fecha_vinculacion")
    readonly_fields = ("fecha_vinculacion",)
    verbose_name = "Perfil en Empresa"
    verbose_name_plural = "Perfiles en Empresas"

    def get_queryset(self, request):
        """Filtrar perfiles según el usuario que accede"""
        qs = super().get_queryset(request)

        # Si es superuser, ve todos
        if request.user.is_superuser:
            return qs

        # Si es dueño de empresa, solo ve perfiles de sus empresas
        if hasattr(request.user, "perfiles_empresa"):
            empresas_del_usuario = request.user.perfiles_empresa.filter(
                rol="dueno"
            ).values_list("empresa_id", flat=True)
            return qs.filter(empresa_id__in=empresas_del_usuario)

        return qs.none()


# Personalización del panel de admin para los usuarios
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "telefono",
        "rol_display",
        "empresa_display",
        "categoria_display",
        "es_administrador_empresa",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "es_administrador_empresa",
        "is_staff",
        "is_active",
        "fecha_creacion",
        "perfiles_empresa__rol",
        "perfiles_empresa__empresa",
    )
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "telefono",
    )
    readonly_fields = ("fecha_creacion", "ultima_actualizacion")
    inlines = [PerfilEmpresaInline]

    # Organizar campos en secciones
    fieldsets = (
        (
            "👤 Información Personal",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "telefono",
                )
            },
        ),
        (
            "🔐 Permisos de Acceso",
            {
                "fields": ("is_active", "is_staff"),
                "description": "Permisos básicos de acceso al sistema",
            },
        ),
        (
            "🏢 Información Empresarial",
            {
                "fields": ("es_administrador_empresa",),
                "description": "Roles relacionados con la empresa",
            },
        ),
        (
            "📅 Fechas",
            {
                "fields": ("fecha_creacion", "ultima_actualizacion"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        """
        Filtrar usuarios según el rol del usuario que accede
        """
        qs = super().get_queryset(request)

        # Si es superuser, ve todos los usuarios
        if request.user.is_superuser:
            return qs

        # Si es dueño de empresa (no superuser), solo ve usuarios de sus
        # empresas
        if hasattr(request.user, "perfiles_empresa"):
            # Obtener empresas donde es dueño
            empresas_del_dueno = request.user.perfiles_empresa.filter(
                rol="dueno"
            ).values_list("empresa_id", flat=True)

            if empresas_del_dueno:
                # Solo mostrar usuarios que pertenecen a sus empresas
                usuarios_de_sus_empresas = Usuario.objects.filter(
                    perfiles_empresa__empresa_id__in=empresas_del_dueno
                ).distinct()

                # Excluir superusers - los dueños NO deben ver superadmins
                return usuarios_de_sus_empresas.filter(is_superuser=False)

        # Si no es ni superuser ni dueño, no ve nada
        return qs.none()

    def rol_display(self, obj):
        """Mostrar el rol principal del usuario"""
        perfil = obj.perfiles_empresa.first()
        if perfil:
            rol_icons = {
                "dueno": "👑",
                "operador_miami": "🌎",
                "operador_cuba": "🇨🇺",
                "remitente": "📦",
                "destinatario": "📬",
            }
            icon = rol_icons.get(perfil.rol, "👤")
            return format_html(f"{icon} {perfil.get_rol_display()}")
        return "❓ Sin rol"

    rol_display.short_description = "Rol"

    def empresa_display(self, obj):
        """Mostrar la empresa del usuario"""
        perfil = obj.perfiles_empresa.first()
        if perfil:
            return perfil.empresa.nombre
        return "❓ Sin empresa"

    empresa_display.short_description = "Empresa"

    def categoria_display(self, obj):
        """Mostrar la categoría del usuario (Personal vs Cliente)"""
        perfil = obj.perfiles_empresa.first()
        if perfil:
            if perfil.rol in ["dueno", "operador_miami", "operador_cuba"]:
                return format_html(
                    '<span style="color: #2e7d32; font-weight: bold;">'
                    "👥 Personal</span>"
                )
            else:
                return format_html(
                    '<span style="color: #1976d2; font-weight: bold;">'
                    "👤 Cliente</span>"
                )
        return "❓ Sin categoría"

    categoria_display.short_description = "Categoría"

    def has_change_permission(self, request, obj=None):
        """
        Controlar permisos de edición
        """
        # Superusers pueden editar todo
        if request.user.is_superuser:
            return True

        # Si no hay objeto específico, verificar permiso general
        if obj is None:
            return request.user.is_staff

        # Dueños NO pueden editar superusers
        if obj.is_superuser:
            return False

        # Dueños solo pueden editar usuarios de sus empresas
        if hasattr(request.user, "perfiles_empresa"):
            empresas_del_dueno = request.user.perfiles_empresa.filter(
                rol="dueno"
            ).values_list("empresa_id", flat=True)

            # Verificar si el usuario objetivo pertenece a alguna empresa
            # del dueño
            if obj.perfiles_empresa.filter(
                empresa_id__in=empresas_del_dueno
            ).exists():
                return True

        return False

    def has_delete_permission(self, request, obj=None):
        """
        Controlar permisos de eliminación
        """
        # Superusers pueden eliminar todo
        if request.user.is_superuser:
            return True

        # Dueños NO pueden eliminar superusers
        if obj and obj.is_superuser:
            return False

        # Usar la misma lógica que change_permission
        return self.has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        """
        Campos de solo lectura según el usuario
        """
        readonly = list(self.readonly_fields)

        # Si no es superuser, no puede modificar permisos de Django
        if not request.user.is_superuser:
            readonly.extend([
                "is_superuser", "is_staff", "user_permissions", "groups"
            ])

        return readonly

    # Agrupaciones de campos en el formulario
    def get_fieldsets(self, request, obj=None):
        """
        Fieldsets según el tipo de usuario
        """
        if request.user.is_superuser:
            # Superusers ven todos los campos
            return (
                (None, {"fields": ("email", "username", "password")}),
                (
                    "Información Personal",
                    {
                        "fields": (
                            "first_name",
                            "last_name",
                            "telefono",
                            "cargo",
                            "foto_perfil",
                        )
                    },
                ),
                (
                    "Permisos",
                    {
                        "fields": (
                            "es_administrador_empresa",
                            "is_active",
                            "is_staff",
                            "is_superuser",
                            "groups",
                            "user_permissions",
                        )
                    },
                ),
                (
                    "Fechas Importantes",
                    {
                        "fields": (
                            "last_login",
                            "date_joined",
                            "fecha_creacion",
                            "ultima_actualizacion",
                        )
                    },
                ),
            )
        else:
            # Dueños de empresa ven campos limitados
            return (
                (None, {"fields": ("email", "username")}),
                (
                    "Información Personal",
                    {
                        "fields": (
                            "first_name",
                            "last_name",
                            "telefono",
                            "cargo",
                            "foto_perfil",
                        )
                    },
                ),
                (
                    "Estado",
                    {
                        "fields": (
                            "es_administrador_empresa",
                            "is_active",
                        )
                    },
                ),
                (
                    "Fechas",
                    {
                        "fields": (
                            "date_joined",
                            "fecha_creacion",
                            "ultima_actualizacion",
                        )
                    },
                ),
            )

    # Formulario para la creación de nuevos usuarios
    def get_add_fieldsets(self, request, obj=None):
        """
        Campos para crear usuarios según el rol
        """
        if request.user.is_superuser:
            return (
                (
                    None,
                    {
                        "classes": ("wide",),
                        "fields": (
                            "email",
                            "username",
                            "password1",
                            "password2",
                            "first_name",
                            "last_name",
                            "is_active",
                            "is_staff",
                        ),
                    },
                ),
            )
        else:
            # Dueños solo pueden crear usuarios básicos
            return (
                (
                    None,
                    {
                        "classes": ("wide",),
                        "fields": (
                            "email",
                            "username",
                            "password1",
                            "password2",
                            "first_name",
                            "last_name",
                            "is_active",
                        ),
                    },
                ),
            )

    def total_empresas(self, obj):
        """Mostrar número de empresas a las que pertenece el usuario"""
        return obj.perfiles_empresa.count()

    total_empresas.short_description = "Total Empresas"
    total_empresas.admin_order_field = "perfiles_empresa__count"


# ===============================================
# 👥 ADMINISTRADORES ESPECIALIZADOS POR CATEGORÍA
# ===============================================


@admin.register(PersonalEmpresa)
class PersonalEmpresaAdmin(UsuarioAdmin):
    """Admin especializado para personal de la empresa (dueño, operadores)"""

    def get_queryset(self, request):
        """Solo mostrar personal de la empresa"""
        # Primero aplicar filtros de seguridad de la clase padre
        qs = super().get_queryset(request)
        # Luego filtrar solo personal de empresa
        return qs.filter(
            perfiles_empresa__rol__in=[
                "dueno",
                "operador_miami",
                "operador_cuba",
            ]
        ).distinct()

    list_display = (
        "email",
        "first_name",
        "last_name",
        "rol_display",
        "telefono",
        "is_active",
        "ultima_actualizacion",
    )

    list_filter = (
        "perfiles_empresa__rol",
        "is_active",
        "ultima_actualizacion",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "telefono",
    )

    # Campos específicos para personal de empresa
    fieldsets = (
        (
            "👤 Información Personal",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "telefono",
                    "cargo",
                )
            },
        ),
        (
            "🔐 Permisos de Acceso",
            {
                "fields": ("is_active", "is_staff"),
                "description": "Control de acceso al sistema",
            },
        ),
        (
            "🏢 Rol en la Empresa",
            {
                "fields": ("es_administrador_empresa",),
                "description": "Permisos administrativos de empresa",
            },
        ),
        (
            "📅 Fechas",
            {
                "fields": ("fecha_creacion", "ultima_actualizacion"),
                "classes": ("collapse",),
            },
        ),
    )

    # Acciones personalizadas
    actions = ["activar_usuarios", "desactivar_usuarios"]

    def activar_usuarios(self, request, queryset):
        """Activar usuarios seleccionados"""
        count = queryset.update(is_active=True)
        self.message_user(request, f"Se activaron {count} usuarios.")

    activar_usuarios.short_description = "✅ Activar usuarios seleccionados"

    def desactivar_usuarios(self, request, queryset):
        """Desactivar usuarios seleccionados"""
        count = queryset.update(is_active=False)
        self.message_user(request, f"Se desactivaron {count} usuarios.")

    desactivar_usuarios.short_description = (
        "❌ Desactivar usuarios seleccionados"
    )


@admin.register(ClienteUsuario)
class ClientesAdmin(UsuarioAdmin):
    """Admin especializado para clientes (remitentes, destinatarios)"""

    def get_queryset(self, request):
        """Solo mostrar clientes"""
        # Primero aplicar filtros de seguridad de la clase padre
        qs = super().get_queryset(request)
        # Luego filtrar solo clientes
        return qs.filter(
            perfiles_empresa__rol__in=["remitente", "destinatario"]
        ).distinct()

    list_display = (
        "email",
        "first_name",
        "last_name",
        "rol_display",
        "telefono",
        "total_envios",
        "is_active",
        "fecha_creacion",
    )

    list_filter = (
        "perfiles_empresa__rol",
        "is_active",
        "fecha_creacion",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "telefono",
    )

    # Los clientes tienen campos más simples
    fieldsets = (
        (
            "👤 Información del Cliente",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "telefono",
                )
            },
        ),
        (
            "📦 Estado de la Cuenta",
            {
                "fields": ("is_active",),
                "description": "Estado de activación de la cuenta del cliente",
            },
        ),
        (
            "📅 Información de Registro",
            {
                "fields": ("fecha_creacion", "ultima_actualizacion"),
                "classes": ("collapse",),
            },
        ),
    )

    # Acciones para clientes
    actions = ["activar_clientes", "desactivar_clientes", "exportar_clientes"]

    def activar_clientes(self, request, queryset):
        """Activar clientes seleccionados"""
        count = queryset.update(is_active=True)
        self.message_user(request, f"Se activaron {count} clientes.")

    activar_clientes.short_description = "✅ Activar clientes seleccionados"

    def desactivar_clientes(self, request, queryset):
        """Desactivar clientes seleccionados"""
        count = queryset.update(is_active=False)
        self.message_user(request, f"Se desactivaron {count} clientes.")

    desactivar_clientes.short_description = (
        "❌ Desactivar clientes seleccionados"
    )

    def total_envios(self, obj):
        """Mostrar total de envíos del cliente"""
        try:
            from envios.models import Envio

            total = Envio.objects.filter(
                models.Q(remitente__email=obj.email)
                | models.Q(destinatario__email=obj.email)
            ).count()
            return f"📦 {total}"
        except Exception:
            return "📦 0"

    total_envios.short_description = "Total Envíos"
