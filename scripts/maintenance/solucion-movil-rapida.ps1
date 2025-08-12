# 🇨🇺 PACKFY CUBA - SOLUCION RAPIDA MOVIL

Write-Host "🔧 Packfy Cuba - Solucion Rapida Movil" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Verificar estado de servicios
Write-Host "📊 Verificando servicios..." -ForegroundColor Yellow

$frontendRunning = netstat -ano | findstr ":5173" | Select-String "LISTENING"
$backendRunning = netstat -ano | findstr ":8000" | Select-String "LISTENING"

if ($frontendRunning) {
    Write-Host "✅ Frontend corriendo en puerto 5173" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend NO esta corriendo" -ForegroundColor Red
    Write-Host "🔄 Intentando reiniciar frontend..." -ForegroundColor Yellow
    
    # Navegar al directorio frontend y iniciar
    $frontendDir = "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend"
    if (Test-Path $frontendDir) {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; npm run dev"
        Write-Host "✅ Frontend iniciado en nueva ventana" -ForegroundColor Green
    }
}

if ($backendRunning) {
    Write-Host "✅ Backend corriendo en puerto 8000" -ForegroundColor Green
} else {
    Write-Host "❌ Backend NO esta corriendo" -ForegroundColor Red
    Write-Host "🔄 Intentando reiniciar backend..." -ForegroundColor Yellow
    
    # Navegar al directorio backend y iniciar
    $backendDir = "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend"
    if (Test-Path $backendDir) {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; python manage.py runserver"
        Write-Host "✅ Backend iniciado en nueva ventana" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "📱 URLS PARA MOVIL:" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "🌐 Principal:    https://192.168.12.178:5173" -ForegroundColor Yellow
Write-Host "🔧 Diagnostico:  https://192.168.12.178:5173/test-movil-diagnostico.html" -ForegroundColor Yellow
Write-Host "🏠 Local:        https://localhost:5173" -ForegroundColor Yellow

Write-Host ""
Write-Host "🛠️ PROBLEMAS COMUNES Y SOLUCIONES:" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

Write-Host "1. 🔒 Certificado HTTPS no confiable:" -ForegroundColor White
Write-Host "   • En Chrome: Clic en 'Avanzado' > 'Ir al sitio'" -ForegroundColor Gray
Write-Host "   • En Safari: Clic en 'Mostrar detalles' > 'Visitar sitio'" -ForegroundColor Gray

Write-Host ""
Write-Host "2. 📶 Problemas de red:" -ForegroundColor White
Write-Host "   • Verificar misma WiFi en PC y movil" -ForegroundColor Gray
Write-Host "   • Desactivar VPN temporalmente" -ForegroundColor Gray
Write-Host "   • Reiniciar WiFi en el movil" -ForegroundColor Gray

Write-Host ""
Write-Host "3. 🌐 Navegador incompatible:" -ForegroundColor White
Write-Host "   • Usar Chrome o Safari" -ForegroundColor Gray
Write-Host "   • Evitar navegadores de redes sociales" -ForegroundColor Gray

Write-Host ""
Write-Host "4. 🚫 Pagina en blanco:" -ForegroundColor White
Write-Host "   • Limpiar cache del navegador" -ForegroundColor Gray
Write-Host "   • Cerrar y abrir navegador" -ForegroundColor Gray
Write-Host "   • Probar modo incognito" -ForegroundColor Gray

Write-Host ""
Write-Host "📋 VERIFICACION RAPIDA:" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

# Mostrar IP actual
try {
    $ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress
    Write-Host "🖥️ IP del PC: $ip" -ForegroundColor Green
    
    if ($ip -eq "192.168.12.178") {
        Write-Host "✅ IP coincide con configuracion" -ForegroundColor Green
    } else {
        Write-Host "⚠️ IP diferente - usar: https://${ip}:5173" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ No se pudo detectar IP automaticamente" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 COMANDOS UTILES:" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "• Verificar puertos: netstat -ano | findstr ':5173'" -ForegroundColor Gray
Write-Host "• Reiniciar servicios: .\start-packfy.ps1" -ForegroundColor Gray
Write-Host "• Diagnostico: https://192.168.12.178:5173/test-movil-diagnostico.html" -ForegroundColor Gray

Write-Host ""
Write-Host "✅ Diagnostico completado" -ForegroundColor Green
Write-Host "📱 Intenta acceder desde tu movil ahora" -ForegroundColor Yellow
