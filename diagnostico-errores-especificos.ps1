#!/usr/bin/env pwsh
# 🔧 PACKFY CUBA - DIAGNOSTICO ERRORES ESPECIFICOS
# ==============================================

Write-Host "🔧 PACKFY CUBA - DIAGNOSTICO ERRORES ESPECIFICOS" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

$projectRoot = "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"

# 1. VERIFICAR PROCESOS ACTIVOS
Write-Host "`n📊 1. VERIFICANDO PROCESOS ACTIVOS" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
$nodeProcesses = Get-Process node -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "✅ Python procesos: $($pythonProcesses.Count)" -ForegroundColor Green
    foreach ($proc in $pythonProcesses) {
        Write-Host "   📍 PID: $($proc.Id) - CPU: $($proc.CPU)" -ForegroundColor Cyan
    }
}
else {
    Write-Host "❌ No hay procesos Python activos" -ForegroundColor Red
}

if ($nodeProcesses) {
    Write-Host "✅ Node procesos: $($nodeProcesses.Count)" -ForegroundColor Green
    foreach ($proc in $nodeProcesses) {
        Write-Host "   📍 PID: $($proc.Id) - CPU: $($proc.CPU)" -ForegroundColor Cyan
    }
}
else {
    Write-Host "❌ No hay procesos Node activos" -ForegroundColor Red
}

# 2. VERIFICAR PUERTOS
Write-Host "`n📡 2. VERIFICANDO PUERTOS" -ForegroundColor Yellow
Write-Host "========================" -ForegroundColor Yellow

$backend8000 = netstat -an | Select-String ":8000" | Select-String "LISTENING"
$frontend5173 = netstat -an | Select-String ":5173" | Select-String "LISTENING"

if ($backend8000) {
    Write-Host "✅ Backend (8000): ACTIVO" -ForegroundColor Green
}
else {
    Write-Host "❌ Backend (8000): NO ACTIVO" -ForegroundColor Red
}

if ($frontend5173) {
    Write-Host "✅ Frontend (5173): ACTIVO" -ForegroundColor Green
}
else {
    Write-Host "❌ Frontend (5173): NO ACTIVO" -ForegroundColor Red
}

# 3. PROBAR CONECTIVIDAD LOCAL
Write-Host "`n🌐 3. PROBANDO CONECTIVIDAD LOCAL" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

