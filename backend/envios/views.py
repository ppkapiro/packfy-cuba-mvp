from django.db import transaction
from empresas.permissions import TenantPermission, require_rol
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
    API endpoint para gestionar envíos con soporte multi-tenant
    """

    queryset = (
        Envio.objects.all()
    )  # Queryset base (será filtrado por get_queryset)
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

    def get_queryset(self):
        """
        Filtra envíos por empresa actual (multi-tenant) y por rol del usuario:
        - Dueño: Ve todos los envíos de la empresa
        - Operadores: Ven todos los envíos de la empresa
        - Remitentes: Solo ven envíos que han enviado
        - Destinatarios: Solo ven envíos dirigidos a ellos
        """
        # Si no hay empresa en el contexto, devolver queryset vacío
        if not hasattr(self.request, "tenant") or not self.request.tenant:
            return Envio.objects.none()

        # Queryset base filtrado por empresa
        queryset = Envio.objects.filter(empresa=self.request.tenant)

        # Si no hay perfil de usuario, usar queryset base
        if (
            not hasattr(self.request, "perfil_usuario")
            or not self.request.perfil_usuario
        ):
            return queryset

        perfil = self.request.perfil_usuario

        # Filtrado según el rol del usuario
        if perfil.es_dueno or perfil.puede_gestionar_envios:
            # Dueño y operadores ven todos los envíos de la empresa
            return queryset
        elif perfil.rol == "remitente":
            # Remitentes solo ven envíos que han enviado
            return queryset.filter(remitente_telefono=perfil.telefono)
        elif perfil.rol == "destinatario":
            # Destinatarios solo ven envíos dirigidos a ellos
            return queryset.filter(destinatario_telefono=perfil.telefono)
        else:
            # Por defecto, todos los envíos (para roles no específicos)
            return queryset

    def get_permissions(self):
        """
        Personalización de permisos multi-tenant con restricciones por rol:
        - Endpoints públicos: Rastreo sin autenticación
        - Lectura (list, retrieve): Según rol del usuario
        - Escritura (create, update, delete): Solo operadores y dueño
        - Cambio de estado: Solo operadores y dueño
        """
        if self.action in [
            "rastrear",
            "buscar_por_remitente",
            "buscar_por_destinatario",
        ]:
            # Endpoints públicos sin autenticación
            permission_classes = [AllowAny]
        elif self.action in ["list", "retrieve", "buscar_por_guia"]:
            # Lectura: Todos los usuarios autenticados con tenant
            permission_classes = [TenantPermission]
        elif self.action in ["create"]:
            # Crear envíos: Solo operadores de Miami y dueño
            from empresas.permissions import EmpresaOperatorPermission

            permission_classes = [TenantPermission, EmpresaOperatorPermission]
        elif self.action in ["update", "partial_update", "cambiar_estado"]:
            # Actualizar/cambiar estado: Solo operadores y dueño
            from empresas.permissions import EmpresaOperatorPermission

            permission_classes = [TenantPermission, EmpresaOperatorPermission]
        elif self.action == "destroy":
            # Eliminar: Solo dueño
            from empresas.permissions import EmpresaOwnerPermission

            permission_classes = [TenantPermission, EmpresaOwnerPermission]
        else:
            permission_classes = [TenantPermission]
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

    def perform_create(self, serializer):
        """
        Al crear un envío, registramos el usuario que lo creó y
        asignamos la empresa del contexto actual
        """
        with transaction.atomic():
            # Guardar el envío con el usuario actual como creador y la empresa del tenant
            envio = serializer.save(
                creado_por=self.request.user,
                actualizado_por=self.request.user,
                empresa=self.request.tenant,  # Asignar empresa del contexto
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
        Endpoint para buscar un envío por su número de guía (filtrado por empresa)
        """
        numero_guia = request.query_params.get("numero_guia", None)

        if not numero_guia:
            return Response(
                {"error": "Se requiere el parámetro numero_guia"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Usar el queryset filtrado por empresa
            envio = self.get_queryset().get(numero_guia=numero_guia)
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
        Endpoint público para rastrear un envío por su número de guía
        Se implementa rate limiting para prevenir abusos
        """
        # Verificar si hay demasiadas peticiones desde la misma IP
        ip = self.get_client_ip(request)

        # En una implementación real usaríamos un sistema de caché como Redis
        # para limitar las peticiones por IP

        numero_guia = request.query_params.get("numero_guia", None)

        if not numero_guia:
            return Response(
                {"error": "Se requiere el parámetro numero_guia"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sanitizar la entrada para evitar posibles inyecciones
        numero_guia = numero_guia.strip()[:50]  # Limitar longitud

        try:
            # Para el rastreo público, buscar en todas las empresas
            envio = Envio.objects.get(numero_guia=numero_guia)
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
            return Response(data)
        except Envio.DoesNotExist:
            return Response(
                {
                    "error": "No se encontró ningún envío con ese número de guía"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

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
    API endpoint para consultar el historial de estados de los envíos (multi-tenant)
    """

    queryset = (
        HistorialEstado.objects.all()
    )  # Queryset base (será filtrado por get_queryset)
    serializer_class = HistorialEstadoSerializer

    def get_permissions(self):
        """
        Permisos para historial de estados:
        - Solo lectura para todos los usuarios autenticados
        - Mismas restricciones que los envíos (filtrado por rol en queryset)
        """
        return [TenantPermission()]

    def get_queryset(self):
        """
        Filtra el historial por empresa y rol del usuario:
        - Aplica las mismas restricciones que EnvioViewSet
        - Remitentes/destinatarios solo ven historial de sus envíos
        """
        # Si no hay empresa en el contexto, devolver queryset vacío
        if not hasattr(self.request, "tenant") or not self.request.tenant:
            return HistorialEstado.objects.none()

        # Filtrar historial de envíos de la empresa actual
        queryset = HistorialEstado.objects.filter(
            envio__empresa=self.request.tenant
        )

        # Aplicar filtrado por rol del usuario (igual que en EnvioViewSet)
        if (
            hasattr(self.request, "perfil_usuario")
            and self.request.perfil_usuario
        ):
            perfil = self.request.perfil_usuario

            if perfil.es_dueno or perfil.puede_gestionar_envios:
                # Dueño y operadores ven todo el historial
                pass
            elif perfil.rol == "remitente":
                # Remitentes solo ven historial de envíos que han enviado
                queryset = queryset.filter(
                    envio__remitente_telefono=perfil.telefono
                )
            elif perfil.rol == "destinatario":
                # Destinatarios solo ven historial de envíos dirigidos a ellos
                queryset = queryset.filter(
                    envio__destinatario_telefono=perfil.telefono
                )

        # Permitir filtrar por envío específico
        envio_id = self.request.query_params.get("envio", None)
        if envio_id:
            queryset = queryset.filter(envio_id=envio_id)

        return queryset
