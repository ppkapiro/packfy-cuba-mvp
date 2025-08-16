# 📱 PACKFY CUBA - Diagnóstico Móvil Completo v4.0
# Script para verificar el acceso móvil HTTPS

Write-Host "🇨🇺 === PACKFY CUBA - DIAGNÓSTICO MÓVIL COMPLETO ===" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar estado de contenedores
Write-Host "📦 ESTADO DE CONTENEDORES:" -ForegroundColor Yellow
docker-compose ps

Write-Host ""

# 2. Verificar frontend
Write-Host "🌐 FRONTEND (Puerto 5173):" -ForegroundColor Yellow
Write-Host "✅ Probando acceso HTTPS al frontend..."
try {
    $frontendResponse = curl -k -s -o /dev/null -w "%{http_code}" https://192.168.12.178:5173
    Write-Host "   Estado: HTTP $frontendResponse" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Error en frontend: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Verificar backend API
Write-Host ""
Write-Host "🔧 BACKEND API (Puerto 8443):" -ForegroundColor Yellow
Write-Host "✅ Probando acceso HTTPS al backend..."
try {
    $backendResponse = curl -k -s -o /dev/null -w "%{http_code}" https://192.168.12.178:8443/api/
    Write-Host "   Estado: HTTP $backendResponse" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Error en backend: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Verificar certificados SSL
Write-Host ""
Write-Host "🔐 CERTIFICADOS SSL:" -ForegroundColor Yellow
if (Test-Path "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend\certs\localhost.crt") {
    Write-Host "   ✅ Certificado frontend: OK" -ForegroundColor Green
}
else {
    Write-Host "   ❌ Certificado frontend: NO ENCONTRADO" -ForegroundColor Red
}

if (Test-Path "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend\certs\localhost.crt") {
    Write-Host "   ✅ Certificado backend: OK" -ForegroundColor Green
}
else {
    Write-Host "   ❌ Certificado backend: NO ENCONTRADO" -ForegroundColor Red
}

# 5. Verificar red Docker
Write-Host ""
Write-Host "🌐 RED DOCKER:" -ForegroundColor Yellow
docker network inspect packfy-cuba-mvp_default | Select-String -Pattern "192\.168|172\.20" | ForEach-Object {
    Write-Host "   📍 $_" -ForegroundColor Cyan
}

# 6. Mostrar IPs de acceso móvil
Write-Host ""
Write-Host "📱 ACCESO MÓVIL - URLs PARA PROBAR:" -ForegroundColor Yellow
Write-Host "   🌐 Frontend: https://192.168.12.178:5173" -ForegroundColor Cyan
Write-Host "   🔧 Backend:  https://192.168.12.178:8443" -ForegroundColor Cyan
Write-Host ""

# 7. Logs recientes del frontend
Write-Host "📝 LOGS RECIENTES FRONTEND:" -ForegroundColor Yellow
docker-compose logs frontend --tail=5

Write-Host ""
Write-Host "🎉 DIAGNÓSTICO COMPLETADO" -ForegroundColor Green
Write-Host ""
Write-Host "📱 INSTRUCCIONES PARA MÓVIL:" -ForegroundColor Cyan
Write-Host "   1. Conecta tu móvil a la misma red WiFi" -ForegroundColor White
Write-Host "   2. Abre el navegador móvil" -ForegroundColor White
Write-Host "   3. Ve a: https://192.168.12.178:5173" -ForegroundColor White
Write-Host "   4. Acepta el certificado SSL cuando se solicite" -ForegroundColor White
Write-Host "   5. La aplicación debería cargar normalmente" -ForegroundColor White
Write-Host ""
