#!/usr/bin/env pwsh
# Diagnóstico específico para problemas de login y red

Write-Host "🔍 DIAGNÓSTICO PROBLEMAS LOGIN Y RED" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Verificar servidores
Write-Host ""
Write-Host "📊 1. ESTADO DE SERVIDORES" -ForegroundColor Yellow

$backend8000 = Test-NetConnection -ComputerName "localhost" -Port 8000 -InformationLevel Quiet
$frontend5173 = Test-NetConnection -ComputerName "localhost" -Port 5173 -InformationLevel Quiet

Write-Host "Backend (8000): " -NoNewline
if ($backend8000) { Write-Host "✅ ACTIVO" -ForegroundColor Green } else { Write-Host "❌ INACTIVO" -ForegroundColor Red }

Write-Host "Frontend (5173): " -NoNewline
if ($frontend5173) { Write-Host "✅ ACTIVO" -ForegroundColor Green } else { Write-Host "❌ INACTIVO" -ForegroundColor Red }

# Verificar IP local
Write-Host ""
Write-Host "🌐 2. INFORMACIÓN DE RED" -ForegroundColor Yellow

try {
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress | Select-Object -First 1
    Write-Host "IP Local detectada: $localIP" -ForegroundColor Cyan
    
    if ($localIP) {
        Write-Host "URLs de acceso:" -ForegroundColor White
        Write-Host "  🖥️ Localhost: http://localhost:5173" -ForegroundColor Green
        Write-Host "  📱 Red local: http://${localIP}:5173" -ForegroundColor Green
        
        # Verificar conectividad a la IP local
        if ($frontend5173) {
            Write-Host ""
            Write-Host "🧪 Probando conectividad a IP local..." -ForegroundColor Cyan
            try {
                $response = Invoke-WebRequest -Uri "http://${localIP}:5173" -Method GET -TimeoutSec 5 -UseBasicParsing
                Write-Host "✅ IP local accesible: $($response.StatusCode)" -ForegroundColor Green
            } catch {
                Write-Host "❌ Error accediendo a IP local: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "   Esto podría explicar los problemas con .178" -ForegroundColor Yellow
            }
        }
    }
} catch {
    Write-Host "❌ Error obteniendo IP local" -ForegroundColor Red
}

# Verificar endpoints de login
Write-Host ""
Write-Host "🔐 3. PRUEBA DE ENDPOINTS DE LOGIN" -ForegroundColor Yellow

if ($backend8000) {
    Write-Host "Probando endpoints de autenticación..." -ForegroundColor Cyan
    
    # Probar endpoint directo
    try {
        $loginDirect = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/login/" -Method POST -TimeoutSec 10 -UseBasicParsing -Body '{}' -ContentType 'application/json'
        Write-Host "✅ Backend directo - Login endpoint: $($loginDirect.StatusCode)" -ForegroundColor Green
    } catch {
        $statusCode = if ($_.Exception.Response) { $_.Exception.Response.StatusCode } else { "Sin respuesta" }
        Write-Host "📍 Backend directo - Login: $statusCode (esperado 400/422)" -ForegroundColor Yellow
    }
    
    # Probar a través del proxy si frontend está activo
    if ($frontend5173) {
        try {
            $loginProxy = Invoke-WebRequest -Uri "http://localhost:5173/api/auth/login/" -Method POST -TimeoutSec 10 -UseBasicParsing -Body '{}' -ContentType 'application/json'
            Write-Host "✅ Proxy - Login endpoint: $($loginProxy.StatusCode)" -ForegroundColor Green
        } catch {
            $statusCode = if ($_.Exception.Response) { $_.Exception.Response.StatusCode } else { "Sin respuesta" }
            Write-Host "📍 Proxy - Login: $statusCode (esperado 400/422)" -ForegroundColor Yellow
        }
    }
}

# Verificar problemas de HMR/recargas constantes
Write-Host ""
Write-Host "🔄 4. DIAGNÓSTICO DE RECARGAS CONSTANTES" -ForegroundColor Yellow

if (Test-Path "frontend\vite.config.ts") {
    Write-Host "Verificando configuración de Vite..." -ForegroundColor Cyan
    $viteConfig = Get-Content "frontend\vite.config.ts" -Raw
    
    if ($viteConfig -match "usePolling.*true") {
        Write-Host "⚠️ Polling habilitado - puede causar recargas frecuentes" -ForegroundColor Yellow
    } else {
        Write-Host "✅ Polling deshabilitado - configuración correcta" -ForegroundColor Green
    }
    
    if ($viteConfig -match "overlay.*false") {
        Write-Host "✅ Error overlay deshabilitado" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Error overlay podría estar causando problemas" -ForegroundColor Yellow
    }
}

# Verificar archivos problemáticos
Write-Host ""
Write-Host "📁 5. VERIFICACIÓN DE ARCHIVOS" -ForegroundColor Yellow

$apiFile = Test-Path "frontend\src\services\api.ts"
Write-Host "API Service: $(if ($apiFile) { '✅ Existe' } else { '❌ No encontrado' })" -ForegroundColor $(if ($apiFile) { 'Green' } else { 'Red' })

if ($apiFile) {
    try {
        $apiContent = Get-Content "frontend\src\services\api.ts" -Raw
        if ($apiContent -match "PackfyAutoConfig") {
            Write-Host "✅ Sistema auto-configurante detectado" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Sistema auto-configurante no detectado" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Error leyendo archivo API" -ForegroundColor Red
    }
}

# Recomendaciones específicas
Write-Host ""
Write-Host "💡 6. RECOMENDACIONES ESPECÍFICAS" -ForegroundColor Yellow

Write-Host "Para solucionar los problemas reportados:" -ForegroundColor Cyan

Write-Host ""
Write-Host "🔧 Problema: Error en .178 (red local)" -ForegroundColor Yellow
Write-Host "   Solución: Usar localhost en lugar de IP local para desarrollo" -ForegroundColor Green
Write-Host "   URL recomendada: http://localhost:5173" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 Problema: Página se actualiza constantemente" -ForegroundColor Yellow
Write-Host "   Causa probable: HMR (Hot Module Replacement) o errores de compilación" -ForegroundColor Cyan
Write-Host "   Solución: Reiniciar frontend con cache limpio" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 Problema: Login no funciona" -ForegroundColor Yellow
Write-Host "   Verificar: Configuración de CORS y rutas de API" -ForegroundColor Cyan
Write-Host "   Solución: Usar proxy en localhost para evitar CORS" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 COMANDOS RECOMENDADOS:" -ForegroundColor Green
Write-Host "   1. Limpiar cache: npm run build; Remove-Item frontend\dist -Recurse -Force" -ForegroundColor White
Write-Host "   2. Reiniciar todo: .\inicio-robusto.ps1" -ForegroundColor White
Write-Host "   3. Usar localhost: http://localhost:5173" -ForegroundColor White

Write-Host ""
Read-Host "Presiona Enter para continuar"
