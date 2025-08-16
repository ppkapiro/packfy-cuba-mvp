#!/bin/sh
set -eux  # mostrar comandos y salir al primer error
echo "🇨🇺 PACKFY CUBA - Entrypoint inicio"

# Ejecutar migraciones directamente
echo "📋 Ejecutando migraciones..."
python manage.py migrate --noinput -v2

# Crear datos demo (incluye usuarios de prueba)
echo "🎯 Creando datos de demostración..."
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

echo "✅ Migraciones completadas."

# Configurar HTTPS si está habilitado
USE_HTTPS=${USE_HTTPS:-false}
if [ "$USE_HTTPS" = "true" ]; then
    echo "🔒 Configurando servidor HTTPS..."
    python scripts/configure_https_fixed.py

    # Iniciar servidor HTTPS y HTTP en paralelo
    echo "🚀 Iniciando servidores HTTP y HTTPS..."
    python manage.py runserver 0.0.0.0:8000 &
    echo "✅ Servidor HTTP iniciado en puerto 8000"

    # HTTPS opcional: si runsslserver no existe, mantener solo HTTP (el proxy usa HTTP interno)
    if python -c "import importlib; import sys; sys.exit(0 if importlib.util.find_spec('sslserver') else 1)"; then
        CERT_FILE="/app/certs/cert.crt"; KEY_FILE="/app/certs/cert.key"
        [ -f "/app/certs/localhost.crt" ] && [ -f "/app/certs/localhost.key" ] && CERT_FILE="/app/certs/localhost.crt" && KEY_FILE="/app/certs/localhost.key"
        if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
            echo "🔒 Iniciando servidor HTTPS en puerto 8443..."
            python manage.py runsslserver 0.0.0.0:8443 --certificate "$CERT_FILE" --key "$KEY_FILE" &
            echo "✅ Servidor HTTPS iniciado en puerto 8443"
        else
            echo "⚠️  Certificados no encontrados, solo servidor HTTP disponible"
        fi
    else
        echo "ℹ️  sslserver no disponible, continúo solo con HTTP en 8000"
    fi

    # Esperar indefinidamente
    wait
else
    echo "🌐 Iniciando servidor HTTP..."
    python manage.py runserver 0.0.0.0:8000
fi
