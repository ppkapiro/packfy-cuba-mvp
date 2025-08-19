# 🏥 HEALTH CHECK - PACKFY CUBA MVP
# Script para verificar el estado de todos los servicios

Write-Host "🇨🇺 PACKFY CUBA - Health Check..." -ForegroundColor Cyan

# Verificar contenedores
Write-Host "`n📊 Estado de contenedores:" -ForegroundColor Yellow
docker compose ps

# Verificar salud del backend
Write-Host "`n🔧 Verificando backend..." -ForegroundColor Yellow
try {
    $backendHealth = Invoke-RestMethod -Uri "http://localhost:8000/api/health/" -TimeoutSec 5
    if ($backendHealth.status -eq "ok") {
        Write-Host "✅ Backend: OK (v$($backendHealth.version))" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend: Error en respuesta" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Backend: No accesible" -ForegroundColor Red
}

# Verificar frontend
Write-Host "`n🌐 Verificando frontend..." -ForegroundColor Yellow
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 5 -UseBasicParsing
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend: OK" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend: No accesible" -ForegroundColor Red
}

# Verificar base de datos
Write-Host "`n🗄️ Verificando base de datos..." -ForegroundColor Yellow
$dbCheck = docker compose exec -T database pg_isready -U postgres -d packfy 2>$null
if ($dbCheck -match "accepting connections") {
    Write-Host "✅ Database: OK" -ForegroundColor Green
} else {
    Write-Host "❌ Database: No accesible" -ForegroundColor Red
}

# Verificar Redis
Write-Host "`n⚡ Verificando Redis..." -ForegroundColor Yellow
$redisCheck = docker compose exec -T redis redis-cli ping 2>$null
if ($redisCheck -match "PONG") {
    Write-Host "✅ Redis: OK" -ForegroundColor Green
} else {
    Write-Host "❌ Redis: No accesible" -ForegroundColor Red
}

Write-Host "`n🎉 Health check completado!" -ForegroundColor Cyan
