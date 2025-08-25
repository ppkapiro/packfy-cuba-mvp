# GUIA RAPIDA: PWA en Android sin HTTPS
Write-Host "GUIA RAPIDA: PWA EN ANDROID SIN HTTPS" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Write-Host "PASOS PARA TU MOVIL ANDROID:" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

Write-Host "`n1. Abrir Chrome en tu movil" -ForegroundColor Cyan
Write-Host "2. Ir a: chrome://flags/" -ForegroundColor Cyan
Write-Host "3. Buscar: 'Insecure origins treated as secure'" -ForegroundColor Cyan
Write-Host "4. Anadir: http://192.168.12.179:5173" -ForegroundColor Cyan
Write-Host "5. Cambiar a: 'Enabled'" -ForegroundColor Cyan
Write-Host "6. Reiniciar Chrome" -ForegroundColor Cyan

Write-Host "`nALTERNATIVA: Si tienes cable USB" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow
Write-Host "1. Conecta tu movil por USB" -ForegroundColor Cyan
Write-Host "2. Habilita 'Depuracion USB' en tu movil" -ForegroundColor Cyan
Write-Host "3. En Chrome PC: chrome://inspect" -ForegroundColor Cyan
Write-Host "4. Configure port forwarding: 5173 -> localhost:5173" -ForegroundColor Cyan

Write-Host "`nURLs PARA PROBAR:" -ForegroundColor Yellow
Write-Host "=================" -ForegroundColor Yellow
$ip = (ipconfig | findstr "IPv4" | Select-Object -First 1) -replace '.*: ', ''
Write-Host "App principal: http://$ip:5173" -ForegroundColor Green
Write-Host "Test PWA: http://$ip:5173/test-pwa.html" -ForegroundColor Green
Write-Host "Login: admin@correo.com / admin123" -ForegroundColor Green

Write-Host "`nVERIFICAR SERVICIOS:" -ForegroundColor Yellow
docker compose ps

Write-Host "`nSi todo falla, usa Firefox Mobile (mas permisivo)" -ForegroundColor Red
