from django.contrib import admin
from .models import Envio, HistorialEstado

class HistorialEstadoInline(admin.TabularInline):
    model = HistorialEstado
    extra = 0
    readonly_fields = ('fecha',)
    fields = ('estado', 'comentario', 'ubicacion', 'registrado_por', 'fecha')
    can_delete = False  # No permitir eliminar registros de historial
    
    def has_add_permission(self, request, obj=None):
        return True  # Permitir agregar nuevos estados
    
@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ('numero_guia', 'remitente_nombre', 'destinatario_nombre', 'estado_actual', 'fecha_creacion', 'fecha_estimada_entrega')
    list_filter = ('estado_actual', 'fecha_creacion')
    search_fields = ('numero_guia', 'remitente_nombre', 'remitente_telefono', 'destinatario_nombre', 'destinatario_telefono', 'descripcion')
    readonly_fields = ('numero_guia', 'fecha_creacion', 'ultima_actualizacion', 'creado_por', 'actualizado_por')
    inlines = [HistorialEstadoInline]
    
    fieldsets = (
        ('Información de Seguimiento', {
            'fields': ('numero_guia', 'estado_actual', 'fecha_creacion', 'fecha_estimada_entrega')
        }),
        ('Datos del Paquete', {
            'fields': ('descripcion', 'peso', 'valor_declarado')
        }),
        ('Datos del Remitente', {
            'fields': ('remitente_nombre', 'remitente_direccion', 'remitente_telefono', 'remitente_email')
        }),
        ('Datos del Destinatario', {
            'fields': ('destinatario_nombre', 'destinatario_direccion', 'destinatario_telefono', 'destinatario_email')
        }),
        ('Notas y Metadatos', {
            'fields': ('notas', 'creado_por', 'actualizado_por', 'ultima_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una creación nueva
            obj.creado_por = request.user
        obj.actualizado_por = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, HistorialEstado):
                if not instance.registrado_por:  # Si no tiene usuario asignado
                    instance.registrado_por = request.user
            instance.save()
        formset.save_m2m()

@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ('envio', 'estado', 'fecha', 'registrado_por')
    list_filter = ('estado', 'fecha')
    search_fields = ('envio__numero_guia', 'comentario', 'ubicacion')
    readonly_fields = ('fecha',)
    
    def has_add_permission(self, request):
        # Desactivar la creación directa de historiales (deben crearse a través del Envio)
        return False
