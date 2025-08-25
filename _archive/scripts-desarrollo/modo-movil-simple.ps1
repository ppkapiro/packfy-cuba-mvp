# 📱 Servidor Móvil Estable - Packfy Cuba
# Script para ejecutar servidor optimizado para dispositivos móviles

Write-Host "🚀 INICIANDO SERVIDOR OPTIMIZADO PARA MÓVIL" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan

# Detener procesos anteriores
Write-Host "`n🔄 Deteniendo servidores anteriores..." -ForegroundColor Yellow
try {
    Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "✅ Procesos anteriores detenidos" -ForegroundColor Green
} catch {
    Write-Host "ℹ️ No había procesos anteriores" -ForegroundColor Gray
}

# Limpiar puerto 5173
Write-Host "`n🧹 Liberando puerto 5173..." -ForegroundColor Yellow
try {
    $processOnPort = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
    if ($processOnPort) {
        $pid = $processOnPort.OwningProcess
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "✅ Puerto 5173 liberado" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ Puerto 5173 ya estaba libre" -ForegroundColor Gray
    }
} catch {
    Write-Host "ℹ️ Puerto verificado" -ForegroundColor Gray
}

# Navegar al directorio frontend
Set-Location "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend"
Write-Host "`n📁 Directorio: $(Get-Location)" -ForegroundColor Cyan

# Verificar que el backend esté corriendo
Write-Host "`n🔍 Verificando backend..." -ForegroundColor Yellow
try {
    $backendResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/swagger/" -UseBasicParsing -TimeoutSec 5
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend funcionando en http://127.0.0.1:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Backend no responde. Asegúrate de ejecutar:" -ForegroundColor Red
    Write-Host "   cd backend" -ForegroundColor White
    Write-Host "   python manage.py runserver" -ForegroundColor White
    Write-Host ""
}

# Configuración específica para móvil
Write-Host "`n📱 CONFIGURACIÓN MÓVIL OPTIMIZADA:" -ForegroundColor Magenta
Write-Host "   ✨ HMR estabilizado para dispositivos móviles"
Write-Host "   ✨ Polling desactivado (mejor rendimiento)"
Write-Host "   ✨ Timeouts extendidos para conexiones lentas"
Write-Host "   ✨ Overlay de errores desactivado"

# Mostrar información de conexión
Write-Host "`n🌐 INFORMACIÓN DE CONEXIÓN:" -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Cyan

# Obtener IP local
$localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi" -ErrorAction SilentlyContinue).IPAddress
if (-not $localIP) {
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" }).IPAddress | Select-Object -First 1
}

Write-Host "🖥️  Desktop: http://localhost:5173" -ForegroundColor White
Write-Host "📱 Móvil: http://${localIP}:5173" -ForegroundColor Yellow
Write-Host "🔗 PWA: Chrome → Menú → Instalar Packfy Cuba" -ForegroundColor Cyan

Write-Host "`n🧪 CREDENCIALES DE PRUEBA:" -ForegroundColor Magenta
Write-Host "👑 admin@packfy.cu / admin123" -ForegroundColor White
Write-Host "🏢 empresa@test.cu / empresa123" -ForegroundColor White
Write-Host "🇨🇺 cliente@test.cu / cliente123" -ForegroundColor White

Write-Host "`n💡 CONSEJOS PARA MÓVIL:" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "1. 📶 Usa conexión WiFi estable"
Write-Host "2. 🔄 Si se actualiza mucho, cierra y vuelve a abrir Chrome"
Write-Host "3. 📱 Considera instalar como PWA para mejor estabilidad"
Write-Host "4. 🚫 Evita el modo incógnito en móvil"
Write-Host "5. 💾 Activa caché en configuración de Chrome"

Write-Host "`n🚀 Iniciando servidor móvil estable..." -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan

# Iniciar servidor con configuración móvil
npm run dev
