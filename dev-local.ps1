# 🚀 Packfy - Desarrollo Local Nativo
# Ejecuta backend y frontend localmente con solo la BD en Docker

Write-Host "🚀 INICIANDO DESARROLLO LOCAL NATIVO" -ForegroundColor Green

# Solo levantar la base de datos en Docker
Write-Host "📊 Iniciando solo PostgreSQL..." -ForegroundColor Cyan
docker-compose up -d database

# Esperar a que la BD esté lista
Write-Host "⏳ Esperando que PostgreSQL esté listo..." -ForegroundColor Yellow
Start-Sleep 10

# Backend Django (local)
Write-Host "🔧 Iniciando Backend Django localmente..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd backend; python manage.py runserver 127.0.0.1:8000"
) -WindowStyle Normal

# Frontend React (local)
Write-Host "🌐 Iniciando Frontend React localmente..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd frontend; npm run dev"
) -WindowStyle Normal

Write-Host "✅ Desarrollo local iniciado:" -ForegroundColor Green
Write-Host "   📊 Base de datos: http://localhost:5433" -ForegroundColor White
Write-Host "   🔧 Backend: http://localhost:8000" -ForegroundColor White
Write-Host "   🌐 Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "💡 Beneficios:" -ForegroundColor Yellow
Write-Host "   ⚡ Cambios instantáneos" -ForegroundColor White
Write-Host "   🔍 Debug directo en VS Code" -ForegroundColor White
Write-Host "   🚀 Hot reload automático" -ForegroundColor White
