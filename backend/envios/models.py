from django.db import models
from django.utils.translation import gettext_lazy as _
from usuarios.models import Usuario


class Envio(models.Model):
    """
    Modelo para gestionar los envíos de paquetes
    """

    # Opciones para los estados
    class EstadoChoices(models.TextChoices):
        RECIBIDO = "RECIBIDO", _("Recibido")
        EN_TRANSITO = "EN_TRANSITO", _("En tránsito")
        EN_REPARTO = "EN_REPARTO", _("En reparto")
        ENTREGADO = "ENTREGADO", _("Entregado")
        DEVUELTO = "DEVUELTO", _("Devuelto")
        CANCELADO = "CANCELADO", _("Cancelado")

    # Campos de seguimiento
    numero_guia = models.CharField(max_length=20, unique=True)
    estado_actual = models.CharField(
        max_length=20, choices=EstadoChoices.choices, default=EstadoChoices.RECIBIDO
    )

    # Campos de fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_estimada_entrega = models.DateField(null=True, blank=True)

    # Datos del paquete
    descripcion = models.TextField()
    peso = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Peso en libras"
    )
    valor_declarado = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Datos del remitente
    remitente_nombre = models.CharField(max_length=100)
    remitente_direccion = models.TextField()
    remitente_telefono = models.CharField(max_length=20)
    remitente_email = models.EmailField(null=True, blank=True)

    # Datos del destinatario
    destinatario_nombre = models.CharField(max_length=100)
    destinatario_direccion = models.TextField()
    destinatario_telefono = models.CharField(max_length=20)
    destinatario_email = models.EmailField(null=True, blank=True)

    # Metadata y relaciones
    notas = models.TextField(null=True, blank=True)
    creado_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name="envios_creados"
    )
    actualizado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name="envios_actualizados",
    )
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Envío #{self.numero_guia} - {self.estado_actual}"

    def save(self, *args, **kwargs):
        if not self.numero_guia:
            # Generar un número de guía si no existe
            ultimo_envio = Envio.objects.order_by("-id").first()
            ultimo_id = ultimo_envio.id if ultimo_envio else 0
            self.numero_guia = f"PKF{ultimo_id + 1:08d}"

        super().save(*args, **kwargs)


class HistorialEstado(models.Model):
    """
    Modelo para registrar los cambios de estado de un envío
    """

    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="historial")
    estado = models.CharField(max_length=20, choices=Envio.EstadoChoices.choices)
    comentario = models.TextField(null=True, blank=True)
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Historial de Estado"
        verbose_name_plural = "Historial de Estados"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.envio.numero_guia} - {self.estado} - {self.fecha}"
