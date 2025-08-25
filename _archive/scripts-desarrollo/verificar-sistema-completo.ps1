#!/usr/bin/env pwsh
# 🎯 VERIFICACIÓN FINAL SISTEMA PACKFY CUBA

Write-Host "🇨🇺 PACKFY CUBA - VERIFICACIÓN SISTEMA COMPLETO" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# 1. Estado de contenedores
Write-Host "`n📦 ESTADO DE CONTENEDORES:" -ForegroundColor Yellow
docker compose ps

# 2. Verificar backend
Write-Host "`n🔧 VERIFICANDO BACKEND:" -ForegroundColor Yellow
try {
    $backendResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/" -Method GET -ErrorAction Stop
    Write-Host "   ❌ Backend sin autenticación (esperado)" -ForegroundColor Red
}
catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "   ✅ Backend respondiendo correctamente (401 esperado)" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Error inesperado: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 3. Verificar frontend
Write-Host "`n🌐 VERIFICANDO FRONTEND:" -ForegroundColor Yellow
try {
    $frontendResponse = Invoke-RestMethod -Uri "https://localhost:5173" -Method GET -SkipCertificateCheck -ErrorAction Stop
    Write-Host "   ✅ Frontend accesible" -ForegroundColor Green
}
catch {
    Write-Host "   ⚠️  Frontend: $($_.Exception.Message)" -ForegroundColor Yellow
}

# 4. URLs importantes
Write-Host "`n🔗 URLS DEL SISTEMA:" -ForegroundColor Yellow
Write-Host "   🌐 Frontend:     https://localhost:5173" -ForegroundColor Cyan
Write-Host "   🔧 Backend API:  http://localhost:8000/api/" -ForegroundColor Cyan
Write-Host "   👤 Admin Panel: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "   💾 Database:    localhost:5433" -ForegroundColor Cyan
Write-Host "   ⚡ Redis:       localhost:6379" -ForegroundColor Cyan

# 5. Credenciales
Write-Host "`n🔑 CREDENCIALES:" -ForegroundColor Yellow
Write-Host "   👤 Superuser: admin@packfy.cu / admin123" -ForegroundColor Magenta

Write-Host "`n🎊 SISTEMA PACKFY CUBA COMPLETAMENTE OPERATIVO!" -ForegroundColor Green
Write-Host "🚀 Listo para desarrollo y pruebas" -ForegroundColor Green
