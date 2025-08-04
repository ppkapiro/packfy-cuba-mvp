from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, get_tenant_domain_model

class Command(BaseCommand):
    help = 'Lista todos los tenants en el sistema'

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()
        DomainModel = get_tenant_domain_model()
        
        tenants = TenantModel.objects.all()
        
        self.stdout.write(self.style.SUCCESS(f"Hay {tenants.count()} tenants en el sistema:"))
        
        for tenant in tenants:
            domains = DomainModel.objects.filter(tenant=tenant)
            domains_str = ", ".join([domain.domain for domain in domains])
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"- {tenant.nombre} (schema: {tenant.schema_name}, dominios: {domains_str})"
                )
            )
