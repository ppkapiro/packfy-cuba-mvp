# 🇨🇺 PACKFY CUBA - Sistema de Inteligencia Artificial v4.0
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from django.conf import settings
from django.utils import timezone
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

logger = logging.getLogger(__name__)


class AIPredictor:
    """Sistema de predicción inteligente para PACKFY CUBA"""

    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.model_path = os.path.join(settings.BASE_DIR, "ai_models")
        self._ensure_model_directory()

    def _ensure_model_directory(self):
        """Crear directorio de modelos si no existe"""
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

    # ===============================
    # PREDICCIÓN DE TIEMPOS DE ENTREGA
    # ===============================

    def predict_delivery_time(
        self,
        origin: str,
        destination: str,
        weight: float,
        package_type: str,
        priority: str = "normal",
    ) -> Dict[str, Any]:
        """
        Predice el tiempo de entrega basado en datos históricos

        Args:
            origin: Ciudad de origen
            destination: Ciudad de destino
            weight: Peso del paquete en kg
            package_type: Tipo de paquete
            priority: Prioridad del envío

        Returns:
            Dict con predicción de tiempo y confianza
        """
        try:
            # Cargar modelo si existe
            model_name = "delivery_time_predictor"
            if model_name not in self.models:
                self._load_or_create_delivery_model()

            # Preparar características
            features = self._prepare_delivery_features(
                origin, destination, weight, package_type, priority
            )

            # Realizar predicción
            if model_name in self.models:
                prediction = self.models[model_name].predict([features])[0]
                confidence = self._calculate_prediction_confidence(
                    model_name, features
                )

                # Ajustes por prioridad
                if priority == "express":
                    prediction *= 0.7  # 30% más rápido
                elif priority == "economy":
                    prediction *= 1.3  # 30% más lento

                return {
                    "estimated_hours": max(1, int(prediction)),
                    "estimated_days": max(1, int(prediction / 24)),
                    "confidence": confidence,
                    "factors": {
                        "distance": self._calculate_distance_factor(
                            origin, destination
                        ),
                        "weight": self._calculate_weight_factor(weight),
                        "priority": priority,
                        "season": self._get_seasonal_factor(),
                    },
                }
            else:
                # Fallback a estimación básica
                return self._basic_delivery_estimation(
                    origin, destination, weight, priority
                )

        except Exception as e:
            logger.error(f"Error predicting delivery time: {e}")
            return self._basic_delivery_estimation(
                origin, destination, weight, priority
            )

    def _prepare_delivery_features(
        self,
        origin: str,
        destination: str,
        weight: float,
        package_type: str,
        priority: str,
    ) -> List[float]:
        """Preparar características para predicción de entrega"""
        features = []

        # Codificar ubicaciones geográficas
        cuba_cities = {
            "la_habana": 0,
            "santiago": 1,
            "camaguey": 2,
            "holguin": 3,
            "guantanamo": 4,
            "santa_clara": 5,
            "bayamo": 6,
            "las_tunas": 7,
            "cienfuegos": 8,
            "pinar_del_rio": 9,
            "matanzas": 10,
            "ciego_de_avila": 11,
            "sancti_spiritus": 12,
            "granma": 13,
            "isla_juventud": 14,
        }

        origin_code = cuba_cities.get(origin.lower().replace(" ", "_"), 0)
        dest_code = cuba_cities.get(destination.lower().replace(" ", "_"), 0)

        features.extend(
            [
                origin_code,
                dest_code,
                abs(origin_code - dest_code),  # Distancia relativa
                weight,
                min(weight, 50),  # Peso limitado
            ]
        )

        # Codificar tipo de paquete
        package_types = {"documento": 0, "paquete": 1, "caja": 2, "sobre": 3}
        features.append(package_types.get(package_type.lower(), 1))

        # Codificar prioridad
        priorities = {"economy": 0, "normal": 1, "express": 2, "urgent": 3}
        features.append(priorities.get(priority.lower(), 1))

        # Factores temporales
        now = datetime.now()
        features.extend(
            [
                now.weekday(),  # Día de la semana
                now.hour,  # Hora del día
                now.month,  # Mes del año
                1 if now.weekday() >= 5 else 0,  # Es fin de semana
            ]
        )

        return features

    def _basic_delivery_estimation(
        self, origin: str, destination: str, weight: float, priority: str
    ) -> Dict[str, Any]:
        """Estimación básica cuando no hay modelo entrenado"""
        # Distancias aproximadas entre ciudades principales de Cuba
        base_hours = 24  # Base de 1 día

        # Ajustes por distancia (simplificado)
        if origin.lower() != destination.lower():
            base_hours += 12  # +12 horas por cambio de ciudad

        # Ajustes por peso
        if weight > 10:
            base_hours += 6
        elif weight > 25:
            base_hours += 12

        # Ajustes por prioridad
        if priority == "express":
            base_hours = int(base_hours * 0.7)
        elif priority == "economy":
            base_hours = int(base_hours * 1.5)

        return {
            "estimated_hours": base_hours,
            "estimated_days": max(1, base_hours // 24),
            "confidence": 0.6,  # Confianza media para estimación básica
            "factors": {
                "distance": "estimated",
                "weight": weight,
                "priority": priority,
                "season": "normal",
            },
        }

    # ===============================
    # OPTIMIZACIÓN DE RUTAS
    # ===============================

    def optimize_route(self, deliveries: List[Dict]) -> Dict[str, Any]:
        """
        Optimiza rutas de entrega usando algoritmo inteligente

        Args:
            deliveries: Lista de entregas con ubicaciones y prioridades

        Returns:
            Ruta optimizada con orden de entrega y métricas
        """
        try:
            if not deliveries:
                return {
                    "optimized_route": [],
                    "total_distance": 0,
                    "estimated_time": 0,
                }

            # Implementación básica de optimización de rutas
            # En producción, se podría usar algoritmos más avanzados como TSP o VRP

            # Separar por prioridad
            urgent = [d for d in deliveries if d.get("priority") == "urgent"]
            express = [d for d in deliveries if d.get("priority") == "express"]
            normal = [
                d
                for d in deliveries
                if d.get("priority") in ["normal", "economy"]
            ]

            # Ordenar geográficamente dentro de cada prioridad
            urgent_sorted = self._sort_by_location(urgent)
            express_sorted = self._sort_by_location(express)
            normal_sorted = self._sort_by_location(normal)

            # Combinar en orden de prioridad
            optimized_route = urgent_sorted + express_sorted + normal_sorted

            # Calcular métricas
            total_distance = self._calculate_route_distance(optimized_route)
            estimated_time = self._calculate_route_time(optimized_route)

            return {
                "optimized_route": optimized_route,
                "total_distance": total_distance,
                "estimated_time": estimated_time,
                "efficiency_score": self._calculate_efficiency_score(
                    deliveries, optimized_route
                ),
                "recommendations": self._generate_route_recommendations(
                    optimized_route
                ),
            }

        except Exception as e:
            logger.error(f"Error optimizing route: {e}")
            return {
                "optimized_route": deliveries,
                "total_distance": 0,
                "estimated_time": len(deliveries) * 30,  # 30 min por entrega
                "efficiency_score": 0.5,
                "recommendations": [
                    "Error en optimización, usar ruta original"
                ],
            }

    def _sort_by_location(self, deliveries: List[Dict]) -> List[Dict]:
        """Ordena entregas por proximidad geográfica"""
        if not deliveries:
            return []

        # Implementación simplificada - en producción usar coordenadas reales
        cuba_regions = {
            "occidental": [
                "la_habana",
                "pinar_del_rio",
                "matanzas",
                "isla_juventud",
            ],
            "central": [
                "villa_clara",
                "cienfuegos",
                "sancti_spiritus",
                "ciego_de_avila",
                "camaguey",
            ],
            "oriental": [
                "las_tunas",
                "holguin",
                "granma",
                "santiago_de_cuba",
                "guantanamo",
            ],
        }

        # Agrupar por región
        by_region = {"occidental": [], "central": [], "oriental": []}

        for delivery in deliveries:
            location = (
                delivery.get("destination", "").lower().replace(" ", "_")
            )
            region_found = False

            for region, cities in cuba_regions.items():
                if any(city in location for city in cities):
                    by_region[region].append(delivery)
                    region_found = True
                    break

            if not region_found:
                by_region["occidental"].append(
                    delivery
                )  # Default a occidental

        # Combinar regiones en orden geográfico
        return (
            by_region["occidental"]
            + by_region["central"]
            + by_region["oriental"]
        )

    # ===============================
    # ANÁLISIS PREDICTIVO DE DEMANDA
    # ===============================

    def predict_demand(
        self, location: str, time_horizon: int = 7
    ) -> Dict[str, Any]:
        """
        Predice la demanda de envíos para una ubicación

        Args:
            location: Ubicación para predecir demanda
            time_horizon: Días hacia adelante para predecir

        Returns:
            Predicción de demanda con tendencias
        """
        try:
            # Cargar modelo de demanda
            model_name = "demand_predictor"
            if model_name not in self.models:
                self._load_or_create_demand_model()

            predictions = []

            for days_ahead in range(1, time_horizon + 1):
                future_date = datetime.now() + timedelta(days=days_ahead)
                features = self._prepare_demand_features(location, future_date)

                if model_name in self.models:
                    demand = max(
                        0, int(self.models[model_name].predict([features])[0])
                    )
                else:
                    # Fallback a estimación básica
                    demand = self._basic_demand_estimation(
                        location, future_date
                    )

                predictions.append(
                    {
                        "date": future_date.strftime("%Y-%m-%d"),
                        "predicted_shipments": demand,
                        "confidence": (
                            0.75 if model_name in self.models else 0.5
                        ),
                    }
                )

            # Análisis de tendencias
            values = [p["predicted_shipments"] for p in predictions]
            trend = "stable"
            if len(values) > 2:
                if values[-1] > values[0] * 1.1:
                    trend = "increasing"
                elif values[-1] < values[0] * 0.9:
                    trend = "decreasing"

            return {
                "location": location,
                "time_horizon": time_horizon,
                "predictions": predictions,
                "trend": trend,
                "total_predicted": sum(values),
                "peak_day": max(
                    predictions, key=lambda x: x["predicted_shipments"]
                )["date"],
                "recommendations": self._generate_demand_recommendations(
                    predictions, trend
                ),
            }

        except Exception as e:
            logger.error(f"Error predicting demand: {e}")
            return self._basic_demand_prediction(location, time_horizon)

    def _basic_demand_estimation(self, location: str, date: datetime) -> int:
        """Estimación básica de demanda"""
        base_demand = 10  # Base de 10 envíos por día

        # Ajustes por día de la semana
        if date.weekday() == 0:  # Lunes
            base_demand *= 1.5
        elif date.weekday() in [5, 6]:  # Fin de semana
            base_demand *= 0.7

        # Ajustes por ubicación (ciudades principales)
        major_cities = ["la_habana", "santiago", "camaguey", "holguin"]
        if any(city in location.lower() for city in major_cities):
            base_demand *= 2

        return int(base_demand)

    # ===============================
    # DETECCIÓN DE ANOMALÍAS
    # ===============================

    def detect_anomalies(self, shipment_data: Dict) -> Dict[str, Any]:
        """
        Detecta anomalías en patrones de envío

        Args:
            shipment_data: Datos del envío a analizar

        Returns:
            Resultado de análisis de anomalías
        """
        anomalies = []
        risk_score = 0

        try:
            # Verificar peso vs tamaño declarado
            weight = shipment_data.get("weight", 0)
            declared_value = shipment_data.get("declared_value", 0)

            if weight > 50 and declared_value < 100:
                anomalies.append(
                    {
                        "type": "value_weight_mismatch",
                        "severity": "medium",
                        "description": "Peso alto con valor declarado bajo",
                    }
                )
                risk_score += 30

            # Verificar patrones de envío del remitente
            sender_history = shipment_data.get("sender_history", {})
            if sender_history.get("shipments_today", 0) > 10:
                anomalies.append(
                    {
                        "type": "high_frequency_sender",
                        "severity": "medium",
                        "description": "Remitente con alta frecuencia de envíos",
                    }
                )
                risk_score += 20

            # Verificar destinos inusuales
            destination = shipment_data.get("destination", "")
            if self._is_unusual_destination(destination):
                anomalies.append(
                    {
                        "type": "unusual_destination",
                        "severity": "low",
                        "description": "Destino poco común detectado",
                    }
                )
                risk_score += 10

            # Verificar horario de envío
            timestamp = shipment_data.get("timestamp", datetime.now())
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(
                    timestamp.replace("Z", "+00:00")
                )

            if timestamp.hour < 6 or timestamp.hour > 22:
                anomalies.append(
                    {
                        "type": "unusual_time",
                        "severity": "low",
                        "description": "Envío en horario inusual",
                    }
                )
                risk_score += 15

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
                "requires_review": risk_score >= 40,
                "recommendations": self._generate_anomaly_recommendations(
                    anomalies, risk_level
                ),
            }

        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return {
                "anomalies": [],
                "risk_score": 0,
                "risk_level": "low",
                "requires_review": False,
                "recommendations": [],
            }

    # ===============================
    # UTILIDADES DE MODELO
    # ===============================

    def _load_or_create_delivery_model(self):
        """Cargar o crear modelo de predicción de entrega"""
        model_file = os.path.join(self.model_path, "delivery_time_model.pkl")

        if os.path.exists(model_file):
            try:
                self.models["delivery_time_predictor"] = joblib.load(
                    model_file
                )
                logger.info("Modelo de tiempo de entrega cargado exitosamente")
            except Exception as e:
                logger.error(f"Error loading delivery model: {e}")
                self._create_default_delivery_model()
        else:
            self._create_default_delivery_model()

    def _create_default_delivery_model(self):
        """Crear modelo básico de predicción de entrega"""
        try:
            # Crear datos sintéticos para entrenamiento inicial
            np.random.seed(42)
            n_samples = 1000

            # Generar características sintéticas
            X = np.random.rand(n_samples, 11)  # 11 características

            # Generar tiempos de entrega sintéticos basados en lógica de negocio
            y = []
            for i in range(n_samples):
                base_time = 24  # 24 horas base
                distance_factor = X[i, 2] * 12  # Factor de distancia
                weight_factor = X[i, 3] * 6  # Factor de peso
                priority_factor = X[i, 6] * -12  # Prioridad reduce tiempo
                time = (
                    base_time
                    + distance_factor
                    + weight_factor
                    + priority_factor
                )
                y.append(max(1, time))  # Mínimo 1 hora

            # Entrenar modelo
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)

            # Guardar modelo
            self.models["delivery_time_predictor"] = model
            model_file = os.path.join(
                self.model_path, "delivery_time_model.pkl"
            )
            joblib.dump(model, model_file)

            logger.info("Modelo de tiempo de entrega creado y guardado")

        except Exception as e:
            logger.error(f"Error creating delivery model: {e}")

    def retrain_models(self) -> Dict[str, bool]:
        """Reentrenar modelos con datos actualizados"""
        results = {}

        try:
            # Reentrenar modelo de tiempo de entrega
            results["delivery_time"] = self._retrain_delivery_model()

            # Reentrenar modelo de demanda
            results["demand"] = self._retrain_demand_model()

            logger.info(f"Modelos reentrenados: {results}")
            return results

        except Exception as e:
            logger.error(f"Error retraining models: {e}")
            return {"delivery_time": False, "demand": False}

    def get_model_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de los modelos"""
        return {
            "models_loaded": list(self.models.keys()),
            "model_path": self.model_path,
            "last_update": datetime.now().isoformat(),
            "performance_metrics": {
                "delivery_time_accuracy": 0.85,  # Placeholder
                "demand_accuracy": 0.78,  # Placeholder
                "anomaly_detection_precision": 0.92,  # Placeholder
            },
        }


# Instancia global del predictor de IA
ai_predictor = AIPredictor()
