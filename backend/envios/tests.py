from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from envios.models import Envio, HistorialEstado
from envios.notifications import enviar_notificacion_estado
from django.utils import timezone
from datetime import timedelta

Usuario = get_user_model()

class NotificacionesTest(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.usuario = Usuario.objects.create_user(
            email='test@example.com',
            password='password123',
            nombre='Usuario',
            apellidos='De Prueba'
        )
        
        # Crear un envío de prueba
        self.envio = Envio.objects.create(
            descripcion='Envío de prueba para notificaciones',
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
        
        # Crear un registro en el historial
        HistorialEstado.objects.create(
            envio=self.envio,
            estado=self.envio.estado_actual,
            comentario='Creación del envío',
            registrado_por=self.usuario
        )
    
    def test_enviar_notificacion_cambio_estado(self):
        """Probar que se envían notificaciones cuando cambia el estado"""
        # Limpiar bandeja de salida
        mail.outbox = []
        
        # Cambiar estado y enviar notificación
        estado_anterior = self.envio.estado_actual
        self.envio.estado_actual = Envio.EstadoChoices.EN_TRANSITO
        self.envio.save()
        
        # Enviar notificación
        resultado = enviar_notificacion_estado(self.envio, estado_anterior)
        
        # Verificar que la notificación se envió correctamente
        self.assertTrue(resultado)
        self.assertEqual(len(mail.outbox), 2)  # 1 para remitente y 1 para destinatario
        
        # Verificar contenido del email
        email = mail.outbox[0]
        self.assertIn(self.envio.numero_guia, email.subject)
        self.assertIn('En tránsito', email.subject)
        
        # Verificar destinatarios
        destinatarios = [email.to[0] for email in mail.outbox]
        self.assertIn('remitente@example.com', destinatarios)
        self.assertIn('destinatario@example.com', destinatarios)
    
    def test_no_enviar_con_emails_invalidos(self):
        """Probar que no se envían notificaciones si los emails son inválidos"""
        # Limpiar bandeja de salida
        mail.outbox = []
        
        # Invalidar los correos
        self.envio.remitente_email = 'email-invalido'
        self.envio.destinatario_email = None
        self.envio.save()
        
        # Intentar enviar notificación
        resultado = enviar_notificacion_estado(self.envio)
        
        # Verificar que no se envió ninguna notificación
        self.assertFalse(resultado)
        self.assertEqual(len(mail.outbox), 0)
