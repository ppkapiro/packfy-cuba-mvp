# 🇨🇺 PACKFY CUBA - URLs Anti-Cache para Móvil
# URLs específicas que evitan problemas de cache

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$random = Get-Random -Minimum 1000 -Maximum 9999

Write-Host "📱 === URLS ANTI-CACHE PARA MÓVIL ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 USA ESTAS URLS EN TU MÓVIL (copia exactamente):" -ForegroundColor Green
Write-Host ""

Write-Host "📋 URL PRINCIPAL con timestamp:" -ForegroundColor Yellow
Write-Host "https://192.168.12.178:5173?v=$timestamp&r=$random" -ForegroundColor White
Write-Host ""

Write-Host "📋 URL ALTERNATIVA con hash:" -ForegroundColor Yellow
Write-Host "https://192.168.12.178:5173?nocache=true&t=$timestamp" -ForegroundColor White
Write-Host ""

Write-Host "📋 URL FORZADA sin cache:" -ForegroundColor Yellow
Write-Host "https://192.168.12.178:5173?cache=false&reload=true&v=$timestamp" -ForegroundColor White
Write-Host ""

Write-Host "🔍 VERIFICANDO SERVIDOR..." -ForegroundColor Cyan
Start-Sleep 3

$status = curl -k -s -o /dev/null -w "%{http_code}" "https://192.168.12.178:5173?v=$timestamp"
Write-Host "Estado del servidor: HTTP $status $(if($status -eq '200') { '✅ OK' } else { '❌ ERROR' })" -ForegroundColor $(if ($status -eq '200') { 'Green' } else { 'Red' })

Write-Host ""
Write-Host "📱 PASOS PARA TU MÓVIL:" -ForegroundColor Magenta
Write-Host ""
Write-Host "1. 🧹 LIMPIA EL CACHE PRIMERO:" -ForegroundColor Red
Write-Host "   • Android: Configuración → Apps → Chrome → Almacenamiento → Borrar cache" -ForegroundColor White
Write-Host "   • iOS: Configuración → Safari → Borrar historial y datos" -ForegroundColor White
Write-Host ""

Write-Host "2. 🌐 USA MODO INCÓGNITO:" -ForegroundColor Red
Write-Host "   • Abre una ventana privada/incógnito" -ForegroundColor White
Write-Host "   • Esto garantiza que no hay cache previo" -ForegroundColor White
Write-Host ""

Write-Host "3. 🔗 COPIA UNA DE ESTAS URLS:" -ForegroundColor Red
Write-Host "   https://192.168.12.178:5173?v=$timestamp&r=$random" -ForegroundColor Cyan
Write-Host ""

Write-Host "4. ✅ ACEPTA EL CERTIFICADO SSL" -ForegroundColor Red
Write-Host "   • Aparecerá advertencia de seguridad" -ForegroundColor White
Write-Host "   • Toca 'Avanzado' → 'Continuar al sitio'" -ForegroundColor White
Write-Host ""

Write-Host "🚨 SI AÚN DA ERROR HTTP 500:" -ForegroundColor Red
Write-Host ""
Write-Host "🔄 MÉTODO DE EMERGENCIA:" -ForegroundColor Yellow
Write-Host "   1. Cierra completamente el navegador móvil" -ForegroundColor White
Write-Host "   2. Reinicia tu móvil" -ForegroundColor White
Write-Host "   3. Conecta a WiFi nuevamente" -ForegroundColor White
Write-Host "   4. Abre navegador en modo incógnito" -ForegroundColor White
Write-Host "   5. Va a: https://192.168.12.178:5173?emergency=$timestamp" -ForegroundColor Cyan
Write-Host ""

Write-Host "💡 CONSEJO:" -ForegroundColor Green
Write-Host "   Guarda una de estas URLs en favoritos para futuras actualizaciones" -ForegroundColor White
Write-Host ""

# Crear archivo con las URLs para fácil acceso
$urlsContent = @"
🇨🇺 PACKFY CUBA - URLs Anti-Cache Móvil
Generado: $(Get-Date)

URL Principal:
https://192.168.12.178:5173?v=$timestamp&r=$random

URL Alternativa:
https://192.168.12.178:5173?nocache=true&t=$timestamp

URL Forzada:
https://192.168.12.178:5173?cache=false&reload=true&v=$timestamp

URL de Emergencia:
https://192.168.12.178:5173?emergency=$timestamp

Instrucciones:
1. Limpia cache del navegador móvil
2. Usa modo incógnito
3. Copia una URL exactamente
4. Acepta certificado SSL
"@

$urlsContent | Out-File -FilePath "urls-movil-anticache.txt" -Encoding UTF8
Write-Host "📄 URLs guardadas en: urls-movil-anticache.txt" -ForegroundColor Cyan
Write-Host ""
