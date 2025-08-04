# Script de prueba de conectividad para móvil
# No requiere permisos de administrador

Write-Host "🧪 Probando conectividad Packfy para móvil..." -ForegroundColor Yellow
Write-Host "IP detectada: 192.168.12.179" -ForegroundColor Cyan

Write-Host "`n📡 Probando Frontend..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "http://192.168.12.179:5173" -Method GET -TimeoutSec 5
    Write-Host "✅ Frontend OK (Status: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🔧 Probando Backend..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "http://192.168.12.179:8000/api/" -Method GET -TimeoutSec 5
    Write-Host "❌ Respuesta inesperada del Backend" -ForegroundColor Yellow
} catch {
    if ($_.Exception.Message -like "*401*" -or $_.Exception.Message -like "*autenticación*") {
        Write-Host "✅ Backend OK (Error 401 es normal)" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n📱 URLs para probar en móvil:" -ForegroundColor Yellow
Write-Host "   http://192.168.12.179:5173" -ForegroundColor White
Write-Host "   http://192.168.12.179:5173/test-ip.html" -ForegroundColor White

Write-Host "`n🔑 Credenciales de prueba:" -ForegroundColor Yellow
Write-Host "   Email: test@test.com" -ForegroundColor White
Write-Host "   Password: 123456" -ForegroundColor White

Write-Host "`n💡 Si hay problemas:" -ForegroundColor Cyan
Write-Host "   1. Ejecuta 'configurar-firewall.ps1' como Administrador" -ForegroundColor White
Write-Host "   2. Verifica que el móvil esté en la misma red WiFi" -ForegroundColor White
Write-Host "   3. Verifica que no haya antivirus bloqueando" -ForegroundColor White

Read-Host "`nPresiona Enter para cerrar"
