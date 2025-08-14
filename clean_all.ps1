# 🇨🇺 PACKFY CUBA - LIMPIEZA TOTAL Y RESET COMPLETO

Write-Host "🇨🇺 PACKFY CUBA - LIMPIEZA TOTAL DEL SISTEMA" -ForegroundColor Red
Write-Host "=" * 60 -ForegroundColor Red

# Cambiar al directorio del proyecto
Set-Location "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"

Write-Host "`n🛑 DETENIENDO TODOS LOS CONTENEDORES" -ForegroundColor Yellow
docker compose down

Write-Host "`n🧹 LIMPIEZA COMPLETA DE DOCKER" -ForegroundColor Yellow
Write-Host "Eliminando volúmenes..."
docker compose down -v

Write-Host "Limpiando imágenes locales del proyecto..."
docker image prune -f

Write-Host "Limpiando cache de build..."
docker builder prune -f

Write-Host "`n📊 VERIFICANDO ESTADO DE LIMPIEZA" -ForegroundColor Yellow
Write-Host "Contenedores activos:"
docker ps

Write-Host "`nVolúmenes restantes:"
docker volume ls

Write-Host "`n✅ LIMPIEZA COMPLETA TERMINADA" -ForegroundColor Green
Write-Host "El sistema está limpio y listo para reconstruirse correctamente."
