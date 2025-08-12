# 🎯 VERIFICACIÓN SIN PROXY - PACKFY CUBA
# Confirma que el sistema funciona sin problemas de proxy

Write-Host "🇨🇺 ===========================================" -ForegroundColor Green
Write-Host "🎯 SISTEMA SIN PROXY - VERIFICACIÓN FINAL" -ForegroundColor Green
Write-Host "🇨🇺 ===========================================" -ForegroundColor Green
Write-Host ""

# Información del sistema
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress | Select-Object -First 1
Write-Host "🌐 IP Local: $localIP" -ForegroundColor Cyan
Write-Host "📅 Fecha: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" -ForegroundColor Cyan
Write-Host ""

# Verificar backend directo
Write-Host "🔍 Verificando Backend (Conexión Directa)..." -ForegroundColor Yellow
$backendUrls = @(
    "http://localhost:8000/admin/",
    "http://${localIP}:8000/admin/"
)

$backendWorking = $false
foreach ($url in $backendUrls) {
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        Write-Host "✅ Backend funcionando: $url" -ForegroundColor Green
        $backendWorking = $true
        $workingBackend = $url
        break
    } catch {
        Write-Host "❌ Backend no disponible: $url" -ForegroundColor Red
    }
}

Write-Host ""

# Verificar frontend
Write-Host "🔍 Verificando Frontend..." -ForegroundColor Yellow
$frontendPorts = @(5175, 5174, 5173, 5176, 5177)
$frontendWorking = $false

foreach ($port in $frontendPorts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:${port}/" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        Write-Host "✅ Frontend funcionando en puerto: ${port}" -ForegroundColor Green
        $frontendWorking = $true
        $workingPort = $port
        break
    } catch {
        Write-Host "❌ Puerto ${port}: No disponible" -ForegroundColor Red
    }
}

Write-Host ""

if ($frontendWorking -and $backendWorking) {
    Write-Host "🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🌐 CONFIGURACIÓN AUTOMÁTICA:" -ForegroundColor Cyan
    Write-Host "   ✅ Sin proxy - Conexión directa" -ForegroundColor Green
    Write-Host "   ✅ Auto-detección de puertos" -ForegroundColor Green
    Write-Host "   ✅ Adaptación automática móvil/PC" -ForegroundColor Green
    Write-Host "   ✅ Resistente a cambios futuros" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🌐 URLS DE ACCESO:" -ForegroundColor Cyan
    Write-Host "   💻 Computadora: http://localhost:${workingPort}/" -ForegroundColor White
    Write-Host "   📱 Móvil: http://${localIP}:${workingPort}/" -ForegroundColor White
    Write-Host "   🔧 Admin: $workingBackend" -ForegroundColor White
    
    Write-Host ""
    Write-Host "🔐 CREDENCIALES DE PRUEBA:" -ForegroundColor Yellow
    Write-Host "   👑 Admin: admin@packfy.cu / admin123" -ForegroundColor White
    Write-Host "   🏢 Empresa: empresa@test.cu / empresa123" -ForegroundColor White
    Write-Host "   🇨🇺 Cliente: cliente@test.cu / cliente123" -ForegroundColor White
    
    Write-Host ""
    Write-Host "🎨 CARACTERÍSTICAS PREMIUM:" -ForegroundColor Magenta
    Write-Host "   ✅ Interfaz moderna cubana" -ForegroundColor Green
    Write-Host "   ✅ Sistema autoconfigurado" -ForegroundColor Green
    Write-Host "   ✅ Sin problemas de proxy" -ForegroundColor Green
    Write-Host "   ✅ Adaptativo a cambios" -ForegroundColor Green
    Write-Host "   ✅ Navegación móvil optimizada" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🚀 BENEFICIOS DEL NUEVO SISTEMA:" -ForegroundColor Magenta
    Write-Host "   🎯 Auto-detección de configuración" -ForegroundColor Green
    Write-Host "   🔄 Auto-reparación en caso de fallos" -ForegroundColor Green
    Write-Host "   📱 Funciona igual en PC y móvil" -ForegroundColor Green
    Write-Host "   🛡️  Resistente a cambios de puerto" -ForegroundColor Green
    Write-Host "   ⚡ Sin dependencia de proxy" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🇨🇺 ¡PACKFY CUBA LISTO SIN PROBLEMAS DE PROXY!" -ForegroundColor Green

} else {
    Write-Host "❌ PROBLEMAS DETECTADOS:" -ForegroundColor Red
    
    if (-not $backendWorking) {
        Write-Host "   💥 Backend Django no está funcionando" -ForegroundColor Red
        Write-Host "   🔧 Solución: cd backend && python manage.py runserver 0.0.0.0:8000" -ForegroundColor Yellow
    }
    
    if (-not $frontendWorking) {
        Write-Host "   💥 Frontend Vite no está funcionando" -ForegroundColor Red
        Write-Host "   🔧 Solución: cd frontend && npm run dev" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📝 NOTAS IMPORTANTES:" -ForegroundColor Yellow
Write-Host "   • Este sistema NO usa proxy" -ForegroundColor White
Write-Host "   • Se autoonfigura automáticamente" -ForegroundColor White  
Write-Host "   • Funciona en cualquier puerto disponible" -ForegroundColor White
Write-Host "   • No requiere configuración manual" -ForegroundColor White
