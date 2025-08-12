# 🛑 Packfy Cuba MVP - Parar servicios
# Script para detener todos los contenedores

Write-Host "🛑 Deteniendo Packfy Cuba MVP..." -ForegroundColor Yellow

docker-compose down

Write-Host "✅ Servicios detenidos correctamente" -ForegroundColor Green
