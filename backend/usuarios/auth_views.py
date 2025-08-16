# 🇨🇺 PACKFY CUBA - Views de Autenticación Seguras v4.0

import hashlib
import json
import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone
from rest_framework import exceptions as drf_exceptions
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    throttle_classes,
)
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .auth_security import AuthenticationService, SecureRefreshToken
from .models import Usuario
from .serializers import UsuarioSerializer

logger = logging.getLogger("packfy.auth")


class SecureLoginThrottle(AnonRateThrottle):
    """Rate limiting específico para login"""

    scope = "login"
    rate = "5/min"  # 5 intentos por minuto


class SecureTokenObtainPairView(TokenObtainPairView):
    """
    Vista de login mejorada con:
    - Rate limiting
    - Logging de seguridad
    - Validaciones adicionales
    - Metadata de dispositivo
    """

    throttle_classes = [SecureLoginThrottle]

    def post(self, request, *args, **kwargs):
        """Login con validaciones de seguridad"""

        # Log del intento de login
        ip = self._get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        # ✅ ARREGLO: Aceptar tanto email como username
        email = request.data.get("email") or request.data.get(
            "username", "unknown"
        )
        password = request.data.get("password")

        # Copiar data para no mutar request.data
        try:
            payload = request.data.copy()
        except Exception:
            payload = dict(request.data or {})
        if payload.get("username") and not payload.get("email"):
            payload["email"] = payload["username"]

        logger.info(f"Login attempt for email: {email} from IP: {ip}")

        # Verificar si la IP está bloqueada
        if self._is_ip_blocked(ip):
            logger.warning(f"Login attempt from blocked IP: {ip}")
            return Response(
                {
                    "error": "Access denied",
                    "detail": "Your IP has been temporarily blocked due to suspicious activity",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Validación de campos requeridos
        if not email or not password:
            self._log_failed_attempt(ip, email, "missing_credentials")
            return Response(
                {
                    "error": "Invalid credentials",
                    "detail": "Email/username and password are required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Autenticación usando el serializer directamente (sin mutar request)
            serializer = self.get_serializer(data=payload)
            serializer.is_valid(raise_exception=True)
            data = dict(serializer.validated_data)

            # Login exitoso - buscar usuario por email ya que es el USERNAME_FIELD
            try:
                user = Usuario.objects.get(email=payload.get("email", ""))
            except Usuario.DoesNotExist:
                user = None
            if user:
                self._log_successful_login(user, ip, user_agent)
                # Crear tokens seguros (opcional, mantenemos los del serializer)
                # AuthenticationService.create_tokens_for_user(user, request)
                extra = {
                    "user": UsuarioSerializer(user).data,
                    "login_time": timezone.now().isoformat(),
                    "device_registered": True,
                }
            else:
                extra = {
                    "login_time": timezone.now().isoformat(),
                    "device_registered": True,
                }

            # Limpiar intentos fallidos
            self._clear_failed_attempts(ip)

            data.update(extra)
            return Response(data, status=status.HTTP_200_OK)

        except (InvalidToken, TokenError) as e:
            # Credenciales inválidas o token error → 401
            logger.warning(f"Login failed for {email} from IP {ip}: {str(e)}")
            self._log_failed_attempt(ip, email, "invalid_credentials")
            self._track_failed_attempt(ip)
            return Response(
                {
                    "error": "Invalid credentials",
                    "detail": "Email/username or password incorrect",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except drf_exceptions.ValidationError as e:
            # Errores de validación (credenciales inválidas) → 401/400
            self._log_failed_attempt(ip, email, "invalid_credentials")
            self._track_failed_attempt(ip)
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            # Si viene de validación de serializer (p.ej., 400 Bad Request), respóndalo adecuadamente
            msg = str(e)
            if (
                "No active account found" in msg
                or "no tiene una cuenta activa" in msg.lower()
            ):
                self._log_failed_attempt(ip, email, "invalid_credentials")
                self._track_failed_attempt(ip)
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            logger.error(f"Login error for {email}: {str(e)}")
            self._log_failed_attempt(ip, email, "system_error")
            return Response(
                {
                    "error": "Authentication failed",
                    "detail": "Please try again later",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return ip

    def _is_ip_blocked(self, ip):
        """Verificar si una IP está bloqueada"""
        failed_attempts = cache.get(f"failed_login_attempts:{ip}", 0)
        return failed_attempts >= 10  # Bloquear después de 10 intentos

    def _track_failed_attempt(self, ip):
        """Registrar intento fallido"""
        cache_key = f"failed_login_attempts:{ip}"
        attempts = cache.get(cache_key, 0) + 1
        cache.set(cache_key, attempts, 3600)  # 1 hora

        if attempts >= 10:
            logger.warning(f"IP blocked due to multiple failed attempts: {ip}")

    def _clear_failed_attempts(self, ip):
        """Limpiar intentos fallidos después de login exitoso"""
        cache.delete(f"failed_login_attempts:{ip}")

    def _log_successful_login(self, user, ip, user_agent):
        """Log de login exitoso"""
        log_data = {
            "event": "successful_login",
            "user_id": user.id,
            "username": user.username,
            "ip": ip,
            "user_agent": user_agent[:200],
            "timestamp": timezone.now().isoformat(),
        }
        logger.info(f"Successful login: {json.dumps(log_data)}")

    def _log_failed_attempt(self, ip, username, reason):
        """Log de intento fallido"""
        log_data = {
            "event": "failed_login",
            "username": username,
            "ip": ip,
            "reason": reason,
            "timestamp": timezone.now().isoformat(),
        }
        logger.warning(f"Failed login: {json.dumps(log_data)}")


class SecureTokenRefreshView(TokenRefreshView):
    """Vista de refresh de token mejorada"""

    def post(self, request, *args, **kwargs):
        """Refresh token con validaciones adicionales"""

        ip = self._get_client_ip(request)

        try:
            # Refresh normal
            response = super().post(request, *args, **kwargs)

            if response.status_code == 200:
                logger.info(f"Token refreshed successfully from IP: {ip}")

            return response

        except TokenError as e:
            logger.warning(
                f"Token refresh failed from IP: {ip}, reason: {str(e)}"
            )
            return Response(
                {
                    "error": "Token refresh failed",
                    "detail": "Please login again",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def _get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return ip


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@throttle_classes([UserRateThrottle])
def secure_logout(request):
    """
    Logout seguro con blacklist de tokens
    """
    try:
        # Obtener refresh token del request
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {
                    "error": "Refresh token required",
                    "detail": "Refresh token must be provided for secure logout",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Logout usando el servicio de autenticación
        success = AuthenticationService.logout_user(refresh_token)

        if success:
            logger.info(
                f"User {request.user.username} logged out successfully"
            )
            return Response(
                {
                    "message": "Logout successful",
                    "detail": "All tokens have been revoked",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": "Logout failed",
                    "detail": "Invalid or expired token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        logger.error(
            f"Logout error for user {request.user.username}: {str(e)}"
        )
        return Response(
            {"error": "Logout failed", "detail": "Please try again"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Obtener perfil del usuario autenticado con información de sesión
    """
    try:
        user = request.user
        serializer = UsuarioSerializer(user)

        # Información adicional de la sesión
        session_info = {
            "last_login": (
                user.last_login.isoformat() if user.last_login else None
            ),
            "is_staff": user.is_staff,
            "date_joined": user.date_joined.isoformat(),
            "current_ip": request.META.get("REMOTE_ADDR", "0.0.0.0"),
        }

        return Response(
            {
                "user": serializer.data,
                "session": session_info,
                "permissions": {
                    "is_admin": getattr(
                        user, "es_administrador_empresa", False
                    ),
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                },
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        return Response(
            {
                "error": "Profile retrieval failed",
                "detail": "Please try again",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """
    Cambio de contraseña seguro
    """
    try:
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        # Validaciones
        if not old_password or not new_password:
            return Response(
                {
                    "error": "Missing passwords",
                    "detail": "Both old and new passwords are required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verificar contraseña actual
        if not user.check_password(old_password):
            logger.warning(
                f"Failed password change attempt for user: {user.username}"
            )
            return Response(
                {
                    "error": "Invalid password",
                    "detail": "Current password is incorrect",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar nueva contraseña
        if len(new_password) < 8:
            return Response(
                {
                    "error": "Weak password",
                    "detail": "Password must be at least 8 characters long",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Cambiar contraseña
        user.set_password(new_password)
        user.save()

        logger.info(f"Password changed successfully for user: {user.username}")

        return Response(
            {
                "message": "Password changed successfully",
                "detail": "Please login again with your new password",
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        return Response(
            {"error": "Password change failed", "detail": "Please try again"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
