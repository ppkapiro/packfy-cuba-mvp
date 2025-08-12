# PACKFY CUBA - PRUEBA DE ACCESO CHROME LOCAL
# Script para probar diferentes metodos de acceso

Write-Host "PACKFY - PRUEBA DE ACCESO CHROME" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

Write-Host "`n1. Verificando servicios..." -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}" | Select-Object -First 4

Write-Host "`n2. URLs disponibles:" -ForegroundColor Cyan
Write-Host "   HTTPS: https://localhost:5173" -ForegroundColor White
Write-Host "   HTTP:  http://localhost:5173 (puede no funcionar)" -ForegroundColor Gray
Write-Host "   IP:    https://192.168.12.178:5173" -ForegroundColor White

Write-Host "`n3. Abriendo Chrome con configuracion especial..." -ForegroundColor Cyan

# Opcion 1: HTTPS localhost
Write-Host "`n   Intentando HTTPS localhost..." -ForegroundColor Yellow
Start-Process "chrome.exe" -ArgumentList @(
    "--ignore-certificate-errors",
    "--ignore-ssl-errors", 
    "--allow-running-insecure-content",
    "--disable-web-security",
    "--user-data-dir=C:\temp\chrome-packfy-https",
    "https://localhost:5173"
)

Start-Sleep 3

# Opcion 2: IP local con HTTPS
Write-Host "   Intentando IP local con HTTPS..." -ForegroundColor Yellow
Start-Process "chrome.exe" -ArgumentList @(
    "--ignore-certificate-errors",
    "--ignore-ssl-errors",
    "--allow-running-insecure-content", 
    "--disable-web-security",
    "--user-data-dir=C:\temp\chrome-packfy-ip",
    "https://192.168.12.178:5173"
)

Write-Host "`n4. Instrucciones:" -ForegroundColor Green
Write-Host "   - Se abrieron 2 ventanas de Chrome" -ForegroundColor White
Write-Host "   - Si aparece 'No es seguro', haz clic en 'Avanzado' > 'Acceder'" -ForegroundColor White  
Write-Host "   - Prueba ambas URLs para ver cual funciona mejor" -ForegroundColor White

Write-Host "`n5. Credenciales para login:" -ForegroundColor Cyan
Write-Host "   Email: admin@packfy.cu" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White

Write-Host "`n6. Si no funciona ninguna, ejecuta:" -ForegroundColor Red
Write-Host "   docker restart packfy-frontend" -ForegroundColor White
Write-Host "   y vuelve a intentar" -ForegroundColor White
