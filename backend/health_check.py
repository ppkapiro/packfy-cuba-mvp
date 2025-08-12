import json
from datetime import datetime

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def health_check(request):
    """
    Endpoint de health check para verificar el estado del backend
    """
    try:
        # Verificar conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse(
            {
                "status": "healthy",
                "database": "connected",
                "service": "backend",
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0",
            }
        )
    except Exception as e:
        return JsonResponse(
            {
                "status": "unhealthy",
                "database": "disconnected",
                "service": "backend",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0",
            },
            status=500,
        )
