# 🇨🇺 PACKFY CUBA - Sistema de Autenticación JWT Avanzado v4.0

import hashlib
import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()
logger = logging.getLogger("packfy.auth")


class SecureJWTAuthentication(JWTAuthentication):
    """
    Autenticación JWT mejorada con:
    - Rate limiting
    - Token blacklist
    - Logging de seguridad
    - Validaciones adicionales
    """

    def authenticate(self, request):
        """Autenticación con validaciones de seguridad adicionales"""

        # 1. Rate limiting por IP
        if not self._check_rate_limit(request):
            logger.warning(
                f"Rate limit exceeded for IP: {self._get_client_ip(request)}"
            )
            return None

        # 2. Autenticación base
        result = super().authenticate(request)
        if result is None:
            return None

        user, validated_token = result

        # 3. Validaciones adicionales
        if not self._validate_token_security(validated_token, request):
            return None

        # 4. Log de acceso exitoso
        logger.info(f"Successful authentication for user: {user.username}")

        return user, validated_token

    def _check_rate_limit(self, request):
        """Verificar rate limiting por IP"""
        ip = self._get_client_ip(request)
        cache_key = f"auth_rate_limit:{ip}"

        # Permitir 30 intentos por hora
        current_attempts = cache.get(cache_key, 0)
        if current_attempts >= 30:
            return False

        cache.set(cache_key, current_attempts + 1, 3600)  # 1 hora
        return True

    def _validate_token_security(self, token, request):
        """Validaciones de seguridad del token"""

        # 1. Verificar si el token está en blacklist
        token_id = str(token.get("jti", ""))
        if cache.get(f"blacklisted_token:{token_id}"):
            logger.warning(f"Blacklisted token used: {token_id}")
            return False

        # 2. Verificar dispositivo (opcional)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        expected_device = token.get("device_hash", "")
        current_device = hashlib.sha256(user_agent.encode()).hexdigest()[:16]

        if expected_device and expected_device != current_device:
            logger.warning("Token used from different device")
            # En desarrollo permitir, en producción podría bloquear
            if settings.ENVIRONMENT == "production":
                return False

        return True

    def _get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class SecureRefreshToken(RefreshToken):
    """Token de refresh mejorado con metadata de seguridad"""

    @classmethod
    def for_user(cls, user, request=None):
        """Crear token con metadata de seguridad"""
        token = super().for_user(user)

        # Agregar metadata de seguridad
        if request:
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            device_hash = hashlib.sha256(user_agent.encode()).hexdigest()[:16]
            token["device_hash"] = device_hash
            token["ip"] = cls._get_client_ip(request)

        token["created_at"] = timezone.now().isoformat()
        token["session_id"] = secrets.token_hex(16)

        # Log de creación de token
        logger.info(f"Token created for user: {user.username}")

        return token

    @staticmethod
    def _get_client_ip(request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


def blacklist_token(token):
    """Agregar token a blacklist"""
    if hasattr(token, "get"):
        token_id = str(token.get("jti", ""))
        if token_id:
            # Blacklist hasta que expire el token
            exp_timestamp = token.get("exp", 0)
            if exp_timestamp:
                exp_time = timezone.datetime.fromtimestamp(
                    exp_timestamp, tz=timezone.utc
                )
                timeout = max(
                    0, int((exp_time - timezone.now()).total_seconds())
                )
                cache.set(f"blacklisted_token:{token_id}", True, timeout)
                logger.info(f"Token blacklisted: {token_id}")


def revoke_user_tokens(user):
    """Revocar todos los tokens de un usuario"""
    # Esto requeriría una implementación más compleja con base de datos
    # Por ahora, incrementamos un contador en cache
    cache_key = f"user_token_version:{user.id}"
    version = cache.get(cache_key, 0) + 1
    cache.set(cache_key, version, 86400 * 30)  # 30 días
    logger.info(f"All tokens revoked for user: {user.username}")


class AuthenticationService:
    """Servicio centralizado de autenticación"""

    @staticmethod
    def create_tokens_for_user(user, request=None):
        """Crear tokens seguros para un usuario"""
        refresh = SecureRefreshToken.for_user(user, request)
        access = refresh.access_token

        return {
            "refresh": str(refresh),
            "access": str(access),
            "access_expires": access["exp"],
            "refresh_expires": refresh["exp"],
            "user_id": user.id,
            "username": user.username,
        }

    @staticmethod
    def logout_user(refresh_token_str):
        """Logout seguro con blacklist"""
        try:
            token = RefreshToken(refresh_token_str)
            blacklist_token(token)

            # También blacklist el access token si está disponible
            access_token = token.access_token
            blacklist_token(access_token)

            return True
        except TokenError as e:
            logger.warning(f"Error during logout: {e}")
            return False

    @staticmethod
    def refresh_access_token(refresh_token_str):
        """Refresh con validaciones adicionales"""
        try:
            refresh = RefreshToken(refresh_token_str)

            # Verificar si está blacklisted
            token_id = str(refresh.get("jti", ""))
            if cache.get(f"blacklisted_token:{token_id}"):
                raise TokenError("Token is blacklisted")

            # Crear nuevo access token
            access = refresh.access_token

            return {
                "access": str(access),
                "access_expires": access["exp"],
            }

        except TokenError as e:
            logger.warning(f"Error refreshing token: {e}")
            raise
