#!/usr/bin/env pwsh
# Script de diagnóstico de conectividad para Packfy Cuba MVP

Write-Host "🔍 DIAGNÓSTICO DE CONECTIVIDAD PACKFY" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Función para verificar puerto
function Test-Port {
    param([string]$HostName, [int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect($HostName, $Port)
        $connection.Close()
        return $true
    } catch {
        return $false
    }
}

# Función para hacer petición HTTP
function Test-HttpEndpoint {
    param([string]$Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -Method GET -TimeoutSec 10 -UseBasicParsing
        return @{
            Success = $true
            StatusCode = $response.StatusCode
        }
    } catch {
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

Write-Host "📊 1. VERIFICACIÓN DE PUERTOS" -ForegroundColor Yellow
Write-Host "==============================" -ForegroundColor Yellow

$backend8000 = Test-Port -HostName "localhost" -Port 8000
$frontend5173 = Test-Port -HostName "localhost" -Port 5173

Write-Host "Backend (8000): " -NoNewline
if ($backend8000) { Write-Host "✅ ACTIVO" -ForegroundColor Green } else { Write-Host "❌ INACTIVO" -ForegroundColor Red }

Write-Host "Frontend (5173): " -NoNewline
if ($frontend5173) { Write-Host "✅ ACTIVO" -ForegroundColor Green } else { Write-Host "❌ INACTIVO" -ForegroundColor Red }

Write-Host ""
Write-Host "📡 2. PRUEBAS DE CONECTIVIDAD HTTP" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

# Probar endpoints del backend
if ($backend8000) {
    Write-Host "🔧 Probando backend directo..." -ForegroundColor Cyan
    
    $adminTest = Test-HttpEndpoint -Url "http://localhost:8000/admin/"
    Write-Host "Admin: " -NoNewline
    if ($adminTest.Success) { 
        Write-Host "✅ OK ($($adminTest.StatusCode))" -ForegroundColor Green 
    } else { 
        Write-Host "❌ Error: $($adminTest.Error)" -ForegroundColor Red 
    }
    
    $apiTest = Test-HttpEndpoint -Url "http://localhost:8000/api/"
    Write-Host "API Root: " -NoNewline
    if ($apiTest.Success) { 
        Write-Host "✅ OK ($($apiTest.StatusCode))" -ForegroundColor Green 
    } else { 
        Write-Host "❌ Error: $($apiTest.Error)" -ForegroundColor Red 
    }
} else {
    Write-Host "❌ Backend no disponible - no se pueden probar endpoints" -ForegroundColor Red
}

# Probar frontend y proxy
if ($frontend5173) {
    Write-Host ""
    Write-Host "⚛️ Probando frontend y proxy..." -ForegroundColor Cyan
    
    $frontendTest = Test-HttpEndpoint -Url "http://localhost:5173/"
    Write-Host "Frontend: " -NoNewline
    if ($frontendTest.Success) { 
        Write-Host "✅ OK ($($frontendTest.StatusCode))" -ForegroundColor Green 
    } else { 
        Write-Host "❌ Error: $($frontendTest.Error)" -ForegroundColor Red 
    }
    
    if ($backend8000) {
        $proxyTest = Test-HttpEndpoint -Url "http://localhost:5173/api/"
        Write-Host "Proxy: " -NoNewline
        if ($proxyTest.Success) { 
            Write-Host "✅ OK ($($proxyTest.StatusCode))" -ForegroundColor Green 
        } else { 
            Write-Host "❌ Error: $($proxyTest.Error)" -ForegroundColor Red 
        }
    } else {
        Write-Host "Proxy: ⚠️ No se puede probar (backend inactivo)" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Frontend no disponible - no se pueden probar endpoints" -ForegroundColor Red
}

Write-Host ""
Write-Host "🌐 3. INFORMACIÓN DE RED" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow

# Obtener IP local
try {
    $localIPs = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" }
    if ($localIPs) {
        Write-Host "IPs locales disponibles:" -ForegroundColor Cyan
        foreach ($ip in $localIPs) {
            Write-Host "  📍 $($ip.IPAddress)" -ForegroundColor Green
            if ($frontend5173 -and ($ip.IPAddress -like "192.168.*" -or $ip.IPAddress -like "10.*")) {
                Write-Host "     📱 Acceso móvil: http://$($ip.IPAddress):5173" -ForegroundColor Cyan
            }
        }
    } else {
        Write-Host "⚠️ No se encontraron IPs locales válidas" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error obteniendo información de red" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔧 4. VERIFICACIÓN DE CONFIGURACIÓN" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

# Verificar archivos de configuración
$viteConfig = Test-Path "frontend\vite.config.ts"
$packageJson = Test-Path "frontend\package.json"
$managePy = Test-Path "backend\manage.py"

Write-Host "Vite Config: " -NoNewline
if ($viteConfig) { Write-Host "✅ Existe" -ForegroundColor Green } else { Write-Host "❌ No encontrado" -ForegroundColor Red }

Write-Host "Package.json: " -NoNewline
if ($packageJson) { Write-Host "✅ Existe" -ForegroundColor Green } else { Write-Host "❌ No encontrado" -ForegroundColor Red }

Write-Host "Manage.py: " -NoNewline
if ($managePy) { Write-Host "✅ Existe" -ForegroundColor Green } else { Write-Host "❌ No encontrado" -ForegroundColor Red }

Write-Host ""
Write-Host "📋 5. RESUMEN Y RECOMENDACIONES" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

$issues = @()

if (-not $backend8000) {
    $issues += "Backend (puerto 8000) no está ejecutándose"
}

if (-not $frontend5173) {
    $issues += "Frontend (puerto 5173) no está ejecutándose"
}

if (-not $viteConfig) {
    $issues += "Archivo vite.config.ts no encontrado"
}

if ($issues.Count -eq 0) {
    Write-Host "🎉 ¡TODO ESTÁ FUNCIONANDO CORRECTAMENTE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "URLs disponibles:" -ForegroundColor Cyan
    Write-Host "  🌐 Frontend: http://localhost:5173" -ForegroundColor Green
    Write-Host "  🔧 Backend: http://localhost:8000" -ForegroundColor Green
    Write-Host "  📚 Admin: http://localhost:8000/admin" -ForegroundColor Green
} else {
    Write-Host "❌ PROBLEMAS DETECTADOS:" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  • $issue" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "💡 RECOMENDACIONES:" -ForegroundColor Yellow
    Write-Host "  • Ejecutar: .\inicio-robusto.ps1" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Presiona Enter para salir"
