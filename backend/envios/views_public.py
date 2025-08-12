# views_public.py - Views públicas para el sistema
from envios.models import Envio
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def rastrear_por_nombre_publico(request):
    """
    Endpoint público para rastrear envíos por nombre (remitente o destinatario)
    """
    nombre = request.query_params.get("nombre", None)
    tipo = request.query_params.get("tipo", "ambos")

    if not nombre:
        return Response(
            {"error": "Se requiere el parámetro nombre"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Limpiar entrada
    nombre = nombre.strip()

    if len(nombre) < 2:
        return Response(
            {"error": "El nombre debe tener al menos 2 caracteres"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Construir query
    queryset = Envio.objects.none()

    if tipo in ["remitente", "ambos"]:
        remitente_query = Envio.objects.filter(remitente_nombre__icontains=nombre)
        queryset = queryset.union(remitente_query)

    if tipo in ["destinatario", "ambos"]:
        destinatario_query = Envio.objects.filter(destinatario_nombre__icontains=nombre)
        queryset = queryset.union(destinatario_query)

    # Ordenar y limitar resultados
    envios = queryset.order_by("-fecha_creacion")[:20]

    if not envios:
        return Response(
            {"error": f"No se encontraron envíos para '{nombre}'"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Datos públicos simplificados
    data = {
        "resultados": len(envios),
        "nombre_buscado": nombre,
        "tipo_busqueda": tipo,
        "envios": [
            {
                "numero_guia": envio.numero_guia,
                "estado": envio.estado_actual,
                "estado_display": envio.get_estado_actual_display(),
                "remitente_nombre": envio.remitente_nombre,
                "destinatario_nombre": envio.destinatario_nombre,
                "fecha_creacion": envio.fecha_creacion,
                "ultima_actualizacion": envio.ultima_actualizacion,
            }
            for envio in envios
        ],
    }

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def rastrear_por_guia_publico(request):
    """
    Endpoint público para rastrear un envío por su número de guía
    """
    numero_guia = request.query_params.get("numero_guia", None)

    if not numero_guia:
        return Response(
            {"error": "Se requiere el parámetro numero_guia"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Sanitizar la entrada para evitar posibles inyecciones
    numero_guia = numero_guia.strip()[:50]  # Limitar longitud

    try:
        envio = Envio.objects.get(numero_guia=numero_guia)
        # Usar datos públicos simplificados
        data = {
            "numero_guia": envio.numero_guia,
            "estado": envio.estado_actual,
            "estado_display": envio.get_estado_actual_display(),
            "remitente_nombre": envio.remitente_nombre,
            "destinatario_nombre": envio.destinatario_nombre,
            "fecha_creacion": envio.fecha_creacion,
            "ultima_actualizacion": envio.ultima_actualizacion,
        }
        return Response(data)
    except Envio.DoesNotExist:
        return Response(
            {"error": "No se encontró ningún envío con ese número de guía"},
            status=status.HTTP_404_NOT_FOUND,
        )
