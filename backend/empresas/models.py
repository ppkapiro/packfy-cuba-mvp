import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Empresa(models.Model):
    """
    Modelo para representar una empresa en el sistema multi-tenant.
    Cada empresa opera de forma completamente independiente.
    """

    # Mantenemos el ID auto-generado por simplicidad en la migración
    # En futuras versiones se puede migrar a UUID

    # Identificadores únicos
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Identificador único para URLs",
        null=True,
        blank=True,  # Permitir null temporalmente para migración
    )

    # Información básica
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    # Estado y configuración
    activo = models.BooleanField(
        default=True, help_text="Empresa activa en el sistema"
    )
    dominio = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Dominio personalizado (futuro)",
    )
    configuracion = models.JSONField(
        default=dict,
        blank=True,
        help_text="Configuraciones específicas de la empresa",
    )

    # Campos para el seguimiento de cambios
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["nombre"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class PerfilUsuario(models.Model):
    """
    Perfil extendido de usuario con información de empresa y rol.
    Conecta usuarios de Django con empresas y define sus roles.
    """

    class RolChoices(models.TextChoices):
        DUENO = "dueno", "Dueño"
        OPERADOR_MIAMI = "operador_miami", "Operador Miami"
        OPERADOR_CUBA = "operador_cuba", "Operador Cuba"
        REMITENTE = "remitente", "Remitente"
        DESTINATARIO = "destinatario", "Destinatario"

    # Relaciones principales
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="usuarios"
    )

    # Información del rol
    rol = models.CharField(max_length=20, choices=RolChoices.choices)
    activo = models.BooleanField(
        default=True, help_text="Usuario activo en la empresa"
    )

    # Información adicional
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    # Fechas importantes
    fecha_vinculacion = models.DateTimeField(auto_now_add=True)
    ultima_actividad = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        unique_together = [
            "usuario",
            "empresa",
        ]  # Un usuario solo puede tener un rol por empresa
        ordering = ["empresa__nombre", "rol", "usuario__first_name"]

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.get_rol_display()} ({self.empresa.nombre})"

    @property
    def es_dueno(self):
        return self.rol == self.RolChoices.DUENO

    @property
    def es_operador(self):
        return self.rol in [
            self.RolChoices.OPERADOR_MIAMI,
            self.RolChoices.OPERADOR_CUBA,
        ]

    @property
    def es_cliente(self):
        return self.rol in [
            self.RolChoices.REMITENTE,
            self.RolChoices.DESTINATARIO,
        ]

    @property
    def puede_gestionar_empresa(self):
        return self.rol == self.RolChoices.DUENO

    @property
    def puede_gestionar_envios(self):
        return self.rol in [
            self.RolChoices.DUENO,
            self.RolChoices.OPERADOR_MIAMI,
            self.RolChoices.OPERADOR_CUBA,
        ]
