# PACKFY CUBA PWA - SOLUCION PROBLEMA INSTALACION CHROME

Write-Host ""
Write-Host "🔧 CAMBIOS IMPLEMENTADOS PARA CHROME:" -ForegroundColor Yellow
Write-Host ""

Write-Host "✅ Service Worker recreado (sin errores de codificacion)" -ForegroundColor Green
Write-Host "✅ Prompt de instalacion mas agresivo (1 segundo)" -ForegroundColor Green  
Write-Host "✅ Boton manual flotante agregado" -ForegroundColor Green
Write-Host "✅ Segundo intento si usuario rechaza" -ForegroundColor Green
Write-Host "✅ Instrucciones iOS para Safari" -ForegroundColor Green

Write-Host ""
Write-Host "📱 COMO PROBAR EN CHROME MOVIL:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ve a: http://192.168.12.178:5173" -ForegroundColor White
Write-Host "2. Abre DevTools (F12) en PC primero para verificar" -ForegroundColor Yellow  
Write-Host "3. Ve a Application > Manifest (debe estar sin errores)" -ForegroundColor Yellow
Write-Host "4. Ve a Application > Service Workers (debe estar activo)" -ForegroundColor Yellow
Write-Host "5. Luego abre en tu movil Chrome" -ForegroundColor White
Write-Host "6. Debe aparecer banner automatico O boton flotante" -ForegroundColor Green

Write-Host ""
Write-Host "🔍 VERIFICACION RAPIDA:" -ForegroundColor Magenta
try {
    $response = Invoke-WebRequest "http://localhost:5173/manifest.json" -TimeoutSec 5
    Write-Host "✅ Manifest accesible (200 OK)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error accediendo manifest" -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest "http://localhost:5173/sw.js" -TimeoutSec 5  
    Write-Host "✅ Service Worker accesible (200 OK)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error accediendo Service Worker" -ForegroundColor Red
}

Write-Host ""
Write-Host "💡 SI AUN NO APARECE EL BANNER:" -ForegroundColor Yellow
Write-Host "• Busca el boton flotante '📱 Instalar Packfy Cuba' abajo-derecha" -ForegroundColor White
Write-Host "• O ve al menu Chrome > 'Agregar a pantalla de inicio'" -ForegroundColor White  
Write-Host "• Verifica que Chrome este actualizado" -ForegroundColor White
Write-Host "• Asegurate de usar HTTPS en produccion" -ForegroundColor White

Write-Host ""
Write-Host "🇨🇺 URL PARA TU MOVIL: http://192.168.12.178:5173 🇨🇺" -ForegroundColor Red
Write-Host ""
