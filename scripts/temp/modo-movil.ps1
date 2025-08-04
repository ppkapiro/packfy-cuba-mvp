# Script para modo móvil - Sin HMR para evitar actualizaciones constantes
Write-Host "📱 Iniciando modo móvil (sin HMR)..." -ForegroundColor Green

# Crear configuración temporal sin HMR
$envContent = @"
VITE_API_BASE_URL=http://192.168.12.179:8000
VITE_DISABLE_HMR=true
NODE_ENV=production
"@

Write-Host "📝 Configurando variables de entorno para móvil..." -ForegroundColor Cyan
$envContent | Out-File -FilePath "frontend\.env" -Encoding UTF8

# Reiniciar frontend
Write-Host "🔄 Reiniciando frontend en modo móvil..." -ForegroundColor Yellow
docker-compose restart frontend

Write-Host "⏱️ Esperando que el frontend esté listo..." -ForegroundColor Blue
Start-Sleep -Seconds 10

Write-Host "`n✅ Frontend configurado para móvil!" -ForegroundColor Green
Write-Host "📱 URLs para acceder desde móvil:" -ForegroundColor Yellow
Write-Host "   http://192.168.12.179:5173" -ForegroundColor White
Write-Host "   http://192.168.12.179:5173/test-ip.html" -ForegroundColor White

Write-Host "`n🔑 Credenciales:" -ForegroundColor Yellow
Write-Host "   test@test.com / 123456" -ForegroundColor White

Write-Host "`n💡 Características del modo móvil:" -ForegroundColor Cyan
Write-Host "   ✅ Sin actualizaciones automáticas (HMR deshabilitado)" -ForegroundColor Green
Write-Host "   ✅ Configuración optimizada para acceso por IP" -ForegroundColor Green
Write-Host "   ✅ Proxy configurado para backend móvil" -ForegroundColor Green

Write-Host "`n🔄 Para volver al modo desarrollo normal:" -ForegroundColor Yellow
Write-Host "   Ejecuta: .\dev.ps1" -ForegroundColor White

Read-Host "`nPresiona Enter para continuar"
