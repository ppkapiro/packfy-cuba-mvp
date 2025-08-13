# REINICIO COMPLETO DEL SISTEMA PACKFY
# Script para reiniciar todo despues de problemas de conectividad

Write-Host "INICIANDO REINICIO COMPLETO DEL SISTEMA" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

# Navegar al directorio del proyecto
Set-Location "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"
Write-Host "Ubicacion: $(Get-Location)" -ForegroundColor Yellow

# Detener todos los servicios
Write-Host "`nDeteniendo servicios Docker..." -ForegroundColor Yellow
docker-compose down --volumes --remove-orphans

# Limpiar sistema Docker
Write-Host "`nLimpiando sistema Docker..." -ForegroundColor Yellow
docker system prune -f
docker volume prune -f

# Verificar archivos criticos
Write-Host "`nVerificando archivos criticos..." -ForegroundColor Yellow
$archivos = @(
    "frontend\src\components\PremiumCompleteForm.tsx",
    "frontend\src\pages\ModernAdvancedPage.tsx",
    "frontend\src\components\SimpleAdvancedForm.tsx",
    "frontend\src\pages\SimpleAdvancedPage.tsx"
)

foreach ($archivo in $archivos) {
    if (Test-Path $archivo) {
        Write-Host "OK: $archivo" -ForegroundColor Green
    }
    else {
        Write-Host "FALTA: $archivo" -ForegroundColor Red
    }
}

# Reconstruir servicios
Write-Host "`nReconstruyendo servicios..." -ForegroundColor Yellow
docker-compose build --no-cache

# Iniciar servicios
Write-Host "`nIniciando servicios..." -ForegroundColor Yellow
docker-compose up -d

# Esperar a que los servicios esten listos
Write-Host "`nEsperando que los servicios esten listos..." -ForegroundColor Yellow
Start-Sleep 30

# Verificar estado
Write-Host "`nEstado de servicios:" -ForegroundColor Yellow
docker-compose ps

# Verificar logs
Write-Host "`nLogs recientes:" -ForegroundColor Yellow
docker-compose logs --tail 10

Write-Host "`nURLs PARA PROBAR:" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  Premium: http://localhost:5173/envios/modern" -ForegroundColor Cyan
Write-Host "  Simple: http://localhost:5173/envios/simple" -ForegroundColor Cyan
Write-Host "  API: http://localhost:8000/api/" -ForegroundColor Cyan

Write-Host "`nREINICIO COMPLETO FINALIZADO" -ForegroundColor Green
Write-Host "Abre el navegador en las URLs mostradas arriba para probar" -ForegroundColor Yellow
