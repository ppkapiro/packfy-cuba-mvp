# 🇨🇺 PACKFY CUBA - Tests de API de Envíos v4.0

from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from empresas.models import Empresa
from envios.models import Envio, HistorialEstado
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.django_db
class TestEnvioAPI(APITestCase):
    """Tests para la API de envíos"""

    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear empresa de prueba
        self.empresa = Empresa.objects.create(
            nombre="Empresa Test", codigo="TEST001", activa=True
        )

        # Crear usuarios de prueba
        self.admin_user = User.objects.create_user(
            username="admin_test",
            email="admin@test.com",
            password="test_password_123",
            empresa=self.empresa,
            es_administrador_empresa=True,
        )

        self.regular_user = User.objects.create_user(
            username="user_test",
            email="user@test.com",
            password="test_password_123",
            empresa=self.empresa,
            es_administrador_empresa=False,
        )

        # Crear envío de prueba
        self.envio = Envio.objects.create(
            numero_guia="TEST123456",
            estado_actual="PENDIENTE",
            remitente_nombre="Juan Pérez",
            remitente_telefono="53123456789",
            destinatario_nombre="María García",
            destinatario_direccion="Calle 23 #456",
            descripcion="Paquete de prueba",
            peso=2.5,
            usuario=self.regular_user,
            empresa=self.empresa,
        )

        self.client = APIClient()

    def _get_tokens_for_user(self, user):
        """Obtener tokens JWT para un usuario"""
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def _authenticate_user(self, user):
        """Autenticar usuario en el cliente"""
        tokens = self._get_tokens_for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}'
        )
        return tokens

    @pytest.mark.unit
    def test_list_envios_authenticated(self):
        """Test: Listar envíos como usuario autenticado"""
        self._authenticate_user(self.regular_user)

        url = reverse("envio-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["numero_guia"], "TEST123456"
        )

    @pytest.mark.unit
    def test_list_envios_unauthenticated(self):
        """Test: Listar envíos sin autenticación debe fallar"""
        url = reverse("envio-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.unit
    def test_create_envio_valid_data(self):
        """Test: Crear envío con datos válidos"""
        self._authenticate_user(self.regular_user)

        data = {
            "numero_guia": "NEW123456",
            "estado_actual": "PENDIENTE",
            "remitente_nombre": "Ana López",
            "remitente_telefono": "53987654321",
            "destinatario_nombre": "Carlos Ruiz",
            "destinatario_direccion": "Avenida 26 #789",
            "descripcion": "Nuevo paquete",
            "peso": 1.5,
        }

        url = reverse("envio-list")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["numero_guia"], "NEW123456")
        self.assertEqual(response.data["usuario"], self.regular_user.id)

        # Verificar que se creó en la base de datos
        self.assertTrue(Envio.objects.filter(numero_guia="NEW123456").exists())

    @pytest.mark.security
    def test_user_cannot_access_other_company_envios(self):
        """Test: Usuario no puede acceder a envíos de otra empresa"""
        # Crear otra empresa y usuario
        empresa2 = Empresa.objects.create(nombre="Empresa 2", codigo="EMP2")
        user2 = User.objects.create_user(
            username="user2", password="pass", empresa=empresa2
        )

        self._authenticate_user(user2)

        # Intentar acceder al envío de la empresa 1
        url = reverse("envio-detail", kwargs={"pk": self.envio.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
