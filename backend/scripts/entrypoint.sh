#!/bin/sh
set -eux  # mostrar comandos y salir al primer error
echo "Entrypoint inicio"
# Entry point para contenedor Django
# Ejecuta migraciones y luego arranca la aplicación
/app/scripts/run_migrations.sh
exec "$@"
