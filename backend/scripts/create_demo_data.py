import os
import sys
import django
import random
from datetime import datetime, timedelta

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from empresas.models import Empresa
from envios.models import Envio, HistorialEstado

Usuario = get_user_model()

def create_demo_data():
    """
    Crea datos de demostración para el sistema:
    - Empresas
    - Usuarios con distintos roles
    - Envíos con diferentes estados
    """
    print("Creando datos de demostración...")
    
    # Crear empresa principal si no existe
    empresa, created = Empresa.objects.get_or_create(
        nombre="Packfy Demo",
        defaults={
            'dominio': 'demo.packfy.com',
            'direccion': 'Calle 23 #512, La Habana, Cuba',
            'telefono': '+53 555-1234',
            'email': 'info@packfy.com',
            'activo': True,
            'ruc': '12345678901'
        }
    )
    
    if created:
        print(f"✅ Empresa creada: {empresa.nombre}")
    else:
        print(f"ℹ️ Empresa ya existente: {empresa.nombre}")
    
    # Crear usuarios de prueba con credenciales CORRECTAS para Packfy Cuba
    usuarios = {
        'admin': {
            'email': 'admin@packfy.cu',
            'password': 'admin123',
            'is_staff': True,
            'is_superuser': True,
            'first_name': 'Admin',
            'last_name': 'Packfy',
            'es_administrador_empresa': True
        },
        'empresa': {
            'email': 'empresa@test.cu',
            'password': 'empresa123',
            'first_name': 'Empresa',
            'last_name': 'Test',
            'es_administrador_empresa': True,
            'is_staff': False
        },
        'cliente': {
            'email': 'cliente@test.cu',
            'password': 'cliente123',
            'first_name': 'Cliente',
            'last_name': 'Test',
            'es_administrador_empresa': False,
            'is_staff': False
        }
    }
    
    # Crear o actualizar usuarios
    created_users = []
    for role, user_data in usuarios.items():
        user, created = Usuario.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'username': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'is_staff': user_data.get('is_staff', False),
                'is_superuser': user_data.get('is_superuser', False),
                'es_administrador_empresa': user_data['es_administrador_empresa']
            }
        )
        
        # Establecer la contraseña
        user.set_password(user_data['password'])
        user.save()
        
        created_users.append(user)
        status = "✅ Creado" if created else "ℹ️ Actualizado"
        print(f"{status}: Usuario {user.email} ({role})")
    
    # Crear envíos de prueba con diferentes estados
    admin_user = Usuario.objects.get(email='admin@packfy.com')
    operador_user = Usuario.objects.get(email='operador@packfy.com')
    
    # Datos para generar envíos aleatorios
    nombres_remitentes = ["Juan Pérez", "María Rodríguez", "Carlos Gómez", "Ana Martínez", "Luis Hernández"]
    nombres_destinatarios = ["Pedro Sánchez", "Laura González", "Miguel Torres", "Sofía Ramírez", "José Díaz"]
    direcciones = ["Calle 13 #456, Vedado, La Habana", "Ave 5ta #789, Miramar, La Habana", 
                  "Calle 42 #123, Playa, La Habana", "Paseo #567, Centro Habana", "Ave. 31 #890, Nuevo Vedado"]
    telefonos = ["+53 555-1234", "+53 555-5678", "+53 555-9012", "+53 555-3456", "+53 555-7890"]
    correos = ["cliente1@ejemplo.com", "cliente2@ejemplo.com", "cliente3@ejemplo.com", 
              "cliente4@ejemplo.com", "cliente5@ejemplo.com"]
    descripciones = ["Documentos importantes", "Ropa y accesorios", "Artículos electrónicos", 
                     "Medicamentos", "Artículos de regalo", "Libros y revistas"]
    
    # Crear 20 envíos con diferentes estados
    estados_envio = list(Envio.EstadoChoices.choices)
    for i in range(1, 21):
        # Seleccionar datos aleatorios
        remitente = random.choice(nombres_remitentes)
        destinatario = random.choice(nombres_destinatarios)
        while destinatario == remitente:  # Evitar que remitente y destinatario sean iguales
            destinatario = random.choice(nombres_destinatarios)
        
        # Definir fechas
        dias_atras = random.randint(1, 30)
        fecha_creacion = datetime.now() - timedelta(days=dias_atras)
        fecha_entrega = fecha_creacion + timedelta(days=random.randint(3, 10))
        
        # Determinar el estado según la fecha
        if dias_atras > 25:
            estado = Envio.EstadoChoices.ENTREGADO
        elif dias_atras > 20:
            estado = Envio.EstadoChoices.EN_REPARTO
        elif dias_atras > 15:
            estado = Envio.EstadoChoices.EN_TRANSITO
        elif dias_atras > 10:
            estados_posibles = [Envio.EstadoChoices.RECIBIDO, Envio.EstadoChoices.EN_TRANSITO]
            estado = random.choice(estados_posibles)
        elif dias_atras > 5:
            estado = Envio.EstadoChoices.RECIBIDO
        else:
            # Para envíos recientes, algunos pueden estar cancelados o devueltos
            estados_posibles = [Envio.EstadoChoices.RECIBIDO, Envio.EstadoChoices.CANCELADO, 
                              Envio.EstadoChoices.DEVUELTO, Envio.EstadoChoices.EN_TRANSITO]
            estado = random.choice(estados_posibles)
        
        # Crear el envío
        envio = Envio(
            estado_actual=estado,
            descripcion=random.choice(descripciones),
            peso=round(random.uniform(0.1, 20.0), 2),
            valor_declarado=round(random.uniform(10, 5000), 2) if random.random() > 0.3 else None,
            remitente_nombre=remitente,
            remitente_direccion=random.choice(direcciones),
            remitente_telefono=random.choice(telefonos),
            remitente_email=random.choice(correos) if random.random() > 0.5 else None,
            destinatario_nombre=destinatario,
            destinatario_direccion=random.choice(direcciones),
            destinatario_telefono=random.choice(telefonos),
            destinatario_email=random.choice(correos) if random.random() > 0.5 else None,
            fecha_estimada_entrega=fecha_entrega if random.random() > 0.2 else None,
            creado_por=random.choice([admin_user, operador_user]),
            actualizado_por=random.choice([admin_user, operador_user]),
        )
        envio.save()
        
        # Crear historial de estados
        # Primero, la creación del envío
        HistorialEstado.objects.create(
            envio=envio,
            estado=Envio.EstadoChoices.RECIBIDO,
            comentario="Creación del envío",
            ubicacion="La Habana",
            fecha=fecha_creacion,
            registrado_por=envio.creado_por
        )
        
        # Si el estado actual no es RECIBIDO, agregar más estados al historial
        if estado != Envio.EstadoChoices.RECIBIDO:
            estados_historico = []
            if estado == Envio.EstadoChoices.EN_TRANSITO or estado == Envio.EstadoChoices.EN_REPARTO or estado == Envio.EstadoChoices.ENTREGADO or estado == Envio.EstadoChoices.DEVUELTO:
                estados_historico.append({
                    'estado': Envio.EstadoChoices.EN_TRANSITO,
                    'comentario': "Envío recogido por transportista",
                    'ubicacion': "Centro de distribución, La Habana",
                    'fecha': fecha_creacion + timedelta(days=1 + random.randint(0, 2))
                })
            
            if estado == Envio.EstadoChoices.EN_REPARTO or estado == Envio.EstadoChoices.ENTREGADO or estado == Envio.EstadoChoices.DEVUELTO:
                estados_historico.append({
                    'estado': Envio.EstadoChoices.EN_REPARTO,
                    'comentario': "En ruta para entrega final",
                    'ubicacion': "Vehículo de reparto, La Habana",
                    'fecha': fecha_creacion + timedelta(days=3 + random.randint(0, 2))
                })
            
            if estado == Envio.EstadoChoices.ENTREGADO:
                estados_historico.append({
                    'estado': Envio.EstadoChoices.ENTREGADO,
                    'comentario': "Entregado al destinatario",
                    'ubicacion': "Domicilio del destinatario, La Habana",
                    'fecha': fecha_creacion + timedelta(days=5 + random.randint(0, 3))
                })
            elif estado == Envio.EstadoChoices.DEVUELTO:
                estados_historico.append({
                    'estado': Envio.EstadoChoices.DEVUELTO,
                    'comentario': "Destinatario ausente, envío devuelto",
                    'ubicacion': "Domicilio del destinatario, La Habana",
                    'fecha': fecha_creacion + timedelta(days=5 + random.randint(0, 3))
                })
            elif estado == Envio.EstadoChoices.CANCELADO:
                estados_historico.append({
                    'estado': Envio.EstadoChoices.CANCELADO,
                    'comentario': "Cancelado a petición del remitente",
                    'ubicacion': "Centro de distribución, La Habana",
                    'fecha': fecha_creacion + timedelta(hours=random.randint(1, 24))
                })
            
            # Crear registros en el historial
            for hist in estados_historico:
                HistorialEstado.objects.create(
                    envio=envio,
                    estado=hist['estado'],
                    comentario=hist['comentario'],
                    ubicacion=hist['ubicacion'],
                    fecha=hist['fecha'],
                    registrado_por=random.choice(created_users)
                )
        
        print(f"✅ Creado: Envío #{envio.numero_guia} - Estado: {envio.get_estado_actual_display()}")
    
    print("\n✅ DATOS DE DEMOSTRACIÓN CREADOS CORRECTAMENTE")
    print("\nCredenciales de acceso:")
    for role, user_data in usuarios.items():
        print(f"- {role.capitalize()}: {user_data['email']} / {user_data['password']}")

if __name__ == '__main__':
    create_demo_data()
