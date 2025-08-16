# 🇨🇺 PACKFY CUBA - Test Final Móvil v4.0
# Verificación completa del sistema después del rebuild

Write-Host "🇨🇺 === TEST FINAL MÓVIL - POST REBUILD ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Verificar contenedores
Write-Host "1. 📦 CONTENEDORES:" -ForegroundColor Yellow
$containers = docker-compose ps --format json | ConvertFrom-Json
foreach ($container in $containers) {
    $status = if ($container.State -eq "running") { "✅ ACTIVO" } else { "❌ INACTIVO" }
    Write-Host "   $($container.Service): $status" -ForegroundColor $(if ($container.State -eq "running") { "Green" } else { "Red" })
}

Write-Host ""

# Test 2: Verificar conectividad frontend
Write-Host "2. 🌐 FRONTEND HTTPS:" -ForegroundColor Yellow
try {
    $frontendResponse = curl -k -s -o /dev/null -w "%{http_code}" https://192.168.12.178:5173
    $frontendStatus = if ($frontendResponse -eq "200") { "✅ FUNCIONANDO" } else { "❌ ERROR ($frontendResponse)" }
    Write-Host "   Estado: $frontendStatus" -ForegroundColor $(if ($frontendResponse -eq "200") { "Green" } else { "Red" })
}
catch {
    Write-Host "   ❌ ERROR DE CONEXIÓN" -ForegroundColor Red
}

# Test 3: Verificar conectividad backend
Write-Host ""
Write-Host "3. 🔧 BACKEND API:" -ForegroundColor Yellow
try {
    $backendResponse = curl -k -s -o /dev/null -w "%{http_code}" https://192.168.12.178:8443/api/
    $backendStatus = if ($backendResponse -eq "401") { "✅ FUNCIONANDO" } else { "❌ ERROR ($backendResponse)" }
    Write-Host "   Estado: $backendStatus" -ForegroundColor $(if ($backendResponse -eq "401") { "Green" } else { "Red" })
}
catch {
    Write-Host "   ❌ ERROR DE CONEXIÓN" -ForegroundColor Red
}

# Test 4: Verificar certificados
Write-Host ""
Write-Host "4. 🔐 CERTIFICADOS SSL:" -ForegroundColor Yellow
$frontendCert = Test-Path "frontend/certs/localhost.crt"
$backendCert = Test-Path "backend/certs/localhost.crt"

Write-Host "   Frontend: $(if($frontendCert) { "✅ OK" } else { "❌ FALTANTE" })" -ForegroundColor $(if ($frontendCert) { "Green" } else { "Red" })
Write-Host "   Backend:  $(if($backendCert) { "✅ OK" } else { "❌ FALTANTE" })" -ForegroundColor $(if ($backendCert) { "Green" } else { "Red" })

# Test 5: Test de contenido HTML
Write-Host ""
Write-Host "5. 📄 CONTENIDO HTML:" -ForegroundColor Yellow
try {
    $htmlContent = curl -k -s https://192.168.12.178:5173
    $hasPWA = $htmlContent -match "PWA" -or $htmlContent -match "mobile-web-app"
    $hasTitle = $htmlContent -match "Packfy Cuba"

    Write-Host "   PWA Meta Tags: $(if($hasPWA) { "✅ PRESENTES" } else { "❌ FALTANTES" })" -ForegroundColor $(if ($hasPWA) { "Green" } else { "Red" })
    Write-Host "   Título correcto: $(if($hasTitle) { "✅ OK" } else { "❌ FALTANTE" })" -ForegroundColor $(if ($hasTitle) { "Green" } else { "Red" })
}
catch {
    Write-Host "   ❌ NO SE PUDO OBTENER CONTENIDO" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 === RESULTADO FINAL ===" -ForegroundColor Magenta

# Evaluar estado general
$allGood = $frontendResponse -eq "200" -and $backendResponse -eq "401" -and $frontendCert -and $backendCert

if ($allGood) {
    Write-Host "✅ SISTEMA COMPLETAMENTE FUNCIONAL PARA MÓVIL" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 LISTO PARA PROBAR EN TU MÓVIL:" -ForegroundColor Cyan
    Write-Host "   URL: https://192.168.12.178:5173" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 El error HTTP 500 debería estar resuelto." -ForegroundColor Green
}
else {
    Write-Host "❌ SISTEMA CON PROBLEMAS - REVISAR LOGS" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Ejecuta: docker-compose logs --tail=20" -ForegroundColor Yellow
}

Write-Host ""
