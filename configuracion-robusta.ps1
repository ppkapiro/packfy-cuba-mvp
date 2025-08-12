#!/usr/bin/env pwsh
# Configuración robusta de Docker Compose para evitar desconexiones
# Packfy Cuba MVP

Write-Host "🛡️  CONFIGURACIÓN ROBUSTA ANTI-DESCONEXIÓN" -ForegroundColor Green -BackgroundColor Black
Write-Host "=============================================" -ForegroundColor Green

# Crear docker-compose override para configuración robusta
$dockerOverride = @"
version: '3.8'

services:
  frontend:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "https://localhost:5173", "-k"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
    deploy:
      restart_policy:
        condition: any
        delay: 5s
        max_attempts: 5
    environment:
      - NODE_ENV=development
      - VITE_HMR_PORT=5173
    volumes:
      - ./frontend:/app
      - /app/node_modules
    networks:
      - packfy-network

  backend:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health/", "||", "exit", "1"]
      interval: 15s
      timeout: 10s
      retries: 3
      start_period: 60s
    deploy:
      restart_policy:
        condition: any
        delay: 10s
        max_attempts: 5
    environment:
      - DJANGO_SETTINGS_MODULE=backend.settings
      - DEBUG=1
    volumes:
      - ./backend:/app
    networks:
      - packfy-network
    depends_on:
      database:
        condition: service_healthy

  database:
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U packfy_user -d packfy_db"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      restart_policy:
        condition: any
        delay: 5s
        max_attempts: 3
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup_db.sql:/docker-entrypoint-initdb.d/backup.sql:ro
    networks:
      - packfy-network

networks:
  packfy-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  postgres_data:
    driver: local
"@

Write-Host "📝 Creando docker-compose.override.yml..." -ForegroundColor Cyan
$dockerOverride | Out-File -FilePath "docker-compose.override.yml" -Encoding UTF8

# Crear endpoint de health check para el backend
$healthEndpoint = @"
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

@csrf_exempt
def health_check(request):
    try:
        # Verificar conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': '$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': '$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")'
        }, status=500)
"@

Write-Host "📝 Creando endpoint de health check..." -ForegroundColor Cyan
$healthEndpoint | Out-File -FilePath "backend/health_check.py" -Encoding UTF8

# Actualizar urls.py para incluir el health check
$urlsUpdate = @"
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('envios.urls')),
    path('api/health/', health_check.health_check),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', SpectacularSwaggerView.as_view(url_name='schema')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"@

Write-Host "📝 Actualizando backend URLs..." -ForegroundColor Cyan
$urlsUpdate | Out-File -FilePath "backend/backend/urls.py" -Encoding UTF8

# Crear script de inicio robusto
$startupScript = @"
#!/usr/bin/env pwsh
# Script de inicio robusto para Packfy

Write-Host "🚀 INICIANDO PACKFY CON CONFIGURACIÓN ROBUSTA" -ForegroundColor Green -BackgroundColor Black

# Detener servicios existentes
Write-Host "🛑 Deteniendo servicios existentes..." -ForegroundColor Yellow
docker compose down 2>$null

# Limpiar contenedores huérfanos
Write-Host "🧹 Limpiando contenedores huérfanos..." -ForegroundColor Yellow
docker compose down --remove-orphans 2>$null

# Construir imágenes frescas si es necesario
Write-Host "🔨 Verificando imágenes..." -ForegroundColor Cyan
docker compose build --no-cache

# Iniciar servicios con configuración robusta
Write-Host "🚀 Iniciando servicios robustos..." -ForegroundColor Green
docker compose up -d

# Esperar que los servicios estén saludables
Write-Host "⏳ Esperando que los servicios estén saludables..." -ForegroundColor Cyan
$maxWait = 120
$waited = 0

do {
    Start-Sleep 5
    $waited += 5

    $status = docker compose ps --format json | ConvertFrom-Json
    $allHealthy = $true

    foreach ($container in $status) {
        if ($container.State -ne "running") {
            $allHealthy = $false
            Write-Host "   ⏳ Esperando $($container.Service)..." -ForegroundColor Gray
            break
        }
    }

    if ($waited -ge $maxWait) {
        Write-Host "⚠️  Tiempo de espera agotado - verificando manualmente..." -ForegroundColor Yellow
        break
    }

} while (-not $allHealthy)

# Verificar conectividad final
Write-Host "🔍 Verificación final de conectividad..." -ForegroundColor Cyan

try {
    $frontend = Invoke-WebRequest -Uri "https://localhost:5173" -Method Head -TimeoutSec 10 -SkipCertificateCheck
    Write-Host "✅ Frontend: CONECTADO" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend: PROBLEMA" -ForegroundColor Red
}

try {
    $backend = Invoke-WebRequest -Uri "http://localhost:8000/api/health/" -TimeoutSec 10
    Write-Host "✅ Backend: CONECTADO" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend: PROBLEMA" -ForegroundColor Red
}

Write-Host "`n🎯 URLs de acceso:" -ForegroundColor Green
Write-Host "   Frontend: https://localhost:5173" -ForegroundColor Cyan
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Health:   http://localhost:8000/api/health/" -ForegroundColor Cyan

Write-Host "`n✅ PACKFY INICIADO CON CONFIGURACIÓN ROBUSTA" -ForegroundColor Green -BackgroundColor Black
"@

Write-Host "📝 Creando script de inicio robusto..." -ForegroundColor Cyan
$startupScript | Out-File -FilePath "inicio-robusto.ps1" -Encoding UTF8

Write-Host "`n✅ CONFIGURACIÓN ROBUSTA COMPLETADA" -ForegroundColor Green
Write-Host "📋 Archivos creados:" -ForegroundColor Cyan
Write-Host "   • docker-compose.override.yml - Configuración robusta" -ForegroundColor White
Write-Host "   • backend/health_check.py - Endpoint de salud" -ForegroundColor White
Write-Host "   • backend/backend/urls.py - URLs actualizadas" -ForegroundColor White
Write-Host "   • inicio-robusto.ps1 - Script de inicio mejorado" -ForegroundColor White

Write-Host "`n🚀 Para usar la configuración robusta:" -ForegroundColor Green
Write-Host "   ./inicio-robusto.ps1" -ForegroundColor Cyan
