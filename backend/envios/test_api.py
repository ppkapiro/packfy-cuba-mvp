from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from envios.models import Envio, HistorialEstado
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from empresas.models import Empresa

Usuario = get_user_model()

class APIPublicaTest(TestCase):
    def setUp(self):
        # Crear una empresa de prueba
        self.empresa = Empresa.objects.create(
            nombre='Empresa de Prueba',
            dominio='test.paqueteria.local',
            activo=True
        )
        self.empresa.save()
        
        # Configurar cliente API
        self.client = APIClient()
        
        # Crear un usuario de prueba
        self.usuario = Usuario.objects.create_user(
            email='test@example.com',
            password='password123',
            nombre='Usuario',
            apellidos='De Prueba'
        )
        
        # Crear un envío de prueba
        self.envio = Envio.objects.create(
            descripcion='Envío de prueba para API',
            peso=5.0,
            valor_declarado=100.0,
            remitente_nombre='Remitente Prueba',
            remitente_direccion='Dirección Remitente',
            remitente_telefono='+53 55123456',
            remitente_email='remitente@example.com',
            destinatario_nombre='Destinatario Prueba',
            destinatario_direccion='Dirección Destinatario',
            destinatario_telefono='+53 55654321',
            destinatario_email='destinatario@example.com',
            fecha_estimada_entrega=timezone.now() + timedelta(days=5),
            estado_actual=Envio.EstadoChoices.RECIBIDO,
            creado_por=self.usuario,
            actualizado_por=self.usuario
        )
        
        # Crear registros en el historial
        HistorialEstado.objects.create(
            envio=self.envio,
            estado=Envio.EstadoChoices.RECIBIDO,
            comentario='Creación del envío',
            ubicacion='La Habana',
            registrado_por=self.usuario
        )
        
        # Configurar cliente API
        self.api_client = APIClient()
    
    def test_rastreo_publico(self):
        """Probar que la API de rastreo público funciona correctamente"""
        # Hacer solicitud a la API pública
        response = self.client.get(f'/api/envios/rastrear/?numero_guia={self.envio.numero_guia}')
        
        # Verificar respuesta correcta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar datos básicos en la respuesta
        data = response.json()
        self.assertEqual(data['numero_guia'], self.envio.numero_guia)
        self.assertEqual(data['estado'], self.envio.estado_actual)
        self.assertEqual(data['remitente_nombre'], self.envio.remitente_nombre)
        self.assertEqual(data['destinatario_nombre'], self.envio.destinatario_nombre)
        
        # Verificar que incluye el historial
        self.assertTrue('historial' in data)
        self.assertEqual(len(data['historial']), 1)
        
        # Verificar que el historial tiene los datos correctos
        historial = data['historial'][0]
        self.assertEqual(historial['estado'], Envio.EstadoChoices.RECIBIDO)
        self.assertEqual(historial['comentario'], 'Creación del envío')
        self.assertEqual(historial['ubicacion'], 'La Habana')
    
    def test_rastreo_numero_guia_inexistente(self):
        """Probar que la API devuelve error cuando el número de guía no existe"""
        # Hacer solicitud con número de guía inexistente
        response = self.client.get('/api/envios/rastrear/?numero_guia=INEXISTENTE')
        
        # Verificar que devuelve error 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Verificar mensaje de error
        self.assertEqual(response.json()['error'], 'No se encontró ningún envío con ese número de guía')
    
    def test_rastreo_sin_numero_guia(self):
        """Probar que la API devuelve error cuando no se proporciona número de guía"""
        # Hacer solicitud sin número de guía
        response = self.client.get('/api/envios/rastrear/')
        
        # Verificar que devuelve error 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verificar mensaje de error
        self.assertEqual(response.json()['error'], 'Se requiere el parámetro numero_guia')
