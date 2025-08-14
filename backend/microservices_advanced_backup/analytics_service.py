# 🇨🇺 PACKFY CUBA - Sistema de Analytics Avanzado v4.0
import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from django.core.cache import cache
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Tipos de métricas de analytics"""

    REVENUE = "revenue"
    SHIPMENTS = "shipments"
    USERS = "users"
    PERFORMANCE = "performance"
    GEOGRAPHY = "geography"
    CUSTOMER_SATISFACTION = "customer_satisfaction"
    OPERATIONAL = "operational"


class TimeRange(Enum):
    """Rangos de tiempo para analytics"""

    HOUR = "1h"
    DAY = "1d"
    WEEK = "7d"
    MONTH = "30d"
    QUARTER = "90d"
    YEAR = "365d"


@dataclass
class AnalyticsQuery:
    """Query de analytics estructurada"""

    metric_type: MetricType
    time_range: TimeRange
    filters: Dict[str, Any]
    aggregation: str  # sum, avg, count, etc.
    dimensions: List[str]  # grouping dimensions


class GlobalAnalyticsService:
    """
    Servicio de analytics global para PACKFY CUBA
    Proporciona métricas en tiempo real y análisis predictivo
    """

    def __init__(self):
        self.cache_timeout = 300  # 5 minutos
        self.regions = ["cuba", "mexico", "colombia", "usa", "spain"]

    async def get_real_time_dashboard(
        self, region: str = "all"
    ) -> Dict[str, Any]:
        """
        Obtiene dashboard en tiempo real con métricas clave
        """
        try:
            cache_key = f"realtime_dashboard_{region}"
            dashboard = cache.get(cache_key)

            if not dashboard:
                # Ejecutar queries en paralelo
                tasks = [
                    self._get_revenue_metrics(region),
                    self._get_shipment_metrics(region),
                    self._get_user_metrics(region),
                    self._get_performance_metrics(region),
                    self._get_geographic_metrics(region),
                ]

                results = await asyncio.gather(*tasks, return_exceptions=True)

                dashboard = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "region": region,
                    "revenue": (
                        results[0]
                        if not isinstance(results[0], Exception)
                        else {}
                    ),
                    "shipments": (
                        results[1]
                        if not isinstance(results[1], Exception)
                        else {}
                    ),
                    "users": (
                        results[2]
                        if not isinstance(results[2], Exception)
                        else {}
                    ),
                    "performance": (
                        results[3]
                        if not isinstance(results[3], Exception)
                        else {}
                    ),
                    "geography": (
                        results[4]
                        if not isinstance(results[4], Exception)
                        else {}
                    ),
                    "alerts": await self._get_system_alerts(region),
                }

                cache.set(cache_key, dashboard, self.cache_timeout)

            return dashboard

        except Exception as e:
            logger.error(f"Error obteniendo dashboard en tiempo real: {e}")
            return {"error": str(e)}

    async def _get_revenue_metrics(self, region: str) -> Dict[str, Any]:
        """Obtiene métricas de ingresos"""
        try:
            from envios.models import Envio

            now = timezone.now()
            today = now.date()
            yesterday = today - timedelta(days=1)
            this_month = now.replace(day=1)
            last_month = (this_month - timedelta(days=1)).replace(day=1)

            # Query base con filtro de región si aplica
            base_query = Envio.objects.all()
            if region != "all":
                base_query = base_query.filter(region=region)

            # Ingresos de hoy
            today_revenue = (
                base_query.filter(
                    fecha_creacion__date=today,
                    estado__in=["entregado", "pagado"],
                ).aggregate(total=Sum("precio"))["total"]
                or 0
            )

            # Ingresos de ayer
            yesterday_revenue = (
                base_query.filter(
                    fecha_creacion__date=yesterday,
                    estado__in=["entregado", "pagado"],
                ).aggregate(total=Sum("precio"))["total"]
                or 0
            )

            # Ingresos del mes
            month_revenue = (
                base_query.filter(
                    fecha_creacion__gte=this_month,
                    estado__in=["entregado", "pagado"],
                ).aggregate(total=Sum("precio"))["total"]
                or 0
            )

            # Ingresos del mes pasado
            last_month_revenue = (
                base_query.filter(
                    fecha_creacion__gte=last_month,
                    fecha_creacion__lt=this_month,
                    estado__in=["entregado", "pagado"],
                ).aggregate(total=Sum("precio"))["total"]
                or 0
            )

            # Calcular cambios porcentuales
            daily_change = self._calculate_percentage_change(
                yesterday_revenue, today_revenue
            )
            monthly_change = self._calculate_percentage_change(
                last_month_revenue, month_revenue
            )

            # Ingresos por día de la semana
            weekly_revenue = []
            for i in range(7):
                day = today - timedelta(days=i)
                day_revenue = (
                    base_query.filter(
                        fecha_creacion__date=day,
                        estado__in=["entregado", "pagado"],
                    ).aggregate(total=Sum("precio"))["total"]
                    or 0
                )

                weekly_revenue.append(
                    {
                        "date": day.isoformat(),
                        "revenue": float(day_revenue),
                        "day_name": day.strftime("%A"),
                    }
                )

            return {
                "today": float(today_revenue),
                "yesterday": float(yesterday_revenue),
                "month": float(month_revenue),
                "last_month": float(last_month_revenue),
                "daily_change_percent": daily_change,
                "monthly_change_percent": monthly_change,
                "weekly_trend": weekly_revenue,
                "currency": "USD",
            }

        except Exception as e:
            logger.error(f"Error obteniendo métricas de ingresos: {e}")
            return {}

    async def _get_shipment_metrics(self, region: str) -> Dict[str, Any]:
        """Obtiene métricas de envíos"""
        try:
            from envios.models import Envio

            now = timezone.now()
            today = now.date()
            this_hour = now.replace(minute=0, second=0, microsecond=0)

            base_query = Envio.objects.all()
            if region != "all":
                base_query = base_query.filter(region=region)

            # Envíos de hoy
            today_shipments = base_query.filter(
                fecha_creacion__date=today
            ).count()

            # Envíos por estado
            status_counts = (
                base_query.filter(fecha_creacion__date=today)
                .values("estado")
                .annotate(count=Count("id"))
            )

            status_distribution = {
                item["estado"]: item["count"] for item in status_counts
            }

            # Envíos por hora (últimas 24 horas)
            hourly_shipments = []
            for i in range(24):
                hour_start = this_hour - timedelta(hours=i)
                hour_end = hour_start + timedelta(hours=1)

                count = base_query.filter(
                    fecha_creacion__gte=hour_start, fecha_creacion__lt=hour_end
                ).count()

                hourly_shipments.append(
                    {
                        "hour": hour_start.strftime("%H:00"),
                        "count": count,
                        "timestamp": hour_start.isoformat(),
                    }
                )

            # Tiempo promedio de entrega
            delivered_shipments = base_query.filter(
                estado="entregado", fecha_entrega__isnull=False
            )

            avg_delivery_time = 0
            if delivered_shipments.exists():
                delivery_times = []
                for shipment in delivered_shipments[:100]:  # Muestra de 100
                    if shipment.fecha_entrega and shipment.fecha_creacion:
                        delta = (
                            shipment.fecha_entrega - shipment.fecha_creacion
                        )
                        delivery_times.append(
                            delta.total_seconds() / 3600
                        )  # Horas

                if delivery_times:
                    avg_delivery_time = np.mean(delivery_times)

            return {
                "today_total": today_shipments,
                "status_distribution": status_distribution,
                "hourly_trend": hourly_shipments,
                "avg_delivery_hours": round(avg_delivery_time, 2),
                "active_shipments": base_query.filter(
                    estado__in=["pendiente", "en_transito", "en_aduana"]
                ).count(),
            }

        except Exception as e:
            logger.error(f"Error obteniendo métricas de envíos: {e}")
            return {}

    async def _get_user_metrics(self, region: str) -> Dict[str, Any]:
        """Obtiene métricas de usuarios"""
        try:
            from django.contrib.auth import get_user_model
            from envios.models import Envio

            User = get_user_model()
            now = timezone.now()
            today = now.date()

            # Usuarios activos (con actividad en los últimos 30 días)
            active_users = User.objects.filter(
                last_login__gte=now - timedelta(days=30)
            ).count()

            # Nuevos usuarios hoy
            new_users_today = User.objects.filter(
                date_joined__date=today
            ).count()

            # Usuarios con envíos hoy
            users_with_shipments = (
                Envio.objects.filter(fecha_creacion__date=today)
                .values("usuario")
                .distinct()
                .count()
            )

            # Top usuarios por volumen de envíos
            top_users = (
                Envio.objects.values("usuario__email")
                .annotate(
                    shipment_count=Count("id"), total_value=Sum("precio")
                )
                .order_by("-shipment_count")[:10]
            )

            # Distribución geográfica (simulada)
            geographic_distribution = {
                "cuba": 0.7,
                "mexico": 0.15,
                "colombia": 0.08,
                "usa": 0.05,
                "otros": 0.02,
            }

            return {
                "active_users": active_users,
                "new_today": new_users_today,
                "users_with_shipments_today": users_with_shipments,
                "top_users": list(top_users),
                "geographic_distribution": geographic_distribution,
                "user_retention_rate": 0.78,  # Simulado
            }

        except Exception as e:
            logger.error(f"Error obteniendo métricas de usuarios: {e}")
            return {}

    async def _get_performance_metrics(self, region: str) -> Dict[str, Any]:
        """Obtiene métricas de rendimiento del sistema"""
        try:
            # Métricas simuladas (en producción usar APM real)
            return {
                "api_response_time_ms": 250,
                "database_query_time_ms": 45,
                "cache_hit_rate": 0.87,
                "error_rate": 0.02,
                "uptime_percentage": 99.9,
                "active_connections": 156,
                "memory_usage_percent": 68,
                "cpu_usage_percent": 45,
                "disk_usage_percent": 23,
            }

        except Exception as e:
            logger.error(f"Error obteniendo métricas de rendimiento: {e}")
            return {}

    async def _get_geographic_metrics(self, region: str) -> Dict[str, Any]:
        """Obtiene métricas geográficas"""
        try:
            from envios.models import Envio

            # Distribución por origen/destino
            today = timezone.now().date()

            base_query = Envio.objects.filter(fecha_creacion__date=today)
            if region != "all":
                base_query = base_query.filter(region=region)

            # Top orígenes
            top_origins = (
                base_query.values("origen")
                .annotate(count=Count("id"))
                .order_by("-count")[:10]
            )

            # Top destinos
            top_destinations = (
                base_query.values("destino")
                .annotate(count=Count("id"))
                .order_by("-count")[:10]
            )

            # Rutas más populares
            popular_routes = (
                base_query.values("origen", "destino")
                .annotate(count=Count("id"))
                .order_by("-count")[:15]
            )

            return {
                "top_origins": list(top_origins),
                "top_destinations": list(top_destinations),
                "popular_routes": list(popular_routes),
                "international_percentage": 0.25,  # Simulado
            }

        except Exception as e:
            logger.error(f"Error obteniendo métricas geográficas: {e}")
            return {}

    async def _get_system_alerts(self, region: str) -> List[Dict[str, Any]]:
        """Obtiene alertas del sistema"""
        try:
            alerts = []

            # Simulación de alertas basadas en métricas
            from envios.models import Envio

            today = timezone.now().date()
            pending_count = Envio.objects.filter(
                fecha_creacion__date=today, estado="pendiente"
            ).count()

            if pending_count > 50:
                alerts.append(
                    {
                        "type": "warning",
                        "message": f"{pending_count} envíos pendientes de procesamiento",
                        "timestamp": datetime.utcnow().isoformat(),
                        "priority": "medium",
                    }
                )

            # Alertas de rendimiento
            current_hour = timezone.now().replace(
                minute=0, second=0, microsecond=0
            )
            hourly_shipments = Envio.objects.filter(
                fecha_creacion__gte=current_hour
            ).count()

            if hourly_shipments > 100:
                alerts.append(
                    {
                        "type": "info",
                        "message": f"Alto volumen de envíos: {hourly_shipments} en la última hora",
                        "timestamp": datetime.utcnow().isoformat(),
                        "priority": "low",
                    }
                )

            return alerts

        except Exception as e:
            logger.error(f"Error obteniendo alertas del sistema: {e}")
            return []

    def _calculate_percentage_change(
        self, old_value: float, new_value: float
    ) -> float:
        """Calcula cambio porcentual entre dos valores"""
        if old_value == 0:
            return 100.0 if new_value > 0 else 0.0

        return round(((new_value - old_value) / old_value) * 100, 2)

    async def get_predictive_analytics(
        self, metric_type: MetricType, days_ahead: int = 7
    ) -> Dict[str, Any]:
        """
        Genera predicciones usando análisis de tendencias
        """
        try:
            # Obtener datos históricos
            historical_data = await self._get_historical_data(
                metric_type, days=30
            )

            if len(historical_data) < 7:
                return {"error": "Datos insuficientes para predicción"}

            # Preparar datos para predicción
            values = [point["value"] for point in historical_data]
            dates = [point["date"] for point in historical_data]

            # Análisis de tendencia simple (en producción usar modelos ML)
            trend = self._calculate_trend(values)
            seasonality = self._detect_seasonality(values)

            # Generar predicciones
            predictions = []
            last_value = values[-1]

            for i in range(1, days_ahead + 1):
                # Predicción simple basada en tendencia
                predicted_value = last_value + (trend * i)

                # Aplicar estacionalidad
                if seasonality:
                    day_of_week = (len(values) + i) % 7
                    seasonal_factor = seasonality.get(day_of_week, 1.0)
                    predicted_value *= seasonal_factor

                predictions.append(
                    {
                        "date": (datetime.now() + timedelta(days=i))
                        .date()
                        .isoformat(),
                        "predicted_value": max(0, round(predicted_value, 2)),
                        "confidence": max(
                            0.5, 1.0 - (i * 0.1)
                        ),  # Confianza decrece con tiempo
                    }
                )

            return {
                "metric_type": metric_type.value,
                "predictions": predictions,
                "trend": (
                    "increasing"
                    if trend > 0
                    else "decreasing" if trend < 0 else "stable"
                ),
                "trend_strength": abs(trend),
                "has_seasonality": bool(seasonality),
            }

        except Exception as e:
            logger.error(f"Error en analytics predictivo: {e}")
            return {"error": str(e)}

    async def _get_historical_data(
        self, metric_type: MetricType, days: int
    ) -> List[Dict[str, Any]]:
        """Obtiene datos históricos para análisis"""
        try:
            from envios.models import Envio

            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=days)

            historical_data = []

            for i in range(days):
                date = start_date + timedelta(days=i)

                if metric_type == MetricType.REVENUE:
                    value = (
                        Envio.objects.filter(
                            fecha_creacion__date=date,
                            estado__in=["entregado", "pagado"],
                        ).aggregate(total=Sum("precio"))["total"]
                        or 0
                    )

                elif metric_type == MetricType.SHIPMENTS:
                    value = Envio.objects.filter(
                        fecha_creacion__date=date
                    ).count()

                else:
                    value = 0  # Otros tipos de métricas

                historical_data.append(
                    {"date": date.isoformat(), "value": float(value)}
                )

            return historical_data

        except Exception as e:
            logger.error(f"Error obteniendo datos históricos: {e}")
            return []

    def _calculate_trend(self, values: List[float]) -> float:
        """Calcula tendencia lineal simple"""
        if len(values) < 2:
            return 0.0

        x = list(range(len(values)))
        y = values

        # Regresión lineal simple
        n = len(values)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)

        return slope

    def _detect_seasonality(
        self, values: List[float]
    ) -> Optional[Dict[int, float]]:
        """Detecta patrones estacionales simples (por día de semana)"""
        if len(values) < 14:  # Necesita al menos 2 semanas
            return None

        # Agrupar por día de semana
        weekly_patterns = {}
        for i, value in enumerate(values):
            day_of_week = i % 7
            if day_of_week not in weekly_patterns:
                weekly_patterns[day_of_week] = []
            weekly_patterns[day_of_week].append(value)

        # Calcular factores estacionales
        overall_mean = np.mean(values)
        seasonal_factors = {}

        for day, day_values in weekly_patterns.items():
            day_mean = np.mean(day_values)
            seasonal_factors[day] = (
                day_mean / overall_mean if overall_mean > 0 else 1.0
            )

        return seasonal_factors

    async def generate_custom_report(
        self, query: AnalyticsQuery
    ) -> Dict[str, Any]:
        """
        Genera reporte personalizado basado en query estructurada
        """
        try:
            cache_key = f"custom_report_{self._hash_query(query)}"
            report = cache.get(cache_key)

            if not report:
                report = await self._execute_analytics_query(query)
                cache.set(
                    cache_key, report, self.cache_timeout * 2
                )  # Cache más largo

            return report

        except Exception as e:
            logger.error(f"Error generando reporte personalizado: {e}")
            return {"error": str(e)}

    def _hash_query(self, query: AnalyticsQuery) -> str:
        """Genera hash único para query de analytics"""
        query_str = f"{query.metric_type.value}:{query.time_range.value}:{json.dumps(query.filters, sort_keys=True)}:{query.aggregation}:{':'.join(query.dimensions)}"
        return hashlib.md5(query_str.encode()).hexdigest()

    async def _execute_analytics_query(
        self, query: AnalyticsQuery
    ) -> Dict[str, Any]:
        """Ejecuta query de analytics"""
        # Implementar lógica específica basada en el tipo de métrica y filtros
        # Por ahora retorna estructura básica

        return {
            "query": {
                "metric_type": query.metric_type.value,
                "time_range": query.time_range.value,
                "filters": query.filters,
                "aggregation": query.aggregation,
                "dimensions": query.dimensions,
            },
            "results": [],
            "total_records": 0,
            "execution_time_ms": 100,
            "timestamp": datetime.utcnow().isoformat(),
        }


# Instancia global del servicio
analytics_service = GlobalAnalyticsService()
