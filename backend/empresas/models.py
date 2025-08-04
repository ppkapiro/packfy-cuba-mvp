from django.db import models

class Empresa(models.Model):
    """
    Modelo para representar una empresa en el sistema.
    """
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    dominio = models.CharField(max_length=100, blank=True, null=True)
    
    # Campos para el seguimiento de cambios
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre
