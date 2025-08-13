#!/usr/bin/env pwsh
# 🇨🇺 PACKFY CUBA - Script de Inicio v4.0
# Sistema moderno de gestión de envíos

Write-Host "🇨🇺 PACKFY CUBA v4.0 - SISTEMA MODERNO DE GESTIÓN" -ForegroundColor Cyan
Write-Host "=" -repeat 55 -ForegroundColor Yellow

# Verificar Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker no está disponible" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose no está disponible" -ForegroundColor Red
    exit 1
}

# Limpiar contenedores anteriores
Write-Host "🧹 Limpiando contenedores anteriores..." -ForegroundColor Yellow
docker-compose down --remove-orphans

# Iniciar servicios
Write-Host "🚀 Iniciando servicios..." -ForegroundColor Green
docker-compose up -d

# Esperar servicios
Write-Host "⏳ Esperando que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Verificar estado
Write-Host "📊 Estado de los servicios:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "✅ PACKFY CUBA v4.0 INICIADO CORRECTAMENTE" -ForegroundColor Green
Write-Host "=" -repeat 45 -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "🔧 Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "📊 Admin:    http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Credenciales de prueba:" -ForegroundColor Cyan
Write-Host "   Email:    test@test.com" -ForegroundColor White
Write-Host "   Password: 123456" -ForegroundColor White
Write-Host ""
Write-Host "🎨 Características v4.0:" -ForegroundColor Magenta
Write-Host "   ✨ Interfaz glassmorphism cubana" -ForegroundColor Green
Write-Host "   🎯 Sistema CSS unificado" -ForegroundColor Green
Write-Host "   📱 Responsive completo" -ForegroundColor Green
Write-Host "   ⚡ Performance optimizada" -ForegroundColor Green
Write-Host ""
Write-Host "🛑 Para detener: docker-compose down" -ForegroundColor Gray
