# 🇨🇺 PACKFY CUBA - Views Optimizadas con Caché v4.0
# Optimización de performance en las views principales

import logging

from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, Prefetch, Q, Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from usuarios.permissions import EsAdministrador, EsCreadorOAdministrador
from utils.cache_system import (
    CacheKeys,
    CacheTimeouts,
    SmartCache,
    cache_envio_data,
    cached_method,
    get_cached_envio,
    invalidate_envio_cache,
)

from .models import Envio, HistorialEstado
from .notifications import enviar_notificacion_estado
from .serializers import (
    CambioEstadoSerializer,
    EnvioSerializer,
    HistorialEstadoSerializer,
)

logger = logging.getLogger("packfy.views")


class OptimizedEnvioViewSet(viewsets.ModelViewSet):
    """
    ViewSet de envíos optimizado con caché y queries eficientes
    """

    serializer_class = EnvioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "numero_guia",
        "estado_actual",
        "remitente_nombre",
        "destinatario_nombre",
        "descripcion",
    ]
    ordering_fields = ["fecha_creacion", "estado_actual"]
    ordering = ["-fecha_creacion"]

    def get_queryset(self):
        """Queryset optimizado con prefetch y select_related"""

        # Query base optimizada
        queryset = Envio.objects.select_related(
            "usuario", "empresa"
        ).prefetch_related(
            Prefetch(
                "historial_estados",
                queryset=HistorialEstado.objects.select_related(
                    "usuario"
                ).order_by("-fecha_cambio"),
            )
        )

        # Filtros por usuario
        user = self.request.user
        if not (
            user.is_staff or getattr(user, "es_administrador_empresa", False)
        ):
            queryset = queryset.filter(usuario=user)

        # Filtros adicionales por parámetros
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado_actual=estado)

        fecha_desde = self.request.query_params.get("fecha_desde")
        if fecha_desde:
            queryset = queryset.filter(fecha_creacion__gte=fecha_desde)

        fecha_hasta = self.request.query_params.get("fecha_hasta")
        if fecha_hasta:
            queryset = queryset.filter(fecha_creacion__lte=fecha_hasta)

        return queryset

    @cached_method(timeout=CacheTimeouts.SHORT, key_prefix="envios")
    def list(self, request, *args, **kwargs):
        """Lista de envíos con caché inteligente"""

        # Generar clave de caché basada en parámetros
        user_id = request.user.id
        page = request.query_params.get("page", 1)
        search = request.query_params.get("search", "")
        estado = request.query_params.get("estado", "")

        cache_key = f"envios_list:{user_id}:page_{page}:search_{search}:estado_{estado}"

        # Intentar obtener del caché
        cached_response = cache.get(cache_key)
        if cached_response:
            logger.debug(f"Cache hit for envios list: {cache_key}")
            return Response(cached_response)

        # Ejecutar query normal
        response = super().list(request, *args, **kwargs)

        # Cachear respuesta si es exitosa
        if response.status_code == 200:
            cache.set(cache_key, response.data, CacheTimeouts.SHORT)
            logger.debug(f"Cache set for envios list: {cache_key}")

        return response

    def retrieve(self, request, *args, **kwargs):
        """Detalle de envío con caché"""

        envio_id = kwargs.get("pk")

        # Intentar obtener del caché
        cached_data = get_cached_envio(envio_id)
        if cached_data:
            logger.debug(f"Cache hit for envio {envio_id}")
            return Response(cached_data)

        # Obtener envío con queries optimizadas
        try:
            envio = self.get_queryset().get(pk=envio_id)
            serializer = self.get_serializer(envio)

            # Cachear datos
            cache_envio_data(envio_id, serializer.data, CacheTimeouts.MEDIUM)

            return Response(serializer.data)

        except Envio.DoesNotExist:
            return Response(
                {"error": "Envío no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def create(self, request, *args, **kwargs):
        """Crear envío e invalidar caché relacionado"""

        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            # Invalidar caché de listas del usuario
            user_id = request.user.id
            self._invalidate_user_envios_cache(user_id)

            logger.info(
                f"Envío creado, caché invalidado para usuario {user_id}"
            )

        return response

    def update(self, request, *args, **kwargs):
        """Actualizar envío e invalidar caché"""

        envio_id = kwargs.get("pk")

        response = super().update(request, *args, **kwargs)

        if response.status_code == 200:
            # Invalidar caché específico del envío
            envio = self.get_object()
            invalidate_envio_cache(envio_id, envio.numero_guia)

            # Invalidar listas del usuario
            self._invalidate_user_envios_cache(envio.usuario_id)

            logger.info(f"Envío {envio_id} actualizado, caché invalidado")

        return response

    @action(detail=True, methods=["post"])
    def cambiar_estado(self, request, pk=None):
        """Cambiar estado con optimizaciones"""

        envio = self.get_object()
        serializer = CambioEstadoSerializer(data=request.data)

        if serializer.is_valid():
            nuevo_estado = serializer.validated_data["nuevo_estado"]
            observaciones = serializer.validated_data.get("observaciones", "")

            with transaction.atomic():
                # Actualizar estado
                envio.estado_actual = nuevo_estado
                envio.save(update_fields=["estado_actual"])

                # Crear historial
                HistorialEstado.objects.create(
                    envio=envio,
                    estado_anterior=envio.estado_actual,
                    estado_nuevo=nuevo_estado,
                    usuario=request.user,
                    observaciones=observaciones,
                )

                # Invalidar cachés relacionados
                invalidate_envio_cache(pk, envio.numero_guia)
                self._invalidate_user_envios_cache(envio.usuario_id)

                # Enviar notificación (asíncrono si es posible)
                try:
                    enviar_notificacion_estado(envio, nuevo_estado)
                except Exception as e:
                    logger.error(f"Error enviando notificación: {e}")

            return Response(
                {
                    "message": "Estado actualizado correctamente",
                    "nuevo_estado": nuevo_estado,
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    @cached_method(timeout=CacheTimeouts.MEDIUM, key_prefix="envios_stats")
    def estadisticas(self, request):
        """Estadísticas optimizadas con caché"""

        user = request.user

        # Query optimizada para estadísticas
        queryset = self.get_queryset()

        stats = queryset.aggregate(
            total_envios=Count("id"),
            total_pendientes=Count("id", filter=Q(estado_actual="PENDIENTE")),
            total_en_transito=Count(
                "id", filter=Q(estado_actual="EN_TRANSITO")
            ),
            total_entregados=Count("id", filter=Q(estado_actual="ENTREGADO")),
        )

        # Estadísticas por mes (últimos 6 meses)
        from datetime import timedelta

        from django.utils import timezone

        hace_6_meses = timezone.now() - timedelta(days=180)
        envios_por_mes = (
            queryset.filter(fecha_creacion__gte=hace_6_meses)
            .extra({"mes": "date_trunc('month', fecha_creacion)"})
            .values("mes")
            .annotate(cantidad=Count("id"))
            .order_by("mes")
        )

        return Response(
            {
                "resumen": stats,
                "por_mes": list(envios_por_mes),
                "cache_info": {
                    "cached_at": timezone.now().isoformat(),
                    "cache_timeout": CacheTimeouts.MEDIUM,
                },
            }
        )

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def seguimiento_publico(self, request):
        """Seguimiento público optimizado con caché"""

        numero_guia = request.query_params.get("numero_guia")
        if not numero_guia:
            return Response(
                {"error": "Número de guía requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Intentar obtener del caché
        cache_key = CacheKeys.ENVIO_TRACKING.format(
            numero_seguimiento=numero_guia
        )
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.debug(f"Cache hit for tracking: {numero_guia}")
            return Response(cached_data)

        try:
            # Query optimizada para seguimiento
            envio = (
                Envio.objects.select_related("empresa")
                .prefetch_related("historial_estados__usuario")
                .get(numero_guia=numero_guia)
            )

            tracking_data = {
                "numero_guia": envio.numero_guia,
                "estado_actual": envio.estado_actual,
                "fecha_creacion": envio.fecha_creacion,
                "empresa": envio.empresa.nombre if envio.empresa else None,
                "historial": [
                    {
                        "estado": hist.estado_nuevo,
                        "fecha": hist.fecha_cambio,
                        "observaciones": hist.observaciones,
                    }
                    for hist in envio.historial_estados.all()
                ],
            }

            # Cachear datos de seguimiento
            cache.set(cache_key, tracking_data, CacheTimeouts.TRACKING)

            return Response(tracking_data)

        except Envio.DoesNotExist:
            return Response(
                {"error": "Envío no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def _invalidate_user_envios_cache(self, user_id: int):
        """Invalidar caché de envíos de un usuario"""
        patterns = [f"envios_list:{user_id}:*", f"envios_stats:{user_id}:*"]

        # Invalidación simple - en producción usaríamos Redis SCAN
        for i in range(1, 11):  # Páginas 1-10
            cache_keys = [
                f"envios_list:{user_id}:page_{i}:search_:estado_",
                f"envios_list:{user_id}:page_{i}:search_*:estado_*",
            ]
            cache.delete_many(cache_keys)


# Mantener la clase original como alias
class EnvioViewSet(OptimizedEnvioViewSet):
    """Alias para compatibilidad hacia atrás"""

    pass
