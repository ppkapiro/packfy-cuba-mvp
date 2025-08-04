from django.core.management.base import BaseCommand
import random
from datetime import timedelta, datetime
from django.utils import timezone
from django_tenants.utils import tenant_context, get_tenant_model
from envios.models import Envio, HistorialEstado
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Genera datos de ejemplo para la aplicación'

    def handle(self, *args, **kwargs):
        # Obtener todos los tenants
        TenantModel = get_tenant_model()
        tenants = TenantModel.objects.all()
        
        for tenant in tenants:
            self.stdout.write(f"Generando datos para el tenant {tenant.schema_name}...")
            
            with tenant_context(tenant):
                # Verificar si hay usuarios
                if not Usuario.objects.exists():
                    self.stdout.write("No hay usuarios en este tenant. Saltando...")
                    continue
                
                # Obtener usuario administrador para registrar los envíos
                admin_user = Usuario.objects.filter(is_superuser=True).first()
                if not admin_user:
                    admin_user = Usuario.objects.first()
                
                # Generar envíos de ejemplo
                self.generar_envios(admin_user, 20)
                
                self.stdout.write(self.style.SUCCESS(f"Datos generados correctamente para {tenant.schema_name}"))
    
    def generar_envios(self, usuario, cantidad):
        # Datos de ejemplo
        remitentes = [
            {"nombre": "Juan Pérez", "direccion": "Calle 10 #123, La Habana", "telefono": "+53 55123456", "email": "juan@ejemplo.com"},
            {"nombre": "María González", "direccion": "Avenida 5ta #45, Varadero", "telefono": "+53 55789012", "email": "maria@ejemplo.com"},
            {"nombre": "Carlos Rodríguez", "direccion": "Calle 23 #890, La Habana", "telefono": "+53 55345678", "email": "carlos@ejemplo.com"},
            {"nombre": "Ana Martínez", "direccion": "Calle Central #56, Santa Clara", "telefono": "+53 55901234", "email": "ana@ejemplo.com"},
            {"nombre": "Roberto Fernández", "direccion": "Avenida Malecón #234, La Habana", "telefono": "+53 55567890", "email": "roberto@ejemplo.com"},
        ]
        
        destinatarios = [
            {"nombre": "Luis Sánchez", "direccion": "Calle 60 #789, Santiago de Cuba", "telefono": "+53 55234567", "email": "luis@ejemplo.com"},
            {"nombre": "Laura Díaz", "direccion": "Avenida Principal #12, Cienfuegos", "telefono": "+53 55890123", "email": "laura@ejemplo.com"},
            {"nombre": "Pedro Gómez", "direccion": "Calle 14 #456, Holguín", "telefono": "+53 55456789", "email": "pedro@ejemplo.com"},
            {"nombre": "Sofía Álvarez", "direccion": "Calle Real #78, Pinar del Río", "telefono": "+53 55012345", "email": "sofia@ejemplo.com"},
            {"nombre": "Eduardo Torres", "direccion": "Avenida Cuba #345, Matanzas", "telefono": "+53 55678901", "email": "eduardo@ejemplo.com"},
        ]
        
        descripciones = [
            "Caja con ropa y artículos personales",
            "Paquete con documentos importantes",
            "Equipos electrónicos (laptops, tablets)",
            "Medicamentos y material médico",
            "Libros y material educativo",
            "Repuestos de automóvil",
            "Artículos deportivos",
            "Instrumentos musicales",
            "Alimentos no perecederos",
            "Suministros de oficina"
        ]
        
        # Crear envíos
        envios_creados = 0
        for _ in range(cantidad):
            # Seleccionar datos aleatorios
            remitente = random.choice(remitentes)
            destinatario = random.choice(destinatarios)
            descripcion = random.choice(descripciones)
            
            # Generar valores aleatorios para pesos y dimensiones
            peso = round(random.uniform(0.5, 30.0), 2)
            valor_declarado = round(random.uniform(10.0, 1000.0), 2)
            
            # Fechas de entrega estimadas
            fecha_actual = timezone.now()
            fecha_estimada = fecha_actual + timedelta(days=random.randint(3, 15))
            
            # Crear el envío
            envio = Envio(
                descripcion=descripcion,
                peso=peso,
                valor_declarado=valor_declarado,
                
                remitente_nombre=remitente["nombre"],
                remitente_direccion=remitente["direccion"],
                remitente_telefono=remitente["telefono"],
                remitente_email=remitente["email"],
                
                destinatario_nombre=destinatario["nombre"],
                destinatario_direccion=destinatario["direccion"],
                destinatario_telefono=destinatario["telefono"],
                destinatario_email=destinatario["email"],
                
                fecha_estimada_entrega=fecha_estimada,
                creado_por=usuario,
                actualizado_por=usuario
            )
            
            # Decidir el estado actual basado en probabilidades
            estados = list(Envio.EstadoChoices)
            probabilidades = [0.2, 0.3, 0.2, 0.15, 0.1, 0.05]  # Más probabilidad para estados iniciales
            estado_actual = random.choices(estados, probabilidades)[0]
            envio.estado_actual = estado_actual
            
            # Guardar el envío
            envio.save()
            envios_creados += 1
            
            # Generar historial de estados
            self.generar_historial_estados(envio, usuario)
            
        self.stdout.write(f"Se han creado {envios_creados} envíos de ejemplo")
    
    def generar_historial_estados(self, envio, usuario):
        # Generar historial basado en el estado actual
        estados_posibles = ['RECIBIDO', 'EN_TRANSITO', 'EN_REPARTO', 'ENTREGADO', 'DEVUELTO', 'CANCELADO']
        indice_estado_actual = estados_posibles.index(envio.estado_actual)
        
        # Solo generar historial hasta el estado actual
        estados_historial = estados_posibles[:indice_estado_actual + 1]
        
        # Comentarios posibles para cada estado
        comentarios = {
            'RECIBIDO': [
                "Paquete recibido en oficina principal",
                "Envío registrado en sistema",
                "Paquete recibido del remitente"
            ],
            'EN_TRANSITO': [
                "Envío en tránsito hacia destino",
                "Salió del centro de distribución",
                "En ruta entre ciudades"
            ],
            'EN_REPARTO': [
                "Envío con repartidor local",
                "En proceso de entrega final",
                "Ruta de reparto local iniciada"
            ],
            'ENTREGADO': [
                "Entregado al destinatario",
                "Firmado por destinatario",
                "Entrega completada exitosamente"
            ],
            'DEVUELTO': [
                "Destinatario ausente, paquete devuelto",
                "Dirección incorrecta, retornando a origen",
                "No reclamado, se devuelve al remitente"
            ],
            'CANCELADO': [
                "Servicio cancelado por el cliente",
                "Cancelado por problemas de transporte",
                "Cancelado por disposiciones aduaneras"
            ]
        }
        
        # Ubicaciones posibles
        ubicaciones = [
            "La Habana", "Santiago de Cuba", "Santa Clara", 
            "Holguín", "Camagüey", "Guantánamo", "Matanzas"
        ]
        
        # Fecha base (fecha de creación del envío)
        fecha_base = envio.fecha_creacion
        
        # Generar un registro para cada estado hasta el actual
        for i, estado in enumerate(estados_historial):
            # Seleccionar comentario y ubicación aleatoria
            comentario = random.choice(comentarios[estado])
            ubicacion = random.choice(ubicaciones)
            
            # Incrementar la fecha para cada estado
            fecha = fecha_base + timedelta(hours=random.randint(1, 12) * i)
            
            # Crear el registro de historial
            HistorialEstado.objects.create(
                envio=envio,
                estado=estado,
                comentario=comentario,
                ubicacion=ubicacion,
                fecha=fecha,
                registrado_por=usuario
            )
