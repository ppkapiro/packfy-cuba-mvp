# 🇨🇺 PACKFY CUBA - URLs de Inteligencia Artificial v4.0
from django.urls import path

from .ai_views import (
    ChatbotView,
    detect_shipment_anomalies,
    optimize_delivery_route,
    predict_delivery_time,
    predict_demand,
)

app_name = "ai"

urlpatterns = [
    # 🤖 Chatbot endpoints
    path("chatbot/", ChatbotView.as_view(), name="chatbot"),
    # 🔮 Predicción de tiempo de entrega
    path(
        "predict-delivery-time/",
        predict_delivery_time,
        name="predict_delivery_time",
    ),
    # 📈 Predicción de demanda
    path("predict-demand/", predict_demand, name="predict_demand"),
    # 🗺️ Optimización de rutas
    path("optimize-route/", optimize_delivery_route, name="optimize_route"),
    # ⚠️ Detección de anomalías
    path(
        "detect-anomalies/", detect_shipment_anomalies, name="detect_anomalies"
    ),
]
