from envios.models import Envio
from django.contrib.auth.models import User

# Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print('✅ Superusuario creado')

# Limpiar envíos existentes
Envio.objects.all().delete()

# Crear envío simple
envio = Envio.objects.create(
    numero_guia='TEST001',
    remitente_nombre='José García',
    destinatario_nombre='María López',
    estado_actual='RECIBIDO',
    peso=2.5,
    descripcion='Paquete de prueba',
    remitente_direccion='La Habana, Cuba',
    remitente_telefono='12345678',
    destinatario_direccion='Santiago, Cuba',
    destinatario_telefono='87654321'
)

print(f'✅ Envío creado: {envio.numero_guia} - {envio.remitente_nombre} → {envio.destinatario_nombre}')
