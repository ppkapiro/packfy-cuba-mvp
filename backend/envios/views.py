import logging

from django.core.cache import cache
from django.db import transaction
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from usuarios.permissions import EsAdministrador, EsCreadorOAdministrador

from .models import Envio, HistorialEstado
from .notifications import enviar_notificacion_estado
from .serializers import (
    CambioEstadoSerializer,
    EnvioSerializer,
    HistorialEstadoSerializer,
)


class EnvioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar envíos
    """

    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "numero_guia",
        "estado_actual",
        "remitente_nombre",
        "destinatario_nombre",
        "descripcion",
    ]
    ordering_fields = [
        "fecha_creacion",
        "fecha_estimada_entrega",
        "estado_actual",
    ]

    def get_permissions(self):
        """
        Personalización de permisos:
        - El endpoint de rastreo es público
        - Listar y ver detalles requiere autenticación
        - Crear, actualizar y eliminar requiere ser administrador o el creador
        """
        if self.action in [
            "rastrear",
            "buscar_por_remitente",
            "buscar_por_destinatario",
        ]:
            permission_classes = [AllowAny]
        elif self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "cambiar_estado",
        ]:
            permission_classes = [EsCreadorOAdministrador]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_client_ip(self, request):
        """
        Obtiene la dirección IP real del cliente, considerando proxies
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # Tomar la primera IP en la cadena de proxies
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def get_queryset(self):
        qs = Envio.objects.all()
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated:
            empresa = getattr(user, "empresa", None)
            if empresa:
                qs = qs.filter(empresa=empresa)
        return qs

    def perform_create(self, serializer):
        """
        Al crear un envío, registramos el usuario que lo creó y
        creamos el primer registro en el historial de estados
        """
        with transaction.atomic():
            # Guardar el envío con el usuario actual como creador
            envio = serializer.save(
                creado_por=self.request.user,
                actualizado_por=self.request.user,
                usuario=self.request.user,
                empresa=getattr(self.request.user, "empresa", None),
            )

            # Crear el primer registro en el historial
            HistorialEstado.objects.create(
                envio=envio,
                estado=envio.estado_actual,
                comentario="Creación del envío",
                registrado_por=self.request.user,
            )

            # Enviar notificación de creación
            enviar_notificacion_estado(envio)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Log de depuración: mostrar errores del serializer
            logger = logging.getLogger(__name__)
            try:
                logger.debug({"envio_create_errors": serializer.errors})
            except Exception:
                pass
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_update(self, serializer):
        """
        Al actualizar un envío, registramos el usuario que lo actualizó
        """
        serializer.save(actualizado_por=self.request.user)

    @action(detail=True, methods=["post"])
    def cambiar_estado(self, request, pk=None):
        """
        Endpoint para cambiar el estado de un envío y registrarlo en el historial
        """
        envio = self.get_object()
        serializer = CambioEstadoSerializer(data=request.data)
        if serializer.is_valid():
            estado = serializer.validated_data["estado"]
            comentario = serializer.validated_data.get("comentario", "")
            ubicacion = serializer.validated_data.get("ubicacion", "")

            # Guardar el estado anterior para las notificaciones
            estado_anterior = envio.estado_actual

            with transaction.atomic():
                # Actualizar el estado del envío
                envio.estado_actual = estado
                envio.actualizado_por = request.user
                envio.save()

                # Crear registro en el historial
                HistorialEstado.objects.create(
                    envio=envio,
                    estado=estado,
                    comentario=comentario,
                    ubicacion=ubicacion,
                    registrado_por=request.user,
                )

                # Enviar notificaciones por email
                enviar_notificacion_estado(envio, estado_anterior)

            # Devolver el envío actualizado
            return Response(EnvioSerializer(envio).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def buscar_por_guia(self, request):
        """
        Endpoint para buscar un envío por su número de guía
        """
        numero_guia = request.query_params.get("numero_guia", None)

        if not numero_guia:
            return Response(
                {"error": "Se requiere el parámetro numero_guia"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            envio = Envio.objects.get(numero_guia=numero_guia)
            serializer = self.get_serializer(envio)
            return Response(serializer.data)
        except Envio.DoesNotExist:
            return Response(
                {
                    "error": "No se encontró ningún envío con ese número de guía"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def rastrear(self, request):
        """
        Endpoint público para rastrear un envío por su número de guía.
        """
        # Nota: Para rate limiting real se recomienda Redis u otro backend de caché distribuido.
        _ = self.get_client_ip(request)

        numero_guia = request.query_params.get("numero_guia")
        if not numero_guia:
            return Response(
                {"error": "Se requiere el parámetro numero_guia"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sanitizar la entrada para evitar posibles inyecciones
        numero_guia = numero_guia.strip()[:50]

        cache_key = f"rastrear:{numero_guia}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        try:
            envio = Envio.objects.get(numero_guia=numero_guia)
        except Envio.DoesNotExist:
            return Response(
                {
                    "error": "No se encontró ningún envío con ese número de guía"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Usar un serializer simplificado que solo incluye la información pública
        data = {
            "numero_guia": envio.numero_guia,
            "estado": envio.estado_actual,
            "estado_display": envio.get_estado_actual_display(),
            "remitente_nombre": envio.remitente_nombre,
            "destinatario_nombre": envio.destinatario_nombre,
            "fecha_actualizacion": envio.ultima_actualizacion,
            "historial": [
                {
                    "estado": h.estado,
                    "fecha": h.fecha,
                    "comentario": h.comentario,
                    "ubicacion": h.ubicacion,
                }
                for h in envio.historial.all().order_by("-fecha")
            ],
        }
        cache.set(cache_key, data, timeout=30)  # Cache 30s
        return Response(data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def buscar_por_remitente(self, request):
        """
        Endpoint público para buscar envíos por nombre del remitente
        """
        nombre_remitente = request.query_params.get("nombre", None)

        if not nombre_remitente:
            return Response(
                {
                    "error": "Se requiere el parámetro 'nombre' para buscar por remitente"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sanitizar la entrada
        nombre_remitente = nombre_remitente.strip()[:100]

        try:
            # Buscar envíos que contengan el nombre del remitente (búsqueda parcial)
            envios = Envio.objects.filter(
                remitente_nombre__icontains=nombre_remitente
            ).order_by("-fecha_creacion")[
                :10
            ]  # Limitar a 10 resultados

            if not envios.exists():
                return Response(
                    {
                        "error": f"No se encontraron envíos para el remitente: '{nombre_remitente}'"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Crear respuesta con información simplificada
            resultados = []
            for envio in envios:
                resultados.append(
                    {
                        "numero_guia": envio.numero_guia,
                        "estado": envio.estado_actual,
                        "estado_display": envio.get_estado_actual_display(),
                        "remitente_nombre": envio.remitente_nombre,
                        "destinatario_nombre": envio.destinatario_nombre,
                        "fecha_actualizacion": envio.ultima_actualizacion,
                    }
                )

            return Response({"count": len(resultados), "results": resultados})

        except Exception as e:
            return Response(
                {"error": f"Error en la búsqueda: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AllowAny],
    )
    def estadisticas(self, request):
        """Estadísticas agregadas simples por estado (cache 60s)."""
        from datetime import timedelta

        from django.db import connection
        from django.db.models import Count
        from django.utils import timezone

        cache_key = "envios:estadisticas:v1"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        data = None
        try:
            with connection.cursor() as cur:
                cur.execute(
                    "SELECT estado_actual, total FROM envio_estado_stats"
                )
                rows = cur.fetchall()
                total_envios = sum(r[1] for r in rows)
                data = {
                    "total": total_envios,
                    "por_estado": {r[0]: r[1] for r in rows},
                    "origen": "matview",
                }
        except Exception:
            # Fallback directo si la vista no existe
            qs = (
                Envio.objects.values("estado_actual")
                .annotate(total=Count("id"))
                .order_by("estado_actual")
            )
            total_envios = sum(r["total"] for r in qs)
            data = {
                "total": total_envios,
                "por_estado": {r["estado_actual"]: r["total"] for r in qs},
                "origen": "query",
            }

        # Métricas adicionales (no presentes en la matview):
        today_start = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        seven_days_ago = timezone.now() - timedelta(days=7)
        pendientes = Envio.objects.exclude(
            estado_actual__in=["ENTREGADO", "CANCELADO", "DEVUELTO"]
        ).count()
        entregados_hoy = Envio.objects.filter(
            estado_actual="ENTREGADO", ultima_actualizacion__gte=today_start
        ).count()
        recientes = Envio.objects.filter(
            fecha_creacion__gte=seven_days_ago
        ).count()

        # Añadir claves snake y camel para compatibilidad con frontend
        por_estado = data.get("por_estado", {}) if data else {}
        data = data or {"total": 0, "por_estado": {}, "origen": "query"}
        data.update(
            {
                "pendientes": pendientes,
                "entregados_hoy": entregados_hoy,
                "recientes": recientes,
                "porEstado": por_estado,
                "entregadosHoy": entregados_hoy,
            }
        )
        cache.set(cache_key, data, 60)
        return Response(data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def buscar_por_destinatario(self, request):
        """
        Endpoint público para buscar envíos por nombre del destinatario
        """
        nombre_destinatario = request.query_params.get("nombre", None)

        if not nombre_destinatario:
            return Response(
                {
                    "error": "Se requiere el parámetro 'nombre' para buscar por destinatario"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sanitizar la entrada
        nombre_destinatario = nombre_destinatario.strip()[:100]

        try:
            # Buscar envíos que contengan el nombre del destinatario (búsqueda parcial)
            envios = Envio.objects.filter(
                destinatario_nombre__icontains=nombre_destinatario
            ).order_by("-fecha_creacion")[
                :10
            ]  # Limitar a 10 resultados

            if not envios.exists():
                return Response(
                    {
                        "error": f"No se encontraron envíos para el destinatario: '{nombre_destinatario}'"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Crear respuesta con información simplificada
            resultados = []
            for envio in envios:
                resultados.append(
                    {
                        "numero_guia": envio.numero_guia,
                        "estado": envio.estado_actual,
                        "estado_display": envio.get_estado_actual_display(),
                        "remitente_nombre": envio.remitente_nombre,
                        "destinatario_nombre": envio.destinatario_nombre,
                        "fecha_actualizacion": envio.ultima_actualizacion,
                    }
                )

            return Response({"count": len(resultados), "results": resultados})

        except Exception as e:
            return Response(
                {"error": f"Error en la búsqueda: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class HistorialEstadoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para consultar el historial de estados de los envíos
    """

    queryset = HistorialEstado.objects.all()
    serializer_class = HistorialEstadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Permite filtrar el historial por envío usando el parámetro 'envio'
        """
        queryset = HistorialEstado.objects.all()
        envio_id = self.request.query_params.get("envio", None)

        if envio_id:
            queryset = queryset.filter(envio_id=envio_id)

        return queryset
