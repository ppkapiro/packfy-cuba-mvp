from django.contrib.auth import get_user_model

User = get_user_model()

# Verificar si ya existe
try:
    user = User.objects.get(email='admin@correo.com')
    print(f'Usuario ya existe: {user.email}')
    # Actualizar password
    user.set_password('admin123')
    user.save()
    print('Password actualizado')
except User.DoesNotExist:
    # Crear nuevo usuario
    user = User.objects.create_superuser(
        email='admin@correo.com',
        password='admin123'
    )
    print(f'Usuario creado: {user.email}')

print('Configuración completada!')
