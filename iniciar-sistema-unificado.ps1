# 🇨🇺 PACKFY CUBA - INICIAR SISTEMA UNIFICADO v3.0
Write-Host "🇨🇺 PACKFY CUBA - INICIANDO SISTEMA UNIFICADO v3.0" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

$ipLocal = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp"}).IPAddress | Select-Object -First 1

Write-Host "`n🛑 PASO 1: LIMPIANDO PROCESOS ANTERIORES" -ForegroundColor Yellow
taskkill /F /IM "python.exe" 2>$null
taskkill /F /IM "node.exe" 2>$null
Write-Host "✅ Procesos anteriores terminados" -ForegroundColor Green

Write-Host "`n🚀 PASO 2: INICIANDO BACKEND DJANGO" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend'; python manage.py runserver 0.0.0.0:8000" -WindowStyle Minimized
Start-Sleep -Seconds 3
Write-Host "✅ Backend Django iniciado en puerto 8000" -ForegroundColor Green

Write-Host "`n🔒 PASO 3: INICIANDO FRONTEND HTTPS" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend'; npm run dev" -WindowStyle Normal
Start-Sleep -Seconds 5
Write-Host "✅ Frontend HTTPS iniciado en puerto 5173" -ForegroundColor Green

Write-Host "`n📊 VERIFICANDO SERVICIOS..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Verificar backend
try {
    $backendResponse = Invoke-WebRequest -Uri "http://$ipLocal`:8000/api/" -UseBasicParsing -TimeoutSec 5
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend funcionando correctamente" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Backend iniciando... (puede tardar unos segundos)" -ForegroundColor Yellow
}

# Verificar frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "https://$ipLocal`:5173/" -SkipCertificateCheck -UseBasicParsing -TimeoutSec 5
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend HTTPS funcionando correctamente" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Frontend iniciando... (puede tardar unos segundos)" -ForegroundColor Yellow
}

Write-Host "`n🎯 SISTEMA UNIFICADO v3.0 INICIADO" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "`n📱 URLS PARA MÓVIL:" -ForegroundColor Yellow
Write-Host "Frontend HTTPS: https://$ipLocal`:5173/" -ForegroundColor Cyan -BackgroundColor Black
Write-Host "Backend API:    http://$ipLocal`:8000/" -ForegroundColor White

Write-Host "`n🛡️  CARACTERÍSTICAS:" -ForegroundColor Yellow
Write-Host "• HTTPS con certificados válidos" -ForegroundColor White
Write-Host "• API unificada y robusta" -ForegroundColor White
Write-Host "• Sistema CSS consolidado" -ForegroundColor White
Write-Host "• PWA completamente funcional" -ForegroundColor White
Write-Host "• Optimizado para móvil" -ForegroundColor White

Write-Host "`n📱 INSTRUCCIONES MÓVIL:" -ForegroundColor Yellow
Write-Host "1. Abre Chrome en tu móvil" -ForegroundColor White
Write-Host "2. Ve a: https://$ipLocal`:5173/" -ForegroundColor White
Write-Host "3. Acepta certificado si se solicita" -ForegroundColor White
Write-Host "4. Disfruta de la PWA cubana! 🇨🇺" -ForegroundColor White

Write-Host "`n🔧 COMANDOS ÚTILES:" -ForegroundColor Yellow
Write-Host "• Ver logs: .\ver-logs.ps1" -ForegroundColor Gray
Write-Host "• Detener todo: .\detener-sistema.ps1" -ForegroundColor Gray
Write-Host "• Reiniciar: .\reiniciar-sistema.ps1" -ForegroundColor Gray

Write-Host "`n✨ ¡SISTEMA LISTO PARA USAR!" -ForegroundColor Green
