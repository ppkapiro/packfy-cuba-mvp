FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias base
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
COPY pip.conf /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . /app/
RUN apt-get update && apt-get install -y dos2unix && dos2unix /app/scripts/*.sh

RUN chmod +x /app/scripts/run_migrations.sh

# Copiar y dar permisos al entrypoint
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh

# Definir entrypoint para ejecutar migraciones antes de arrancar
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# Puerto en el que escucha la aplicación
EXPOSE 8000

# Usar runserver directo para evitar prompts interactivos de tenant_command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]