# 🇨🇺 PACKFY CUBA - Sistema de Notificaciones Push
import json
import logging
from typing import Dict, List, Optional

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from pywebpush import WebPushException, webpush

logger = logging.getLogger(__name__)


class PushSubscription(models.Model):
    """Modelo para almacenar suscripciones a notificaciones push"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="push_subscriptions"
    )
    endpoint = models.URLField(max_length=500)
    p256dh_key = models.CharField(max_length=255)
    auth_key = models.CharField(max_length=255)
    browser_info = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "push_subscriptions"
        unique_together = ["user", "endpoint"]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Push subscription for {self.user.username}"

    def to_dict(self) -> Dict:
        """Convierte la suscripción al formato requerido por pywebpush"""
        return {
            "endpoint": self.endpoint,
            "keys": {"p256dh": self.p256dh_key, "auth": self.auth_key},
        }


class NotificationTemplate(models.Model):
    """Plantillas para diferentes tipos de notificaciones"""

    NOTIFICATION_TYPES = [
        ("shipment_created", "Envío Creado"),
        ("shipment_status_update", "Actualización de Estado"),
        ("shipment_delivered", "Envío Entregado"),
        ("delivery_reminder", "Recordatorio de Entrega"),
        ("payment_required", "Pago Requerido"),
        ("system_maintenance", "Mantenimiento del Sistema"),
        ("promotion", "Promoción"),
        ("welcome", "Bienvenida"),
    ]

    type = models.CharField(
        max_length=30, choices=NOTIFICATION_TYPES, unique=True
    )
    title_template = models.CharField(max_length=200)
    body_template = models.TextField()
    icon_url = models.URLField(blank=True)
    action_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    require_interaction = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification_templates"

    def __str__(self):
        return f"Template: {self.get_type_display()}"

    def render(self, context: Dict) -> Dict:
        """Renderiza la plantilla con el contexto proporcionado"""
        try:
            title = self.title_template.format(**context)
            body = self.body_template.format(**context)

            notification_data = {
                "title": title,
                "body": body,
                "icon": self.icon_url or "/icons/icon-192.svg",
                "badge": "/icons/badge-72x72.png",
                "tag": f"{self.type}-{context.get('id', 'default')}",
                "requireInteraction": self.require_interaction,
                "data": {
                    "type": self.type,
                    "url": (
                        self.action_url.format(**context)
                        if self.action_url
                        else "/"
                    ),
                    "timestamp": timezone.now().isoformat(),
                    **context,
                },
            }

            # Agregar acciones según el tipo
            notification_data["actions"] = self._get_actions_for_type(context)

            return notification_data

        except KeyError as e:
            logger.error(
                f"Error rendering notification template {self.type}: Missing key {e}"
            )
            return self._get_fallback_notification(context)

    def _get_actions_for_type(self, context: Dict) -> List[Dict]:
        """Obtiene las acciones específicas según el tipo de notificación"""
        actions_map = {
            "shipment_status_update": [
                {
                    "action": "track",
                    "title": "Rastrear",
                    "icon": "/icons/track-action.png",
                },
                {
                    "action": "view",
                    "title": "Ver Detalles",
                    "icon": "/icons/view-action.png",
                },
            ],
            "delivery_reminder": [
                {
                    "action": "confirm",
                    "title": "Confirmar",
                    "icon": "/icons/confirm-action.png",
                },
                {
                    "action": "reschedule",
                    "title": "Reprogramar",
                    "icon": "/icons/reschedule-action.png",
                },
            ],
            "payment_required": [
                {
                    "action": "pay",
                    "title": "Pagar Ahora",
                    "icon": "/icons/pay-action.png",
                },
                {
                    "action": "view",
                    "title": "Ver Detalles",
                    "icon": "/icons/view-action.png",
                },
            ],
        }

        return actions_map.get(
            self.type,
            [
                {
                    "action": "view",
                    "title": "Ver",
                    "icon": "/icons/view-action.png",
                }
            ],
        )

    def _get_fallback_notification(self, context: Dict) -> Dict:
        """Notificación de respaldo en caso de error"""
        return {
            "title": "PACKFY CUBA",
            "body": "Nueva notificación disponible",
            "icon": "/icons/icon-192.svg",
            "badge": "/icons/badge-72x72.png",
            "tag": f"{self.type}-fallback",
            "data": {"type": self.type, "url": "/", **context},
        }


class NotificationLog(models.Model):
    """Log de notificaciones enviadas"""

    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("sent", "Enviada"),
        ("failed", "Fallida"),
        ("expired", "Expirada"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        PushSubscription, on_delete=models.SET_NULL, null=True, blank=True
    )
    notification_type = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    body = models.TextField()
    payload = models.JSONField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification_logs"
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["notification_type", "created_at"]),
            models.Index(fields=["sent_at"]),
        ]

    def __str__(self):
        return f"Notification {self.id} - {self.user.username} - {self.status}"


class PushNotificationService:
    """Servicio principal para manejo de notificaciones push"""

    def __init__(self):
        self.vapid_private_key = getattr(settings, "VAPID_PRIVATE_KEY", None)
        self.vapid_public_key = getattr(settings, "VAPID_PUBLIC_KEY", None)
        self.vapid_claims = {
            "sub": f"mailto:{getattr(settings, 'VAPID_ADMIN_EMAIL', 'admin@packfycuba.com')}"
        }

    def send_notification(
        self,
        user: User,
        notification_type: str,
        context: Dict,
        priority: str = "normal",
    ) -> bool:
        """
        Envía una notificación push a un usuario específico

        Args:
            user: Usuario destinatario
            notification_type: Tipo de notificación
            context: Contexto para renderizar la plantilla
            priority: Prioridad de la notificación ('high', 'normal', 'low')

        Returns:
            bool: True si se envió exitosamente, False en caso contrario
        """
        try:
            # Obtener plantilla
            template = NotificationTemplate.objects.get(
                type=notification_type, is_active=True
            )
        except NotificationTemplate.DoesNotExist:
            logger.error(
                f"No template found for notification type: {notification_type}"
            )
            return False

        # Renderizar notificación
        notification_data = template.render(context)

        # Obtener suscripciones activas del usuario
        subscriptions = PushSubscription.objects.filter(
            user=user, is_active=True
        )

        if not subscriptions.exists():
            logger.warning(
                f"No active push subscriptions for user: {user.username}"
            )
            return False

        # Enviar a cada suscripción
        success_count = 0
        total_count = subscriptions.count()

        for subscription in subscriptions:
            if self._send_to_subscription(
                subscription, notification_data, template, priority
            ):
                success_count += 1

        logger.info(
            f"Push notification sent: {success_count}/{total_count} successful "
            f"for user {user.username}, type {notification_type}"
        )

        return success_count > 0

    def send_bulk_notification(
        self,
        users: List[User],
        notification_type: str,
        context: Dict,
        priority: str = "normal",
    ) -> Dict[str, int]:
        """
        Envía notificación a múltiples usuarios

        Returns:
            Dict con estadísticas de envío
        """
        stats = {"sent": 0, "failed": 0, "no_subscription": 0}

        for user in users:
            try:
                if self.send_notification(
                    user, notification_type, context, priority
                ):
                    stats["sent"] += 1
                else:
                    # Verificar si el usuario tiene suscripciones
                    if PushSubscription.objects.filter(
                        user=user, is_active=True
                    ).exists():
                        stats["failed"] += 1
                    else:
                        stats["no_subscription"] += 1
            except Exception as e:
                logger.error(
                    f"Error sending bulk notification to {user.username}: {e}"
                )
                stats["failed"] += 1

        return stats

    def _send_to_subscription(
        self,
        subscription: PushSubscription,
        notification_data: Dict,
        template: NotificationTemplate,
        priority: str,
    ) -> bool:
        """Envía notificación a una suscripción específica"""

        # Crear log de notificación
        log_entry = NotificationLog.objects.create(
            user=subscription.user,
            subscription=subscription,
            notification_type=template.type,
            title=notification_data["title"],
            body=notification_data["body"],
            payload=notification_data,
        )

        try:
            # Configurar headers adicionales
            headers = {
                "TTL": "86400",  # 24 horas
                "Content-Encoding": "gzip",
            }

            if priority == "high":
                headers["Urgency"] = "high"
            elif priority == "low":
                headers["Urgency"] = "low"

            # Enviar notificación
            webpush(
                subscription_info=subscription.to_dict(),
                data=json.dumps(notification_data),
                vapid_private_key=self.vapid_private_key,
                vapid_claims=self.vapid_claims,
                headers=headers,
            )

            # Actualizar log como exitoso
            log_entry.status = "sent"
            log_entry.sent_at = timezone.now()
            log_entry.save()

            # Actualizar última vez usado de la suscripción
            subscription.last_used = timezone.now()
            subscription.save(update_fields=["last_used"])

            return True

        except WebPushException as e:
            error_msg = str(e)
            logger.error(
                f"WebPush error for subscription {subscription.id}: {error_msg}"
            )

            # Manejar errores específicos
            if e.response and e.response.status_code in [410, 413, 404]:
                # Suscripción expirada o inválida
                subscription.is_active = False
                subscription.save()
                log_entry.status = "expired"
            else:
                log_entry.status = "failed"

            log_entry.error_message = error_msg
            log_entry.save()
            return False

        except Exception as e:
            error_msg = str(e)
            logger.error(
                f"Unexpected error sending push notification: {error_msg}"
            )

            log_entry.status = "failed"
            log_entry.error_message = error_msg
            log_entry.save()
            return False

    def register_subscription(
        self, user: User, subscription_data: Dict, browser_info: Dict = None
    ) -> PushSubscription:
        """Registra una nueva suscripción push"""

        subscription, created = PushSubscription.objects.get_or_create(
            user=user,
            endpoint=subscription_data["endpoint"],
            defaults={
                "p256dh_key": subscription_data["keys"]["p256dh"],
                "auth_key": subscription_data["keys"]["auth"],
                "browser_info": browser_info or {},
                "is_active": True,
            },
        )

        if not created and not subscription.is_active:
            # Reactivar suscripción existente
            subscription.is_active = True
            subscription.p256dh_key = subscription_data["keys"]["p256dh"]
            subscription.auth_key = subscription_data["keys"]["auth"]
            subscription.browser_info = browser_info or {}
            subscription.save()

        logger.info(
            f"Push subscription {'created' if created else 'updated'} for user {user.username}"
        )
        return subscription

    def unregister_subscription(self, user: User, endpoint: str) -> bool:
        """Desregistra una suscripción push"""
        try:
            subscription = PushSubscription.objects.get(
                user=user, endpoint=endpoint
            )
            subscription.is_active = False
            subscription.save()

            logger.info(
                f"Push subscription unregistered for user {user.username}"
            )
            return True
        except PushSubscription.DoesNotExist:
            return False

    def cleanup_expired_subscriptions(self, days: int = 30) -> int:
        """Limpia suscripciones no utilizadas en X días"""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)

        expired_count = PushSubscription.objects.filter(
            last_used__lt=cutoff_date, is_active=True
        ).update(is_active=False)

        logger.info(f"Deactivated {expired_count} expired push subscriptions")
        return expired_count


# Instancia global del servicio
push_service = PushNotificationService()
