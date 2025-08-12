# 🔧 SOLUCIONADOR DE CONEXIÓN - PACKFY CUBA
# Script para diagnosticar y solucionar problemas de conexión

Write-Host "🇨🇺 =========================================" -ForegroundColor Cyan
Write-Host "🔧 DIAGNÓSTICO DE CONEXIÓN PACKFY CUBA" -ForegroundColor Cyan
Write-Host "🇨🇺 =========================================" -ForegroundColor Cyan
Write-Host ""

# Detener procesos anteriores que puedan estar interfiriendo
Write-Host "🛑 Limpiando procesos anteriores..." -ForegroundColor Yellow
try {
    Get-Process | Where-Object {$_.ProcessName -like "*node*" -or $_.ProcessName -like "*vite*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Procesos Node/Vite limpiados" -ForegroundColor Green
} catch {
    Write-Host "⚠️  No se encontraron procesos para limpiar" -ForegroundColor Yellow
}

Write-Host ""

# Verificar puertos disponibles
Write-Host "🔍 Verificando puertos..." -ForegroundColor Yellow
$ports = @(5173, 5174, 5175, 8000)
foreach ($port in $ports) {
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
        if ($connection) {
            Write-Host "🟢 Puerto ${port}: EN USO" -ForegroundColor Green
        } else {
            Write-Host "🔴 Puerto ${port}: LIBRE" -ForegroundColor Red
        }
    } catch {
        Write-Host "🔴 Puerto ${port}: LIBRE" -ForegroundColor Red
    }
}

Write-Host ""

# Obtener IP local
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress | Select-Object -First 1
Write-Host "🌐 IP Local detectada: $localIP" -ForegroundColor Cyan

Write-Host ""

# Iniciar backend
Write-Host "🚀 Iniciando Backend Django..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend'; python manage.py runserver 0.0.0.0:8000"

# Esperar un poco
Start-Sleep -Seconds 3

# Iniciar frontend
Write-Host "🚀 Iniciando Frontend Vite..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend'; npm run dev"

# Esperar para que inicien
Write-Host "⏳ Esperando que los servidores inicien..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host ""

# Verificar conectividad
Write-Host "🔍 Verificando conectividad..." -ForegroundColor Yellow

# Backend
try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend funcionando correctamente" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend NO responde" -ForegroundColor Red
}

# Frontend puertos posibles
$frontendWorking = $false
foreach ($port in @(5173, 5174, 5175, 5176)) {
    try {
        $frontendResponse = Invoke-WebRequest -Uri "http://localhost:$port/" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($frontendResponse.StatusCode -eq 200) {
            Write-Host "✅ Frontend funcionando en puerto ${port}" -ForegroundColor Green
            $frontendWorking = $true
            $workingPort = $port
            break
        }
    } catch {
        # Continuar probando otros puertos
    }
}

if (-not $frontendWorking) {
    Write-Host "❌ Frontend NO responde en ningún puerto" -ForegroundColor Red
}

Write-Host ""

# URLs finales
if ($frontendWorking) {
    Write-Host "🌐 URLs de acceso:" -ForegroundColor Cyan
    Write-Host "   💻 Computadora: http://localhost:${workingPort}/" -ForegroundColor White
    Write-Host "   📱 Móvil: http://${localIP}:${workingPort}/" -ForegroundColor White
    Write-Host "   🔧 Admin: http://localhost:8000/admin/" -ForegroundColor White
} else {
    Write-Host "⚠️  Revisa las ventanas de PowerShell que se abrieron para ver errores" -ForegroundColor Yellow
}

Write-Host ""

# Credenciales
Write-Host "🔐 Credenciales de prueba:" -ForegroundColor Yellow
Write-Host "   👑 Admin: admin@packfy.cu / admin123" -ForegroundColor White
Write-Host "   🏢 Empresa: empresa@test.cu / empresa123" -ForegroundColor White
Write-Host "   🇨🇺 Cliente: cliente@test.cu / cliente123" -ForegroundColor White

Write-Host ""

# Troubleshooting
Write-Host "🔧 Si sigues teniendo problemas:" -ForegroundColor Yellow
Write-Host "   1. Verifica que las ventanas de PowerShell estén abiertas" -ForegroundColor White
Write-Host "   2. Revisa los errores en la consola del navegador (F12)" -ForegroundColor White
Write-Host "   3. Verifica que el firewall no esté bloqueando" -ForegroundColor White
Write-Host "   4. En móvil, asegúrate de estar en la misma red WiFi" -ForegroundColor White

Write-Host ""
Write-Host "🇨🇺 ¡Packfy Cuba configurado!" -ForegroundColor Green
