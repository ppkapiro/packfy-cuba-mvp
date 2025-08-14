# 🇨🇺 PACKFY CUBA - Sistema de Expansión Internacional v4.0
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class Country(Enum):
    """Países soportados por PACKFY"""

    CUBA = "CU"
    MEXICO = "MX"
    COLOMBIA = "CO"
    USA = "US"
    SPAIN = "ES"
    DOMINICAN_REPUBLIC = "DO"
    VENEZUELA = "VE"
    ARGENTINA = "AR"


class Currency(Enum):
    """Monedas soportadas"""

    CUP = "CUP"  # Peso Cubano
    USD = "USD"  # Dólar Estadounidense
    EUR = "EUR"  # Euro
    MXN = "MXN"  # Peso Mexicano
    COP = "COP"  # Peso Colombiano
    DOP = "DOP"  # Peso Dominicano
    ARS = "ARS"  # Peso Argentino


@dataclass
class CountryConfig:
    """Configuración específica por país"""

    code: str
    name: str
    currency: Currency
    tax_rate: float
    customs_required: bool
    max_weight_kg: float
    max_value_usd: float
    shipping_zones: List[str]
    languages: List[str]
    time_zone: str
    working_days: List[int]  # 0=Monday, 6=Sunday
    postal_code_format: str
    phone_format: str
    customs_forms: List[str]


