# PACKFY CUBA - INICIAR SERVICIOS v3.0

Write-Host "Iniciando Packfy Cuba - Sistema Unificado v3.0" -ForegroundColor Green

# Verificar archivos
$manageFile = ".\manage.py"
$frontendPackage = ".\frontend\package.json"

if (!(Test-Path $manageFile)) {
    Write-Host "Error: No se encuentra manage.py" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $frontendPackage)) {
    Write-Host "Error: No se encuentra frontend/package.json" -ForegroundColor Red
    exit 1
}

Write-Host "Estructura verificada correctamente" -ForegroundColor Green

try {
    # Obtener rutas
    $baseDir = Get-Location
    $frontendDir = Join-Path $baseDir "frontend"
    
    Write-Host "Directorio base: $baseDir" -ForegroundColor Cyan
    Write-Host "Directorio frontend: $frontendDir" -ForegroundColor Cyan
    
    # Iniciar Backend Django
    Write-Host "Iniciando Backend Django..." -ForegroundColor Blue
    $backendCmd = "cd '$baseDir'; python manage.py runserver"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd
    
    Start-Sleep -Seconds 3
    
    # Iniciar Frontend React+Vite
    Write-Host "Iniciando Frontend React+Vite..." -ForegroundColor Blue
    $frontendCmd = "cd '$frontendDir'; npm run dev"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd
    
    Start-Sleep -Seconds 5
    
    Write-Host ""
    Write-Host "SERVICIOS INICIADOS EXITOSAMENTE" -ForegroundColor Green
    Write-Host "Backend Django:  http://127.0.0.1:8000" -ForegroundColor Yellow
    Write-Host "Frontend React:  https://localhost:5173" -ForegroundColor Yellow
    Write-Host "Acceso movil:    https://192.168.12.178:5173" -ForegroundColor Yellow
    
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
