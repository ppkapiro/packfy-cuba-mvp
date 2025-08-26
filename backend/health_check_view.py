from django.http import JsonResponse


def health_check(request):
    """
    Endpoint simple de health check para verificar que el backend
    está funcionando
    """
    return JsonResponse(
        {
            "status": "ok",
            "message": "Backend Django funcionando correctamente",
            "timestamp": "2025-08-25T20:45:00Z",
        }
    )
