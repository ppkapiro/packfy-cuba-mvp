#!/usr/bin/env pwsh
# 🔍 PACKFY CUBA MVP - Verificación del Sistema
# Versión: Sin Multi-tenant (Modo Simple)
# Fecha: 19 de agosto de 2025

Write-Host "🔍 PACKFY CUBA MVP - VERIFICACIÓN DEL SISTEMA" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
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
Write-Host "🐳 VERIFICANDO DOCKER" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan

$containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>$null
if ($containers) {
    Write-Host $containers
    Write-Host ""
}
else {
    Show-Status "No hay contenedores ejecutándose" "WARN"
}

# Verificar servicios específicos
$services = @("packfy-database", "packfy-backend", "packfy-frontend")
foreach ($service in $services) {
    $status = docker ps --filter "name=$service" --format "{{.Status}}" 2>$null
    if ($status -like "*Up*") {
        Show-Status "${service}: $status" "OK"
    }
    else {
        Show-Status "${service}: No disponible" "ERROR"
    }
}

Write-Host ""
Write-Host "🌐 VERIFICANDO CONECTIVIDAD" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan

# Verificar puertos
$ports = @(
    @{Port = 5432; Service = "PostgreSQL Database" }
    @{Port = 8000; Service = "Django Backend" }
    @{Port = 5173; Service = "Vite Frontend" }
)

foreach ($portCheck in $ports) {
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $portCheck.Port -InformationLevel Quiet -WarningAction SilentlyContinue
        if ($connection) {
            Show-Status "$($portCheck.Service) (Puerto $($portCheck.Port))" "OK"
        }
        else {
            Show-Status "$($portCheck.Service) (Puerto $($portCheck.Port)): No disponible" "ERROR"
        }
    }
    catch {
        Show-Status "$($portCheck.Service) (Puerto $($portCheck.Port)): Error verificando" "ERROR"
    }
}

Write-Host ""
Write-Host "📂 VERIFICANDO ARCHIVOS" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

# Verificar archivos clave
$files = @(
    "compose.yml",
    "backend/config/settings.py",
    "backend/manage.py",
    "frontend/package.json",
    "frontend/vite.config.ts"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Show-Status "Archivo: $file" "OK"
    }
    else {
        Show-Status "Archivo: $file - No encontrado" "ERROR"
    }
}

Write-Host ""
Write-Host "🔍 VERIFICANDO CONFIGURACIÓN SIN MULTI-TENANT" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Verificar que no hay referencias a tenant
$tenantCheck = Select-String -Path "backend/config/settings.py" -Pattern "tenant|django_tenants" -Quiet
if (-not $tenantCheck) {
    Show-Status "Configuración limpia (sin multi-tenant)" "OK"
}
else {
    Show-Status "Se encontraron referencias a multi-tenant" "WARN"
}

Write-Host ""
Write-Host "🌐 URLs DE ACCESO:" -ForegroundColor Green
Write-Host "  📱 Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  🔧 Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  📊 Admin:    http://localhost:8000/admin" -ForegroundColor White
Write-Host "  📚 API Docs: http://localhost:8000/swagger/" -ForegroundColor White
Write-Host ""
Write-Host "🔑 CREDENCIALES:" -ForegroundColor Green
Write-Host "  📧 Email:    admin@packfy.com" -ForegroundColor White
Write-Host "  🔐 Password: packfy123" -ForegroundColor White
Write-Host ""
Write-Host "✅ Verificación completada" -ForegroundColor Green
