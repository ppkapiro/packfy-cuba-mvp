# Script de deployment completo para Packfy Cuba MVP v2.0.0

param(
    [string]$Environment = "production",
    [switch]$Build = $false,
    [switch]$Deploy = $false,
    [switch]$Rollback = $false
)

Write-Host "🚀 PACKFY CUBA MVP - DEPLOYMENT SCRIPT v2.0.0" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"

function Show-Status {
    param([string]$Message, [string]$Color = "Yellow")
    Write-Host "🔄 $Message" -ForegroundColor $Color
}

function Show-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Show-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Verificar requisitos
Show-Status "Verificando requisitos..."

if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Show-Error "Docker no está instalado"
    exit 1
}

if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Show-Error "Docker Compose no está instalado"
    exit 1
}

Show-Success "Requisitos verificados"

# Variables de entorno
$PROJECT_NAME = "packfy-cuba-mvp"
$VERSION = "v2.0.0"
$TIMESTAMP = Get-Date -Format "yyyyMMdd-HHmmss"

if ($Build) {
    Show-Status "Construyendo imágenes para $Environment..."
    
    if ($Environment -eq "production") {
        # Build para producción
        docker-compose -f docker-compose.prod.yml build --no-cache
        if ($LASTEXITCODE -ne 0) {
            Show-Error "Error en build de producción"
            exit 1
        }
    } else {
        # Build para desarrollo
        docker-compose build --no-cache
        if ($LASTEXITCODE -ne 0) {
            Show-Error "Error en build de desarrollo"
            exit 1
        }
    }
    
    Show-Success "Imágenes construidas exitosamente"
}

if ($Deploy) {
    Show-Status "Iniciando deployment en $Environment..."
    
    # Backup de la base de datos actual
    Show-Status "Creando backup de base de datos..."
    $backupFile = "backup_${TIMESTAMP}.sql"
    docker-compose exec database pg_dump -U packfy_user packfy_db > "./backups/$backupFile"
    Show-Success "Backup creado: $backupFile"
    
    if ($Environment -eq "production") {
        # Deployment de producción
        Show-Status "Deployando en producción..."
        
        # Detener servicios actuales
        docker-compose -f docker-compose.prod.yml down
        
        # Iniciar nuevos servicios
        docker-compose -f docker-compose.prod.yml up -d
        
        # Esperar que los servicios estén listos
        Show-Status "Esperando que los servicios estén listos..."
        Start-Sleep -Seconds 30
        
        # Verificar salud de los servicios
        $frontendHealth = docker-compose -f docker-compose.prod.yml ps frontend | Select-String "healthy"
        $backendHealth = docker-compose -f docker-compose.prod.yml ps backend | Select-String "healthy"
        
        if ($frontendHealth -and $backendHealth) {
            Show-Success "Deployment de producción completado"
        } else {
            Show-Error "Error en deployment de producción"
            exit 1
        }
    } else {
        # Deployment de desarrollo
        Show-Status "Deployando en desarrollo..."
        docker-compose down
        docker-compose up -d
        Show-Success "Deployment de desarrollo completado"
    }
}

if ($Rollback) {
    Show-Status "Iniciando rollback..."
    
    # Encontrar el último backup
    $latestBackup = Get-ChildItem "./backups/*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if ($latestBackup) {
        Show-Status "Restaurando desde: $($latestBackup.Name)"
        
        # Detener servicios
        if ($Environment -eq "production") {
            docker-compose -f docker-compose.prod.yml down
        } else {
            docker-compose down
        }
        
        # Restaurar base de datos
        if ($Environment -eq "production") {
            docker-compose -f docker-compose.prod.yml up -d database
        } else {
            docker-compose up -d database
        }
        
        Start-Sleep -Seconds 10
        
        # Restaurar backup
        Get-Content $latestBackup.FullName | docker-compose exec -T database psql -U packfy_user -d packfy_db
        
        # Reiniciar todos los servicios
        if ($Environment -eq "production") {
            docker-compose -f docker-compose.prod.yml up -d
        } else {
            docker-compose up -d
        }
        
        Show-Success "Rollback completado"
    } else {
        Show-Error "No se encontraron backups"
        exit 1
    }
}

# Mostrar estado final
Show-Status "Estado final de los servicios:"
if ($Environment -eq "production") {
    docker-compose -f docker-compose.prod.yml ps
} else {
    docker-compose ps
}

Write-Host ""
Write-Host "🎉 DEPLOYMENT SCRIPT COMPLETADO" -ForegroundColor Green
Write-Host "Versión: $VERSION" -ForegroundColor Cyan
Write-Host "Entorno: $Environment" -ForegroundColor Cyan
Write-Host "Timestamp: $TIMESTAMP" -ForegroundColor Cyan

if ($Environment -eq "production") {
    Write-Host ""
    Write-Host "🔗 URLs de producción:" -ForegroundColor Yellow
    Write-Host "  🌐 Web: https://packfy.cu" -ForegroundColor White
    Write-Host "  📱 PWA: https://packfy.cu (instalable)" -ForegroundColor White
    Write-Host "  🔧 API: https://api.packfy.cu" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "🔗 URLs de desarrollo:" -ForegroundColor Yellow
    Write-Host "  🌐 Web: http://localhost:5173" -ForegroundColor White
    Write-Host "  📱 Móvil: http://192.168.12.179:5173" -ForegroundColor White
    Write-Host "  🔧 API: http://localhost:8000" -ForegroundColor White
}
