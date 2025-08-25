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

# Función para ejecutar comando en background
function Start-BackgroundProcess {
    param($Command, $WorkingDir, $Name)
    
    Write-Host "🔄 Iniciando $Name..." -ForegroundColor Yellow
    
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "powershell.exe"
    $startInfo.Arguments = "-Command `"$Command`""
    $startInfo.WorkingDirectory = $WorkingDir
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $false
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    $process.Start()
    
    Write-Host "✅ $Name iniciado (PID: $($process.Id))" -ForegroundColor Green
    
    return $process
}

try {
    # Obtener directorio base
    $baseDir = Get-Location
    $frontendDir = Join-Path $baseDir "frontend"
    
    Write-Host "📁 Directorio base: $baseDir" -ForegroundColor Cyan
    Write-Host "📁 Directorio frontend: $frontendDir" -ForegroundColor Cyan
    Write-Host ""
    
    # Iniciar Backend Django
    Write-Host "🐍 Iniciando Backend Django..." -ForegroundColor Blue
    $backendProcess = Start-BackgroundProcess "python manage.py runserver" $baseDir "Backend Django"
    
    Start-Sleep -Seconds 3
    
    # Iniciar Frontend React+Vite
    Write-Host "⚛️ Iniciando Frontend React+Vite..." -ForegroundColor Blue
    $frontendProcess = Start-BackgroundProcess "npm run dev" $frontendDir "Frontend React+Vite"
    
    Start-Sleep -Seconds 5
    
    Write-Host ""
    Write-Host "🎉 SERVICIOS INICIADOS EXITOSAMENTE" -ForegroundColor Green
    Write-Host "===================================" -ForegroundColor Green
    Write-Host "🐍 Backend Django:  http://127.0.0.1:8000" -ForegroundColor Yellow
    Write-Host "⚛️ Frontend React:  https://localhost:5173" -ForegroundColor Yellow
    Write-Host "📱 Acceso móvil:    https://192.168.12.178:5173" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 PIDs de procesos:" -ForegroundColor Cyan
    Write-Host "   Backend:  $($backendProcess.Id)" -ForegroundColor Cyan
    Write-Host "   Frontend: $($frontendProcess.Id)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⏹️ Para detener: Usa Ctrl+C en las ventanas de los procesos" -ForegroundColor Magenta
    Write-Host "🔍 Para verificar: netstat -ano | findstr ':8000'" -ForegroundColor Magenta
    Write-Host "🔍 Para verificar: netstat -ano | findstr ':5173'" -ForegroundColor Magenta
    
} catch {
    Write-Host "❌ Error al iniciar servicios: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
