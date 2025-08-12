# 📱 TESTING PWA MÓVIL - PACKFY CUBA v2.0
# Guía completa para verificar instalación en dispositivos móviles

Write-Host "📱 PACKFY CUBA - TESTING PWA MÓVIL v2.0" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 ESTADO DE SERVICIOS:" -ForegroundColor Yellow
Write-Host ""

# Verificar que Docker esté corriendo
try {
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}"
    Write-Host "✅ Contenedores Docker:" -ForegroundColor Green
    Write-Host $containers -ForegroundColor White
} catch {
    Write-Host "❌ Error: Docker no está corriendo" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🌐 URLs DE ACCESO:" -ForegroundColor Yellow
Write-Host ""
Write-Host "📱 Principal:" -ForegroundColor Blue
Write-Host "   🔗 http://localhost:5173/" -ForegroundColor White
Write-Host ""
Write-Host "🖥️ Para otros dispositivos en la red:" -ForegroundColor Blue

# Obtener IP local
try {
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi" | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress
    if ($ipAddress) {
        Write-Host "   🔗 http://$ipAddress:5173/" -ForegroundColor White
        Write-Host "   📲 Escanea con tu móvil o accede desde otra red" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️ No se pudo obtener IP local" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📱 TESTING EN MÓVIL - PASOS:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1️⃣ ACCESO INICIAL:" -ForegroundColor Magenta
Write-Host "   ✅ Abre Chrome/Safari en tu móvil" -ForegroundColor White
Write-Host "   ✅ Ve a la URL principal" -ForegroundColor White
Write-Host "   ✅ Espera 3 segundos para prompt automático" -ForegroundColor White
Write-Host ""

Write-Host "2️⃣ INSTALACIÓN PWA:" -ForegroundColor Magenta
Write-Host "   📱 Android Chrome:" -ForegroundColor Blue
Write-Host "      • Aparecerá banner 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "      • O toca menú (⋮) → 'Instalar aplicación'" -ForegroundColor White
Write-Host ""
Write-Host "   🍎 iOS Safari:" -ForegroundColor Blue
Write-Host "      • Toca botón compartir 📤" -ForegroundColor White
Write-Host "      • Selecciona 'Agregar a la pantalla de inicio'" -ForegroundColor White
Write-Host "      • Confirma 'Agregar'" -ForegroundColor White
Write-Host ""

Write-Host "3️⃣ VERIFICACIÓN POST-INSTALACIÓN:" -ForegroundColor Magenta
Write-Host "   ✅ Icono 'Packfy' en pantalla de inicio" -ForegroundColor Green
Write-Host "   ✅ Abre como app nativa (sin barra URL)" -ForegroundColor Green
Write-Host "   ✅ Animaciones fluidas" -ForegroundColor Green
Write-Host "   ✅ Funciona sin internet (offline)" -ForegroundColor Green
Write-Host ""

Write-Host "🎯 FUNCIONALIDADES A PROBAR:" -ForegroundColor Yellow
Write-Host ""
Write-Host "✨ ANIMACIONES:" -ForegroundColor Cyan
Write-Host "   🇨🇺 Bandera flotante" -ForegroundColor White
Write-Host "   💫 Título con gradiente animado" -ForegroundColor White
Write-Host "   🎨 Tarjetas con hover 3D" -ForegroundColor White
Write-Host "   ⚡ Transiciones suaves" -ForegroundColor White
Write-Host ""

Write-Host "💎 FREEMIUM:" -ForegroundColor Cyan
Write-Host "   🆓 Modo Simple (gratuito)" -ForegroundColor White
Write-Host "   💰 Modo Premium ($5 USD)" -ForegroundColor White
Write-Host "   🔄 Cambio entre modos" -ForegroundColor White
Write-Host ""

Write-Host "📱 RESPONSIVE:" -ForegroundColor Cyan
Write-Host "   👆 Touch optimizado" -ForegroundColor White
Write-Host "   📐 Se adapta a pantalla" -ForegroundColor White
Write-Host "   🔄 Orientación vertical/horizontal" -ForegroundColor White
Write-Host ""

Write-Host "🔧 TROUBLESHOOTING:" -ForegroundColor Red
Write-Host ""
Write-Host "❓ Si no aparece prompt de instalación:" -ForegroundColor Yellow
Write-Host "   1. Recarga página (↻)" -ForegroundColor White
Write-Host "   2. Borra datos del sitio" -ForegroundColor White
Write-Host "   3. Intenta modo incógnito" -ForegroundColor White
Write-Host ""

Write-Host "❓ Si no se ve bien:" -ForegroundColor Yellow
Write-Host "   1. Fuerza recarga completa" -ForegroundColor White
Write-Host "   2. Verifica Service Worker en DevTools" -ForegroundColor White
Write-Host "   3. Limpia cache del navegador" -ForegroundColor White
Write-Host ""

Write-Host "🎉 RESULTADO ESPERADO:" -ForegroundColor Green
Write-Host ""
Write-Host "✅ App instalada como nativa" -ForegroundColor Green
Write-Host "✅ Icono personalizado Packfy Cuba" -ForegroundColor Green  
Write-Host "✅ Funciona offline" -ForegroundColor Green
Write-Host "✅ Animaciones fluidas" -ForegroundColor Green
Write-Host "✅ Interface responsive perfecta" -ForegroundColor Green
Write-Host ""

Write-Host "📞 ¿LISTO PARA PROBAR?" -ForegroundColor Green
Write-Host "Abre tu móvil y ve a la URL principal 🚀" -ForegroundColor Yellow
Write-Host ""

# Test de conectividad rápido
Write-Host "🔍 Testing conectividad rápida..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173/" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Servidor funcionando correctamente" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error: Servidor no responde" -ForegroundColor Red
    Write-Host "💡 Ejecuta: docker-compose up -d" -ForegroundColor Yellow
}
