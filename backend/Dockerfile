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

# Instalar dos2unix y corregir line endings, luego dar permisos
RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix /app/scripts/*.sh && \
    chmod +x /app/scripts/*.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Definir entrypoint para ejecutar migraciones antes de arrancar
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# Puerto en el que escucha la aplicación
EXPOSE 8000

# Usar runserver directo para evitar prompts interactivos de tenant_command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
