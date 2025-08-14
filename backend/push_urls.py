# 🇨🇺 PACKFY CUBA - URLs para Sistema de Notificaciones Push
from django.urls import path

from . import push_views

app_name = "push_notifications"

urlpatterns = [
    # Gestión de suscripciones
    path(
        "subscribe/",
        push_views.PushSubscriptionView.as_view(),
        name="push_subscribe",
    ),
    # Configuración VAPID
    path("vapid-key/", push_views.get_vapid_public_key, name="vapid_key"),
    # Gestión de usuario
    path(
        "subscriptions/",
        push_views.get_user_subscriptions,
        name="user_subscriptions",
    ),
    path("test/", push_views.test_notification, name="test_notification"),
    # Historial y estadísticas
    path(
        "history/",
        push_views.get_notification_history,
        name="notification_history",
    ),
    path(
        "stats/", push_views.get_notification_stats, name="notification_stats"
    ),
]
