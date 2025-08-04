from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import transaction
from .models import Envio, HistorialEstado
from .serializers import EnvioSerializer, HistorialEstadoSerializer, CambioEstadoSerializer
from .notifications import enviar_notificacion_estado
from usuarios.permissions import EsAdministrador, EsCreadorOAdministrador

class EnvioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar envíos
    """
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_guia', 'estado_actual', 'remitente_nombre', 
                     'destinatario_nombre', 'descripcion']
    ordering_fields = ['fecha_creacion', 'fecha_estimada_entrega', 'estado_actual']    
    
    def get_permissions(self):
        """
        Personalización de permisos:
        - El endpoint de rastreo es público
        - Listar y ver detalles requiere autenticación
        - Crear, actualizar y eliminar requiere ser administrador o el creador
        """
        if self.action == 'rastrear':
            permission_classes = [AllowAny]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'cambiar_estado']:
            permission_classes = [EsCreadorOAdministrador]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_client_ip(self, request):
        """
        Obtiene la dirección IP real del cliente, considerando proxies
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Tomar la primera IP en la cadena de proxies
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    def perform_create(self, serializer):
        """
        Al crear un envío, registramos el usuario que lo creó y
        creamos el primer registro en el historial de estados
        """
        with transaction.atomic():
            # Guardar el envío con el usuario actual como creador
            envio = serializer.save(
                creado_por=self.request.user,
                actualizado_por=self.request.user
            )
            
            # Crear el primer registro en el historial
            HistorialEstado.objects.create(
                envio=envio,
                estado=envio.estado_actual,
                comentario="Creación del envío",
                registrado_por=self.request.user
            )
            
            # Enviar notificación de creación
            enviar_notificacion_estado(envio)
    
    def perform_update(self, serializer):
        """
        Al actualizar un envío, registramos el usuario que lo actualizó
        """
        serializer.save(actualizado_por=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """
        Endpoint para cambiar el estado de un envío y registrarlo en el historial
        """
        envio = self.get_object()
        serializer = CambioEstadoSerializer(data=request.data)
        if serializer.is_valid():
            estado = serializer.validated_data['estado']
            comentario = serializer.validated_data.get('comentario', '')
            ubicacion = serializer.validated_data.get('ubicacion', '')
            
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
                    registrado_por=request.user
                )
                
                # Enviar notificaciones por email
                enviar_notificacion_estado(envio, estado_anterior)
                
            # Devolver el envío actualizado
            return Response(EnvioSerializer(envio).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def buscar_por_guia(self, request):
        """
        Endpoint para buscar un envío por su número de guía
        """
        numero_guia = request.query_params.get('numero_guia', None)
        
        if not numero_guia:
            return Response(
                {"error": "Se requiere el parámetro numero_guia"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            envio = Envio.objects.get(numero_guia=numero_guia)
            serializer = self.get_serializer(envio)
            return Response(serializer.data)
        except Envio.DoesNotExist:
            return Response(
                {"error": "No se encontró ningún envío con ese número de guía"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def rastrear(self, request):
        """
        Endpoint público para rastrear un envío por su número de guía
        Se implementa rate limiting para prevenir abusos
        """
        # Verificar si hay demasiadas peticiones desde la misma IP
        ip = self.get_client_ip(request)
        
        # En una implementación real usaríamos un sistema de caché como Redis
        # para limitar las peticiones por IP
        
        numero_guia = request.query_params.get('numero_guia', None)
        
        if not numero_guia:
            return Response(
                {"error": "Se requiere el parámetro numero_guia"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Sanitizar la entrada para evitar posibles inyecciones
        numero_guia = numero_guia.strip()[:50]  # Limitar longitud
            
        try:
            envio = Envio.objects.get(numero_guia=numero_guia)
            # Usar un serializer simplificado que solo incluye la información pública
            data = {
                'numero_guia': envio.numero_guia,
                'estado': envio.estado_actual,
                'estado_display': envio.get_estado_actual_display(),
                'remitente_nombre': envio.remitente_nombre,
                'destinatario_nombre': envio.destinatario_nombre,
                'fecha_actualizacion': envio.ultima_actualizacion,
                'historial': [
                    {
                        'estado': h.estado,
                        'fecha': h.fecha,
                        'comentario': h.comentario,
                        'ubicacion': h.ubicacion
                    } for h in envio.historial.all().order_by('-fecha')
                ]
            }
            return Response(data)
        except Envio.DoesNotExist:
            return Response(
                {"error": "No se encontró ningún envío con ese número de guía"}, 
                status=status.HTTP_404_NOT_FOUND
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
        envio_id = self.request.query_params.get('envio', None)
        
        if envio_id:
            queryset = queryset.filter(envio_id=envio_id)
            
        return queryset
