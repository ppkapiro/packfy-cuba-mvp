# 🔍 VERIFICACIÓN NAVEGACIÓN EN VIVO
# Packfy Cuba v3.0 - Diagnóstico de Navegación Dueño

Write-Host "🇨🇺 PACKFY CUBA - VERIFICACIÓN NAVEGACIÓN DUEÑO" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

$frontendUrl = "http://localhost:5174"
$backendUrl = "http://localhost:8000"

Write-Host ""
Write-Host "🌐 VERIFICANDO SERVICIOS..." -ForegroundColor Yellow

# Verificar frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri $frontendUrl -TimeoutSec 5 -UseBasicParsing
    Write-Host "   ✅ Frontend disponible en $frontendUrl" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Frontend NO disponible en $frontendUrl" -ForegroundColor Red
    Write-Host "   💡 Ejecutar: npm run dev en la carpeta frontend" -ForegroundColor Yellow
}

# Verificar backend
try {
    $backendResponse = Invoke-WebRequest -Uri "$backendUrl/api/health/" -TimeoutSec 5 -UseBasicParsing
    Write-Host "   ✅ Backend disponible en $backendUrl" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Backend NO disponible en $backendUrl" -ForegroundColor Red
    Write-Host "   💡 Ejecutar: python manage.py runserver en la carpeta backend" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 CHECKLIST PARA VER NAVEGACIÓN DUEÑO:" -ForegroundColor Magenta
Write-Host "-" * 40

Write-Host "1. ✅ Servidor frontend ejecutándose" -ForegroundColor Green
Write-Host "2. ✅ Servidor backend ejecutándose" -ForegroundColor Green
Write-Host "3. 🔍 Usuario con rol 'dueno' necesario" -ForegroundColor Yellow
Write-Host "4. 🔍 Autenticación activa requerida" -ForegroundColor Yellow

Write-Host ""
Write-Host "🎯 PASOS PARA PROBAR:" -ForegroundColor Cyan
Write-Host "1. Abrir navegador en: $frontendUrl" -ForegroundColor White
Write-Host "2. Hacer login con usuario dueño" -ForegroundColor White
Write-Host "3. Verificar navegación en header" -ForegroundColor White
Write-Host "4. Navegar a: $frontendUrl/admin/dashboard" -ForegroundColor White

Write-Host ""
Write-Host "🔧 COMANDOS ÚTILES:" -ForegroundColor Magenta
Write-Host "Frontend:" -ForegroundColor Yellow
Write-Host "   cd frontend && npm run dev" -ForegroundColor Gray
Write-Host "Backend:" -ForegroundColor Yellow
Write-Host "   cd backend && python manage.py runserver" -ForegroundColor Gray
Write-Host "Crear usuario dueño:" -ForegroundColor Yellow
Write-Host "   cd backend && python manage.py shell" -ForegroundColor Gray

Write-Host ""
Write-Host "🐛 SI NO SE VE LA NAVEGACIÓN:" -ForegroundColor Red
Write-Host "1. Verificar que el usuario tenga rol 'dueno'" -ForegroundColor White
Write-Host "2. Verificar que esté autenticado" -ForegroundColor White
Write-Host "3. Verificar consola del navegador por errores" -ForegroundColor White
Write-Host "4. Verificar que los archivos de navegación existan" -ForegroundColor White

Write-Host ""
Write-Host "🚀 VERIFICACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
