"""
📊 PACKFY CUBA - Sistema de Monitoreo y Health Checks v4.1
Endpoint para verificar el estado de todos los servicios
"""

import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check completo del sistema
    """
    start_time = time.time()
    status = "healthy"
    services = {}

    # 1. Check Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        services["database"] = {
            "status": "healthy",
            "response_time": round((time.time() - start_time) * 1000, 2),
        }
    except Exception as e:
        services["database"] = {"status": "unhealthy", "error": str(e)}
        status = "degraded"

    # 2. Check Redis Cache
    redis_start = time.time()
    try:
        cache.set("health_check", "test", 10)
        cache.get("health_check")
        cache.delete("health_check")
        services["redis"] = {
            "status": "healthy",
            "response_time": round((time.time() - redis_start) * 1000, 2),
        }
    except Exception as e:
        services["redis"] = {"status": "unhealthy", "error": str(e)}
        status = "degraded"

    # 3. Check Disk Space
    try:
        import shutil

        disk_usage = shutil.disk_usage("/")
        free_space_percent = (disk_usage.free / disk_usage.total) * 100

        services["disk"] = {
            "status": "healthy" if free_space_percent > 10 else "warning",
            "free_space_percent": round(free_space_percent, 2),
            "free_gb": round(disk_usage.free / (1024**3), 2),
        }

        if free_space_percent <= 5:
            status = "critical"
        elif free_space_percent <= 10:
            status = "warning"

    except Exception as e:
        services["disk"] = {"status": "unknown", "error": str(e)}

    # 4. Check Memory Usage
    try:
        import psutil

        memory = psutil.virtual_memory()

        services["memory"] = {
            "status": "healthy" if memory.percent < 90 else "warning",
            "usage_percent": round(memory.percent, 2),
            "available_gb": round(memory.available / (1024**3), 2),
        }

        if memory.percent >= 95:
            status = "critical"
        elif memory.percent >= 90:
            status = "warning"

    except ImportError:
        services["memory"] = {
            "status": "unknown",
            "note": "psutil not installed",
        }
    except Exception as e:
        services["memory"] = {"status": "unknown", "error": str(e)}

    total_time = round((time.time() - start_time) * 1000, 2)

    response_data = {
        "status": status,
        "timestamp": timezone.now().isoformat(),
        "version": getattr(settings, "VERSION", "4.1.0"),
        "environment": getattr(settings, "ENVIRONMENT", "development"),
        "response_time_ms": total_time,
        "services": services,
        "uptime_seconds": time.time()
        - getattr(settings, "START_TIME", time.time()),
    }

    # Log health check
    if status in ["critical", "degraded"]:
        logger.error(f"Health check failed: {status} - {services}")
    else:
        logger.debug(f"Health check passed: {total_time}ms")

    # Return appropriate HTTP status
    http_status = {
        "healthy": 200,
        "warning": 200,
        "degraded": 503,
        "critical": 503,
    }.get(status, 200)

    return JsonResponse(response_data, status=http_status)


@api_view(["GET"])
@permission_classes([AllowAny])
def metrics(request):
    """
    Métricas básicas del sistema para monitoreo
    """
    try:
        from envios.models import Envio

        # Estadísticas de envíos
        total_envios = Envio.objects.count()
        envios_hoy = Envio.objects.filter(
            fecha_creacion__date=timezone.now().date()
        ).count()

        # Estados de envíos
        estados = {}
        for estado_choice in Envio.EstadoChoices:
            estados[estado_choice.value] = Envio.objects.filter(
                estado_actual=estado_choice.value
            ).count()

        metrics_data = {
            "timestamp": timezone.now().isoformat(),
            "business_metrics": {
                "total_envios": total_envios,
                "envios_hoy": envios_hoy,
                "estados_envios": estados,
            },
            "system_metrics": {
                "active_connections": len(connection.queries),
                "cache_stats": get_cache_stats(),
            },
        }

        return JsonResponse(metrics_data)

    except Exception as e:
        logger.error(f"Error obteniendo métricas: {e}")
        return JsonResponse(
            {
                "error": "Error obteniendo métricas",
                "timestamp": timezone.now().isoformat(),
            },
            status=500,
        )


def get_cache_stats():
    """Obtener estadísticas del cache"""
    try:
        # Test básico de cache
        test_key = f"cache_test_{int(time.time())}"
        cache.set(test_key, "test", 10)
        cache.get(test_key)
        cache.delete(test_key)

        return {"status": "operational", "test_passed": True}
    except Exception as e:
        return {"status": "error", "error": str(e), "test_passed": False}


@api_view(["GET"])
@permission_classes([AllowAny])
def version_info(request):
    """
    Información de versión y build
    """
    return JsonResponse(
        {
            "version": "4.1.0",
            "build_date": timezone.now().date().isoformat(),
            "environment": getattr(settings, "ENVIRONMENT", "development"),
            "debug": settings.DEBUG,
            "features": {
                "pwa": True,
                "security_enhanced": True,
                "error_handling": True,
                "performance_optimized": True,
                "monitoring": True,
            },
        }
    )
