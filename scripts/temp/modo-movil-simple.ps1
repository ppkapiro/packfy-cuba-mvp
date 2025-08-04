# Script para modo movil - Sin HMR
Write-Host "Iniciando modo movil (sin HMR)..." -ForegroundColor Green

# Crear configuracion temporal sin HMR
$envContent = @"
VITE_API_BASE_URL=http://192.168.12.179:8000
VITE_DISABLE_HMR=true
NODE_ENV=production
"@

Write-Host "Configurando variables de entorno para movil..." -ForegroundColor Cyan
$envContent | Out-File -FilePath "frontend\.env" -Encoding UTF8

# Reiniciar frontend
Write-Host "Reiniciando frontend en modo movil..." -ForegroundColor Yellow
docker-compose restart frontend

Write-Host "Esperando que el frontend este listo..." -ForegroundColor Blue
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "Frontend configurado para movil!" -ForegroundColor Green
Write-Host "URLs para acceder desde movil:" -ForegroundColor Yellow
Write-Host "   http://192.168.12.179:5173" -ForegroundColor White
Write-Host "   http://192.168.12.179:5173/test-ip.html" -ForegroundColor White

Write-Host ""
Write-Host "Credenciales:" -ForegroundColor Yellow
Write-Host "   test@test.com / 123456" -ForegroundColor White

Write-Host ""
Write-Host "Caracteristicas del modo movil:" -ForegroundColor Cyan
Write-Host "   Sin actualizaciones automaticas (HMR deshabilitado)" -ForegroundColor Green
Write-Host "   Configuracion optimizada para acceso por IP" -ForegroundColor Green
Write-Host "   Proxy configurado para backend movil" -ForegroundColor Green

Write-Host ""
Write-Host "Para volver al modo desarrollo normal:" -ForegroundColor Yellow
Write-Host "   Ejecuta: .\dev.ps1" -ForegroundColor White

Read-Host "`nPresiona Enter para continuar"