# Backend local
try {
    $backendLocal = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Backend localhost: $($backendLocal.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend localhost: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# Frontend local
try {
    $frontendLocal = Invoke-WebRequest -Uri "https://localhost:5173/" -UseBasicParsing -SkipCertificateCheck -TimeoutSec 5
    Write-Host "✅ Frontend localhost: $($frontendLocal.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend localhost: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# 4. PROBAR CONECTIVIDAD MOVIL (IP DE RED)
Write-Host "`n📱 4. PROBANDO CONECTIVIDAD MOVIL" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

# Obtener IP de red Wi-Fi
$ipWifi = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi" -ErrorAction SilentlyContinue).IPAddress
if ($ipWifi) {
    Write-Host "📍 IP Wi-Fi detectada: $ipWifi" -ForegroundColor Cyan

    # Backend desde IP
    try {
        $backendIP = Invoke-WebRequest -Uri "http://$($ipWifi):8000/admin/" -UseBasicParsing -TimeoutSec 5
        Write-Host "✅ Backend IP ($ipWifi): $($backendIP.StatusCode)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Backend IP ($ipWifi): ERROR - $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   💡 Probable causa del error HTTP 500 en móvil" -ForegroundColor Yellow
    }

    # Frontend desde IP
    try {
        $frontendIP = Invoke-WebRequest -Uri "https://$($ipWifi):5173/" -UseBasicParsing -SkipCertificateCheck -TimeoutSec 5
        Write-Host "✅ Frontend IP ($ipWifi): $($frontendIP.StatusCode)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Frontend IP ($ipWifi): ERROR - $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   💡 Probable causa de la aplicación no visible en móvil" -ForegroundColor Yellow
    }
}
else {
    Write-Host "❌ No se pudo detectar IP Wi-Fi" -ForegroundColor Red
}

# 5. VERIFICAR ARCHIVOS DE CONFIGURACION
Write-Host "`n📄 5. VERIFICANDO ARCHIVOS DE CONFIGURACION" -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Yellow

$layoutFile = "$projectRoot\frontend\src\components\Layout.tsx"
$trackingPageFile = "$projectRoot\frontend\src\pages\TrackingPage.tsx"
$trackingCSSFile = "$projectRoot\frontend\src\pages\TrackingPage.css"

if (Test-Path $layoutFile) {
    Write-Host "✅ Layout.tsx existe" -ForegroundColor Green
}
else {
    Write-Host "❌ Layout.tsx NO encontrado" -ForegroundColor Red
}

if (Test-Path $trackingPageFile) {
    Write-Host "✅ TrackingPage.tsx existe" -ForegroundColor Green
}
else {
    Write-Host "❌ TrackingPage.tsx NO encontrado" -ForegroundColor Red
}

if (Test-Path $trackingCSSFile) {
    Write-Host "✅ TrackingPage.css existe" -ForegroundColor Green
}
else {
    Write-Host "❌ TrackingPage.css NO encontrado - CAUSA DE PAGINA EN BLANCO" -ForegroundColor Red
}

# 6. VERIFICAR RUTAS EN LAYOUT
Write-Host "`n🔗 6. VERIFICANDO RUTAS EN LAYOUT" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

if (Test-Path $layoutFile) {
    $layoutContent = Get-Content $layoutFile -Raw
    if ($layoutContent -match 'to="/rastreo"') {
        Write-Host "✅ Ruta /rastreo encontrada en Layout" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Ruta /rastreo NO encontrada en Layout" -ForegroundColor Red
    }

    if ($layoutContent -match 'to="/seguimiento"') {
        Write-Host "⚠️  Ruta /seguimiento encontrada (INCONSISTENCIA)" -ForegroundColor Yellow
    }
}

# 7. SUGERENCIAS DE SOLUCION
Write-Host "`n💡 7. SUGERENCIAS DE SOLUCION" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

Write-Host "`n🔧 PARA SOLUCIONAR ERROR HTTP 500 EN MOVIL:" -ForegroundColor Cyan
Write-Host "1. Asegurar que backend se ejecute con: python manage.py runserver 0.0.0.0:8000" -ForegroundColor White
Write-Host "2. Configurar firewall para permitir puerto 8000" -ForegroundColor White
Write-Host "3. Verificar CORS en Django settings" -ForegroundColor White

Write-Host "`n🔧 PARA SOLUCIONAR PAGINA EN BLANCO EN PC:" -ForegroundColor Cyan
Write-Host "1. Asegurar que TrackingPage.css existe y se importa" -ForegroundColor White
Write-Host "2. Verificar rutas /rastreo vs /seguimiento" -ForegroundColor White
Write-Host "3. Compilar frontend sin errores TypeScript" -ForegroundColor White

Write-Host "`n🔧 PARA SOLUCIONAR APLICACION NO VISIBLE EN MOVIL:" -ForegroundColor Cyan
Write-Host "1. Asegurar que frontend se ejecute con: npm run dev" -ForegroundColor White
Write-Host "2. Acceder a https://$($ipWifi):5173/ desde móvil" -ForegroundColor White
Write-Host "3. Aceptar certificado HTTPS inseguro en móvil" -ForegroundColor White

Write-Host "`n📋 8. COMANDOS PARA EJECUTAR:" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow
Write-Host "Backend:  cd backend && python manage.py runserver 0.0.0.0:8000" -ForegroundColor Green
Write-Host "Frontend: cd frontend && npm run dev" -ForegroundColor Green
Write-Host "Firewall: .\configurar-firewall-movil.ps1" -ForegroundColor Green

Write-Host "`n🎯 URLS PARA PROBAR:" -ForegroundColor Yellow
Write-Host "===================" -ForegroundColor Yellow
Write-Host "PC Local:  https://localhost:5173/" -ForegroundColor Green
Write-Host "Móvil:     https://$($ipWifi):5173/" -ForegroundColor Green
Write-Host "Backend:   http://$($ipWifi):8000/admin/" -ForegroundColor Green

Write-Host "`n🇨🇺 Packfy Cuba - Diagnóstico completado!" -ForegroundColor Green
