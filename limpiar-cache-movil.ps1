# 🇨🇺 PACKFY CUBA - Limpieza de Cache Móvil v4.0
# Script para forzar limpieza de cache y resolver problemas de HTTP 500

Write-Host "🧹 === LIMPIEZA COMPLETA DE CACHE MÓVIL ===" -ForegroundColor Cyan
Write-Host ""

# 1. Limpiar cache del servidor
Write-Host "1. 🧹 LIMPIANDO CACHE DEL SERVIDOR..." -ForegroundColor Yellow

Write-Host "   • Reiniciando frontend con cache limpio..." -ForegroundColor White
docker-compose exec frontend rm -rf /app/node_modules/.vite 2>$null
docker-compose exec frontend rm -rf /app/dist 2>$null
docker-compose restart frontend

Write-Host "   • Limpiando cache de Django..." -ForegroundColor White
docker-compose exec backend python manage.py clear_cache 2>$null

Write-Host "   ✅ Cache del servidor limpiado" -ForegroundColor Green

Write-Host ""

# 2. Forzar recarga con versioning
Write-Host "2. 🔄 FORZANDO NUEVA VERSIÓN..." -ForegroundColor Yellow

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Write-Host "   • Nuevo timestamp: $timestamp" -ForegroundColor Cyan
Write-Host "   • URL con cache-busting: https://192.168.12.178:5173?v=$timestamp" -ForegroundColor Cyan

Write-Host ""

# 3. Instrucciones detalladas para móvil
Write-Host "3. 📱 INSTRUCCIONES PARA LIMPIAR CACHE EN MÓVIL:" -ForegroundColor Red
Write-Host ""

Write-Host "🤖 ANDROID (Chrome):" -ForegroundColor Green
Write-Host "   1. Abre Chrome en tu móvil" -ForegroundColor White
Write-Host "   2. Toca los 3 puntos (⋮) en la esquina superior derecha" -ForegroundColor White
Write-Host "   3. Selecciona 'Configuración'" -ForegroundColor White
Write-Host "   4. Toca 'Privacidad y seguridad'" -ForegroundColor White
Write-Host "   5. Selecciona 'Borrar datos de navegación'" -ForegroundColor White
Write-Host "   6. Marca 'Imágenes y archivos en caché'" -ForegroundColor White
Write-Host "   7. Toca 'Borrar datos'" -ForegroundColor White
Write-Host ""

Write-Host "🍎 iOS (Safari):" -ForegroundColor Blue
Write-Host "   1. Ve a Configuración → Safari" -ForegroundColor White
Write-Host "   2. Desplázate hacia abajo" -ForegroundColor White
Write-Host "   3. Toca 'Borrar historial y datos de sitios web'" -ForegroundColor White
Write-Host "   4. Confirma tocando 'Borrar historial y datos'" -ForegroundColor White
Write-Host ""

Write-Host "🔄 MÉTODO RÁPIDO PARA CUALQUIER NAVEGADOR:" -ForegroundColor Magenta
Write-Host "   1. Abre el navegador móvil" -ForegroundColor White
Write-Host "   2. Ve a la URL: https://192.168.12.178:5173?v=$timestamp" -ForegroundColor Cyan
Write-Host "   3. Mantén presionado el botón de recargar (🔄)" -ForegroundColor White
Write-Host "   4. Selecciona 'Recarga completa' o 'Hard refresh'" -ForegroundColor White
Write-Host ""

Write-Host "🚨 SI AÚN NO FUNCIONA:" -ForegroundColor Red
Write-Host ""

Write-Host "📋 MÉTODO ALTERNATIVO 1 - Modo Incógnito:" -ForegroundColor Yellow
Write-Host "   1. Abre una ventana de incógnito/privada en el móvil" -ForegroundColor White
Write-Host "   2. Ve a: https://192.168.12.178:5173" -ForegroundColor White
Write-Host "   3. Esto ignora completamente el cache" -ForegroundColor White
Write-Host ""

Write-Host "📋 MÉTODO ALTERNATIVO 2 - Reiniciar navegador:" -ForegroundColor Yellow
Write-Host "   1. Cierra completamente el navegador móvil" -ForegroundColor White
Write-Host "   2. Ve a las aplicaciones recientes y desliza para cerrar" -ForegroundColor White
Write-Host "   3. Espera 10 segundos" -ForegroundColor White
Write-Host "   4. Abre el navegador de nuevo" -ForegroundColor White
Write-Host "   5. Ve a: https://192.168.12.178:5173?v=$timestamp" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 MÉTODO ALTERNATIVO 3 - Diferentes navegadores:" -ForegroundColor Yellow
Write-Host "   • Prueba con Chrome si usabas Safari" -ForegroundColor White
Write-Host "   • Prueba con Firefox si usabas Chrome" -ForegroundColor White
Write-Host "   • Prueba con Edge si usabas otros" -ForegroundColor White
Write-Host ""

# 4. Verificar que el servidor esté respondiendo correctamente
Write-Host "4. ✅ VERIFICANDO SERVIDOR DESPUÉS DE LIMPIEZA:" -ForegroundColor Yellow

Start-Sleep 5

$frontendStatus = curl -k -s -o /dev/null -w "%{http_code}" https://192.168.12.178:5173
$backendStatus = curl -k -s -o /dev/null -w "%{http_code}" https://192.168.12.178:8443/api/

Write-Host "   Frontend: HTTP $frontendStatus $(if($frontendStatus -eq '200') { '✅' } else { '❌' })" -ForegroundColor $(if ($frontendStatus -eq '200') { 'Green' } else { 'Red' })
Write-Host "   Backend:  HTTP $backendStatus $(if($backendStatus -eq '401') { '✅' } else { '❌' })" -ForegroundColor $(if ($backendStatus -eq '401') { 'Green' } else { 'Red' })

Write-Host ""

if ($frontendStatus -eq "200" -and $backendStatus -eq "401") {
    Write-Host "🎉 SERVIDOR FUNCIONANDO CORRECTAMENTE" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 AHORA PRUEBA EN TU MÓVIL CON CACHE LIMPIO:" -ForegroundColor Cyan
    Write-Host "   URL: https://192.168.12.178:5173?v=$timestamp" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Si seguís teniendo problemas, usa el modo incógnito primero." -ForegroundColor Yellow
}
else {
    Write-Host "❌ PROBLEMA EN EL SERVIDOR - VERIFICAR LOGS" -ForegroundColor Red
    Write-Host "   Ejecuta: docker-compose logs --tail=20" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 CONSEJO: Guarda esta URL con timestamp en favoritos móviles" -ForegroundColor Cyan
Write-Host "    para futuras actualizaciones: https://192.168.12.178:5173?v=$timestamp" -ForegroundColor White
Write-Host ""
