# 🇨🇺 PACKFY CUBA - Sistema de Caché Avanzado v4.0
# Configuración y gestión de caché con Redis para optimización de performance

import hashlib
import json
import logging
from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Optional

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger("packfy.cache")


class CacheKeys:
    """Constantes para claves de caché organizadas"""

    # Usuarios y autenticación
    USER_PROFILE = "user_profile:{user_id}"
    USER_PERMISSIONS = "user_permissions:{user_id}"
    USER_EMPRESAS = "user_empresas:{user_id}"

    # Envíos y seguimiento
    ENVIO_DETAIL = "envio_detail:{envio_id}"
    ENVIO_TRACKING = "envio_tracking:{numero_seguimiento}"
    ENVIOS_USER = "envios_user:{user_id}:page_{page}"
    ENVIOS_STATS = "envios_stats:{empresa_id}"

    # Empresas y configuraciones
    EMPRESA_INFO = "empresa_info:{empresa_id}"
    SISTEMA_CONFIG = "sistema_config"

    # Estadísticas y dashboards
    DASHBOARD_STATS = "dashboard_stats:{user_id}:{periodo}"
    ANALYTICS_DATA = "analytics:{empresa_id}:{tipo}:{fecha}"


class CacheTimeouts:
    """Tiempos de caché organizados por tipo de dato"""

    # Cortos (datos que cambian frecuentemente)
    SHORT = 300  # 5 minutos
    TRACKING = 180  # 3 minutos

    # Medios (datos semi-estáticos)
    MEDIUM = 1800  # 30 minutos
    USER_DATA = 900  # 15 minutos

    # Largos (datos estáticos)
    LONG = 3600  # 1 hora
    CONFIG = 7200  # 2 horas

    # Muy largos (datos que casi no cambian)
    VERY_LONG = 86400  # 24 horas


def cache_key_for_user(base_key: str, user_id: int, **kwargs) -> str:
    """Generar clave de caché específica para usuario"""
    key_parts = [base_key, str(user_id)]

    for k, v in kwargs.items():
        key_parts.append(f"{k}_{v}")

    return ":".join(key_parts)


def invalidate_user_cache(user_id: int) -> None:
    """Invalidar todo el caché relacionado con un usuario"""
    patterns = [
        f"user_*:{user_id}",
        f"envios_user:{user_id}:*",
        f"dashboard_stats:{user_id}:*",
    ]

    for pattern in patterns:
        try:
            # En Redis real usaríamos SCAN con pattern
            # Por ahora limpiamos claves conocidas
            cache.delete_many(
                [
                    CacheKeys.USER_PROFILE.format(user_id=user_id),
                    CacheKeys.USER_PERMISSIONS.format(user_id=user_id),
                    CacheKeys.USER_EMPRESAS.format(user_id=user_id),
                ]
            )
            logger.info(f"Cache invalidated for user {user_id}")
        except Exception as e:
            logger.error(f"Error invalidating cache for user {user_id}: {e}")


