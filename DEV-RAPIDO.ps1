# 🚀 DESARROLLO RÁPIDO - PACKFY CUBA MVP
# Script para desarrolladores - inicio rápido

param(
    [string]$Action = "start"
)

Write-Host "🇨🇺 PACKFY CUBA - Desarrollo Rápido..." -ForegroundColor Cyan

switch ($Action.ToLower()) {
    "start" {
        Write-Host "🚀 Iniciando servicios de desarrollo..." -ForegroundColor Green
        docker compose up -d
        Start-Sleep 10
        Write-Host "✅ Servicios iniciados!" -ForegroundColor Green
        Write-Host "🌐 Frontend: http://localhost:5173" -ForegroundColor Blue
        Write-Host "🔧 Backend: http://localhost:8000" -ForegroundColor Blue
        Write-Host "📊 Admin: http://localhost:8000/admin" -ForegroundColor Blue
    }

    "stop" {
        Write-Host "🛑 Deteniendo servicios..." -ForegroundColor Yellow
        docker compose down
        Write-Host "✅ Servicios detenidos!" -ForegroundColor Green
    }

    "restart" {
        Write-Host "🔄 Reiniciando servicios..." -ForegroundColor Yellow
        docker compose restart
        Write-Host "✅ Servicios reiniciados!" -ForegroundColor Green
    }

    "logs" {
        Write-Host "📝 Mostrando logs..." -ForegroundColor Blue
        docker compose logs -f
    }

    "clean" {
        Write-Host "🧹 Limpieza completa..." -ForegroundColor Red
        docker compose down -v
        docker system prune -f
        Write-Host "✅ Limpieza completada!" -ForegroundColor Green
    }

    default {
        Write-Host "📋 Uso: .\DEV-RAPIDO.ps1 [start|stop|restart|logs|clean]" -ForegroundColor White
    }
}
