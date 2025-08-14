# 🇨🇺 PACKFY CUBA - Servicio de Sincronización Global v4.0
import asyncio
import hashlib
import json
import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import aioredis

logger = logging.getLogger(__name__)


class SyncEventType(Enum):
    """Tipos de eventos de sincronización"""

    SHIPMENT_CREATED = "shipment_created"
    SHIPMENT_UPDATED = "shipment_updated"
    SHIPMENT_STATUS_CHANGED = "shipment_status_changed"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    PAYMENT_PROCESSED = "payment_processed"
    INVENTORY_UPDATED = "inventory_updated"
    CUSTOM_EVENT = "custom_event"


class SyncPriority(Enum):
    """Prioridades de sincronización"""

    CRITICAL = 1  # Inmediata
    HIGH = 2  # < 5 segundos
    NORMAL = 3  # < 30 segundos
    LOW = 4  # < 5 minutos


@dataclass
class SyncEvent:
    """Evento de sincronización entre regiones"""

    id: str
    event_type: SyncEventType
    priority: SyncPriority
    source_region: str
    target_regions: List[str]
    data: Dict[str, Any]
    timestamp: str
    retry_count: int = 0
    max_retries: int = 3
    checksum: str = ""

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._generate_checksum()

    def _generate_checksum(self) -> str:
        """Genera checksum para verificar integridad"""
        data_str = json.dumps(self.data, sort_keys=True)
        content = f"{self.event_type.value}:{data_str}:{self.timestamp}"
        return hashlib.md5(content.encode()).hexdigest()


