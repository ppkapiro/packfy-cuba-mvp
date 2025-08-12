# 🇨🇺 PACKFY CUBA - GUÍA COMPLETA PARA MÓVIL
# ==========================================

Write-Host "📱 PACKFY CUBA - CONFIGURACIÓN MÓVIL" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Obtener IP local
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" } | Select-Object -First 1).IPAddress

if (-not $localIP) {
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.*" } | Select-Object -First 1).IPAddress
}

Write-Host "`n📍 INFORMACIÓN DE CONEXIÓN" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow
Write-Host "IP de tu computadora: $localIP" -ForegroundColor Green
Write-Host "URLs para móvil:" -ForegroundColor Cyan
Write-Host "  🌐 Principal: https://$localIP`:5173/" -ForegroundColor White
Write-Host "  🔍 Rastreo público: https://$localIP`:5173/rastrear" -ForegroundColor White
Write-Host "  ⚙️  Admin: http://$localIP`:8000/admin/" -ForegroundColor White

Write-Host "`n📱 PASOS PARA CONFIGURAR EN MÓVIL" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

Write-Host "1. 📶 CONECTAR A LA MISMA RED Wi-Fi" -ForegroundColor Cyan
Write-Host "   • Asegúrate de que tu móvil esté en la misma red Wi-Fi que la computadora" -ForegroundColor White
Write-Host "   • Verifica que ambos dispositivos puedan comunicarse" -ForegroundColor White

Write-Host "`n2. 🌐 ABRIR EN CHROME MÓVIL" -ForegroundColor Cyan
Write-Host "   • Abre Chrome en tu móvil (recomendado)" -ForegroundColor White
Write-Host "   • Escribe esta URL exacta: https://$localIP`:5173/" -ForegroundColor White
Write-Host "   • NO uses safari u otros navegadores para mejor compatibilidad" -ForegroundColor White

Write-Host "`n3. 🔐 ACEPTAR CERTIFICADO" -ForegroundColor Cyan
Write-Host "   • Si aparece 'Conexión no segura' o similar:" -ForegroundColor White
Write-Host "     - Toca 'Avanzado' o 'Advanced'" -ForegroundColor White
Write-Host "     - Toca 'Continuar a $localIP (no seguro)'" -ForegroundColor White
Write-Host "     - O toca 'Aceptar riesgo y continuar'" -ForegroundColor White

Write-Host "`n4. 📲 INSTALAR COMO PWA (Opcional)" -ForegroundColor Cyan
Write-Host "   • Una vez cargada la página:" -ForegroundColor White
Write-Host "     - En Chrome móvil: Menú → 'Añadir a pantalla de inicio'" -ForegroundColor White
Write-Host "     - En Safari: Compartir → 'Añadir a inicio'" -ForegroundColor White
Write-Host "   • Esto creará un icono como una app nativa" -ForegroundColor White

Write-Host "`n🔧 SOLUCIÓN DE PROBLEMAS" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow

Write-Host "❌ Si no carga la página:" -ForegroundColor Red
Write-Host "   • Verifica que estés en la misma red Wi-Fi" -ForegroundColor White
Write-Host "   • Prueba con HTTP: http://$localIP`:5173/" -ForegroundColor White
Write-Host "   • Verifica que no hay firewall bloqueando" -ForegroundColor White

Write-Host "`n❌ Si aparece 'página en blanco':" -ForegroundColor Red
Write-Host "   • Recarga la página (pull down to refresh)" -ForegroundColor White
Write-Host "   • Limpia caché: Configuración → Privacidad → Limpiar datos" -ForegroundColor White
Write-Host "   • Prueba en modo incógnito" -ForegroundColor White

Write-Host "`n❌ Si el diseño se ve mal:" -ForegroundColor Red
Write-Host "   • Asegúrate de usar Chrome en móvil" -ForegroundColor White
Write-Host "   • Verifica que la página esté completamente cargada" -ForegroundColor White
Write-Host "   • Prueba rotar el dispositivo (vertical/horizontal)" -ForegroundColor White

Write-Host "`n🧪 PROBAR CONECTIVIDAD DESDE MÓVIL" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

Write-Host "Desde tu móvil, prueba estas URLs en orden:" -ForegroundColor Cyan
Write-Host "1. http://$localIP`:8000/admin/ (debe mostrar login Django)" -ForegroundColor White
Write-Host "2. https://$localIP`:5173/ (debe mostrar Packfy)" -ForegroundColor White
Write-Host "3. https://$localIP`:5173/rastrear (debe mostrar rastreo público)" -ForegroundColor White

Write-Host "`n📋 FUNCIONES DISPONIBLES EN MÓVIL" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

Write-Host "✅ Rastreo público (sin login):" -ForegroundColor Green
Write-Host "   • Buscar envíos por nombre de remitente o destinatario" -ForegroundColor White
Write-Host "   • Ver estado y detalles básicos" -ForegroundColor White
Write-Host "   • Interfaz optimizada para touch" -ForegroundColor White

Write-Host "`n✅ Sistema completo (con login):" -ForegroundColor Green
Write-Host "   • Dashboard con estadísticas" -ForegroundColor White
Write-Host "   • Crear nuevos envíos" -ForegroundColor White
Write-Host "   • Gestión completa de envíos" -ForegroundColor White
Write-Host "   • Seguimiento avanzado por nombres" -ForegroundColor White

Write-Host "`n🎯 FUNCIONES ESPECÍFICAS DEL RASTREO POR NOMBRES" -ForegroundColor Yellow
Write-Host "=================================================" -ForegroundColor Yellow

Write-Host "🔍 En la página de Seguimiento:" -ForegroundColor Cyan
Write-Host "   • Ingresa el nombre de la persona (remitente o destinatario)" -ForegroundColor White
Write-Host "   • Selecciona tipo de búsqueda:" -ForegroundColor White
Write-Host "     - 'Remitente y Destinatario' (busca en ambos)" -ForegroundColor White
Write-Host "     - 'Solo Remitente' (quien envía)" -ForegroundColor White
Write-Host "     - 'Solo Destinatario' (quien recibe)" -ForegroundColor White
Write-Host "   • Verás todos los envíos relacionados con esa persona" -ForegroundColor White

Write-Host "`n📱 TESTING RÁPIDO" -ForegroundColor Yellow
Write-Host "==================" -ForegroundColor Yellow

# Probar conectividad
try {
    $testBackend = Test-NetConnection -ComputerName $localIP -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($testBackend) {
        Write-Host "✅ Backend accesible desde red local" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Backend NO accesible desde red local" -ForegroundColor Red
    }
}
catch {
    Write-Host "⚠️  No se pudo probar conectividad del backend" -ForegroundColor Yellow
}

try {
    $testFrontend = Test-NetConnection -ComputerName $localIP -Port 5173 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($testFrontend) {
        Write-Host "✅ Frontend accesible desde red local" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Frontend NO accesible desde red local" -ForegroundColor Red
    }
}
catch {
    Write-Host "⚠️  No se pudo probar conectividad del frontend" -ForegroundColor Yellow
}

Write-Host "`n🔗 ENLACES DIRECTOS PARA COPIAR" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow
Write-Host "Copia estos enlaces y envíalos a tu móvil:" -ForegroundColor Cyan
Write-Host "https://$localIP`:5173/" -ForegroundColor White -BackgroundColor Blue
Write-Host "https://$localIP`:5173/rastrear" -ForegroundColor White -BackgroundColor Blue

Write-Host "`n🇨🇺 ¡Packfy Cuba listo para móvil!" -ForegroundColor Green