def cached_method(timeout: int = CacheTimeouts.MEDIUM, key_prefix: str = None):
    """
    Decorador para cachear métodos de viewsets y servicios
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generar clave de caché basada en función y argumentos
            func_name = f"{func.__module__}.{func.__name__}"
            if key_prefix:
                func_name = f"{key_prefix}.{func_name}"

            # Crear hash de argumentos para la clave
            args_hash = hashlib.md5(
                json.dumps(
                    str(args) + str(sorted(kwargs.items())), sort_keys=True
                ).encode()
            ).hexdigest()[:8]

            cache_key = f"method_cache:{func_name}:{args_hash}"

            # Intentar obtener del caché
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func_name}")
                return cached_result

            # Ejecutar función y cachear resultado
            result = func(*args, **kwargs)

            try:
                cache.set(cache_key, result, timeout)
                logger.debug(
                    f"Cache set for {func_name} with timeout {timeout}s"
                )
            except Exception as e:
                logger.warning(f"Failed to cache {func_name}: {e}")

            return result

        return wrapper

    return decorator


class SmartCache:
    """
    Sistema de caché inteligente con invalidación automática
    """

    @staticmethod
    def get_or_set(
        key: str, default_func: Callable, timeout: int = CacheTimeouts.MEDIUM
    ) -> Any:
        """Obtener del caché o ejecutar función y cachear resultado"""

        cached_value = cache.get(key)
        if cached_value is not None:
            logger.debug(f"Cache hit: {key}")
            return cached_value

        # Ejecutar función para obtener valor
        try:
            value = default_func()
            cache.set(key, value, timeout)
            logger.debug(f"Cache set: {key} (timeout: {timeout}s)")
            return value
        except Exception as e:
            logger.error(f"Error getting/setting cache {key}: {e}")
            # Devolver resultado sin cachear en caso de error
            return default_func()

    @staticmethod
    def invalidate_patterns(patterns: list) -> int:
        """Invalidar múltiples patrones de caché"""
        invalidated = 0

        for pattern in patterns:
            try:
                # Implementación básica - en producción usaríamos Redis SCAN
                if "*" in pattern:
                    # Para patrones simples, intentamos claves conocidas
                    base_pattern = pattern.replace("*", "")
                    # Este es un enfoque simplificado
                    pass
                else:
                    cache.delete(pattern)
                    invalidated += 1
            except Exception as e:
                logger.error(f"Error invalidating pattern {pattern}: {e}")

        return invalidated

    @staticmethod
    def warm_up_cache():
        """Precalentar caché con datos frecuentemente accedidos"""
        logger.info("Starting cache warm-up...")

        try:
            # Calentar configuración del sistema
            from empresas.models import Empresa

            empresas = Empresa.objects.all()[:10]  # Primeras 10 empresas

            for empresa in empresas:
                cache_key = CacheKeys.EMPRESA_INFO.format(
                    empresa_id=empresa.id
                )
                if not cache.get(cache_key):
                    empresa_data = {
                        "id": empresa.id,
                        "nombre": empresa.nombre,
                        "activa": empresa.activa,
                    }
                    cache.set(cache_key, empresa_data, CacheTimeouts.LONG)

            logger.info(f"Cache warmed up for {len(empresas)} empresas")

        except Exception as e:
            logger.error(f"Error during cache warm-up: {e}")


class DatabaseQueryOptimizer:
    """
    Optimizador de queries de base de datos
    """

    @staticmethod
    def optimize_envio_queries():
        """Optimizar queries comunes de envíos"""
        from django.db import connection

        # Queries de optimización
        optimization_queries = [
            # Índices para búsquedas frecuentes
            """
            CREATE INDEX IF NOT EXISTS idx_envios_numero_seguimiento
            ON envios_envio(numero_seguimiento);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_envios_usuario_fecha
            ON envios_envio(usuario_id, fecha_creacion);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_envios_estado_fecha
            ON envios_envio(estado, fecha_creacion);
            """,
            # Índice compuesto para paginación
            """
            CREATE INDEX IF NOT EXISTS idx_envios_empresa_estado_fecha
            ON envios_envio(empresa_id, estado, fecha_creacion DESC);
            """,
        ]

        with connection.cursor() as cursor:
            for query in optimization_queries:
                try:
                    cursor.execute(query)
                    logger.info("Database index created successfully")
                except Exception as e:
                    logger.warning(
                        f"Index creation failed (may already exist): {e}"
                    )


# Funciones utilitarias de caché


def cache_envio_data(
    envio_id: int, data: dict, timeout: int = CacheTimeouts.MEDIUM
):
    """Cachear datos de un envío específico"""
    cache_key = CacheKeys.ENVIO_DETAIL.format(envio_id=envio_id)
    cache.set(cache_key, data, timeout)

    # También cachear por número de seguimiento si está disponible
    if "numero_seguimiento" in data:
        tracking_key = CacheKeys.ENVIO_TRACKING.format(
            numero_seguimiento=data["numero_seguimiento"]
        )
        cache.set(tracking_key, data, timeout)


def get_cached_envio(envio_id: int) -> Optional[dict]:
    """Obtener datos cacheados de un envío"""
    cache_key = CacheKeys.ENVIO_DETAIL.format(envio_id=envio_id)
    return cache.get(cache_key)


def invalidate_envio_cache(envio_id: int, numero_seguimiento: str = None):
    """Invalidar caché de un envío específico"""
    cache_keys = [CacheKeys.ENVIO_DETAIL.format(envio_id=envio_id)]

    if numero_seguimiento:
        cache_keys.append(
            CacheKeys.ENVIO_TRACKING.format(
                numero_seguimiento=numero_seguimiento
            )
        )

    cache.delete_many(cache_keys)


def cache_dashboard_stats(user_id: int, periodo: str, stats: dict):
    """Cachear estadísticas del dashboard"""
    cache_key = CacheKeys.DASHBOARD_STATS.format(
        user_id=user_id, periodo=periodo
    )
    cache.set(cache_key, stats, CacheTimeouts.MEDIUM)


def get_cached_dashboard_stats(user_id: int, periodo: str) -> Optional[dict]:
    """Obtener estadísticas cacheadas del dashboard"""
    cache_key = CacheKeys.DASHBOARD_STATS.format(
        user_id=user_id, periodo=periodo
    )
    return cache.get(cache_key)
