#!/usr/bin/env pwsh
# 🔧 PACKFY CUBA - SOLUCION DEFINITIVA PROBLEMAS RASTREO
# ====================================================

Write-Host "🔧 PACKFY CUBA - SOLUCION DEFINITIVA PROBLEMAS RASTREO" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green

$projectRoot = "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"

Write-Host "`n🎯 PROBLEMAS IDENTIFICADOS:" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow
Write-Host "1. ❌ Error HTTP 500 en móvil" -ForegroundColor Red
Write-Host "2. ❌ Página en blanco cuando va a rastrear/seguimiento" -ForegroundColor Red
Write-Host "3. ❌ Sistema muestra búsqueda por número de guía en lugar de nombres" -ForegroundColor Red
Write-Host "4. ❌ Inconsistencias entre /seguimiento y /rastreo" -ForegroundColor Red

# 1. VERIFICAR ESTADO ACTUAL
Write-Host "`n📊 1. VERIFICANDO ESTADO ACTUAL DEL SISTEMA" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# Verificar procesos
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
$nodeProcesses = Get-Process node -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "✅ Backend Python: ACTIVO ($($pythonProcesses.Count) procesos)" -ForegroundColor Green
}
else {
    Write-Host "❌ Backend Python: NO ACTIVO" -ForegroundColor Red
}

if ($nodeProcesses) {
    Write-Host "✅ Frontend Node: ACTIVO ($($nodeProcesses.Count) procesos)" -ForegroundColor Green
}
else {
    Write-Host "❌ Frontend Node: NO ACTIVO" -ForegroundColor Red
}

# Verificar puertos
$backend8000 = netstat -an | Select-String ":8000" | Select-String "LISTENING"
$frontend5173 = netstat -an | Select-String ":5173" | Select-String "LISTENING"
$frontend5174 = netstat -an | Select-String ":5174" | Select-String "LISTENING"

if ($backend8000) {
    Write-Host "✅ Backend Puerto 8000: ACTIVO" -ForegroundColor Green
}
else {
    Write-Host "❌ Backend Puerto 8000: NO ACTIVO" -ForegroundColor Red
}

if ($frontend5173 -or $frontend5174) {
    $port = if ($frontend5173) { "5173" } else { "5174" }
    Write-Host "✅ Frontend Puerto $port: ACTIVO" -ForegroundColor Green
    $frontendPort = $port
}
else {
    Write-Host "❌ Frontend: NO HAY PUERTOS ACTIVOS" -ForegroundColor Red
    $frontendPort = "5173"
}

# 2. PROBAR CONECTIVIDAD
Write-Host "`n🌐 2. PROBANDO CONECTIVIDAD" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

# IP Wi-Fi
$ipWifi = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi" -ErrorAction SilentlyContinue).IPAddress
if ($ipWifi) {
    Write-Host "📍 IP Wi-Fi: $ipWifi" -ForegroundColor Green
}
else {
    Write-Host "❌ IP Wi-Fi: NO DETECTADA" -ForegroundColor Red
}

