"""
🛡️ MIDDLEWARE DE PROTECCIÓN DE BASE DE DATOS
Intercepta operaciones destructivas en Django Admin y API
"""

import logging

from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from protector_bd import ProtectorBaseDatos

logger = logging.getLogger(__name__)


class ProteccionBaseDatosMiddleware:
    """
    Middleware que protege contra operaciones destructivas no autorizadas
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.protector = ProtectorBaseDatos()

        # URLs y acciones que requieren protección
        self.acciones_protegidas = {
            "delete": "ELIMINAR REGISTROS",
            "delete_selected": "ELIMINACIÓN MASIVA",
            "flush": "LIMPIAR BASE DE DATOS",
            "migrate": "EJECUTAR MIGRACIONES",
        }

        # Paths que requieren autorización especial
        self.paths_criticos = [
            "/admin/usuarios/usuario/",
            "/admin/empresas/empresa/",
            "/api/usuarios/",
            "/api/empresas/",
        ]

    def __call__(self, request):
        # Verificar si necesita protección antes del procesamiento
        if self.requiere_autorizacion(request):
            return self.manejar_operacion_protegida(request)

        response = self.get_response(request)
        return response

    def requiere_autorizacion(self, request) -> bool:
        """
        Determina si la operación requiere autorización
        """
        if not self.protector.esta_protegida():
            return False

        # Verificar método HTTP destructivo
        if request.method in ["DELETE"]:
            return True

        # Verificar acciones de admin
        if "action" in request.POST:
            accion = request.POST.get("action")
            if accion in self.acciones_protegidas:
                return True

        # Verificar paths críticos con POST/PUT
        if request.method in ["POST", "PUT", "PATCH"]:
            for path in self.paths_criticos:
                if request.path.startswith(path):
                    return True

        return False

    def manejar_operacion_protegida(self, request):
        """
        Maneja una operación que requiere autorización
        """
        operacion = self.determinar_operacion(request)

        # Log de la operación bloqueada
        logger.warning(
            f"Operación protegida detectada: {operacion} desde {request.META.get('REMOTE_ADDR')}"
        )

        # Si es una petición AJAX/API
        if request.headers.get("Accept", "").startswith(
            "application/json"
        ) or request.path.startswith("/api/"):
            return JsonResponse(
                {
                    "error": "Operación protegida",
                    "message": f'La operación "{operacion}" requiere autorización especial.',
                    "details": "La base de datos está protegida contra cambios no autorizados.",
                    "contact": "Contacte al administrador del sistema para autorización.",
                },
                status=403,
            )

        # Si es desde Django Admin
        if request.path.startswith("/admin/"):
            messages.error(
                request,
                f"🛡️ Operación bloqueada: {operacion}. "
                "La base de datos está protegida. "
                "Use el script de gestión protegida para cambios autorizados.",
            )

            # Redirigir a la página anterior o admin home
            return redirect(request.META.get("HTTP_REFERER", "/admin/"))

        # Respuesta HTML general
        return HttpResponseForbidden(
            f"""
        <html>
        <head><title>Operación Protegida</title></head>
        <body>
            <h1>🛡️ Operación Protegida</h1>
            <p><strong>Operación:</strong> {operacion}</p>
            <p><strong>Estado:</strong> La base de datos está protegida contra cambios no autorizados.</p>
            <p><strong>Solución:</strong> Use el script de gestión protegida:</p>
            <pre>python gestion_bd_protegida.py</pre>
            <p><a href="javascript:history.back()">← Volver</a></p>
        </body>
        </html>
        """
        )

    def determinar_operacion(self, request) -> str:
        """
        Determina qué operación se está intentando realizar
        """
        if request.method == "DELETE":
            return "ELIMINAR REGISTRO"

        if "action" in request.POST:
            accion = request.POST.get("action")
            return self.acciones_protegidas.get(accion, f"ACCIÓN: {accion}")

        if request.method in ["POST", "PUT", "PATCH"]:
            if "delete" in request.path.lower():
                return "ELIMINACIÓN"
            elif request.method == "POST":
                return "CREAR/MODIFICAR REGISTRO"
            else:
                return "MODIFICAR REGISTRO"

        return "OPERACIÓN DESCONOCIDA"