class InternationalExpansionService:
    """
    Servicio para expansión internacional de PACKFY CUBA
    Maneja configuraciones específicas por país y regulaciones
    """

    def __init__(self):
        self.countries_config = self._load_countries_config()
        self.exchange_rates = {}
        self.customs_regulations = {}

    def _load_countries_config(self) -> Dict[str, CountryConfig]:
        """Carga configuración de países soportados"""
        return {
            Country.CUBA.value: CountryConfig(
                code="CU",
                name="Cuba",
                currency=Currency.CUP,
                tax_rate=0.0,  # Sin impuestos locales
                customs_required=False,
                max_weight_kg=50.0,
                max_value_usd=1000.0,
                shipping_zones=["havana", "santiago", "camaguey", "holguin"],
                languages=["es"],
                time_zone="America/Havana",
                working_days=[0, 1, 2, 3, 4],  # Lunes a Viernes
                postal_code_format=r"^\d{5}$",
                phone_format=r"^\+53\d{8}$",
                customs_forms=[],
            ),
            Country.MEXICO.value: CountryConfig(
                code="MX",
                name="México",
                currency=Currency.MXN,
                tax_rate=0.16,  # IVA 16%
                customs_required=True,
                max_weight_kg=100.0,
                max_value_usd=2000.0,
                shipping_zones=["cdmx", "guadalajara", "monterrey", "cancun"],
                languages=["es", "en"],
                time_zone="America/Mexico_City",
                working_days=[0, 1, 2, 3, 4],
                postal_code_format=r"^\d{5}$",
                phone_format=r"^\+52\d{10}$",
                customs_forms=["CN22", "CN23"],
            ),
            Country.COLOMBIA.value: CountryConfig(
                code="CO",
                name="Colombia",
                currency=Currency.COP,
                tax_rate=0.19,  # IVA 19%
                customs_required=True,
                max_weight_kg=75.0,
                max_value_usd=1500.0,
                shipping_zones=["bogota", "medellin", "cali", "barranquilla"],
                languages=["es", "en"],
                time_zone="America/Bogota",
                working_days=[0, 1, 2, 3, 4],
                postal_code_format=r"^\d{6}$",
                phone_format=r"^\+57\d{10}$",
                customs_forms=["CN22", "CN23", "DIAN"],
            ),
            Country.USA.value: CountryConfig(
                code="US",
                name="United States",
                currency=Currency.USD,
                tax_rate=0.08,  # Promedio sales tax
                customs_required=True,
                max_weight_kg=150.0,
                max_value_usd=5000.0,
                shipping_zones=["miami", "new_york", "los_angeles", "chicago"],
                languages=["en", "es"],
                time_zone="America/New_York",
                working_days=[0, 1, 2, 3, 4],
                postal_code_format=r"^\d{5}(-\d{4})?$",
                phone_format=r"^\+1\d{10}$",
                customs_forms=["CN22", "CN23", "USPS_2976A"],
            ),
            Country.SPAIN.value: CountryConfig(
                code="ES",
                name="España",
                currency=Currency.EUR,
                tax_rate=0.21,  # IVA 21%
                customs_required=True,
                max_weight_kg=120.0,
                max_value_usd=3000.0,
                shipping_zones=["madrid", "barcelona", "valencia", "sevilla"],
                languages=["es", "ca", "eu", "gl"],
                time_zone="Europe/Madrid",
                working_days=[0, 1, 2, 3, 4],
                postal_code_format=r"^\d{5}$",
                phone_format=r"^\+34\d{9}$",
                customs_forms=["CN22", "CN23", "EU_CUSTOMS"],
            ),
        }

    def get_country_config(self, country_code: str) -> Optional[CountryConfig]:
        """Obtiene configuración de país específico"""
        return self.countries_config.get(country_code.upper())

    def calculate_international_shipping(
        self,
        origin_country: str,
        destination_country: str,
        weight_kg: float,
        value_usd: float,
        service_type: str = "standard",
    ) -> Dict[str, Any]:
        """
        Calcula costo de envío internacional
        """
        try:
            origin_config = self.get_country_config(origin_country)
            dest_config = self.get_country_config(destination_country)

            if not origin_config or not dest_config:
                raise ValueError("Configuración de país no encontrada")

            # Validar límites del país destino
            if weight_kg > dest_config.max_weight_kg:
                raise ValueError(
                    f"Peso excede límite máximo de {dest_config.max_weight_kg}kg"
                )

            if value_usd > dest_config.max_value_usd:
                raise ValueError(
                    f"Valor excede límite máximo de ${dest_config.max_value_usd}"
                )

            # Calcular costo base por distancia y peso
            base_cost = self._calculate_base_shipping_cost(
                origin_country, destination_country, weight_kg
            )

            # Aplicar multiplicadores por tipo de servicio
            service_multipliers = {
                "economy": 1.0,
                "standard": 1.5,
                "express": 2.5,
                "urgent": 4.0,
            }

            shipping_cost = base_cost * service_multipliers.get(
                service_type, 1.5
            )

            # Calcular impuestos y aranceles
            taxes = self._calculate_international_taxes(
                dest_config, value_usd, weight_kg
            )

            # Calcular tiempo estimado de entrega
            delivery_estimate = self._calculate_international_delivery_time(
                origin_country, destination_country, service_type
            )

            # Documentos requeridos
            required_docs = self._get_required_documents(
                origin_config, dest_config, value_usd
            )

            return {
                "shipping_cost_usd": round(shipping_cost, 2),
                "taxes": taxes,
                "total_cost_usd": round(shipping_cost + taxes["total_tax"], 2),
                "delivery_estimate_days": delivery_estimate,
                "currency": dest_config.currency.value,
                "converted_cost": self._convert_currency(
                    shipping_cost + taxes["total_tax"],
                    Currency.USD,
                    dest_config.currency,
                ),
                "required_documents": required_docs,
                "customs_required": dest_config.customs_required,
                "max_weight_allowed": dest_config.max_weight_kg,
                "max_value_allowed": dest_config.max_value_usd,
            }

        except Exception as e:
            logger.error(f"Error calculando envío internacional: {e}")
            raise

    def _calculate_base_shipping_cost(
        self, origin: str, destination: str, weight: float
    ) -> float:
        """Calcula costo base de envío por distancia y peso"""

        # Tabla de distancias aproximadas (en miles de km)
        distance_matrix = {
            ("CU", "MX"): 1.5,
            ("CU", "CO"): 1.8,
            ("CU", "US"): 1.2,
            ("CU", "ES"): 7.5,
            ("CU", "DO"): 0.5,
            ("MX", "CO"): 3.0,
            ("MX", "US"): 2.0,
            ("US", "ES"): 6.5,
        }

        # Obtener distancia o usar valor por defecto
        distance_key = (origin, destination)
        reverse_key = (destination, origin)

        distance = distance_matrix.get(distance_key) or distance_matrix.get(
            reverse_key, 5.0
        )

        # Fórmula de costo: base + (peso * factor_peso) + (distancia * factor_distancia)
        base_cost = 15.0  # Costo base mínimo
        weight_factor = 2.5
        distance_factor = 3.0

        total_cost = (
            base_cost + (weight * weight_factor) + (distance * distance_factor)
        )

        return max(total_cost, 20.0)  # Costo mínimo de $20

    def _calculate_international_taxes(
        self, dest_config: CountryConfig, value_usd: float, weight_kg: float
    ) -> Dict[str, float]:
        """Calcula impuestos y aranceles internacionales"""

        taxes = {
            "vat_tax": 0.0,
            "customs_duty": 0.0,
            "handling_fee": 0.0,
            "total_tax": 0.0,
        }

        if dest_config.customs_required:
            # IVA/VAT
            taxes["vat_tax"] = value_usd * dest_config.tax_rate

            # Arancel aduanero (típicamente 5-15% para paquetería)
            if value_usd > 50:  # Umbral de exención
                duty_rates = {"MX": 0.10, "CO": 0.12, "US": 0.08, "ES": 0.15}
                duty_rate = duty_rates.get(dest_config.code, 0.10)
                taxes["customs_duty"] = value_usd * duty_rate

            # Tasa de manejo aduanero
            if value_usd > 100:
                taxes["handling_fee"] = min(25.0, value_usd * 0.02)

        taxes["total_tax"] = sum(
            [taxes["vat_tax"], taxes["customs_duty"], taxes["handling_fee"]]
        )

        return taxes

    def _calculate_international_delivery_time(
        self, origin: str, destination: str, service_type: str
    ) -> int:
        """Calcula tiempo estimado de entrega internacional"""

        # Días base por ruta
        base_days = {
            ("CU", "MX"): 7,
            ("CU", "CO"): 10,
            ("CU", "US"): 5,
            ("CU", "ES"): 15,
            ("CU", "DO"): 3,
        }

        route_key = (origin, destination)
        reverse_key = (destination, origin)

        days = base_days.get(route_key) or base_days.get(reverse_key, 12)

        # Ajustar por tipo de servicio
        service_adjustments = {
            "economy": 1.5,
            "standard": 1.0,
            "express": 0.6,
            "urgent": 0.3,
        }

        adjusted_days = int(days * service_adjustments.get(service_type, 1.0))

        return max(adjusted_days, 2)  # Mínimo 2 días

    def _get_required_documents(
        self,
        origin_config: CountryConfig,
        dest_config: CountryConfig,
        value_usd: float,
    ) -> List[str]:
        """Obtiene documentos requeridos para envío internacional"""

        documents = ["Commercial Invoice", "Packing List"]

        if dest_config.customs_required:
            documents.extend(dest_config.customs_forms)

            if value_usd > 500:
                documents.append("Certificate of Origin")

            if value_usd > 1000:
                documents.append("Insurance Certificate")

        return list(set(documents))  # Eliminar duplicados

    def _convert_currency(
        self, amount: float, from_currency: Currency, to_currency: Currency
    ) -> float:
        """Convierte entre monedas usando tasas de cambio actuales"""

        if from_currency == to_currency:
            return amount

        # Tasas de cambio (en producción usar API real como XE, CurrencyLayer, etc.)
        exchange_rates = self._get_exchange_rates()

        # Convertir todo a USD primero, luego a moneda destino
        if from_currency != Currency.USD:
            usd_amount = amount / exchange_rates.get(from_currency.value, 1.0)
        else:
            usd_amount = amount

        if to_currency != Currency.USD:
            final_amount = usd_amount * exchange_rates.get(
                to_currency.value, 1.0
            )
        else:
            final_amount = usd_amount

        return round(final_amount, 2)

    def _get_exchange_rates(self) -> Dict[str, float]:
        """Obtiene tasas de cambio actuales (cacheable)"""

        cache_key = "exchange_rates"
        rates = cache.get(cache_key)

        if not rates:
            # En producción, usar API real de tasas de cambio
            rates = {
                "CUP": 120.0,  # Peso Cubano
                "USD": 1.0,  # Dólar base
                "EUR": 0.92,  # Euro
                "MXN": 17.5,  # Peso Mexicano
                "COP": 4100.0,  # Peso Colombiano
                "DOP": 57.0,  # Peso Dominicano
                "ARS": 350.0,  # Peso Argentino
            }

            # Cachear por 1 hora
            cache.set(cache_key, rates, 3600)

        return rates

    def get_supported_countries(self) -> List[Dict[str, Any]]:
        """Retorna lista de países soportados con información básica"""

        countries = []
        for country_code, config in self.countries_config.items():
            countries.append(
                {
                    "code": config.code,
                    "name": config.name,
                    "currency": config.currency.value,
                    "languages": config.languages,
                    "max_weight_kg": config.max_weight_kg,
                    "max_value_usd": config.max_value_usd,
                    "customs_required": config.customs_required,
                }
            )

        return countries

    def validate_international_address(
        self, country_code: str, postal_code: str, phone: str = None
    ) -> Dict[str, bool]:
        """Valida formato de dirección internacional"""

        config = self.get_country_config(country_code)
        if not config:
            return {"valid": False, "errors": ["País no soportado"]}

        validation = {"valid": True, "errors": []}

        # Validar código postal
        import re

        if not re.match(config.postal_code_format, postal_code):
            validation["valid"] = False
            validation["errors"].append("Formato de código postal inválido")

        # Validar teléfono si se proporciona
        if phone and not re.match(config.phone_format, phone):
            validation["valid"] = False
            validation["errors"].append("Formato de teléfono inválido")

        return validation

    def get_business_hours(self, country_code: str) -> Dict[str, Any]:
        """Obtiene horarios comerciales por país"""

        config = self.get_country_config(country_code)
        if not config:
            return {}

        return {
            "time_zone": config.time_zone,
            "working_days": config.working_days,
            "business_hours": "09:00-18:00",  # Horario estándar
            "weekend_service": False,
        }


# Instancia global del servicio
international_service = InternationalExpansionService()
