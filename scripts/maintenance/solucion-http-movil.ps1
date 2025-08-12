# SOLUCION DEFINITIVA MOVIL - HTTP TEMPORAL
Write-Host "🇨🇺 PACKFY CUBA - CONFIGURACION MOVIL HTTP" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

$ipLocal = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp"}).IPAddress | Select-Object -First 1

Write-Host "`n📱 PARA MOVIL - USA ESTAS URLS:" -ForegroundColor Yellow
Write-Host "Frontend: http://$ipLocal`:5174/" -ForegroundColor Cyan -BackgroundColor Black
Write-Host "Test Page: http://$ipLocal`:5174/test-http-movil.html" -ForegroundColor Cyan -BackgroundColor Black
Write-Host "Backend: http://$ipLocal`:8000/" -ForegroundColor White

Write-Host "`n✅ SOLUCION IMPLEMENTADA:" -ForegroundColor Green
Write-Host "1. HTTP temporal (sin problemas de certificados)" -ForegroundColor White
Write-Host "2. Interfaz moderna v2.1 con cache busting" -ForegroundColor White
Write-Host "3. PWA optimizada para movil" -ForegroundColor White
Write-Host "4. Colores cubanos premium" -ForegroundColor White

Write-Host "`n📱 INSTRUCCIONES MOVIL:" -ForegroundColor Yellow
Write-Host "1. Abre Chrome en tu movil" -ForegroundColor White
Write-Host "2. Ve a: http://$ipLocal`:5174/" -ForegroundColor White
Write-Host "3. NO hay problemas de certificados" -ForegroundColor White
Write-Host "4. La interfaz moderna deberia cargar perfectamente" -ForegroundColor White

Write-Host "`n🔧 VERIFICACION:" -ForegroundColor Yellow
Write-Host "• Test page: http://$ipLocal`:5174/test-http-movil.html" -ForegroundColor White
Write-Host "• App principal: http://$ipLocal`:5174/" -ForegroundColor White

Write-Host "`n📊 VERIFICANDO SERVIDORES:" -ForegroundColor Yellow

# Verificar frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://$ipLocal`:5174/" -UseBasicParsing -TimeoutSec 5
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend HTTP funcionando (puerto 5174)" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend no responde" -ForegroundColor Red
}

# Verificar backend  
try {
    $backendResponse = Invoke-WebRequest -Uri "http://$ipLocal`:8000/api/" -UseBasicParsing -TimeoutSec 5
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend funcionando (puerto 8000)" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend no responde" -ForegroundColor Red
}

Write-Host "`n🎯 RESULTADO:" -ForegroundColor Green
Write-Host "PWA con interfaz moderna lista para movil via HTTP" -ForegroundColor White
Write-Host "Sin problemas de certificados SSL" -ForegroundColor White
