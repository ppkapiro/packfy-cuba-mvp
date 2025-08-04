from django.core.management.base import BaseCommand
from empresas.models import Empresa, Dominio
from django.db import connection
from django_tenants.utils import schema_exists, get_tenant_model, get_tenant_domain_model

class Command(BaseCommand):
    help = 'Inicializa el esquema público y crea un tenant predeterminado si no existe'

    def handle(self, *args, **kwargs):
        TenantModel = get_tenant_model()
        DomainModel = get_tenant_domain_model()
        
        # Verificar si ya existe el tenant público
        if not schema_exists('public'):
            self.stdout.write(self.style.WARNING('El esquema público no existe. Creando...'))
            
            # Crear el tenant público (empresa principal)
            empresa_publica = TenantModel(
                schema_name='public',
                nombre='Packfy Cuba',
                ruc='PACKFY001',
                direccion='Calle Principal #123, La Habana, Cuba',
                telefono='+53 12345678',
                email='info@packfy.com',
                activo=True
            )
            
            # Guardar el tenant
            empresa_publica.save()
            
            # Crear el dominio asociado
            dominio_publico = DomainModel(
                domain='localhost',
                tenant=empresa_publica,
                is_primary=True
            )
            dominio_publico.save()
            
            self.stdout.write(self.style.SUCCESS('Se ha creado el esquema público correctamente.'))
        else:
            self.stdout.write(self.style.SUCCESS('El esquema público ya existe. No se requiere inicialización.'))
            
        # Verificar si hay tenants adicionales
        tenants_count = TenantModel.objects.count()
        if tenants_count <= 1:
            # Crear tenant de ejemplo solo si no existe
            if not schema_exists('ejemplo'):
                self.stdout.write(self.style.WARNING('Solo existe el tenant público. Creando tenant de ejemplo...'))
                empresa_ejemplo = TenantModel(
                    schema_name='ejemplo',
                    nombre='Envíos Express',
                    ruc='EXPRESS001',
                    direccion='Avenida 5ta #456, Santiago de Cuba',
                    telefono='+53 87654321',
                    email='info@enviosexpress.cu',
                    activo=True
                )
                empresa_ejemplo.save()
                dominio_ejemplo = DomainModel(
                    domain='ejemplo.localhost',
                    tenant=empresa_ejemplo,
                    is_primary=True
                )
                dominio_ejemplo.save()
                self.stdout.write(self.style.SUCCESS('Se ha creado el tenant de ejemplo "Envíos Express"'))
            else:
                self.stdout.write(self.style.WARNING('El tenant de ejemplo ya existe. Omitiendo creación.'))
        self.stdout.write(self.style.SUCCESS(f'Hay un total de {tenants_count} tenants en el sistema.'))
