#!/usr/bin/env pwsh
# Reset completo del proyecto Packfy Cuba MVP
# Este script limpia y reinicia todo el proyecto desde cero

Write-Host "🔄 INICIANDO RESET COMPLETO DEL PROYECTO PACKFY CUBA" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# 1. Detener todos los procesos
Write-Host "🛑 Deteniendo procesos existentes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "node" -or $_.ProcessName -eq "python"} | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Limpiar puertos
Write-Host "🧹 Limpiando puertos..." -ForegroundColor Yellow
$ports = @(5173, 5174, 8000, 3000)
foreach ($port in $ports) {
    $processes = netstat -ano | findstr ":$port"
    if ($processes) {
        Write-Host "   Limpiando puerto $port"
        $processIds = ($processes | ForEach-Object { ($_ -split '\s+')[-1] }) | Where-Object { $_ -ne "0" -and $_ -ne "" } | Sort-Object -Unique
        foreach ($procesId in $processIds) {
            taskkill /PID $procesId /F 2>$null
        }
    }
}

# 3. Configurar Backend
Write-Host "🗄️ Configurando Backend Django..." -ForegroundColor Cyan
Set-Location backend

# Verificar que Python esté disponible
try {
    python --version
} catch {
    Write-Host "❌ Error: Python no está instalado o no está en PATH" -ForegroundColor Red
    exit 1
}

# Instalar dependencias del backend
Write-Host "   📦 Instalando dependencias de Python..."
pip install -r requirements.txt

# Limpiar y recrear base de datos
Write-Host "   🗃️ Recreando base de datos..."
if (Test-Path "db.sqlite3") {
    Remove-Item "db.sqlite3" -Force
}

# Aplicar migraciones
Write-Host "   🔄 Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Crear usuarios de prueba
Write-Host "   👥 Creando usuarios de prueba..."
python crear_usuarios.py

# 4. Configurar Frontend
Write-Host "🎨 Configurando Frontend React..." -ForegroundColor Cyan
Set-Location ../frontend

# Verificar que Node esté disponible
try {
    node --version
    npm --version
} catch {
    Write-Host "❌ Error: Node.js/npm no está instalado o no está en PATH" -ForegroundColor Red
    exit 1
}

# Limpiar cache y node_modules
Write-Host "   🧹 Limpiando cache de npm..."
if (Test-Path "node_modules") {
    Remove-Item "node_modules" -Recurse -Force
}
if (Test-Path "package-lock.json") {
    Remove-Item "package-lock.json" -Force
}
npm cache clean --force

# Instalar dependencias del frontend
Write-Host "   📦 Instalando dependencias de Node.js..."
npm install

# 5. Verificar configuraciones
Write-Host "⚙️ Verificando configuraciones..." -ForegroundColor Cyan

# Verificar configuración de Vite
$viteConfig = Get-Content "vite.config.ts" -Raw
if ($viteConfig -notmatch "localhost:8000") {
    Write-Host "   ⚠️ Configuración de proxy corregida" -ForegroundColor Yellow
}

# 6. Iniciar servicios
Write-Host "🚀 Iniciando servicios..." -ForegroundColor Green
Set-Location ../

# Crear scripts de inicio
$backendBat = @"
@echo off
echo Iniciando Backend Django...
cd backend
python manage.py runserver 0.0.0.0:8000
"@
$backendBat | Out-File -FilePath "start-backend.bat" -Encoding ASCII

$frontendBat = @"
@echo off
echo Iniciando Frontend React...
cd frontend
npm run dev
"@
$frontendBat | Out-File -FilePath "start-frontend.bat" -Encoding ASCII

# Iniciar backend en segundo plano
Write-Host "   🗄️ Iniciando Django en puerto 8000..."
Start-Process -FilePath "start-backend.bat" -WindowStyle Minimized

Start-Sleep -Seconds 5

# Iniciar frontend en segundo plano
Write-Host "   🎨 Iniciando React en puerto 5173..."
Start-Process -FilePath "start-frontend.bat" -WindowStyle Minimized

Start-Sleep -Seconds 5

# 7. Verificar que todo esté funcionando
Write-Host "🔍 Verificando servicios..." -ForegroundColor Green

$backendRunning = $false
$frontendRunning = $false

# Verificar backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/" -Method GET -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "   ✅ Backend funcionando en http://localhost:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Backend no responde" -ForegroundColor Red
}

# Verificar frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $frontendRunning = $true
        Write-Host "   ✅ Frontend funcionando en http://localhost:5173" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Frontend no responde" -ForegroundColor Red
}

# 8. Resumen final
Write-Host "`n🎉 RESET COMPLETO FINALIZADO" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

if ($backendRunning -and $frontendRunning) {
    Write-Host "✅ ESTADO: Proyecto funcionando correctamente" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 ACCEDE A LA APLICACIÓN:" -ForegroundColor Cyan
    Write-Host "   🖥️  Escritorio: http://localhost:5173" -ForegroundColor White
    Write-Host "   📱 Móvil: http://192.168.12.178:5173" -ForegroundColor White
    Write-Host ""
    Write-Host "🔑 CREDENCIALES DE PRUEBA:" -ForegroundColor Cyan
    Write-Host "   👤 Admin: admin@packfy.cu / admin123" -ForegroundColor White
    Write-Host "   🏢 Empresa: empresa@test.cu / empresa123" -ForegroundColor White
    Write-Host "   👥 Cliente: cliente@test.cu / cliente123" -ForegroundColor White
    Write-Host ""
    Write-Host "   🛠️ GESTIÓN:" -ForegroundColor Cyan
    Write-Host "   Para detener: ejecuta stop-all.ps1" -ForegroundColor White
    Write-Host "   Para reiniciar: ejecuta reset-completo.ps1" -ForegroundColor White
} else {
    Write-Host "❌ ESTADO: Hay problemas con el proyecto" -ForegroundColor Red
    Write-Host "   Revisa los logs de error arriba" -ForegroundColor Yellow
}

Write-Host "`nPresiona cualquier tecla para continuar..." -ForegroundColor Yellow
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null
