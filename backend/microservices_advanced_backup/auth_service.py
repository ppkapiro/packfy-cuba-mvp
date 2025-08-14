# 🇨🇺 PACKFY CUBA - Servicio de Autenticación Global v4.0
import hashlib
import json
import logging
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import jwt
import redis
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()
logger = logging.getLogger(__name__)


class GlobalAuthService:
    """
    Servicio de autenticación distribuido para PACKFY CUBA
    Maneja autenticación multi-región con sincronización global
    """

    def __init__(self):
        self.redis_client = self._get_redis_client()
        self.encryption_key = self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)

    def _get_redis_client(self):
        """Conexión a Redis para almacenamiento distribuido"""
        try:
            return redis.Redis(
                host=getattr(settings, "REDIS_HOST", "localhost"),
                port=getattr(settings, "REDIS_PORT", 6379),
                db=getattr(settings, "REDIS_AUTH_DB", 2),
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                health_check_interval=30,
            )
        except Exception as e:
            logger.error(f"Error conectando a Redis: {e}")
            return None

    def _get_encryption_key(self):
        """Obtiene o genera clave de cifrado"""
        try:
            key = getattr(settings, "GLOBAL_ENCRYPTION_KEY", None)
            if not key:
                key = Fernet.generate_key()
                logger.warning(
                    "Generando nueva clave de cifrado. Configurar GLOBAL_ENCRYPTION_KEY en producción."
                )
            return key if isinstance(key, bytes) else key.encode()
        except Exception:
            return Fernet.generate_key()

    def create_global_session(
        self, user_id: int, region: str = "cuba", additional_data: Dict = None
    ) -> Dict[str, Any]:
        """
        Crea una sesión global sincronizada entre regiones
        """
        try:
            session_id = secrets.token_urlsafe(32)
            session_data = {
                "user_id": user_id,
                "region": region,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (
                    datetime.utcnow() + timedelta(hours=24)
                ).isoformat(),
                "last_activity": datetime.utcnow().isoformat(),
                "active_regions": [region],
                "security_hash": self._generate_security_hash(
                    user_id, session_id
                ),
                "permissions": self._get_user_permissions(user_id),
                "additional_data": additional_data or {},
            }

            # Cifrar datos sensibles
            encrypted_data = self.cipher_suite.encrypt(
                json.dumps(session_data).encode()
            )

            # Almacenar en Redis con TTL
            if self.redis_client:
                pipeline = self.redis_client.pipeline()
                pipeline.setex(
                    f"global_session:{session_id}",
                    86400,  # 24 horas
                    encrypted_data.decode(),
                )
                pipeline.setex(f"user_sessions:{user_id}", 86400, session_id)
                pipeline.execute()

            # También en cache local como fallback
            cache.set(f"global_session:{session_id}", session_data, 86400)

            logger.info(
                f"Sesión global creada para usuario {user_id} en región {region}"
            )

            return {
                "session_id": session_id,
                "expires_at": session_data["expires_at"],
                "region": region,
                "permissions": session_data["permissions"],
            }

        except Exception as e:
            logger.error(f"Error creando sesión global: {e}")
            raise

    def validate_global_session(
        self, session_id: str, current_region: str = "cuba"
    ) -> Optional[Dict[str, Any]]:
        """
        Valida sesión global y actualiza actividad
        """
        try:
            # Intentar obtener de Redis primero
            session_data = None
            if self.redis_client:
                encrypted_data = self.redis_client.get(
                    f"global_session:{session_id}"
                )
                if encrypted_data:
                    decrypted_data = self.cipher_suite.decrypt(
                        encrypted_data.encode()
                    )
                    session_data = json.loads(decrypted_data.decode())

            # Fallback a cache local
            if not session_data:
                session_data = cache.get(f"global_session:{session_id}")

            if not session_data:
                return None

            # Verificar expiración
            expires_at = datetime.fromisoformat(session_data["expires_at"])
            if datetime.utcnow() > expires_at:
                self.invalidate_global_session(session_id)
                return None

            # Verificar hash de seguridad
            expected_hash = self._generate_security_hash(
                session_data["user_id"], session_id
            )
            if session_data.get("security_hash") != expected_hash:
                logger.warning(
                    f"Hash de seguridad inválido para sesión {session_id}"
                )
                self.invalidate_global_session(session_id)
                return None

            # Actualizar actividad y región
            session_data["last_activity"] = datetime.utcnow().isoformat()
            if current_region not in session_data["active_regions"]:
                session_data["active_regions"].append(current_region)

            # Guardar actualización
            self._update_session_data(session_id, session_data)

            return session_data

        except Exception as e:
            logger.error(f"Error validando sesión global: {e}")
            return None

    def invalidate_global_session(self, session_id: str):
        """
        Invalida sesión en todas las regiones
        """
        try:
            if self.redis_client:
                pipeline = self.redis_client.pipeline()

                # Obtener datos de sesión para limpiar referencias
                encrypted_data = self.redis_client.get(
                    f"global_session:{session_id}"
                )
                if encrypted_data:
                    decrypted_data = self.cipher_suite.decrypt(
                        encrypted_data.encode()
                    )
                    session_data = json.loads(decrypted_data.decode())
                    user_id = session_data.get("user_id")

                    if user_id:
                        pipeline.delete(f"user_sessions:{user_id}")

                pipeline.delete(f"global_session:{session_id}")
                pipeline.execute()

            # También del cache local
            cache.delete(f"global_session:{session_id}")

            logger.info(f"Sesión global {session_id} invalidada")

        except Exception as e:
            logger.error(f"Error invalidando sesión global: {e}")

    def get_user_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene todas las sesiones activas de un usuario
        """
        try:
            sessions = []

            if self.redis_client:
                # Buscar sesiones por patrón
                session_keys = self.redis_client.keys(f"global_session:*")

                for key in session_keys:
                    try:
                        encrypted_data = self.redis_client.get(key)
                        if encrypted_data:
                            decrypted_data = self.cipher_suite.decrypt(
                                encrypted_data.encode()
                            )
                            session_data = json.loads(decrypted_data.decode())

                            if session_data.get("user_id") == user_id:
                                # Verificar que no haya expirado
                                expires_at = datetime.fromisoformat(
                                    session_data["expires_at"]
                                )
                                if datetime.utcnow() <= expires_at:
                                    sessions.append(
                                        {
                                            "session_id": key.split(":")[1],
                                            "region": session_data.get(
                                                "region"
                                            ),
                                            "created_at": session_data.get(
                                                "created_at"
                                            ),
                                            "last_activity": session_data.get(
                                                "last_activity"
                                            ),
                                            "active_regions": session_data.get(
                                                "active_regions", []
                                            ),
                                        }
                                    )
                    except Exception as e:
                        logger.warning(f"Error procesando sesión {key}: {e}")

            return sessions

        except Exception as e:
            logger.error(
                f"Error obteniendo sesiones de usuario {user_id}: {e}"
            )
            return []

    def sync_session_across_regions(
        self, session_id: str, target_regions: List[str]
    ) -> bool:
        """
        Sincroniza sesión a través de múltiples regiones
        """
        try:
            session_data = self.validate_global_session(session_id)
            if not session_data:
                return False

            # Marcar regiones como activas
            for region in target_regions:
                if region not in session_data["active_regions"]:
                    session_data["active_regions"].append(region)

            # Actualizar timestamp de sincronización
            session_data["last_sync"] = datetime.utcnow().isoformat()
            session_data["synced_regions"] = target_regions

            # Guardar actualización
            self._update_session_data(session_id, session_data)

            logger.info(
                f"Sesión {session_id} sincronizada a regiones: {target_regions}"
            )
            return True

        except Exception as e:
            logger.error(f"Error sincronizando sesión: {e}")
            return False

    def _generate_security_hash(self, user_id: int, session_id: str) -> str:
        """
        Genera hash de seguridad para validación de sesión
        """
        secret_key = getattr(settings, "SECRET_KEY", "default-secret")
        data = f"{user_id}:{session_id}:{secret_key}"
        return hashlib.sha256(data.encode()).hexdigest()

    def _get_user_permissions(self, user_id: int) -> List[str]:
        """
        Obtiene permisos del usuario para almacenar en sesión
        """
        try:
            user = User.objects.get(id=user_id)
            permissions = []

            # Permisos básicos
            if user.is_superuser:
                permissions.append("admin")
            if user.is_staff:
                permissions.append("staff")

            # Permisos específicos de grupos
            for group in user.groups.all():
                permissions.append(f"group:{group.name}")

            # Permisos específicos del usuario
            for perm in user.user_permissions.all():
                permissions.append(f"perm:{perm.codename}")

            return permissions

        except Exception as e:
            logger.error(
                f"Error obteniendo permisos de usuario {user_id}: {e}"
            )
            return []

    def _update_session_data(
        self, session_id: str, session_data: Dict[str, Any]
    ):
        """
        Actualiza datos de sesión en almacenamiento distribuido
        """
        try:
            # Cifrar datos actualizados
            encrypted_data = self.cipher_suite.encrypt(
                json.dumps(session_data).encode()
            )

            # Actualizar en Redis
            if self.redis_client:
                self.redis_client.setex(
                    f"global_session:{session_id}",
                    86400,  # 24 horas
                    encrypted_data.decode(),
                )

            # Actualizar cache local
            cache.set(f"global_session:{session_id}", session_data, 86400)

        except Exception as e:
            logger.error(f"Error actualizando sesión {session_id}: {e}")

    def get_session_analytics(self, region: str = None) -> Dict[str, Any]:
        """
        Obtiene analytics de sesiones globales
        """
        try:
            analytics = {
                "total_sessions": 0,
                "active_users": 0,
                "regions": {},
                "recent_activity": [],
            }

            if not self.redis_client:
                return analytics

            session_keys = self.redis_client.keys(f"global_session:*")
            active_users = set()

            for key in session_keys:
                try:
                    encrypted_data = self.redis_client.get(key)
                    if encrypted_data:
                        decrypted_data = self.cipher_suite.decrypt(
                            encrypted_data.encode()
                        )
                        session_data = json.loads(decrypted_data.decode())

                        # Verificar que no haya expirado
                        expires_at = datetime.fromisoformat(
                            session_data["expires_at"]
                        )
                        if datetime.utcnow() <= expires_at:
                            analytics["total_sessions"] += 1
                            active_users.add(session_data["user_id"])

                            # Analytics por región
                            session_region = session_data.get(
                                "region", "unknown"
                            )
                            if session_region not in analytics["regions"]:
                                analytics["regions"][session_region] = 0
                            analytics["regions"][session_region] += 1

                            # Actividad reciente
                            last_activity = datetime.fromisoformat(
                                session_data.get(
                                    "last_activity", session_data["created_at"]
                                )
                            )
                            if datetime.utcnow() - last_activity < timedelta(
                                minutes=30
                            ):
                                analytics["recent_activity"].append(
                                    {
                                        "user_id": session_data["user_id"],
                                        "region": session_region,
                                        "activity": session_data.get(
                                            "last_activity"
                                        ),
                                    }
                                )

                except Exception as e:
                    logger.warning(
                        f"Error procesando analytics para {key}: {e}"
                    )

            analytics["active_users"] = len(active_users)

            return analytics

        except Exception as e:
            logger.error(f"Error obteniendo analytics de sesiones: {e}")
            return {
                "total_sessions": 0,
                "active_users": 0,
                "regions": {},
                "recent_activity": [],
            }


# Instancia global del servicio
global_auth_service = GlobalAuthService()
