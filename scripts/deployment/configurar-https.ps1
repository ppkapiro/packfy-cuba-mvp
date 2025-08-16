#!/usr/bin/env pwsh
# 🇨🇺 PACKFY CUBA - Configuración HTTPS Completa v4.0
# Script para configurar y verificar HTTPS en todo el sistema

Write-Host "🇨🇺 PACKFY CUBA - Iniciando configuración HTTPS completa..." -ForegroundColor Green

# 1. Verificar que Docker esté ejecutándose
Write-Host "🐳 Verificando Docker..." -ForegroundColor Cyan
try {
    docker version | Out-Null
    Write-Host "✅ Docker está funcionando correctamente" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker no está disponible. Por favor, inicia Docker Desktop." -ForegroundColor Red
    exit 1
}

# 2. Verificar contenedores
Write-Host "📦 Verificando contenedores..." -ForegroundColor Cyan
$containers = docker ps --format "{{.Names}}" | Where-Object { $_ -match "packfy-" }
if ($containers.Count -lt 4) {
    Write-Host "⚠️  No todos los contenedores están ejecutándose. Iniciando sistema..." -ForegroundColor Yellow
    docker-compose up -d
    Start-Sleep -Seconds 10
}

# 3. Generar certificados SSL si no existen
Write-Host "🔒 Configurando certificados SSL..." -ForegroundColor Cyan
docker exec packfy-backend-v4 python scripts/configure_https_fixed.py

# 4. Verificar que HTTPS esté funcionando
Write-Host "🌐 Verificando conexión HTTPS..." -ForegroundColor Cyan
try {
    $response = curl -k -X GET https://localhost:8443/api/sistema-info/ -H "Content-Type: application/json" -s
    if ($response -match "Packfy") {
        Write-Host "✅ Backend HTTPS funcionando correctamente en puerto 8443" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Backend HTTPS no responde correctamente" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Error al conectar con HTTPS backend" -ForegroundColor Red
}

# 5. Verificar Frontend
Write-Host "🖥️  Verificando Frontend..." -ForegroundColor Cyan
try {
    $frontendStatus = curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>$null
    if ($frontendStatus -eq "200") {
        Write-Host "✅ Frontend funcionando correctamente en puerto 5173" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Frontend no responde correctamente" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Error al conectar con Frontend" -ForegroundColor Red
}

# 6. Probar login HTTPS
Write-Host "🔐 Probando autenticación HTTPS..." -ForegroundColor Cyan
try {
    $loginData = '{"email": "admin@packfy.cu", "password": "admin123"}'
    $loginResponse = curl -k -X POST https://localhost:8443/api/auth/login/ -H "Content-Type: application/json" -d $loginData -s
    if ($loginResponse -match "access") {
        Write-Host "✅ Autenticación HTTPS funcionando correctamente" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Error en autenticación HTTPS" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Error al probar login HTTPS" -ForegroundColor Red
}

Write-Host "`n🎯 RESUMEN DE CONFIGURACIÓN HTTPS:" -ForegroundColor Magenta
Write-Host "───────────────────────────────────" -ForegroundColor Gray
Write-Host "🌐 Frontend:      http://localhost:5173" -ForegroundColor White
Write-Host "🔒 Backend HTTP:  http://localhost:8000" -ForegroundColor White
Write-Host "🔐 Backend HTTPS: https://localhost:8443" -ForegroundColor Green
Write-Host "🗄️  Base de Datos: localhost:5433" -ForegroundColor White
Write-Host "💾 Redis:         localhost:6379" -ForegroundColor White
Write-Host "`n📋 Credenciales de acceso:" -ForegroundColor Yellow
Write-Host "   Email:    admin@packfy.cu" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White

Write-Host "`n✅ Configuración HTTPS completada!" -ForegroundColor Green
Write-Host "🚀 Abre http://localhost:5173 en tu navegador para usar la aplicación" -ForegroundColor Cyan
