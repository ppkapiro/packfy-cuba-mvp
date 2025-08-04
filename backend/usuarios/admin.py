from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Personalización del panel de admin para los usuarios
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'telefono', 'es_administrador_empresa', 'is_staff', 'is_active')
    list_filter = ('es_administrador_empresa', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'telefono')
    readonly_fields = ('fecha_creacion', 'ultima_actualizacion')
    
    # Agrupaciones de campos en el formulario
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'telefono', 'cargo', 'foto_perfil')}),
        ('Permisos', {'fields': ('es_administrador_empresa', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined', 'fecha_creacion', 'ultima_actualizacion')}),
    )
    
    # Formulario para la creación de nuevos usuarios
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff')}
        ),
    )
