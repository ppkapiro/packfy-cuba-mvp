# 🇨🇺 PACKFY CUBA - API Views para Notificaciones Push
import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .push_notifications import (
    NotificationLog,
    NotificationTemplate,
    PushSubscription,
    push_service,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class PushSubscriptionView(View):
    """Vista para manejar suscripciones push"""

    @method_decorator(login_required)
    def post(self, request):
        """Registrar nueva suscripción push"""
        try:
            data = json.loads(request.body)
            subscription_data = data.get("subscription")
            browser_info = data.get("browserInfo", {})

            if not subscription_data:
                return JsonResponse(
                    {"error": "Datos de suscripción requeridos"}, status=400
                )

            # Validar formato de suscripción
            required_fields = ["endpoint", "keys"]
            if not all(
                field in subscription_data for field in required_fields
            ):
                return JsonResponse(
                    {"error": "Formato de suscripción inválido"}, status=400
                )

            keys = subscription_data["keys"]
            if not all(key in keys for key in ["p256dh", "auth"]):
                return JsonResponse(
                    {"error": "Claves de suscripción requeridas"}, status=400
                )

            # Registrar suscripción
            subscription = push_service.register_subscription(
                user=request.user,
                subscription_data=subscription_data,
                browser_info=browser_info,
            )

            # Enviar notificación de bienvenida
            try:
                push_service.send_notification(
                    user=request.user,
                    notification_type="welcome",
                    context={
                        "username": request.user.first_name
                        or request.user.username,
                        "id": "welcome",
                    },
                )
            except Exception as e:
                logger.warning(f"Error sending welcome notification: {e}")

            return JsonResponse(
                {
                    "success": True,
                    "message": "Suscripción registrada exitosamente",
                    "subscription_id": subscription.id,
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos JSON inválidos"}, status=400)
        except Exception as e:
            logger.error(f"Error registering push subscription: {e}")
            return JsonResponse(
                {"error": "Error interno del servidor"}, status=500
            )

    @method_decorator(login_required)
    def delete(self, request):
        """Desregistrar suscripción push"""
        try:
            data = json.loads(request.body)
            endpoint = data.get("endpoint")

            if not endpoint:
                return JsonResponse(
                    {"error": "Endpoint requerido"}, status=400
                )

            success = push_service.unregister_subscription(
                user=request.user, endpoint=endpoint
            )

            if success:
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Suscripción eliminada exitosamente",
                    }
                )
            else:
                return JsonResponse(
                    {"error": "Suscripción no encontrada"}, status=404
                )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos JSON inválidos"}, status=400)
        except Exception as e:
            logger.error(f"Error unregistering push subscription: {e}")
            return JsonResponse(
                {"error": "Error interno del servidor"}, status=500
            )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_vapid_public_key(request):
    """Obtener clave pública VAPID para el cliente"""
    from django.conf import settings

    vapid_public_key = getattr(settings, "VAPID_PUBLIC_KEY", None)

    if not vapid_public_key:
        return Response(
            {"error": "VAPID no configurado"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({"publicKey": vapid_public_key})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_subscriptions(request):
    """Obtener suscripciones del usuario actual"""
    subscriptions = PushSubscription.objects.filter(
        user=request.user, is_active=True
    ).values("id", "endpoint", "browser_info", "created_at", "last_used")

    return Response(
        {"subscriptions": list(subscriptions), "count": len(subscriptions)}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def test_notification(request):
    """Enviar notificación de prueba al usuario actual"""
    try:
        success = push_service.send_notification(
            user=request.user,
            notification_type="welcome",
            context={
                "username": request.user.first_name or request.user.username,
                "id": "test",
                "timestamp": "ahora",
            },
        )

        if success:
            return Response(
                {"success": True, "message": "Notificación de prueba enviada"}
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "No se pudo enviar la notificación",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        logger.error(f"Error sending test notification: {e}")
        return Response(
            {"error": "Error enviando notificación de prueba"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notification_history(request):
    """Obtener historial de notificaciones del usuario"""
    page_size = int(request.GET.get("page_size", 20))
    page = int(request.GET.get("page", 1))

    offset = (page - 1) * page_size

    notifications = (
        NotificationLog.objects.filter(user=request.user)
        .select_related("subscription")
        .order_by("-created_at")[offset : offset + page_size]
    )

    total_count = NotificationLog.objects.filter(user=request.user).count()

    notification_data = []
    for notification in notifications:
        notification_data.append(
            {
                "id": notification.id,
                "type": notification.notification_type,
                "title": notification.title,
                "body": notification.body,
                "status": notification.status,
                "sent_at": notification.sent_at,
                "created_at": notification.created_at,
                "error_message": notification.error_message,
            }
        )

    return Response(
        {
            "notifications": notification_data,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total_count,
                "has_next": offset + page_size < total_count,
            },
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notification_stats(request):
    """Obtener estadísticas de notificaciones del usuario"""
    from datetime import timedelta

    from django.db.models import Count, Q
    from django.utils import timezone

    # Estadísticas de los últimos 30 días
    thirty_days_ago = timezone.now() - timedelta(days=30)

    stats = NotificationLog.objects.filter(
        user=request.user, created_at__gte=thirty_days_ago
    ).aggregate(
        total=Count("id"),
        sent=Count("id", filter=Q(status="sent")),
        failed=Count("id", filter=Q(status="failed")),
        pending=Count("id", filter=Q(status="pending")),
    )

    # Estadísticas por tipo
    type_stats = (
        NotificationLog.objects.filter(
            user=request.user, created_at__gte=thirty_days_ago
        )
        .values("notification_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Suscripciones activas
    active_subscriptions = PushSubscription.objects.filter(
        user=request.user, is_active=True
    ).count()

    return Response(
        {
            "summary": stats,
            "by_type": list(type_stats),
            "active_subscriptions": active_subscriptions,
            "period": "30 días",
        }
    )


# Funciones auxiliares para envío automático de notificaciones


def notify_shipment_status_change(shipment, old_status, new_status):
    """Notificar cambio de estado de envío"""
    try:
        # Obtener usuarios a notificar (remitente y destinatario)
        users_to_notify = []

        if hasattr(shipment, "empresa") and shipment.empresa.usuario:
            users_to_notify.append(shipment.empresa.usuario)

        if hasattr(shipment, "destinatario_email"):
            # Buscar usuario por email si existe
            from django.contrib.auth.models import User

            try:
                destinatario_user = User.objects.get(
                    email=shipment.destinatario_email
                )
                users_to_notify.append(destinatario_user)
            except User.DoesNotExist:
                pass

        # Preparar contexto
        context = {
            "numero_guia": shipment.numero_guia,
            "old_status": old_status,
            "new_status": new_status,
            "destinatario": shipment.destinatario_nombre,
            "peso": shipment.peso_kg,
            "id": shipment.id,
        }

        # Enviar notificaciones
        for user in users_to_notify:
            push_service.send_notification(
                user=user,
                notification_type="shipment_status_update",
                context=context,
                priority=(
                    "high"
                    if new_status in ["entregado", "en_entrega"]
                    else "normal"
                ),
            )

        logger.info(
            f"Status change notifications sent for shipment {shipment.numero_guia}"
        )

    except Exception as e:
        logger.error(f"Error sending shipment status notifications: {e}")


def notify_new_shipment(shipment):
    """Notificar creación de nuevo envío"""
    try:
        if hasattr(shipment, "empresa") and shipment.empresa.usuario:
            context = {
                "numero_guia": shipment.numero_guia,
                "destinatario": shipment.destinatario_nombre,
                "peso": shipment.peso_kg,
                "valor_declarado": shipment.valor_declarado_usd,
                "id": shipment.id,
            }

            push_service.send_notification(
                user=shipment.empresa.usuario,
                notification_type="shipment_created",
                context=context,
            )

        logger.info(
            f"New shipment notification sent for {shipment.numero_guia}"
        )

    except Exception as e:
        logger.error(f"Error sending new shipment notification: {e}")


def notify_delivery_reminder(shipment):
    """Notificar recordatorio de entrega"""
    try:
        users_to_notify = []

        # Notificar a la empresa
        if hasattr(shipment, "empresa") and shipment.empresa.usuario:
            users_to_notify.append(shipment.empresa.usuario)

        # Notificar al destinatario si tiene cuenta
        if hasattr(shipment, "destinatario_email"):
            from django.contrib.auth.models import User

            try:
                destinatario_user = User.objects.get(
                    email=shipment.destinatario_email
                )
                users_to_notify.append(destinatario_user)
            except User.DoesNotExist:
                pass

        context = {
            "numero_guia": shipment.numero_guia,
            "destinatario": shipment.destinatario_nombre,
            "direccion": getattr(
                shipment, "direccion_entrega", "No especificada"
            ),
            "fecha_estimada": getattr(
                shipment, "fecha_entrega_estimada", "Hoy"
            ),
            "id": shipment.id,
        }

        for user in users_to_notify:
            push_service.send_notification(
                user=user,
                notification_type="delivery_reminder",
                context=context,
                priority="high",
            )

        logger.info(
            f"Delivery reminder sent for shipment {shipment.numero_guia}"
        )

    except Exception as e:
        logger.error(f"Error sending delivery reminder: {e}")
