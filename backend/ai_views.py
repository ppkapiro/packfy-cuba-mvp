# 🇨🇺 PACKFY CUBA - API Views para Automation & AI v4.0
import json
import logging
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .chatbot import packfy_chatbot

# from .ai_system import ai_predictor  # Commented out due to sklearn dependencies

logger = logging.getLogger(__name__)

# ===============================
# CHATBOT API VIEWS
# ===============================


@method_decorator(csrf_exempt, name="dispatch")
class ChatbotView(View):
    """Vista principal para interacción con el chatbot"""

    def post(self, request):
        """Procesar mensaje del chatbot"""
        try:
            data = json.loads(request.body)
            message = data.get("message", "").strip()
            user_id = (
                data.get("user_id")
                or f"guest_{request.session.session_key or 'anonymous'}"
            )
            context = data.get("context", {})

            if not message:
                return JsonResponse({"error": "Mensaje requerido"}, status=400)

            # Agregar contexto del usuario si está autenticado
            if request.user.is_authenticated:
                context.update(
                    {
                        "user_authenticated": True,
                        "username": request.user.username,
                        "user_id": request.user.id,
                    }
                )
                user_id = f"user_{request.user.id}"

            # Procesar mensaje con el chatbot
            response = packfy_chatbot.process_message(
                user_id, message, context
            )

            return JsonResponse({"success": True, "response": response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos JSON inválidos"}, status=400)
        except Exception as e:
            logger.error(f"Error in chatbot view: {e}")
            return JsonResponse(
                {"error": "Error interno del servidor"}, status=500
            )


@api_view(["GET"])
@permission_classes([AllowAny])
def chatbot_health(request):
    """Verificar estado del chatbot"""
    try:
        # Probar respuesta básica del chatbot
        test_response = packfy_chatbot.process_message("health_check", "hola")

        return Response(
            {
                "status": "healthy",
                "chatbot_active": True,
                "knowledge_base_intents": len(packfy_chatbot.intent_patterns),
                "active_sessions": len(packfy_chatbot.user_sessions),
                "test_response": test_response.get("text", "OK"),
            }
        )
    except Exception as e:
        logger.error(f"Chatbot health check failed: {e}")
        return Response({"status": "unhealthy", "error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chatbot_conversation_history(request):
    """Obtener historial de conversación del usuario"""
    try:
        user_id = f"user_{request.user.id}"
        summary = packfy_chatbot.get_conversation_summary(user_id)

        if "error" in summary:
            return Response({"messages": [], "summary": {"total_messages": 0}})

        # Obtener mensajes de la sesión si existe
        session = packfy_chatbot.user_sessions.get(user_id, {})
        messages = session.get("messages", [])

        # Formatear mensajes para la respuesta
        formatted_messages = []
        for msg in messages[-20:]:  # Últimos 20 mensajes
            formatted_messages.append(
                {
                    "type": msg["type"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"].isoformat(),
                    "intent": msg.get("intent"),
                    "confidence": msg.get("confidence"),
                }
            )

        return Response({"messages": formatted_messages, "summary": summary})

    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        return Response({"error": "Error obteniendo historial"}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chatbot_clear_session(request):
    """Limpiar sesión de chatbot del usuario"""
    try:
        user_id = f"user_{request.user.id}"

        if user_id in packfy_chatbot.user_sessions:
            del packfy_chatbot.user_sessions[user_id]

        return Response(
            {"success": True, "message": "Sesión limpiada exitosamente"}
        )

    except Exception as e:
        logger.error(f"Error clearing chatbot session: {e}")
        return Response({"error": "Error limpiando sesión"}, status=500)


# ===============================
# AI PREDICTION API VIEWS
# ===============================


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def predict_delivery_time(request):
    """Predecir tiempo de entrega usando IA"""
    try:
        data = request.data

        required_fields = ["origin", "destination", "weight"]
        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"Campo requerido: {field}"}, status=400
                )

        # Usar predicción básica cuando sklearn no está disponible
        prediction = calculate_basic_delivery_time(
            origin=data["origin"],
            destination=data["destination"],
            weight=float(data["weight"]),
            package_type=data.get("package_type", "paquete"),
            priority=data.get("priority", "normal"),
        )

        return Response(
            {
                "prediction": prediction,
                "method": "basic_calculation",
                "timestamp": datetime.now().isoformat(),
            }
        )

    except ValueError as e:
        return Response({"error": f"Valor inválido: {e}"}, status=400)
    except Exception as e:
        logger.error(f"Error predicting delivery time: {e}")
        return Response({"error": "Error en predicción"}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def optimize_delivery_route(request):
    """Optimizar ruta de entregas"""
    try:
        deliveries = request.data.get("deliveries", [])

        if not deliveries:
            return Response(
                {"error": "Lista de entregas requerida"}, status=400
            )

        # Optimización básica por prioridad y ubicación
        optimized = optimize_basic_route(deliveries)

        return Response(
            {
                "optimized_route": optimized,
                "optimization_method": "priority_location_based",
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"Error optimizing route: {e}")
        return Response({"error": "Error optimizando ruta"}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def detect_shipment_anomalies(request):
    """Detectar anomalías en datos de envío"""
    try:
        shipment_data = request.data

        # Análisis básico de anomalías
        anomalies = detect_basic_anomalies(shipment_data)

        return Response(
            {"anomalies": anomalies, "timestamp": datetime.now().isoformat()}
        )

    except Exception as e:
        logger.error(f"Error detecting anomalies: {e}")
        return Response({"error": "Error detectando anomalías"}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def predict_demand(request):
    """Predecir demanda de envíos"""
    try:
        location = request.GET.get("location", "la_habana")
        days = int(request.GET.get("days", 7))

        # Predicción básica de demanda
        prediction = predict_basic_demand(location, days)

        return Response(
            {
                "prediction": prediction,
                "method": "historical_average",
                "timestamp": datetime.now().isoformat(),
            }
        )

    except ValueError as e:
        return Response({"error": f"Parámetro inválido: {e}"}, status=400)
    except Exception as e:
        logger.error(f"Error predicting demand: {e}")
        return Response({"error": "Error prediciendo demanda"}, status=500)


# ===============================
# FUNCIONES AUXILIARES
# ===============================


def calculate_basic_delivery_time(
    origin: str,
    destination: str,
    weight: float,
    package_type: str,
    priority: str,
) -> dict:
    """Cálculo básico de tiempo de entrega sin ML"""

    # Tiempos base por provincia (en horas)
    delivery_times = {
        "la_habana": 24,
        "santiago_de_cuba": 48,
        "camaguey": 36,
        "holguin": 42,
        "guantanamo": 54,
        "villa_clara": 30,
        "cienfuegos": 32,
        "matanzas": 26,
        "pinar_del_rio": 36,
        "sancti_spiritus": 34,
        "ciego_de_avila": 38,
        "las_tunas": 44,
        "granma": 48,
        "artemisa": 28,
        "mayabeque": 28,
    }

    # Tiempo base
    dest_key = destination.lower().replace(" ", "_")
    base_time = delivery_times.get(dest_key, 36)  # 36h por defecto

    # Ajustes por peso
    if weight > 10:
        base_time += 12
    elif weight > 25:
        base_time += 24

    # Ajustes por tipo de paquete
    if package_type == "documento":
        base_time *= 0.8
    elif package_type == "caja":
        base_time *= 1.2

    # Ajustes por prioridad
    priority_multipliers = {
        "urgent": 0.5,
        "express": 0.7,
        "normal": 1.0,
        "economy": 1.5,
    }
    base_time *= priority_multipliers.get(priority, 1.0)

    # Considerar día de la semana
    now = datetime.now()
    if now.weekday() >= 5:  # Fin de semana
        base_time += 24

    estimated_hours = max(6, int(base_time))  # Mínimo 6 horas

    return {
        "estimated_hours": estimated_hours,
        "estimated_days": max(1, estimated_hours // 24),
        "confidence": 0.75,
        "factors": {
            "base_time": delivery_times.get(dest_key, 36),
            "weight_adjustment": weight > 10,
            "priority": priority,
            "weekend_delay": now.weekday() >= 5,
        },
    }


def optimize_basic_route(deliveries: list) -> dict:
    """Optimización básica de rutas"""

    # Separar por prioridad
    priority_order = {"urgent": 0, "express": 1, "normal": 2, "economy": 3}

    sorted_deliveries = sorted(
        deliveries,
        key=lambda x: (
            priority_order.get(x.get("priority", "normal"), 2),
            x.get("destination", "").lower(),
        ),
    )

    # Calcular métricas básicas
    total_deliveries = len(sorted_deliveries)
    estimated_time = total_deliveries * 30  # 30 min por entrega

    # Agregar tiempo de viaje entre destinos
    unique_destinations = len(
        set(d.get("destination", "") for d in sorted_deliveries)
    )
    travel_time = unique_destinations * 45  # 45 min entre destinos

    return {
        "optimized_route": sorted_deliveries,
        "total_deliveries": total_deliveries,
        "total_destinations": unique_destinations,
        "estimated_time_minutes": estimated_time + travel_time,
        "optimization_score": 0.8,  # Score fijo para optimización básica
        "recommendations": [
            "Ruta optimizada por prioridad y ubicación",
            f"Tiempo estimado total: {(estimated_time + travel_time) // 60}h {(estimated_time + travel_time) % 60}m",
        ],
    }


def detect_basic_anomalies(shipment_data: dict) -> dict:
    """Detección básica de anomalías sin ML"""

    anomalies = []
    risk_score = 0

    # Verificar peso vs valor
    weight = shipment_data.get("weight", 0)
    declared_value = shipment_data.get("declared_value", 0)

    if weight > 20 and declared_value < 50:
        anomalies.append(
            {
                "type": "value_weight_mismatch",
                "severity": "medium",
                "description": f"Peso alto ({weight}kg) con valor bajo (${declared_value})",
            }
        )
        risk_score += 30

    # Verificar destino inusual
    destination = shipment_data.get("destination", "").lower()
    common_destinations = ["la_habana", "santiago", "camaguey", "holguin"]

    if not any(city in destination for city in common_destinations):
        anomalies.append(
            {
                "type": "uncommon_destination",
                "severity": "low",
                "description": f"Destino poco común: {destination}",
            }
        )
        risk_score += 10

    # Verificar cantidad de envíos del día
    daily_shipments = shipment_data.get("sender_daily_count", 0)
    if daily_shipments > 15:
        anomalies.append(
            {
                "type": "high_frequency_sender",
                "severity": "high",
                "description": f"Remitente con {daily_shipments} envíos hoy",
            }
        )
        risk_score += 40

    # Determinar nivel de riesgo
    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "anomalies": anomalies,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "requires_review": risk_score >= 35,
        "recommendations": [
            (
                "Verificar documentación del envío"
                if risk_score >= 35
                else "Envío normal"
            ),
            (
                "Contactar remitente para confirmación"
                if risk_score >= 50
                else "Procesar normalmente"
            ),
        ],
    }


def predict_basic_demand(location: str, days: int) -> dict:
    """Predicción básica de demanda"""

    # Factores base por ciudad
    city_factors = {
        "la_habana": 2.5,
        "santiago_de_cuba": 1.8,
        "camaguey": 1.2,
        "holguin": 1.0,
        "villa_clara": 0.9,
        "matanzas": 0.8,
    }

    base_demand = 8  # Envíos base por día
    city_factor = city_factors.get(location.lower().replace(" ", "_"), 0.7)

    predictions = []
    for day in range(1, days + 1):
        future_date = datetime.now() + timedelta(days=day)

        # Ajustes por día de la semana
        weekday_factor = 1.0
        if future_date.weekday() == 0:  # Lunes
            weekday_factor = 1.4
        elif future_date.weekday() in [5, 6]:  # Fin de semana
            weekday_factor = 0.6

        daily_demand = int(base_demand * city_factor * weekday_factor)

        predictions.append(
            {
                "date": future_date.strftime("%Y-%m-%d"),
                "predicted_shipments": daily_demand,
                "confidence": 0.7,
            }
        )

    # Análisis de tendencia
    values = [p["predicted_shipments"] for p in predictions]
    avg_demand = sum(values) / len(values)

    trend = "stable"
    if len(values) > 2:
        if values[-1] > values[0] * 1.1:
            trend = "increasing"
        elif values[-1] < values[0] * 0.9:
            trend = "decreasing"

    return {
        "location": location,
        "predictions": predictions,
        "trend": trend,
        "average_daily_demand": round(avg_demand, 1),
        "total_predicted": sum(values),
        "peak_day": max(predictions, key=lambda x: x["predicted_shipments"])[
            "date"
        ],
    }
