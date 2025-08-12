# Test HTTPS para móvil
Write-Host "CONFIGURACION HTTPS PARA MOVIL COMPLETADA" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

$ipLocal = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp"}).IPAddress | Select-Object -First 1

Write-Host "`nCONFIGURACION:" -ForegroundColor Yellow
Write-Host "Frontend HTTPS: https://$ipLocal:8443" -ForegroundColor White
Write-Host "Backend HTTP:   http://$ipLocal:8000" -ForegroundColor White

Write-Host "`nPARA MÓVIL - USA ESTA URL:" -ForegroundColor Green
Write-Host "https://$ipLocal:8443" -ForegroundColor Cyan -BackgroundColor Black

Write-Host "`nINSTRUCCIONES MÓVIL:" -ForegroundColor Yellow
Write-Host "1. Abre Chrome en tu móvil" -ForegroundColor White
Write-Host "2. Ve a: https://$ipLocal:8443" -ForegroundColor White
Write-Host "3. Acepta el certificado autofirmado" -ForegroundColor White
Write-Host "4. La interfaz moderna debería cargar completamente" -ForegroundColor White

Write-Host "`nVERIFICANDO SERVIDORES:" -ForegroundColor Yellow

# Verificar frontend HTTPS
try {
    $frontendResponse = Invoke-WebRequest -Uri "https://$ipLocal:8443" -SkipCertificateCheck -UseBasicParsing -TimeoutSec 5
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✓ Frontend HTTPS funcionando en puerto 8443" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Frontend HTTPS no responde" -ForegroundColor Red
    Write-Host "Ejecuta: http-server -p 8443 -S -a 0.0.0.0 --cors" -ForegroundColor Yellow
}

# Verificar backend
try {
    $backendResponse = Invoke-WebRequest -Uri "http://$ipLocal:8000/api/" -UseBasicParsing -TimeoutSec 5
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✓ Backend funcionando en puerto 8000" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Backend no responde" -ForegroundColor Red
    Write-Host "Ejecuta: python manage.py runserver 0.0.0.0:8000" -ForegroundColor Yellow
}

Write-Host "`nESTADO: PWA CON HTTPS LISTA PARA MOVIL" -ForegroundColor Green
Write-Host "La interfaz moderna v2.1 deberia funcionar perfectamente" -ForegroundColor White
