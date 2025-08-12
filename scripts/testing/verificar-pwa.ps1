# 🔍 Script de Verificación PWA
# Ejecuta estos comandos para verificar que todo funcione

Write-Host "🚀 VERIFICACIÓN PWA PACKFY" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# 1. Verificar servicios
Write-Host "📦 1. Estado de servicios:" -ForegroundColor Yellow
docker compose ps

# 2. Verificar manifest
Write-Host "`n📱 2. Manifest PWA:" -ForegroundColor Yellow
try {
    $manifest = Invoke-WebRequest -Uri "http://localhost:5173/manifest.json" -UseBasicParsing
    Write-Host "✅ Manifest OK (Size: $($manifest.Content.Length) bytes)" -ForegroundColor Green
} catch {
    Write-Host "❌ Manifest ERROR: $_" -ForegroundColor Red
}

# 3. Verificar Service Worker
Write-Host "`n🔧 3. Service Worker:" -ForegroundColor Yellow
try {
    $sw = Invoke-WebRequest -Uri "http://localhost:5173/sw.js" -UseBasicParsing
    Write-Host "✅ Service Worker OK (Size: $($sw.Content.Length) bytes)" -ForegroundColor Green
} catch {
    Write-Host "❌ Service Worker ERROR: $_" -ForegroundColor Red
}

# 4. Verificar iconos
Write-Host "`n🎨 4. Iconos PWA:" -ForegroundColor Yellow
try {
    $icon192 = Invoke-WebRequest -Uri "http://localhost:5173/icon-192.svg" -UseBasicParsing
    Write-Host "✅ Icon 192 OK" -ForegroundColor Green
} catch {
    Write-Host "❌ Icon 192 ERROR" -ForegroundColor Red
}

try {
    $icon512 = Invoke-WebRequest -Uri "http://localhost:5173/icon-512.svg" -UseBasicParsing
    Write-Host "✅ Icon 512 OK" -ForegroundColor Green
} catch {
    Write-Host "❌ Icon 512 ERROR" -ForegroundColor Red
}

# 5. Mostrar URLs para testing
Write-Host "`n🌐 5. URLs para probar:" -ForegroundColor Yellow
$ip = (ipconfig | findstr IPv4 | Select-Object -First 1) -replace '.*: ', ''
Write-Host "PC: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Móvil: http://$ip:5173" -ForegroundColor Cyan

# 6. Instrucciones finales
Write-Host "`n📱 6. Como probar:" -ForegroundColor Yellow
Write-Host "• Android: Chrome -> http://$ip:5173 -> 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "• iOS: Safari -> http://$ip:5173 -> Compartir -> 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "• PC: Chrome -> http://localhost:5173 -> Boton instalar en URL o app" -ForegroundColor White

Write-Host "`nVerificacion completada!" -ForegroundColor Green
