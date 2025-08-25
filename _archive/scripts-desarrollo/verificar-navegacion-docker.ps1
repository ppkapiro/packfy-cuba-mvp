# 🎯 SCRIPT DE VERIFICACIÓN RÁPIDA - NAVEGACIÓN DOCKER

Write-Host "🐳 VERIFICANDO DOCKER Y NAVEGACIÓN..." -ForegroundColor Cyan
Write-Host ""

# 1. Verificar estado de contenedores
Write-Host "📦 Estado de Contenedores:" -ForegroundColor Yellow
docker-compose ps
Write-Host ""

# 2. Verificar que frontend esté corriendo
Write-Host "🌐 Verificando Frontend:" -ForegroundColor Yellow
$frontendStatus = docker-compose ps frontend
if ($frontendStatus -match "Up") {
    Write-Host "✅ Frontend corriendo" -ForegroundColor Green
}
else {
    Write-Host "❌ Frontend no está corriendo" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 3. Verificar archivos clave en el contenedor
Write-Host "📁 Verificando archivos en contenedor:" -ForegroundColor Yellow
try {
    Write-Host "🔍 DashboardRouter.tsx:" -ForegroundColor White
    docker exec packfy-frontend ls -la /app/src/components/DashboardRouter.tsx

    Write-Host "🔍 App.tsx (routing):" -ForegroundColor White
    docker exec packfy-frontend grep -A 2 -B 2 "DashboardRouter" /app/src/App.tsx

    Write-Host "✅ Archivos verificados en contenedor" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error verificando archivos en contenedor" -ForegroundColor Red
}
Write-Host ""

# 4. Verificar conectividad
Write-Host "🔗 Verificando Conectividad:" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend accesible en puerto 5173" -ForegroundColor Green
    }
}
catch {
    Write-Host "❌ Frontend no accesible en puerto 5173" -ForegroundColor Red
}
Write-Host ""

# 5. URLs de prueba
Write-Host "🎯 URLs DE PRUEBA:" -ForegroundColor Cyan
Write-Host "▶️ Login: http://localhost:5173/login" -ForegroundColor White
Write-Host "▶️ Dashboard: http://localhost:5173/dashboard" -ForegroundColor White
Write-Host ""

Write-Host "🔑 CREDENCIALES DE PRUEBA:" -ForegroundColor Cyan
Write-Host "Email: dueno@packfy.com" -ForegroundColor White
Write-Host "Password: dueno123!" -ForegroundColor White
Write-Host ""

Write-Host "📋 PASOS DE VERIFICACIÓN:" -ForegroundColor Cyan
Write-Host "1. Ir a http://localhost:5173/login" -ForegroundColor White
Write-Host "2. Login con dueno@packfy.com" -ForegroundColor White
Write-Host "3. Verificar que aparece AdminDashboard" -ForegroundColor White
Write-Host "4. Verificar navegación con dropdowns" -ForegroundColor White
Write-Host ""

Write-Host "✅ VERIFICACIÓN COMPLETA" -ForegroundColor Green
