# 🇨🇺 PACKFY CUBA - Frontend Móvil Optimizado v4.0
FROM node:22-alpine

WORKDIR /app

# Instalar dependencias del sistema para gestión unificada y PWA móvil
RUN apk add --no-cache \
    curl \
    iputils \
    bind-tools \
    git \
    ca-certificates \
    openssl \
    bash

# Copiar archivos de configuración
COPY package*.json ./
COPY tsconfig.json ./
COPY vite.config.ts ./
COPY vite.config.docker.ts ./
COPY vite.config.mobile.ts ./

# Instalar dependencias de Node.js
RUN npm install

# Copiar código fuente
COPY . .

# Configurar Vite para Docker con optimizaciones móviles
RUN cp vite.config.mobile.ts vite.config.ts

# Variables de entorno para sistema móvil optimizado
ENV NODE_ENV=development
ENV HOST=0.0.0.0
ENV PORT=5173
ENV VITE_APP_VERSION=4.0
ENV VITE_APP_NAME="Packfy Cuba - Móvil Optimizado"
ENV VITE_INTERFACE_MODE=mobile-optimized
ENV VITE_FORM_STYLE=cuban-mobile
ENV VITE_SUBSCRIPTION_MODE=disabled
ENV VITE_FEATURE_MOBILE_NAV=enabled
ENV VITE_FEATURE_PWA_OPTIMIZED=enabled
ENV VITE_FEATURE_TOUCH_TARGETS=enabled
ENV VITE_FEATURE_SAFE_AREA=enabled
ENV VITE_API_BASE_URL=https://backend:8000

# Exponer puerto para el servidor de desarrollo
EXPOSE 5173

# Health check para verificar PWA móvil optimizada
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -k -f https://localhost:5173/manifest.json && \
    curl -k -f https://localhost:5173/sw.js && \
    curl -k -f https://localhost:5173 || exit 1

# Comando para iniciar el servidor HTTPS con optimizaciones móviles
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
