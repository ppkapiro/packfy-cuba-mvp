#!/usr/bin/env pwsh
# Script de inicio robusto para Packfy Cuba MVP
# Versión con proxy inteligente y manejo de errores mejorado

Write-Host "🚀 PACKFY CUBA MVP - INICIO ROBUSTO" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Función para verificar si un puerto está en uso
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    } catch {
        return $false
    }
}

# Función para detener procesos en un puerto específico
function Stop-ProcessOnPort {
    param([int]$Port)
    try {
        $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | ForEach-Object { Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue }
        if ($processes) {
            Write-Host "🛑 Deteniendo procesos en puerto $Port..." -ForegroundColor Yellow
            $processes | ForEach-Object { 
                Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
                Write-Host "  ✅ Proceso $($_.ProcessName) (PID: $($_.Id)) detenido" -ForegroundColor Green
            }
            Start-Sleep -Seconds 2
        }
    } catch {
        Write-Host "  ⚠️ No se pudieron detener algunos procesos en puerto $Port" -ForegroundColor Yellow
    }
}

# Verificar directorio del proyecto
if (-not (Test-Path "frontend") -or -not (Test-Path "backend")) {
    Write-Host "❌ Error: No se encontraron los directorios frontend o backend" -ForegroundColor Red
    Write-Host "   Asegúrate de ejecutar este script desde el directorio raíz del proyecto" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "📁 Verificando estructura del proyecto..." -ForegroundColor Green
Write-Host "  ✅ Frontend: $(Test-Path 'frontend')" -ForegroundColor Green
Write-Host "  ✅ Backend: $(Test-Path 'backend')" -ForegroundColor Green

# Limpiar puertos si están ocupados
Write-Host "🧹 Limpiando puertos..." -ForegroundColor Yellow
if (Test-Port 8000) { Stop-ProcessOnPort 8000 }
if (Test-Port 5173) { Stop-ProcessOnPort 5173 }

# Configurar variables de entorno para desarrollo
$env:NODE_ENV = "development"
$env:VITE_API_BASE_URL = ""  # Usar proxy en desarrollo

# Obtener IP local para acceso móvil
try {
    $ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress | Select-Object -First 1
    if (-not $ip) {
        $ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "10.*" }).IPAddress | Select-Object -First 1
    }
    if ($ip) {
        Write-Host "📱 IP Local detectada: $ip" -ForegroundColor Cyan
        Write-Host "   Acceso móvil: http://$ip:5173" -ForegroundColor Cyan
    }
} catch {
    Write-Host "⚠️ No se pudo detectar IP local automáticamente" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 INICIANDO BACKEND (Django)..." -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Magenta

# Iniciar backend en una nueva ventana de PowerShell
$backendScript = @"
Write-Host '🐍 Configurando entorno Python...' -ForegroundColor Green
Set-Location '$PWD\backend'

# Verificar si manage.py existe
if (-not (Test-Path 'manage.py')) {
    Write-Host '❌ Error: manage.py no encontrado en backend' -ForegroundColor Red
    Read-Host 'Presiona Enter para salir'
    exit 1
}

Write-Host '🚀 Iniciando servidor Django en puerto 8000...' -ForegroundColor Green
Write-Host '📍 Backend URL: http://localhost:8000' -ForegroundColor Cyan
Write-Host '📚 Admin URL: http://localhost:8000/admin' -ForegroundColor Cyan
Write-Host ''
Write-Host '⚠️  Para detener el servidor presiona Ctrl+C' -ForegroundColor Yellow
Write-Host '================================================' -ForegroundColor Cyan

try {
    python manage.py runserver 0.0.0.0:8000
} catch {
    Write-Host '❌ Error al iniciar Django. Verificando Python...' -ForegroundColor Red
    python --version
    Read-Host 'Presiona Enter para salir'
}
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

# Esperar a que el backend se inicie
Write-Host "⏳ Esperando a que el backend se inicie..." -ForegroundColor Yellow
$maxWait = 30
$waited = 0
do {
    Start-Sleep -Seconds 1
    $waited++
    Write-Progress -Activity "Esperando backend" -Status "Verificando puerto 8000..." -PercentComplete (($waited / $maxWait) * 100)
} while (-not (Test-Port 8000) -and $waited -lt $maxWait)

if (Test-Port 8000) {
    Write-Host "✅ Backend iniciado correctamente en puerto 8000" -ForegroundColor Green
} else {
    Write-Host "⚠️ Backend tardando en iniciar, continuando con frontend..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 INICIANDO FRONTEND (React + Vite)..." -ForegroundColor Magenta
Write-Host "======================================" -ForegroundColor Magenta

# Verificar que node_modules existe
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "📦 Instalando dependencias del frontend..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    Set-Location ..
}

# Iniciar frontend
$frontendScript = @"
Write-Host '⚛️ Configurando entorno React...' -ForegroundColor Green
Set-Location '$PWD\frontend'

# Verificar package.json
if (-not (Test-Path 'package.json')) {
    Write-Host '❌ Error: package.json no encontrado en frontend' -ForegroundColor Red
    Read-Host 'Presiona Enter para salir'
    exit 1
}

Write-Host '🚀 Iniciando servidor Vite en puerto 5173...' -ForegroundColor Green
Write-Host '🌐 Frontend URL: http://localhost:5173' -ForegroundColor Cyan
if ('$ip' -ne '') {
    Write-Host '📱 Móvil URL: http://$ip:5173' -ForegroundColor Cyan
}
Write-Host '🔗 Proxy configurado: /api → http://localhost:8000' -ForegroundColor Green
Write-Host ''
Write-Host '⚠️  Para detener el servidor presiona Ctrl+C' -ForegroundColor Yellow
Write-Host '================================================' -ForegroundColor Cyan

try {
    npm run dev
} catch {
    Write-Host '❌ Error al iniciar Vite. Verificando Node.js...' -ForegroundColor Red
    node --version
    npm --version
    Read-Host 'Presiona Enter para salir'
}
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

# Esperar a que el frontend se inicie
Write-Host "⏳ Esperando a que el frontend se inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

$maxWait = 20
$waited = 0
do {
    Start-Sleep -Seconds 1
    $waited++
    Write-Progress -Activity "Esperando frontend" -Status "Verificando puerto 5173..." -PercentComplete (($waited / $maxWait) * 100)
} while (-not (Test-Port 5173) -and $waited -lt $maxWait)

Write-Host ""
Write-Host "🎉 PACKFY CUBA MVP INICIADO" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "🔧 Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 Admin:    http://localhost:8000/admin" -ForegroundColor Cyan

if ($ip) {
    Write-Host ""
    Write-Host "📱 ACCESO MÓVIL:" -ForegroundColor Magenta
    Write-Host "   http://$ip:5173" -ForegroundColor Cyan
    Write-Host "   (Conecta tu móvil a la misma red WiFi)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 CONFIGURACIÓN ACTIVA:" -ForegroundColor Magenta
Write-Host "   ✅ Proxy: /api → http://localhost:8000" -ForegroundColor Green
Write-Host "   ✅ CORS configurado para desarrollo" -ForegroundColor Green
Write-Host "   ✅ Timeout: 30 segundos" -ForegroundColor Green
Write-Host "   ✅ Auto-reconexión habilitada" -ForegroundColor Green

Write-Host ""
Write-Host "⚠️  Para detener ambos servidores:" -ForegroundColor Yellow
Write-Host "   Presiona Ctrl+C en ambas ventanas" -ForegroundColor Yellow

# Intentar abrir el navegador
Start-Sleep -Seconds 3
try {
    if (Test-Port 5173) {
        Write-Host "🌍 Abriendo navegador..." -ForegroundColor Green
        Start-Process "http://localhost:5173"
    }
} catch {
    Write-Host "⚠️ No se pudo abrir el navegador automáticamente" -ForegroundColor Yellow
    Write-Host "   Abre manualmente: http://localhost:5173" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "✅ Sistema iniciado correctamente" -ForegroundColor Green
Write-Host "📊 Monitorea las ventanas de backend y frontend para logs" -ForegroundColor Cyan

Read-Host "Presiona Enter para salir de este script (los servidores seguirán ejecutándose)"
