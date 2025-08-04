from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ruc', 'email', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'ruc', 'email')
    readonly_fields = ('fecha_creacion', 'ultima_actualizacion')
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'ruc')
        }),
        ('Información de Contacto', {
            'fields': ('direccion', 'telefono', 'email', 'logo')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'ultima_actualizacion'),
            'classes': ('collapse',)
        })
    )
