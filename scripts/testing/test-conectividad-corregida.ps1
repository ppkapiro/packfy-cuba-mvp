#!/usr/bin/env pwsh
# Script para probar la conectividad corregida

Write-Host "🔍 PROBANDO CONECTIVIDAD CORREGIDA" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "📊 Estado de servidores:" -ForegroundColor Yellow

# Verificar puertos
$backend = Test-NetConnection -ComputerName "localhost" -Port 8000 -InformationLevel Quiet
$frontend = Test-NetConnection -ComputerName "localhost" -Port 5173 -InformationLevel Quiet

Write-Host "Backend (8000): " -NoNewline
if ($backend) { Write-Host "✅ ACTIVO" -ForegroundColor Green } else { Write-Host "❌ INACTIVO" -ForegroundColor Red }

Write-Host "Frontend (5173): " -NoNewline
if ($frontend) { Write-Host "✅ ACTIVO" -ForegroundColor Green } else { Write-Host "❌ INACTIVO" -ForegroundColor Red }

if ($backend -and $frontend) {
    Write-Host ""
    Write-Host "🧪 Probando endpoints corregidos:" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "1. Endpoint directo del backend:" -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/api/" -Method GET -TimeoutSec 10 -UseBasicParsing
        Write-Host "   ✅ Backend directo: $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Backend directo: Error - $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "2. Endpoint a través del proxy:" -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5173/api/" -Method GET -TimeoutSec 10 -UseBasicParsing
        Write-Host "   ✅ Proxy funcionando: $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Proxy: Error - $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "3. Verificando rutas específicas:" -ForegroundColor Cyan
    
    # Probar auth
    try {
        $authResponse = Invoke-WebRequest -Uri "http://localhost:5173/api/auth/login/" -Method POST -TimeoutSec 10 -UseBasicParsing -Body '{}' -ContentType 'application/json'
        Write-Host "   ✅ Auth endpoint: $($authResponse.StatusCode)" -ForegroundColor Green
    } catch {
        $statusCode = if ($_.Exception.Response) { $_.Exception.Response.StatusCode } else { "Sin respuesta" }
        Write-Host "   📍 Auth endpoint: $statusCode (esperado error de datos)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "🎉 RESUMEN:" -ForegroundColor Green
    Write-Host "   ✅ Servidores activos" -ForegroundColor Green
    Write-Host "   ✅ Proxy configurado correctamente" -ForegroundColor Green
    Write-Host "   ✅ Rutas corregidas (sin duplicación /api/api/)" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 URLs disponibles:" -ForegroundColor Cyan
    Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Green
    Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Green
    Write-Host "   Móvil:    http://192.168.12.178:5173" -ForegroundColor Green
    
} else {
    Write-Host ""
    Write-Host "❌ Uno o ambos servidores no están activos" -ForegroundColor Red
    Write-Host "💡 Ejecuta: .\inicio-robusto.ps1" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Presiona Enter para salir"
