#!/usr/bin/env pwsh
# 🚀 PACKFY CUBA MVP - Script de Inicio Limpio
# Versión: Sin Multi-tenant (Modo Simple)
# Fecha: 19 de agosto de 2025

Write-Host "🚀 PACKFY CUBA MVP - INICIO LIMPIO" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Función para mostrar estado
function Show-Status {
    param($Message, $Status)
    if ($Status -eq "OK") {
        Write-Host "✅ $Message" -ForegroundColor Green
    }
    elseif ($Status -eq "WARN") {
        Write-Host "⚠️  $Message" -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ $Message" -ForegroundColor Red
    }
}

# Verificar Docker
Write-Host "🔍 Verificando Docker..." -ForegroundColor Cyan
try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) {
        Show-Status "Docker disponible: $dockerVersion" "OK"
    }
    else {
        Show-Status "Docker no encontrado" "ERROR"
        exit 1
    }
}
catch {
    Show-Status "Error verificando Docker" "ERROR"
    exit 1
}

# Limpiar contenedores anteriores
Write-Host ""
Write-Host "🧹 Limpiando entorno anterior..." -ForegroundColor Cyan
docker-compose down --volumes --remove-orphans 2>$null

# Construir imágenes
Write-Host ""
Write-Host "🔨 Construyendo imágenes..." -ForegroundColor Cyan
docker-compose build --no-cache

# Iniciar servicios
Write-Host ""
Write-Host "🚀 Iniciando servicios..." -ForegroundColor Cyan
docker-compose up -d

# Verificar estado
Write-Host ""
Write-Host "📊 Verificando estado de servicios..." -ForegroundColor Cyan
Start-Sleep 10

$services = @("packfy-database", "packfy-backend", "packfy-frontend")
foreach ($service in $services) {
    $status = docker ps --filter "name=$service" --format "table {{.Names}}\t{{.Status}}" 2>$null
    if ($status -like "*Up*") {
        Show-Status "$service funcionando" "OK"
    }
    else {
        Show-Status "$service no disponible" "WARN"
    }
}

Write-Host ""
Write-Host "🌐 URLs de acceso:" -ForegroundColor Cyan
Write-Host "  📱 Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  🔧 Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  📊 Admin:    http://localhost:8000/admin" -ForegroundColor White
Write-Host "  📚 API Docs: http://localhost:8000/swagger/" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Credenciales de administrador:" -ForegroundColor Cyan
Write-Host "  📧 Email:    admin@packfy.com" -ForegroundColor White
Write-Host "  🔐 Password: packfy123" -ForegroundColor White
Write-Host ""
Write-Host "✅ ¡Sistema iniciado correctamente!" -ForegroundColor Green
