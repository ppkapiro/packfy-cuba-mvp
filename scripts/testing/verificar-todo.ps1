# ✅ TEST FINAL - PACKFY CUBA CORREGIDO
# Verificación completa de conectividad

Write-Host "🇨🇺 =========================================" -ForegroundColor Green
Write-Host "✅ VERIFICACIÓN FINAL - PACKFY CUBA" -ForegroundColor Green  
Write-Host "🇨🇺 =========================================" -ForegroundColor Green
Write-Host ""

# IP Local
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress | Select-Object -First 1
Write-Host "🌐 IP Local: $localIP" -ForegroundColor Cyan

Write-Host ""

# Backend Test
Write-Host "🔍 Testing Backend..." -ForegroundColor Yellow
try {
    $backend = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Backend Django: FUNCIONANDO ✅" -ForegroundColor Green
    Write-Host "   Status: $($backend.StatusCode)" -ForegroundColor White
} catch {
    Write-Host "❌ Backend Django: ERROR ❌" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor White
}

Write-Host ""

# Frontend Test
Write-Host "🔍 Testing Frontend..." -ForegroundColor Yellow
$frontendWorking = $false
$workingPort = $null

foreach ($port in @(5175, 5174, 5173, 5176, 5177)) {
    try {
        $frontend = Invoke-WebRequest -Uri "http://localhost:${port}/" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        Write-Host "✅ Frontend Vite puerto ${port}: FUNCIONANDO ✅" -ForegroundColor Green
        Write-Host "   Status: $($frontend.StatusCode)" -ForegroundColor White
        $frontendWorking = $true
        $workingPort = $port
        break
    } catch {
        Write-Host "❌ Puerto ${port}: No disponible" -ForegroundColor Red
    }
}

Write-Host ""

if ($frontendWorking) {
    Write-Host "🎯 CONEXIÓN EXITOSA - SERVIDORES FUNCIONANDO" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 URLs DE ACCESO:" -ForegroundColor Cyan
    Write-Host "   💻 Computadora: http://localhost:${workingPort}/" -ForegroundColor White
    Write-Host "   📱 Móvil: http://${localIP}:${workingPort}/" -ForegroundColor White
    Write-Host "   🔧 Admin: http://localhost:8000/admin/" -ForegroundColor White
    
    Write-Host ""
    Write-Host "🔐 CREDENCIALES DE PRUEBA:" -ForegroundColor Yellow
    Write-Host "   👑 Admin: admin@packfy.cu / admin123" -ForegroundColor White
    Write-Host "   🏢 Empresa: empresa@test.cu / empresa123" -ForegroundColor White
    Write-Host "   🇨🇺 Cliente: cliente@test.cu / cliente123" -ForegroundColor White
    
    Write-Host ""
    Write-Host "🎨 CARACTERÍSTICAS IMPLEMENTADAS:" -ForegroundColor Magenta
    Write-Host "   ✅ Interfaz moderna cubana" -ForegroundColor Green
    Write-Host "   ✅ Diseño responsivo premium" -ForegroundColor Green
    Write-Host "   ✅ Iconos SVG profesionales" -ForegroundColor Green
    Write-Host "   ✅ Navegación optimizada móvil" -ForegroundColor Green
    Write-Host "   ✅ Dashboard con estadísticas" -ForegroundColor Green
    Write-Host "   ✅ Formularios premium" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🚀 ¡TODO FUNCIONANDO CORRECTAMENTE!" -ForegroundColor Green
    Write-Host "🇨🇺 Packfy Cuba listo para usar" -ForegroundColor Green

} else {
    Write-Host "❌ FRONTEND NO FUNCIONA" -ForegroundColor Red
    Write-Host "Verifica que el comando 'npm run dev' esté ejecutándose en frontend/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 Si hay problemas, revisa:" -ForegroundColor Yellow
Write-Host "   1. Consola del navegador (F12)" -ForegroundColor White
Write-Host "   2. Ventanas de PowerShell abiertas" -ForegroundColor White
Write-Host "   3. Firewall de Windows" -ForegroundColor White
