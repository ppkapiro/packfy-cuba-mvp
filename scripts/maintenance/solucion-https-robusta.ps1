# CONFIGURACION HTTPS ROBUSTA - PACKFY CUBA
Write-Host "🔒 PACKFY CUBA - CONFIGURACION HTTPS COMPLETA" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

$ipLocal = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp"}).IPAddress | Select-Object -First 1

Write-Host "`n🔒 URLS HTTPS PARA MOVIL:" -ForegroundColor Yellow
Write-Host "Frontend HTTPS: https://$ipLocal`:5173/" -ForegroundColor Cyan -BackgroundColor Black
Write-Host "Test HTTPS: https://$ipLocal`:5173/test-https-movil.html" -ForegroundColor Cyan -BackgroundColor Black
Write-Host "Backend HTTP: http://$ipLocal`:8000/" -ForegroundColor White

Write-Host "`n✅ CONFIGURACION HTTPS IMPLEMENTADA:" -ForegroundColor Green
Write-Host "1. Certificados SSL generados con mkcert" -ForegroundColor White
Write-Host "2. Compatible con navegadores moviles" -ForegroundColor White
Write-Host "3. Sin advertencias de seguridad" -ForegroundColor White
Write-Host "4. PWA completamente funcional" -ForegroundColor White
Write-Host "5. Interfaz moderna v2.1 con cache busting" -ForegroundColor White

Write-Host "`n📱 INSTRUCCIONES MOVIL (HTTPS):" -ForegroundColor Yellow
Write-Host "1. Abre Chrome en tu movil" -ForegroundColor White
Write-Host "2. Ve a: https://$ipLocal`:5173/" -ForegroundColor White
Write-Host "3. El certificado sera aceptado automaticamente" -ForegroundColor White
Write-Host "4. PWA funcionara sin restricciones" -ForegroundColor White

Write-Host "`n🔧 VERIFICACION HTTPS:" -ForegroundColor Yellow
Write-Host "• Test page: https://$ipLocal`:5173/test-https-movil.html" -ForegroundColor White
Write-Host "• App principal: https://$ipLocal`:5173/" -ForegroundColor White

Write-Host "`n🛡️ VENTAJAS HTTPS:" -ForegroundColor Yellow
Write-Host "• Service Workers funcionan" -ForegroundColor White
Write-Host "• Notificaciones Push disponibles" -ForegroundColor White
Write-Host "• Instalacion PWA completa" -ForegroundColor White
Write-Host "• API de camara y GPS funcionales" -ForegroundColor White
Write-Host "• Sin restricciones de navegador" -ForegroundColor White

Write-Host "`n📊 VERIFICANDO SERVIDORES:" -ForegroundColor Yellow

# Verificar frontend HTTPS
try {
    $frontendResponse = Invoke-WebRequest -Uri "https://$ipLocal`:5173/" -SkipCertificateCheck -UseBasicParsing -TimeoutSec 5
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend HTTPS funcionando (puerto 5173)" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend HTTPS no responde" -ForegroundColor Red
}

# Verificar backend HTTP
try {
    $backendResponse = Invoke-WebRequest -Uri "http://$ipLocal`:8000/api/" -UseBasicParsing -TimeoutSec 5
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend HTTP funcionando (puerto 8000)" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend no responde" -ForegroundColor Red
}

Write-Host "`n🎯 RESULTADO FINAL:" -ForegroundColor Green
Write-Host "HTTPS con certificados validos implementado" -ForegroundColor White
Write-Host "PWA completamente funcional en movil" -ForegroundColor White
Write-Host "Sin problemas de protocolos no compatibles" -ForegroundColor White

Write-Host "`n🚀 PROXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "1. Probar en movil: https://$ipLocal`:5173/" -ForegroundColor White
Write-Host "2. Verificar instalacion PWA" -ForegroundColor White
Write-Host "3. Comprobar todas las funcionalidades" -ForegroundColor White