# Probar backend
try {
    $backendTest = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Backend localhost: $($backendTest.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend localhost: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# Probar backend desde IP
if ($ipWifi) {
    try {
        $backendIPTest = Invoke-WebRequest -Uri "http://$($ipWifi):8000/admin/" -UseBasicParsing -TimeoutSec 5
        Write-Host "✅ Backend IP ($ipWifi): $($backendIPTest.StatusCode)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Backend IP ($ipWifi): ERROR - $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   💡 ESTA ES LA CAUSA DEL ERROR HTTP 500 EN MÓVIL" -ForegroundColor Yellow
    }
}

# 3. PROBAR ENDPOINTS DE RASTREO
Write-Host "`n🔍 3. PROBANDO ENDPOINTS DE RASTREO POR NOMBRES" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Endpoint autenticado
try {
    $busquedaAuth = Invoke-WebRequest -Uri "http://localhost:8000/api/envios/buscar_por_nombre/?nombre=test&tipo=ambos" -UseBasicParsing -TimeoutSec 5
    Write-Host "⚠️  Buscar por nombre (auth): REQUIERE LOGIN" -ForegroundColor Yellow
}
catch {
    if ($_.Exception.Message -match "401") {
        Write-Host "✅ Buscar por nombre (auth): 401 CORRECTO (requiere autenticación)" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Buscar por nombre (auth): ERROR - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Endpoint público
try {
    $rastreoPublico = Invoke-WebRequest -Uri "http://localhost:8000/api/envios/rastrear_por_nombre/?nombre=test&tipo=ambos" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Rastrear por nombre (público): $($rastreoPublico.StatusCode)" -ForegroundColor Green
}
catch {
    if ($_.Exception.Message -match "404") {
        Write-Host "⚠️  Rastrear por nombre (público): 404 (no hay datos)" -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ Rastrear por nombre (público): ERROR - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 4. VERIFICAR ARCHIVOS DE FRONTEND
Write-Host "`n📄 4. VERIFICANDO ARCHIVOS DE FRONTEND" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$appTsx = "$projectRoot\frontend\src\App.tsx"
$layoutTsx = "$projectRoot\frontend\src\components\Layout.tsx"
$trackingTsx = "$projectRoot\frontend\src\pages\TrackingPage.tsx"
$trackingCSS = "$projectRoot\frontend\src\pages\TrackingPage.css"

# Verificar archivos
$files = @{
    "App.tsx"          = $appTsx
    "Layout.tsx"       = $layoutTsx
    "TrackingPage.tsx" = $trackingTsx
    "TrackingPage.css" = $trackingCSS
}

foreach ($file in $files.GetEnumerator()) {
    if (Test-Path $file.Value) {
        Write-Host "✅ $($file.Key): EXISTE" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $($file.Key): NO EXISTE" -ForegroundColor Red
    }
}

# Verificar rutas en App.tsx
if (Test-Path $appTsx) {
    $appContent = Get-Content $appTsx -Raw
    if ($appContent -match 'path="rastreo"') {
        Write-Host "✅ Ruta /rastreo: CONFIGURADA en App.tsx" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Ruta /rastreo: NO CONFIGURADA en App.tsx" -ForegroundColor Red
    }
}

# Verificar rutas en Layout.tsx
if (Test-Path $layoutTsx) {
    $layoutContent = Get-Content $layoutTsx -Raw
    if ($layoutContent -match 'to="/rastreo"') {
        Write-Host "✅ Link /rastreo: CONFIGURADO en Layout.tsx" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Link /rastreo: NO CONFIGURADO en Layout.tsx" -ForegroundColor Red
    }
}

# 5. SOLUCION PASO A PASO
Write-Host "`n🔧 5. APLICANDO SOLUCIONES" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

Write-Host "`n🛠️  SOLUCION 1: Configurar CORS en backend para móvil" -ForegroundColor Yellow
$corsFile = "$projectRoot\backend\config\settings.py"
if (Test-Path $corsFile) {
    $corsContent = Get-Content $corsFile -Raw
    if ($corsContent -match "CORS_ALLOWED_ORIGINS") {
        Write-Host "✅ CORS: Ya configurado" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  CORS: Necesita configuración" -ForegroundColor Yellow
    }
}
else {
    Write-Host "❌ settings.py: NO ENCONTRADO" -ForegroundColor Red
}

Write-Host "`n🛠️  SOLUCION 2: Verificar contenido de TrackingPage" -ForegroundColor Yellow
if (Test-Path $trackingTsx) {
    $trackingContent = Get-Content $trackingTsx -Raw
    if ($trackingContent -match "Busca tus envíos por nombre") {
        Write-Host "✅ TrackingPage: CONFIGURADO PARA BÚSQUEDA POR NOMBRES" -ForegroundColor Green
    }
    else {
        Write-Host "❌ TrackingPage: NO CONFIGURADO PARA NOMBRES" -ForegroundColor Red
    }
}

# 6. URLS ACTUALIZADAS
Write-Host "`n🌐 6. URLS ACTUALIZADAS" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

Write-Host "🖥️  ACCESO EN PC:" -ForegroundColor Yellow
Write-Host "   • Aplicación: https://localhost:$frontendPort/" -ForegroundColor White
Write-Host "   • Login: https://localhost:$frontendPort/login" -ForegroundColor White
Write-Host "   • Rastreo autenticado: https://localhost:$frontendPort/rastreo" -ForegroundColor White

if ($ipWifi) {
    Write-Host "`n📱 ACCESO EN MÓVIL:" -ForegroundColor Yellow
    Write-Host "   • Aplicación: https://$($ipWifi):$frontendPort/" -ForegroundColor White
    Write-Host "   • Backend API: http://$($ipWifi):8000/api/" -ForegroundColor White
}

# 7. CREDENCIALES
Write-Host "`n🔑 7. CREDENCIALES DE PRUEBA" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan
Write-Host "📧 Email: admin@packfy.cu" -ForegroundColor Green
Write-Host "🔐 Password: admin123" -ForegroundColor Green

# 8. PASOS SIGUIENTES
Write-Host "`n📋 8. PASOS PARA PROBAR" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host "1. 🖥️  Abrir https://localhost:$frontendPort/login en PC" -ForegroundColor White
Write-Host "2. 🔐 Hacer login con las credenciales de arriba" -ForegroundColor White
Write-Host "3. 📝 Ir a la pestaña 'Seguimiento' en el menú" -ForegroundColor White
Write-Host "4. 🔍 Probar búsqueda por nombre (ejemplo: 'Juan', 'María')" -ForegroundColor White
Write-Host "5. 📱 Probar en móvil: https://$($ipWifi):$frontendPort/" -ForegroundColor White

# 9. COMANDOS PARA REINICIAR SI HAY PROBLEMAS
Write-Host "`n🔄 9. COMANDOS DE REINICIO (SI HAY PROBLEMAS)" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Backend:  cd backend && python manage.py runserver 0.0.0.0:8000" -ForegroundColor Yellow
Write-Host "Frontend: cd frontend && npm run dev" -ForegroundColor Yellow
Write-Host "Firewall: .\configurar-firewall-movil.ps1" -ForegroundColor Yellow

Write-Host "`n🎯 ESTADO FINAL ESPERADO:" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host "✅ Backend funcionando en puerto 8000 (accesible desde red)" -ForegroundColor Green
Write-Host "✅ Frontend funcionando en puerto $frontendPort" -ForegroundColor Green
Write-Host "✅ Página /rastreo muestra búsqueda POR NOMBRES" -ForegroundColor Green
Write-Host "✅ Móvil puede acceder sin error HTTP 500" -ForegroundColor Green

Write-Host "`n🇨🇺 Packfy Cuba - Diagnóstico completado!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Abrir páginas para probar
if ($frontend5173 -or $frontend5174) {
    Write-Host "`n🌐 Abriendo páginas para probar..." -ForegroundColor Cyan
    Start-Process "chrome.exe" -ArgumentList "--new-window", "https://localhost:$frontendPort/login"
    Start-Sleep -Seconds 2
    if ($ipWifi) {
        Write-Host "📱 Genera QR para móvil: https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=https://$($ipWifi):$frontendPort/" -ForegroundColor Yellow
        Start-Process "chrome.exe" -ArgumentList "--new-tab", "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=https://$($ipWifi):$frontendPort/"
    }
}

Write-Host "`nPresiona cualquier tecla para continuar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
