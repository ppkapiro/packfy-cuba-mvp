# 🇨🇺 PACKFY CUBA - Backend Gestión Unificada v3.3
FROM python:3.11-slim

# Metadatos del contenedor
LABEL maintainer="Packfy Cuba Team"
LABEL version="3.3"
LABEL description="Backend para gestión y rastreo unificado con HTTPS - Packfy Cuba"

WORKDIR /app

# Instalar dependencias del sistema para HTTPS y gestión unificada
RUN apt-get update && \
    apt-get install -y \
    gcc \
    libpq-dev \
    dos2unix \
    curl \
    wget \
    git \
    postgresql-client \
    openssl \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar Python para mejor rendimiento
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Copiar archivos de configuración
COPY requirements.txt /app/
COPY pip.conf /app/

# Instalar dependencias de Python con cache optimizado
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . /app/

# Corregir line endings y permisos para scripts
RUN find /app -name "*.sh" -type f -exec dos2unix {} \; && \
    find /app -name "*.sh" -type f -exec chmod +x {} \; && \
    find /app -name "*.py" -type f -exec chmod 644 {} \;

# Crear directorios necesarios
RUN mkdir -p /app/logs /app/static /app/media /app/tmp

# Variables de entorno para gestión unificada con HTTPS
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV INTERFACE_VERSION=3.3
ENV FEATURE_UNIFIED_MANAGEMENT=enabled
ENV CORS_ALLOWED_ORIGINS=https://localhost:5173,https://frontend:5173
ENV FRONTEND_URL=https://localhost:5173
ENV USE_HTTPS=true
ENV BACKEND_MODE=optimized

# Health check mejorado
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python manage.py check --deploy || exit 1

# Exponer puerto
EXPOSE 8000

# Entrypoint con migraciones automáticas
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# Comando optimizado para desarrollo con interfaz moderna
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
