# 🎯 VERIFICACIÓN RÁPIDA - PACKFY CUBA
# Test rápido de conectividad

Write-Host "🇨🇺 Verificando Packfy Cuba..." -ForegroundColor Cyan
Write-Host ""

# Obtener IP local
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress | Select-Object -First 1

# Verificar Backend
Write-Host "🔍 Backend (Django)..." -ForegroundColor Yellow -NoNewline
try {
    $backend = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -TimeoutSec 3 -UseBasicParsing -ErrorAction SilentlyContinue
    Write-Host " ✅ OK" -ForegroundColor Green
} catch {
    Write-Host " ❌ ERROR" -ForegroundColor Red
}

# Verificar Frontend en puertos posibles
$frontendPort = $null
foreach ($port in @(5175, 5174, 5173, 5176)) {
    Write-Host "🔍 Frontend puerto ${port}..." -ForegroundColor Yellow -NoNewline
    try {
        $frontend = Invoke-WebRequest -Uri "http://localhost:${port}/" -TimeoutSec 3 -UseBasicParsing -ErrorAction SilentlyContinue
        Write-Host " ✅ OK" -ForegroundColor Green
        $frontendPort = $port
        break
    } catch {
        Write-Host " ❌ ERROR" -ForegroundColor Red
    }
}

Write-Host ""

if ($frontendPort) {
    Write-Host "🌐 URLs:" -ForegroundColor Cyan
    Write-Host "   💻 PC: http://localhost:${frontendPort}/" -ForegroundColor White
    Write-Host "   📱 Móvil: http://${localIP}:${frontendPort}/" -ForegroundColor White
    Write-Host ""
    Write-Host "🔐 Credenciales:" -ForegroundColor Yellow
    Write-Host "   admin@packfy.cu / admin123" -ForegroundColor White
} else {
    Write-Host "❌ Frontend no está funcionando" -ForegroundColor Red
    Write-Host "Ejecuta: cd frontend && npm run dev" -ForegroundColor Yellow
}
