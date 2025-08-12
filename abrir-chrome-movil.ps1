# PACKFY CUBA - SCRIPT DE PRUEBA PARA MOVIL
# Abre Chrome con configuracion especial para certificados

$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress

Write-Host "📱 ABRIENDO PACKFY PARA MOVIL" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

Write-Host "`n1. IP detectada: $ip" -ForegroundColor Cyan
Write-Host "2. Abriendo Chrome con configuracion especial..." -ForegroundColor Cyan

# Abrir Chrome con configuracion para aceptar certificados
Start-Process "chrome.exe" -ArgumentList @(
    "--ignore-certificate-errors",
    "--ignore-ssl-errors", 
    "--allow-running-insecure-content",
    "--disable-web-security",
    "--disable-features=VizDisplayCompositor",
    "--user-data-dir=C:\temp\chrome-packfy-movil",
    "https://$ip`:5173"
)

Write-Host "`n3. Chrome abierto con URL movil: https://$ip`:5173" -ForegroundColor Green

Write-Host "`n4. Instrucciones:" -ForegroundColor Yellow
Write-Host "   - Si aparece 'No es seguro', acepta el certificado" -ForegroundColor White
Write-Host "   - Usa Ctrl+Shift+I para abrir DevTools si hay errores" -ForegroundColor White
Write-Host "   - Revisa la consola para mensajes de error" -ForegroundColor White

Write-Host "`n5. Credenciales de login:" -ForegroundColor Cyan
Write-Host "   Email: admin@packfy.cu" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White

Write-Host "`n6. Si 'Failed to fetch':" -ForegroundColor Red
Write-Host "   - Revisa la consola del navegador (F12)" -ForegroundColor Yellow
Write-Host "   - Verifica que no haya errores de CORS" -ForegroundColor Yellow
Write-Host "   - Asegurate de aceptar el certificado primero" -ForegroundColor Yellow

Write-Host "`nListo para probar!" -ForegroundColor Green
