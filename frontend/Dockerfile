# 🇨🇺 PACKFY CUBA - Frontend Gestión Unificada v3.3
FROM node:22-alpine

WORKDIR /app

# Instalar dependencias del sistema para gestión y rastreo unificado
RUN apk add --no-cache \
    curl \
    iputils \
    bind-tools \
    git \
    ca-certificates \
    openssl

# Copiar archivos de configuración
COPY package*.json ./
COPY tsconfig.json ./
COPY vite.config.ts ./
COPY vite.config.docker.ts ./

# Instalar dependencias de Node.js
RUN npm install

# Copiar código fuente
COPY . .

# Configurar Vite para Docker con sistema unificado
RUN cp vite.config.docker.ts vite.config.ts

# Variables de entorno para gestión y rastreo unificado con HTTPS
ENV NODE_ENV=development
ENV HOST=0.0.0.0
ENV PORT=5173
ENV VITE_APP_VERSION=3.3
ENV VITE_APP_NAME="Packfy Cuba - Gestión Unificada"
ENV VITE_INTERFACE_MODE=unified-management
ENV VITE_FORM_STYLE=cuban-unified
ENV VITE_SUBSCRIPTION_MODE=disabled
ENV VITE_FEATURE_UNIFIED_PAGES=enabled
ENV VITE_API_BASE_URL=https://backend:8000

# Exponer puerto para el servidor de desarrollo
EXPOSE 5173

# Health check para verificar que la gestión unificada HTTPS está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -k -f https://localhost:5173/envios || curl -k -f https://localhost:5173 || exit 1

# Comando para iniciar el servidor HTTPS con gestión unificada
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
