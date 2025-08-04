from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Crea un superusuario por defecto'

    def handle(self, *args, **kwargs):
        # Verificar si ya existe un superusuario
        if Usuario.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Ya existe un superusuario en el sistema.'))
            return
            
        # Crear el superusuario
        admin_user = Usuario.objects.create_superuser(
            username='admin',
            email='admin@packfy.com',
            password='admin123',
            first_name='Administrador',
            last_name='Packfy',
            telefono='+53 12345678',
            es_administrador_empresa=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {admin_user.email}'))
