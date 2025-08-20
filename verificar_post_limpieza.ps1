# Script para verificar el estado después de la limpieza completa

Write-Host "🧹 VERIFICACIÓN POST-LIMPIEZA COMPLETA" -ForegroundColor Cyan
Write-Host "=" * 50

Write-Host "`n📦 Estado de contenedores:" -ForegroundColor Yellow
docker ps

Write-Host "`n🔍 Logs del backend (últimas 10 líneas):" -ForegroundColor Yellow
docker logs packfy-backend --tail 10

Write-Host "`n🏥 Test de conectividad:" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/health/" -Method GET -TimeoutSec 5
    Write-Host "✅ Backend respondiendo: $($response | ConvertTo-Json)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend no responde: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🔐 Test de login:" -ForegroundColor Yellow
try {
    $loginData = @{
        email    = "superadmin@packfy.com"
        password = "super123!"
    } | ConvertTo-Json

    $headers = @{
        "Content-Type"  = "application/json"
        "X-Tenant-Slug" = "packfy-express"
    }

    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Body $loginData -Headers $headers -TimeoutSec 5
    Write-Host "✅ Login exitoso" -ForegroundColor Green
}
catch {
    Write-Host "❌ Login falló: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🌐 Frontend:" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 5
    Write-Host "✅ Frontend respondiendo (Status: $($response.StatusCode))" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend no responde: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🔄 VERIFICACIÓN COMPLETADA" -ForegroundColor Cyan
