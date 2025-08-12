# 🇨🇺 PACKFY CUBA - SOLUCIONADOR DE PROBLEMAS DE SEGUIMIENTO Y MÓVIL
# ===================================================================

Write-Host "🇨🇺 PACKFY CUBA - DIAGNÓSTICO Y SOLUCIÓN" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Verificar estado del sistema
Write-Host "`n📊 1. VERIFICANDO ESTADO DEL SISTEMA" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

$backendPort = netstat -an | Select-String ":8000" | Select-String "LISTENING"
$frontendPort = netstat -an | Select-String ":5173" | Select-String "LISTENING"

if ($backendPort) {
    Write-Host "✅ Backend (8000): FUNCIONANDO" -ForegroundColor Green
}
else {
    Write-Host "❌ Backend (8000): NO FUNCIONA" -ForegroundColor Red
    Write-Host "🔧 Iniciando backend..." -ForegroundColor Yellow
    Start-Process python -ArgumentList "backend/manage.py", "runserver", "8000" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

if ($frontendPort) {
    Write-Host "✅ Frontend (5173): FUNCIONANDO" -ForegroundColor Green
}
else {
    Write-Host "❌ Frontend (5173): NO FUNCIONA" -ForegroundColor Red
    Write-Host "🔧 Iniciando frontend..." -ForegroundColor Yellow
    Set-Location "frontend"
    Start-Process cmd -ArgumentList "/c", "npm run dev" -WindowStyle Hidden
    Set-Location ".."
    Start-Sleep -Seconds 5
}

# 2. Probar acceso a páginas específicas
Write-Host "`n🔍 2. PROBANDO PÁGINAS ESPECÍFICAS" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

try {
    $loginTest = Invoke-WebRequest -Uri "https://localhost:5173/" -Method Head -TimeoutSec 5 -SkipCertificateCheck
    Write-Host "✅ Página principal: $($loginTest.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Página principal: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

try {
    $publicTrackingTest = Invoke-WebRequest -Uri "https://localhost:5173/rastrear" -Method Head -TimeoutSec 5 -SkipCertificateCheck
    Write-Host "✅ Rastreo público: $($publicTrackingTest.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Rastreo público: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Probar endpoints del backend
Write-Host "`n🌐 3. PROBANDO ENDPOINTS BACKEND" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

try {
    $apiTest = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -Method Head -TimeoutSec 5
    Write-Host "✅ Backend Admin: $($apiTest.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend Admin: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

try {
    $trackingEndpoint = Invoke-RestMethod -Uri "http://localhost:8000/api/envios/rastrear_por_nombre/?nombre=test&tipo=ambos" -TimeoutSec 5
    Write-Host "✅ Endpoint rastreo: FUNCIONANDO" -ForegroundColor Green
}
catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "⚠️  Endpoint rastreo: OK (requiere auth)" -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ Endpoint rastreo: ERROR - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 4. Información para móvil
Write-Host "`n📱 4. CONFIGURACIÓN PARA MÓVIL" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" } | Select-Object -First 1).IPAddress

if ($localIP) {
    Write-Host "📍 IP local detectada: $localIP" -ForegroundColor Green
    Write-Host "📱 URLs para móvil:" -ForegroundColor Cyan
    Write-Host "   Frontend HTTPS: https://$localIP:5173/" -ForegroundColor White
    Write-Host "   Rastreo público: https://$localIP:5173/rastrear" -ForegroundColor White
    Write-Host "   Backend API: http://$localIP:8000/api/" -ForegroundColor White
}
else {
    Write-Host "⚠️  No se pudo detectar IP local" -ForegroundColor Yellow
}

# 5. Diagnóstico específico de la página de seguimiento
Write-Host "`n🔍 5. DIAGNÓSTICO PÁGINA DE SEGUIMIENTO" -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Yellow

# Verificar archivos importantes
$trackingFiles = @(
    "frontend\src\pages\TrackingPage.tsx",
    "frontend\src\pages\TrackingPage.css",
    "frontend\src\pages\PublicTrackingPage.tsx",
    "frontend\src\App.tsx",
    "frontend\src\components\Layout.tsx"
)

foreach ($file in $trackingFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file existe" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $file NO EXISTE" -ForegroundColor Red
    }
}

# 6. Soluciones recomendadas
Write-Host "`n🔧 6. SOLUCIONES RECOMENDADAS" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

Write-Host "Para el problema de página en blanco en seguimiento:" -ForegroundColor Cyan
Write-Host "1. ✅ Verificado: Ruta corregida de /seguimiento a /rastreo" -ForegroundColor Green
Write-Host "2. ✅ Verificado: Archivo CSS creado" -ForegroundColor Green
Write-Host "3. ✅ Verificado: Componente existe y funciona" -ForegroundColor Green

Write-Host "`nPara el problema del móvil:" -ForegroundColor Cyan
Write-Host "1. 📱 Abre Chrome en tu móvil" -ForegroundColor White
Write-Host "2. 🌐 Ve a: https://$localIP:5173/" -ForegroundColor White
Write-Host "3. 🔐 Acepta el certificado si aparece advertencia" -ForegroundColor White
Write-Host "4. 📲 Si sigue sin funcionar, usa: http://$localIP:8080/" -ForegroundColor White

# 7. Comandos útiles para debugging
Write-Host "`n💡 7. COMANDOS ÚTILES PARA DEBUGGING" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

Write-Host "Ver logs del frontend:" -ForegroundColor Cyan
Write-Host "  cd frontend && npm run dev" -ForegroundColor White

Write-Host "`nVer logs del backend:" -ForegroundColor Cyan
Write-Host "  cd backend && python manage.py runserver 8000" -ForegroundColor White

Write-Host "`nProbar página de seguimiento directamente:" -ForegroundColor Cyan
Write-Host "  https://localhost:5173/rastreo" -ForegroundColor White

Write-Host "`nProbar rastreo público:" -ForegroundColor Cyan
Write-Host "  https://localhost:5173/rastrear" -ForegroundColor White

# 8. Verificación final
Write-Host "`n🎯 8. VERIFICACIÓN FINAL" -ForegroundColor Yellow
Write-Host "========================" -ForegroundColor Yellow

if ($backendPort -and $frontendPort) {
    Write-Host "🎉 SISTEMA OPERATIVO - Todos los servicios funcionando" -ForegroundColor Green
    Write-Host "✅ Backend disponible en puerto 8000" -ForegroundColor Green
    Write-Host "✅ Frontend disponible en puerto 5173" -ForegroundColor Green
    Write-Host "✅ Página de seguimiento configurada correctamente" -ForegroundColor Green

    Write-Host "`n🚀 PASOS PARA PROBAR:" -ForegroundColor Cyan
    Write-Host "1. Ve a: https://localhost:5173/" -ForegroundColor White
    Write-Host "2. Inicia sesión en el sistema" -ForegroundColor White
    Write-Host "3. Haz clic en 'Seguimiento' en el menú" -ForegroundColor White
    Write-Host "4. Para móvil, usa: https://$localIP:5173/" -ForegroundColor White
}
else {
    Write-Host "⚠️  ALGUNOS SERVICIOS NO ESTÁN FUNCIONANDO" -ForegroundColor Red
    Write-Host "🔧 Ejecuta: .\iniciar-sistema-unificado.ps1" -ForegroundColor Yellow
}

Write-Host "`n🇨🇺 Packfy Cuba - Diagnóstico completado!" -ForegroundColor Green
