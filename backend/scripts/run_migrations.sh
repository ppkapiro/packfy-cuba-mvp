#!/bin/bash

echo "Ejecutando migraciones..."

# Ejecutar migraciones
python manage.py migrate --noinput -v2

# Crear superusuario por defecto si no existe
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    # Crear usuario usando create_superuser
    user = User.objects.create_superuser('admin@ejemplo.com', 'admin123', username='admin');
    # Verificar explícitamente que la contraseña sea correcta
    from django.contrib.auth.hashers import check_password;
    if not check_password('admin123', user.password):
        # Si la contraseña no es correcta, establecerla manualmente
        user.set_password('admin123');
        user.save();
        print('Contraseña de administrador actualizada correctamente');
    print('Superusuario creado correctamente');
"

echo "Migraciones completadas."
