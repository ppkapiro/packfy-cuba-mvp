# PACKFY CUBA - INICIAR BACKEND PARA MOVIL

Write-Host "🐍 Iniciando Backend Django para acceso móvil..." -ForegroundColor Green

# Verificar si ya hay un proceso en puerto 8000
$existingProcess = netstat -ano | findstr ":8000" | findstr "LISTENING"
if ($existingProcess) {
    Write-Host "⚠️ Detectado proceso en puerto 8000, terminando..." -ForegroundColor Yellow
    # Obtener PID y terminar
    $processId = ($existingProcess -split '\s+')[-1]
    try {
        taskkill /F /PID $processId
        Write-Host "✅ Proceso $processId terminado" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ No se pudo terminar proceso" -ForegroundColor Yellow
    }
    Start-Sleep -Seconds 2
}

# Verificar directorio backend
$backendDir = "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend"
if (!(Test-Path $backendDir)) {
    Write-Host "❌ No se encuentra directorio backend: $backendDir" -ForegroundColor Red
    exit 1
}

if (!(Test-Path "$backendDir\manage.py")) {
    Write-Host "❌ No se encuentra manage.py en $backendDir" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Directorio backend verificado: $backendDir" -ForegroundColor Cyan

try {
    # Cambiar al directorio backend
    Set-Location $backendDir
    
    Write-Host "🚀 Iniciando Django en 0.0.0.0:8000 (acceso móvil)..." -ForegroundColor Blue
    
    # Iniciar Django en modo accesible desde móvil
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; python manage.py runserver 0.0.0.0:8000"
    
    Start-Sleep -Seconds 5
    
    # Verificar que se inició correctamente
    $backendCheck = netstat -ano | findstr ":8000" | findstr "LISTENING"
    if ($backendCheck) {
        Write-Host "✅ Backend Django iniciado exitosamente" -ForegroundColor Green
        Write-Host "🌐 Backend disponible en:" -ForegroundColor Yellow
        Write-Host "   • Local: http://127.0.0.1:8000" -ForegroundColor White
        Write-Host "   • Móvil: http://192.168.12.178:8000" -ForegroundColor White
        Write-Host "   • API: http://192.168.12.178:8000/api/" -ForegroundColor White
    } else {
        Write-Host "❌ Backend no se inició correctamente" -ForegroundColor Red
        Write-Host "💡 Verifica que Python y Django estén instalados" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Error al iniciar backend: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Script completado" -ForegroundColor Green
