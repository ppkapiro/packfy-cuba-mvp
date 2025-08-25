# 📱 PACKFY CUBA - Guía de Acceso Móvil v4.0
# Instrucciones paso a paso para acceder desde móvil

Write-Host "🇨🇺 === PACKFY CUBA - ACCESO MÓVIL ===" -ForegroundColor Cyan
Write-Host ""

# Verificar estado del sistema
Write-Host "🔍 VERIFICANDO SISTEMA..." -ForegroundColor Yellow

$frontendStatus = curl -k -s -o /dev/null -w "%{http_code}" https://192.168.12.178:5173
$backendStatus = curl -k -s -o /dev/null -w "%{http_code}" https://192.168.12.178:8443/api/

Write-Host "   Frontend: HTTP $frontendStatus" -ForegroundColor $(if ($frontendStatus -eq "200") { "Green" } else { "Red" })
Write-Host "   Backend:  HTTP $backendStatus" -ForegroundColor $(if ($backendStatus -eq "401") { "Green" } else { "Red" })

if ($frontendStatus -eq "200" -and $backendStatus -eq "401") {
    Write-Host "   ✅ Sistema funcionando correctamente" -ForegroundColor Green
}
else {
    Write-Host "   ❌ Sistema con problemas" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📱 INSTRUCCIONES PARA MÓVIL:" -ForegroundColor Green
Write-Host ""

Write-Host "1. 📶 CONECTAR A LA MISMA RED WIFI" -ForegroundColor Yellow
Write-Host "   - Asegúrate de que tu móvil esté en la misma red WiFi que tu PC" -ForegroundColor White
Write-Host ""

Write-Host "2. 🌐 ABRIR NAVEGADOR MÓVIL" -ForegroundColor Yellow
Write-Host "   - Abre Chrome, Safari, o tu navegador preferido en el móvil" -ForegroundColor White
Write-Host ""

Write-Host "3. 🔗 ACCEDER A LA APLICACIÓN" -ForegroundColor Yellow
Write-Host "   URL: https://192.168.12.178:5173" -ForegroundColor Cyan
Write-Host "   - Copia y pega esta URL exacta en el navegador móvil" -ForegroundColor White
Write-Host ""

Write-Host "4. 🔐 ACEPTAR CERTIFICADO SSL" -ForegroundColor Yellow
Write-Host "   - El navegador mostrará una advertencia de seguridad" -ForegroundColor White
Write-Host "   - En Chrome: Toca 'Avanzado' → 'Acceder a 192.168.12.178 (no seguro)'" -ForegroundColor White
Write-Host "   - En Safari: Toca 'Continuar'" -ForegroundColor White
Write-Host "   - Esto es NORMAL para certificados autofirmados" -ForegroundColor Cyan
Write-Host ""

Write-Host "5. 📱 INSTALAR PWA (OPCIONAL)" -ForegroundColor Yellow
Write-Host "   - Una vez cargada la app, aparecerá opción 'Instalar'" -ForegroundColor White
Write-Host "   - Esto creará un icono en tu pantalla de inicio" -ForegroundColor White
Write-Host ""

Write-Host "🚨 SOLUCIÓN DE PROBLEMAS:" -ForegroundColor Red
Write-Host ""
Write-Host "❌ Si sale 'Sitio no disponible':" -ForegroundColor Yellow
Write-Host "   - Verifica que estés en la misma red WiFi" -ForegroundColor White
Write-Host "   - Prueba recargar la página" -ForegroundColor White
Write-Host ""

Write-Host "❌ Si sale error HTTP 500:" -ForegroundColor Yellow
Write-Host "   - Acepta el certificado SSL primero" -ForegroundColor White
Write-Host "   - Espera 30 segundos y recarga" -ForegroundColor White
Write-Host ""

Write-Host "❌ Si no carga completamente:" -ForegroundColor Yellow
Write-Host "   - Limpia caché del navegador móvil" -ForegroundColor White
Write-Host "   - Reinicia el navegador y vuelve a intentar" -ForegroundColor White
Write-Host ""

Write-Host "📞 CONTACTO DE SOPORTE:" -ForegroundColor Cyan
Write-Host "   Si tienes problemas, documenta:" -ForegroundColor White
Write-Host "   - Modelo de tu móvil" -ForegroundColor White
Write-Host "   - Navegador que usas" -ForegroundColor White
Write-Host "   - Error exacto que aparece" -ForegroundColor White
Write-Host ""

Write-Host "🎉 ¡DISFRUTA PACKFY CUBA EN TU MÓVIL!" -ForegroundColor Green
