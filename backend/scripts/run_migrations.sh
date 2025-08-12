#!/bin/bash

echo "Ejecutando migraciones..."

# Ejecutar migraciones
python manage.py migrate --noinput -v2

# Crear datos demo (incluye usuarios de prueba)
echo "Creando datos de demostración..."
python manage.py shell -c "
import sys
sys.path.append('/app/scripts')
try:
    from create_demo_data import create_demo_data
    create_demo_data()
    print('✅ Datos de demostración creados correctamente')
except Exception as e:
    print(f'❌ Error creando datos demo: {e}')
"

echo "Migraciones completadas."

# Iniciar servidor Django
echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000