class GlobalSyncService:
    """
    Servicio de sincronización global para PACKFY CUBA
    Maneja replicación de datos entre múltiples regiones
    """

    def __init__(self):
        self.redis_client = None
        self.subscribers = {}  # event_type -> List[callback]
        self.sync_queue = asyncio.Queue()
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.regions = {
            "cuba": {"endpoint": "redis://cuba-redis:6379", "active": True},
            "mexico": {
                "endpoint": "redis://mexico-redis:6379",
                "active": False,
            },
            "colombia": {
                "endpoint": "redis://colombia-redis:6379",
                "active": False,
            },
            "usa": {"endpoint": "redis://usa-redis:6379", "active": False},
            "spain": {"endpoint": "redis://spain-redis:6379", "active": False},
        }

    async def initialize(self, redis_url: str = "redis://localhost:6379"):
        """Inicializa el servicio de sincronización"""
        try:
            self.redis_client = await aioredis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
            )

            # Iniciar procesamiento de cola
            if not self.running:
                self.running = True
                asyncio.create_task(self._process_sync_queue())
                asyncio.create_task(self._listen_for_events())

            logger.info("Servicio de sincronización global inicializado")

        except Exception as e:
            logger.error(
                f"Error inicializando servicio de sincronización: {e}"
            )
            raise

    async def publish_event(
        self,
        event_type: SyncEventType,
        data: Dict[str, Any],
        source_region: str = "cuba",
        target_regions: List[str] = None,
        priority: SyncPriority = SyncPriority.NORMAL,
    ) -> str:
        """
        Publica evento para sincronización global
        """
        try:
            event_id = str(uuid.uuid4())

            if target_regions is None:
                target_regions = [
                    region
                    for region in self.regions.keys()
                    if region != source_region
                    and self.regions[region]["active"]
                ]

            sync_event = SyncEvent(
                id=event_id,
                event_type=event_type,
                priority=priority,
                source_region=source_region,
                target_regions=target_regions,
                data=data,
                timestamp=datetime.utcnow().isoformat(),
            )

            # Agregar a cola de sincronización
            await self.sync_queue.put(sync_event)

            # Almacenar evento para auditoría
            await self._store_event(sync_event)

            logger.info(
                f"Evento {event_type.value} publicado con ID {event_id}"
            )
            return event_id

        except Exception as e:
            logger.error(f"Error publicando evento: {e}")
            raise

    async def subscribe_to_event(
        self,
        event_type: SyncEventType,
        callback: Callable[[Dict[str, Any]], None],
    ):
        """
        Suscribe callback a tipo de evento específico
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(callback)
        logger.info(f"Callback suscrito a eventos {event_type.value}")

    async def sync_shipment_data(
        self, shipment_id: int, action: str = "update"
    ):
        """
        Sincroniza datos de envío específico
        """
        try:
            from envios.models import Envio

            shipment = Envio.objects.get(id=shipment_id)
            shipment_data = {
                "id": shipment.id,
                "codigo_seguimiento": shipment.codigo_seguimiento,
                "remitente": shipment.remitente,
                "destinatario": shipment.destinatario,
                "estado": shipment.estado,
                "origen": shipment.origen,
                "destino": shipment.destino,
                "peso": float(shipment.peso),
                "precio": float(shipment.precio),
                "fecha_creacion": shipment.fecha_creacion.isoformat(),
                "fecha_actualizacion": shipment.fecha_actualizacion.isoformat(),
            }

            event_type = (
                SyncEventType.SHIPMENT_CREATED
                if action == "create"
                else SyncEventType.SHIPMENT_UPDATED
            )

            await self.publish_event(
                event_type=event_type,
                data={"action": action, "shipment": shipment_data},
                priority=SyncPriority.HIGH,
            )

        except Exception as e:
            logger.error(f"Error sincronizando envío {shipment_id}: {e}")

    async def sync_user_data(self, user_id: int, action: str = "update"):
        """
        Sincroniza datos de usuario
        """
        try:
            from django.contrib.auth import get_user_model

            User = get_user_model()

            user = User.objects.get(id=user_id)
            user_data = {
                "id": user.id,
                "email": user.email,
                "nombre": getattr(user, "nombre", ""),
                "telefono": getattr(user, "telefono", ""),
                "is_active": user.is_active,
                "date_joined": user.date_joined.isoformat(),
                "last_login": (
                    user.last_login.isoformat() if user.last_login else None
                ),
            }

            event_type = (
                SyncEventType.USER_CREATED
                if action == "create"
                else SyncEventType.USER_UPDATED
            )

            await self.publish_event(
                event_type=event_type,
                data={"action": action, "user": user_data},
                priority=SyncPriority.NORMAL,
            )

        except Exception as e:
            logger.error(f"Error sincronizando usuario {user_id}: {e}")

    async def _process_sync_queue(self):
        """
        Procesa cola de eventos de sincronización
        """
        while self.running:
            try:
                # Obtener evento de la cola
                sync_event = await asyncio.wait_for(
                    self.sync_queue.get(), timeout=1.0
                )

                # Procesar según prioridad
                if sync_event.priority == SyncPriority.CRITICAL:
                    await self._process_event_immediately(sync_event)
                else:
                    # Procesar en background
                    asyncio.create_task(self._process_event(sync_event))

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error procesando cola de sincronización: {e}")
                await asyncio.sleep(1)

    async def _process_event(self, sync_event: SyncEvent):
        """
        Procesa evento individual de sincronización
        """
        try:
            # Aplicar delay según prioridad
            if sync_event.priority == SyncPriority.HIGH:
                await asyncio.sleep(0.1)
            elif sync_event.priority == SyncPriority.NORMAL:
                await asyncio.sleep(1)
            elif sync_event.priority == SyncPriority.LOW:
                await asyncio.sleep(5)

            # Enviar a regiones objetivo
            success_count = 0
            for target_region in sync_event.target_regions:
                try:
                    await self._send_to_region(sync_event, target_region)
                    success_count += 1
                except Exception as e:
                    logger.error(
                        f"Error enviando evento a {target_region}: {e}"
                    )

            # Marcar como procesado si al menos una región recibió el evento
            if success_count > 0:
                await self._mark_event_processed(sync_event.id)

                # Notificar a suscriptores locales
                await self._notify_subscribers(sync_event)
            else:
                # Reintentar si no se pudo enviar a ninguna región
                await self._retry_event(sync_event)

        except Exception as e:
            logger.error(f"Error procesando evento {sync_event.id}: {e}")
            await self._retry_event(sync_event)

    async def _process_event_immediately(self, sync_event: SyncEvent):
        """
        Procesa evento crítico inmediatamente
        """
        tasks = []
        for target_region in sync_event.target_regions:
            task = asyncio.create_task(
                self._send_to_region(sync_event, target_region)
            )
            tasks.append(task)

        # Esperar todas las tareas con timeout
        try:
            await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True), timeout=10.0
            )

            await self._mark_event_processed(sync_event.id)
            await self._notify_subscribers(sync_event)

        except asyncio.TimeoutError:
            logger.warning(
                f"Timeout procesando evento crítico {sync_event.id}"
            )
            await self._retry_event(sync_event)

    async def _send_to_region(self, sync_event: SyncEvent, target_region: str):
        """
        Envía evento a región específica
        """
        try:
            if not self.regions.get(target_region, {}).get("active", False):
                logger.warning(f"Región {target_region} no está activa")
                return

            # Publicar en Redis de la región objetivo
            channel = f"packfy:{target_region}:sync"
            message = json.dumps(asdict(sync_event))

            if self.redis_client:
                await self.redis_client.publish(channel, message)
                logger.debug(
                    f"Evento {sync_event.id} enviado a {target_region}"
                )

        except Exception as e:
            logger.error(f"Error enviando a región {target_region}: {e}")
            raise

    async def _listen_for_events(self):
        """
        Escucha eventos de sincronización entrantes
        """
        if not self.redis_client:
            return

        try:
            pubsub = self.redis_client.pubsub()
            await pubsub.subscribe("packfy:cuba:sync")

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        event_data = json.loads(message["data"])
                        sync_event = SyncEvent(**event_data)

                        # Verificar integridad
                        if (
                            sync_event.checksum
                            == sync_event._generate_checksum()
                        ):
                            await self._handle_incoming_event(sync_event)
                        else:
                            logger.warning(
                                f"Checksum inválido para evento {sync_event.id}"
                            )

                    except Exception as e:
                        logger.error(f"Error procesando evento entrante: {e}")

        except Exception as e:
            logger.error(f"Error escuchando eventos: {e}")

    async def _handle_incoming_event(self, sync_event: SyncEvent):
        """
        Maneja evento de sincronización entrante
        """
        try:
            # Verificar si ya fue procesado
            if await self._is_event_processed(sync_event.id):
                return

            # Aplicar datos según tipo de evento
            if sync_event.event_type == SyncEventType.SHIPMENT_CREATED:
                await self._apply_shipment_create(sync_event.data)
            elif sync_event.event_type == SyncEventType.SHIPMENT_UPDATED:
                await self._apply_shipment_update(sync_event.data)
            elif sync_event.event_type == SyncEventType.USER_CREATED:
                await self._apply_user_create(sync_event.data)
            elif sync_event.event_type == SyncEventType.USER_UPDATED:
                await self._apply_user_update(sync_event.data)

            # Marcar como procesado
            await self._mark_event_processed(sync_event.id)

            # Notificar a suscriptores
            await self._notify_subscribers(sync_event)

            logger.info(
                f"Evento entrante {sync_event.id} procesado exitosamente"
            )

        except Exception as e:
            logger.error(
                f"Error manejando evento entrante {sync_event.id}: {e}"
            )

    async def _apply_shipment_create(self, data: Dict[str, Any]):
        """Aplica creación de envío desde sincronización"""
        # Implementar lógica de creación/actualización de envío
        pass

    async def _apply_shipment_update(self, data: Dict[str, Any]):
        """Aplica actualización de envío desde sincronización"""
        # Implementar lógica de actualización de envío
        pass

    async def _apply_user_create(self, data: Dict[str, Any]):
        """Aplica creación de usuario desde sincronización"""
        # Implementar lógica de creación/actualización de usuario
        pass

    async def _apply_user_update(self, data: Dict[str, Any]):
        """Aplica actualización de usuario desde sincronización"""
        # Implementar lógica de actualización de usuario
        pass

    async def _notify_subscribers(self, sync_event: SyncEvent):
        """
        Notifica a suscriptores del evento
        """
        if sync_event.event_type in self.subscribers:
            for callback in self.subscribers[sync_event.event_type]:
                try:
                    # Ejecutar callback en executor para no bloquear
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(
                        self.executor, callback, sync_event.data
                    )
                except Exception as e:
                    logger.error(f"Error ejecutando callback: {e}")

    async def _store_event(self, sync_event: SyncEvent):
        """Almacena evento para auditoría"""
        if self.redis_client:
            key = f"sync_events:{sync_event.id}"
            await self.redis_client.setex(
                key, 86400 * 7, json.dumps(asdict(sync_event))  # 7 días
            )

    async def _mark_event_processed(self, event_id: str):
        """Marca evento como procesado"""
        if self.redis_client:
            key = f"processed_events:{event_id}"
            await self.redis_client.setex(key, 86400, "1")

    async def _is_event_processed(self, event_id: str) -> bool:
        """Verifica si evento ya fue procesado"""
        if self.redis_client:
            key = f"processed_events:{event_id}"
            return await self.redis_client.exists(key) > 0
        return False

    async def _retry_event(self, sync_event: SyncEvent):
        """
        Reintenta procesar evento fallido
        """
        if sync_event.retry_count < sync_event.max_retries:
            sync_event.retry_count += 1

            # Delay exponencial
            delay = 2**sync_event.retry_count
            await asyncio.sleep(delay)

            # Reagregar a cola
            await self.sync_queue.put(sync_event)

            logger.info(
                f"Reintentando evento {sync_event.id} (intento {sync_event.retry_count})"
            )
        else:
            logger.error(
                f"Evento {sync_event.id} falló después de {sync_event.max_retries} intentos"
            )

    async def get_sync_status(self) -> Dict[str, Any]:
        """
        Obtiene estado del servicio de sincronización
        """
        try:
            status = {
                "running": self.running,
                "queue_size": self.sync_queue.qsize(),
                "regions": self.regions,
                "subscribers": {
                    k.value: len(v) for k, v in self.subscribers.items()
                },
                "redis_connected": self.redis_client is not None,
                "last_check": datetime.utcnow().isoformat(),
            }

            # Estadísticas de eventos recientes
            if self.redis_client:
                recent_events = await self.redis_client.keys("sync_events:*")
                status["recent_events_count"] = len(recent_events)

            return status

        except Exception as e:
            logger.error(f"Error obteniendo estado de sincronización: {e}")
            return {"error": str(e)}

    async def close(self):
        """Cierra el servicio de sincronización"""
        self.running = False
        if self.redis_client:
            await self.redis_client.close()
        logger.info("Servicio de sincronización cerrado")


# Instancia global del servicio
global_sync_service = GlobalSyncService()
