#!/bin/sh
set -eux  # mostrar comandos y salir al primer error
echo "Entrypoint inicio"

# Ejecutar migraciones directamente
echo "Ejecutando migraciones..."
python manage.py migrate --noinput -v2

# Crear estructura exacta con 10 usuarios (en lugar de datos demo)
echo "Creando estructura exacta con 10 usuarios..."
python manage.py shell -c "
import sys
sys.path.append('/app/scripts')

try:
    # Verificar si ya existen usuarios
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if User.objects.count() == 0:
        print('📄 Ejecutando script de 10 usuarios exactos...')
        from crear_10_usuarios import restaurar_10_usuarios
        restaurar_10_usuarios()
    else:
        print(f'ℹ️ Ya existen {User.objects.count()} usuarios, saltando inicialización')
except Exception as e:
    print(f'❌ Error ejecutando restauración: {e}')
    import traceback
    traceback.print_exc()
"

echo "Migraciones completadas."

# Iniciar servidor Django
echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000
