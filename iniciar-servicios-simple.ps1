# 🇨🇺 PACKFY CUBA - INICIAR SERVICIOS UNIFICADOS v3.0

Write-Host "🚀 Iniciando Packfy Cuba - Sistema Unificado v3.0" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Verificar directorio principal
if (!(Test-Path ".\manage.py")) {
    Write-Host "❌ Error: No se encuentra manage.py en el directorio actual" -ForegroundColor Red
    Write-Host "📁 Directorio actual: $((Get-Location).Path)" -ForegroundColor Yellow
    exit 1
}

# Verificar directorio frontend
if (!(Test-Path ".\frontend\package.json")) {
    Write-Host "❌ Error: No se encuentra frontend/package.json" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Estructura del proyecto verificada" -ForegroundColor Green
Write-Host ""

try {
    # Obtener directorio base
    $baseDir = Get-Location
    $frontendDir = Join-Path $baseDir "frontend"
    
    Write-Host "📁 Directorio base: $baseDir" -ForegroundColor Cyan
    Write-Host "📁 Directorio frontend: $frontendDir" -ForegroundColor Cyan
    Write-Host ""
    
    # Iniciar Backend Django en nueva ventana
    Write-Host "🐍 Iniciando Backend Django..." -ForegroundColor Blue
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$baseDir'; python manage.py runserver"
    
    Start-Sleep -Seconds 3
    
    # Iniciar Frontend React+Vite en nueva ventana
    Write-Host "⚛️ Iniciando Frontend React+Vite..." -ForegroundColor Blue
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; npm run dev"
    
    Start-Sleep -Seconds 5
    
    Write-Host ""
    Write-Host "🎉 SERVICIOS INICIADOS EXITOSAMENTE" -ForegroundColor Green
    Write-Host "===================================" -ForegroundColor Green
    Write-Host "🐍 Backend Django:  http://127.0.0.1:8000" -ForegroundColor Yellow
    Write-Host "⚛️ Frontend React:  https://localhost:5173" -ForegroundColor Yellow
    Write-Host "📱 Acceso móvil:    https://192.168.12.178:5173" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⏹️ Para detener: Cierra las ventanas de PowerShell correspondientes" -ForegroundColor Magenta
    Write-Host "🔍 Para verificar: netstat -ano | findstr ':8000'" -ForegroundColor Magenta
    Write-Host "🔍 Para verificar: netstat -ano | findstr ':5173'" -ForegroundColor Magenta
    
} catch {
    Write-Host "❌ Error al iniciar servicios: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
