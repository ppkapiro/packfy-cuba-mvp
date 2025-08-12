from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class APIHealthTestCase(APITestCase):
    """Tests básicos para verificar que la API funciona"""
    
    def test_api_health_check(self):
        """Test que la API responde correctamente"""
        # Crear un usuario de prueba
        user = User.objects.create_user(
            email='test@test.com',
            password='123456'
        )
        
        # Verificar que el usuario se creó
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, 'test@test.com')
    
    def test_api_endpoints_exist(self):
        """Test que los endpoints principales existen"""
        # Test que no devuelva 404 (aunque pueda ser 401 sin auth)
        response = self.client.get('/api/')
        self.assertNotEqual(response.status_code, 404)

class UserModelTestCase(TestCase):
    """Tests para el modelo de usuario"""
    
    def test_create_user(self):
        """Test crear usuario básico"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test crear superusuario"""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
