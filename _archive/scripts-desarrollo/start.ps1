# 🚀 Packfy Cuba MVP - Inicio Simplificado
# Script principal para iniciar el proyecto limpio

Write-Host "🚀 Iniciando Packfy Cuba MVP v2.0.0..." -ForegroundColor Green

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "compose.yml")) {
    Write-Host "❌ Error: No se encuentra compose.yml" -ForegroundColor Red
    Write-Host "Asegúrate de estar en el directorio del proyecto" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Iniciando contenedores Docker..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "⏳ Esperando que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "🔍 Verificando estado de los servicios..." -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host ""
Write-Host "✅ Packfy Cuba MVP iniciado correctamente!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Accesos disponibles:" -ForegroundColor Cyan
Write-Host "  🌐 Frontend (Web):  http://localhost:5173" -ForegroundColor White
Write-Host "  🔧 Backend (API):   http://localhost:8000" -ForegroundColor White
Write-Host "  📊 Admin Django:    http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "👤 Credenciales de prueba:" -ForegroundColor Cyan
Write-Host "  Email:    test@test.com" -ForegroundColor White
Write-Host "  Password: 123456" -ForegroundColor White
Write-Host ""
Write-Host "📱 Para acceso móvil (misma red WiFi):" -ForegroundColor Cyan
Write-Host "  Obtén tu IP: ipconfig" -ForegroundColor White
Write-Host "  Usa: http://[TU-IP]:5173" -ForegroundColor White
