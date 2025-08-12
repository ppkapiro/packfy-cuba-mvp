#!/usr/bin/env pwsh
# Script de diagnóstico de conectividad para Packfy Cuba MVP

Write-Host "🔍 DIAGNÓSTICO DE CONECTIVIDAD PACKFY" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Función para verificar puerto
function Test-Port {
    param([string]$HostAddress, [int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect($HostAddress, $Port)
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
            Content = $response.Content.Substring(0, [Math]::Min(200, $response.Content.Length))
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

Write-Host "Backend (8000):  $(if ($backend8000) { '✅ ACTIVO' } else { '❌ INACTIVO' })" -ForegroundColor $(if ($backend8000) { 'Green' } else { 'Red' })
Write-Host "Frontend (5173): $(if ($frontend5173) { '✅ ACTIVO' } else { '❌ INACTIVO' })" -ForegroundColor $(if ($frontend5173) { 'Green' } else { 'Red' })

Write-Host ""
Write-Host "📡 2. PRUEBAS DE CONECTIVIDAD HTTP" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

# Probar endpoints del backend
if ($backend8000) {
    Write-Host "🔧 Probando backend directo..." -ForegroundColor Cyan
    
    $adminTest = Test-HttpEndpoint -Url "http://localhost:8000/admin/"
    Write-Host "Admin (http://localhost:8000/admin/): $(if ($adminTest.Success) { "✅ OK ($($adminTest.StatusCode))" } else { "❌ Error: $($adminTest.Error)" })" -ForegroundColor $(if ($adminTest.Success) { 'Green' } else { 'Red' })
    
    $apiTest = Test-HttpEndpoint -Url "http://localhost:8000/api/"
    Write-Host "API Root (http://localhost:8000/api/): $(if ($apiTest.Success) { "✅ OK ($($apiTest.StatusCode))" } else { "❌ Error: $($apiTest.Error)" })" -ForegroundColor $(if ($apiTest.Success) { 'Green' } else { 'Red' })
} else {
    Write-Host "❌ Backend no disponible - no se pueden probar endpoints" -ForegroundColor Red
}

# Probar frontend y proxy
if ($frontend5173) {
    Write-Host ""
    Write-Host "⚛️ Probando frontend y proxy..." -ForegroundColor Cyan
    
    $frontendTest = Test-HttpEndpoint -Url "http://localhost:5173/"
    Write-Host "Frontend (http://localhost:5173/): $(if ($frontendTest.Success) { "✅ OK ($($frontendTest.StatusCode))" } else { "❌ Error: $($frontendTest.Error)" })" -ForegroundColor $(if ($frontendTest.Success) { 'Green' } else { 'Red' })
    
    if ($backend8000) {
        $proxyTest = Test-HttpEndpoint -Url "http://localhost:5173/api/"
        Write-Host "Proxy (http://localhost:5173/api/): $(if ($proxyTest.Success) { "✅ OK ($($proxyTest.StatusCode))" } else { "❌ Error: $($proxyTest.Error)" })" -ForegroundColor $(if ($proxyTest.Success) { 'Green' } else { 'Red' })
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
    $localIPs = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } | Select-Object IPAddress, InterfaceAlias
    if ($localIPs) {
        Write-Host "IPs locales disponibles:" -ForegroundColor Cyan
        foreach ($ip in $localIPs) {
            Write-Host "  📍 $($ip.IPAddress) ($($ip.InterfaceAlias))" -ForegroundColor Green
            if ($frontend5173 -and ($ip.IPAddress -like "192.168.*" -or $ip.IPAddress -like "10.*")) {
                Write-Host "     📱 Acceso móvil: http://$($ip.IPAddress):5173" -ForegroundColor Cyan
            }
        }
    } else {
        Write-Host "⚠️ No se encontraron IPs locales válidas" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error obteniendo información de red: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔧 4. VERIFICACIÓN DE CONFIGURACIÓN" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

# Verificar archivos de configuración
$viteConfig = Test-Path "frontend\vite.config.ts"
$packageJson = Test-Path "frontend\package.json"
$manageWpy = Test-Path "backend\manage.py"

Write-Host "Vite Config: $(if ($viteConfig) { '✅ Existe' } else { '❌ No encontrado' })" -ForegroundColor $(if ($viteConfig) { 'Green' } else { 'Red' })
Write-Host "Package.json: $(if ($packageJson) { '✅ Existe' } else { '❌ No encontrado' })" -ForegroundColor $(if ($packageJson) { 'Green' } else { 'Red' })
Write-Host "Manage.py: $(if ($manageWpy) { '✅ Existe' } else { '❌ No encontrado' })" -ForegroundColor $(if ($manageWpy) { 'Green' } else { 'Red' })

# Verificar contenido de vite.config.ts
if ($viteConfig) {
    Write-Host ""
    Write-Host "🔍 Configuración del proxy en vite.config.ts:" -ForegroundColor Cyan
    try {
        $viteContent = Get-Content "frontend\vite.config.ts" -Raw
        if ($viteContent -match "proxy.*api") {
            Write-Host "✅ Proxy configurado correctamente" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Proxy no detectado en la configuración" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Error leyendo vite.config.ts" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📋 5. RESUMEN Y RECOMENDACIONES" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

$issues = @()
$recommendations = @()

if (-not $backend8000) {
    $issues += "Backend (puerto 8000) no está ejecutándose"
    $recommendations += "Ejecutar: cd backend && python manage.py runserver"
}

if (-not $frontend5173) {
    $issues += "Frontend (puerto 5173) no está ejecutándose"
    $recommendations += "Ejecutar: cd frontend && npm run dev"
}

if (-not $viteConfig) {
    $issues += "Archivo vite.config.ts no encontrado"
    $recommendations += "Verificar estructura del proyecto frontend"
}

if ($issues.Count -eq 0) {
    Write-Host "🎉 ¡TODO ESTÁ FUNCIONANDO CORRECTAMENTE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "URLs disponibles:" -ForegroundColor Cyan
    Write-Host "  🌐 Frontend: http://localhost:5173" -ForegroundColor Green
    Write-Host "  🔧 Backend: http://localhost:8000" -ForegroundColor Green
    Write-Host "  📚 Admin: http://localhost:8000/admin" -ForegroundColor Green
    
    if ($localIPs) {
        $mobileIP = $localIPs | Where-Object { $_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" } | Select-Object -First 1
        if ($mobileIP) {
            Write-Host "  📱 Móvil: http://$($mobileIP.IPAddress):5173" -ForegroundColor Green
        }
    }
} else {
    Write-Host "❌ PROBLEMAS DETECTADOS:" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  • $issue" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "💡 RECOMENDACIONES:" -ForegroundColor Yellow
    foreach ($rec in $recommendations) {
        Write-Host "  • $rec" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "🚀 Para un inicio automático, ejecuta:" -ForegroundColor Cyan
    Write-Host "   .\inicio-robusto.ps1" -ForegroundColor Green
}

Write-Host ""
Read-Host "Presiona Enter para salir"
