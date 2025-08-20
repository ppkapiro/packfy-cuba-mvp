from django.contrib import admin

from .models import Empresa, PerfilUsuario


# Inline para mostrar usuarios de una empresa
class PerfilUsuarioInline(admin.TabularInline):
    """
    Inline para gestionar usuarios desde la empresa
    """

    model = PerfilUsuario
    extra = 1
    fields = ("usuario", "rol", "activo", "telefono", "fecha_vinculacion")
    readonly_fields = ("fecha_vinculacion",)
    verbose_name = "Usuario de la Empresa"
    verbose_name_plural = "Usuarios de la Empresa"


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "slug",
        "ruc",
        "email",
        "activo",
        "total_usuarios",
        "fecha_creacion",
    )
    list_filter = ("activo", "fecha_creacion")
    search_fields = ("nombre", "slug", "ruc", "email")
    readonly_fields = ("slug", "fecha_creacion", "ultima_actualizacion")
    inlines = [PerfilUsuarioInline]

    fieldsets = (
        ("Información Principal", {"fields": ("nombre", "slug", "ruc")}),
        (
            "Información de Contacto",
            {"fields": ("direccion", "telefono", "email", "logo")},
        ),
        ("Configuración", {"fields": ("activo", "dominio", "configuracion")}),
        (
            "Metadatos",
            {
                "fields": ("fecha_creacion", "ultima_actualizacion"),
                "classes": ("collapse",),
            },
        ),
    )

    def total_usuarios(self, obj):
        """Mostrar número total de usuarios en la empresa"""
        return obj.usuarios.count()

    total_usuarios.short_description = "Total Usuarios"
    total_usuarios.admin_order_field = "usuarios__count"


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """
    Admin para gestionar perfiles de usuarios en empresas
    """

    list_display = (
        "usuario_nombre",
        "empresa",
        "rol",
        "activo",
        "fecha_vinculacion",
    )
    list_filter = ("rol", "activo", "empresa", "fecha_vinculacion")
    search_fields = (
        "usuario__email",
        "usuario__first_name",
        "usuario__last_name",
        "empresa__nombre",
        "telefono",
    )
    readonly_fields = ("fecha_vinculacion", "ultima_actividad")

    fieldsets = (
        (
            "Usuario y Empresa",
            {"fields": ("usuario", "empresa", "rol", "activo")},
        ),
        ("Información de Contacto", {"fields": ("telefono", "direccion")}),
        (
            "Metadatos",
            {
                "fields": ("fecha_vinculacion", "ultima_actividad"),
                "classes": ("collapse",),
            },
        ),
    )

    # Acciones personalizadas
    actions = ["activar_perfiles", "desactivar_perfiles", "cambiar_a_operador"]

    def usuario_nombre(self, obj):
        """Mostrar nombre completo del usuario"""
        return obj.usuario.get_full_name() or obj.usuario.email

    usuario_nombre.short_description = "Usuario"
    usuario_nombre.admin_order_field = "usuario__first_name"

    def activar_perfiles(self, request, queryset):
        """Activar perfiles seleccionados"""
        count = queryset.update(activo=True)
        self.message_user(request, f"{count} perfiles activados exitosamente.")

    activar_perfiles.short_description = "Activar perfiles seleccionados"

    def desactivar_perfiles(self, request, queryset):
        """Desactivar perfiles seleccionados"""
        count = queryset.update(activo=False)
        self.message_user(
            request, f"{count} perfiles desactivados exitosamente."
        )

    desactivar_perfiles.short_description = "Desactivar perfiles seleccionados"

    def cambiar_a_operador(self, request, queryset):
        """Cambiar rol a operador"""
        count = queryset.update(rol=PerfilUsuario.RolChoices.OPERADOR_MIAMI)
        self.message_user(
            request, f"{count} perfiles cambiados a Operador Miami."
        )

    cambiar_a_operador.short_description = "Cambiar a Operador Miami"
