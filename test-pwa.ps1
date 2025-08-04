# Script de Verificacion PWA
Write-Host "VERIFICACION PWA PACKFY" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

# 1. Verificar servicios
Write-Host "1. Estado de servicios:" -ForegroundColor Yellow
docker compose ps

# 2. Verificar manifest
Write-Host "`n2. Manifest PWA:" -ForegroundColor Yellow
try {
    $manifest = Invoke-WebRequest -Uri "http://localhost:5173/manifest.json" -UseBasicParsing
    Write-Host "Manifest OK (Size: $($manifest.Content.Length) bytes)" -ForegroundColor Green
} catch {
    Write-Host "Manifest ERROR: $_" -ForegroundColor Red
}

# 3. Verificar Service Worker
Write-Host "`n3. Service Worker:" -ForegroundColor Yellow
try {
    $sw = Invoke-WebRequest -Uri "http://localhost:5173/sw.js" -UseBasicParsing
    Write-Host "Service Worker OK (Size: $($sw.Content.Length) bytes)" -ForegroundColor Green
} catch {
    Write-Host "Service Worker ERROR: $_" -ForegroundColor Red
}

# 4. Mostrar URLs para testing
Write-Host "`n4. URLs para probar:" -ForegroundColor Yellow
$ip = (ipconfig | findstr IPv4 | Select-Object -First 1) -replace '.*: ', ''
Write-Host "PC: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Movil: http://$ip:5173" -ForegroundColor Cyan

# 5. Instrucciones
Write-Host "`n5. Como probar en movil:" -ForegroundColor Yellow
Write-Host "Android: Chrome -> http://$ip:5173 -> 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "iOS: Safari -> http://$ip:5173 -> Compartir -> 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "PC: Chrome -> http://localhost:5173 -> Boton instalar" -ForegroundColor White

Write-Host "`nVerificacion completada!" -ForegroundColor Green
