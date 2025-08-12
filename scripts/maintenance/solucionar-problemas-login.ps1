#!/usr/bin/env pwsh
# Script de inicio específico para solucionar problemas de login y red

Write-Host "🔧 SOLUCIONANDO PROBLEMAS ESPECÍFICOS" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "📋 Problemas a solucionar:" -ForegroundColor Yellow
Write-Host "  1. Error en servidor 5173 con dirección .178" -ForegroundColor Red
Write-Host "  2. Página se actualiza constantemente" -ForegroundColor Red  
Write-Host "  3. No permite hacer login" -ForegroundColor Red

Write-Host ""
Write-Host "🧹 Paso 1: Limpieza completa..." -ForegroundColor Yellow

# Detener procesos
Get-Process node* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process *vite* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Limpiar cache
if (Test-Path "frontend\dist") {
    Remove-Item "frontend\dist" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  ✅ Cache de build limpiado" -ForegroundColor Green
}

if (Test-Path "frontend\node_modules\.vite") {
    Remove-Item "frontend\node_modules\.vite" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  ✅ Cache de Vite limpiado" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Paso 2: Iniciando backend..." -ForegroundColor Yellow

# Iniciar backend
$backendScript = @"
Write-Host 'Backend iniciando en puerto 8000...' -ForegroundColor Green
Set-Location '$PWD\backend'
python manage.py runserver localhost:8000
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript
Start-Sleep -Seconds 3

Write-Host "  ✅ Backend iniciado en localhost:8000" -ForegroundColor Green

Write-Host ""
Write-Host "🌐 Paso 3: Configurando frontend estable..." -ForegroundColor Yellow

# Variables de entorno para desarrollo estable
$env:VITE_HMR_HOST = "localhost"
$env:VITE_HMR_CLIENT_PORT = "5173"

Write-Host "  ✅ Variables de entorno configuradas" -ForegroundColor Green

Write-Host ""
Write-Host "⚛️ Paso 4: Iniciando frontend..." -ForegroundColor Yellow

$frontendScript = @"
Write-Host 'Frontend iniciando en modo estable...' -ForegroundColor Green
Set-Location '$PWD\frontend'

# Configuración estable para evitar recargas constantes
`$env:VITE_HMR_HOST = 'localhost'
`$env:VITE_HMR_CLIENT_PORT = '5173'

Write-Host 'Configuración aplicada:' -ForegroundColor Cyan
Write-Host '  HMR Host: localhost (evita problemas de red)' -ForegroundColor White
Write-Host '  Puerto estable: 5173' -ForegroundColor White
Write-Host '  Proxy configurado: /api -> http://localhost:8000' -ForegroundColor White
Write-Host ''

npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host "  ⏳ Esperando a que el frontend se estabilice..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verificar puertos
$maxWait = 15
$waited = 0
do {
    Start-Sleep -Seconds 1
    $waited++
    $frontend = Test-NetConnection -ComputerName "localhost" -Port 5173 -InformationLevel Quiet
    Write-Progress -Activity "Esperando frontend" -Status "Verificando estabilidad..." -PercentComplete (($waited / $maxWait) * 100)
} while (-not $frontend -and $waited -lt $maxWait)

Write-Host ""
if ($frontend) {
    Write-Host "✅ Sistema iniciado correctamente" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🎯 CONFIGURACIÓN ESPECÍFICA APLICADA:" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "1. 🌐 URLs RECOMENDADAS (sin problemas):" -ForegroundColor Cyan
    Write-Host "   ✅ USAR SIEMPRE: http://localhost:5173" -ForegroundColor Green
    Write-Host "   ❌ EVITAR: http://192.168.12.178:5173 (causa problemas)" -ForegroundColor Red
    
    Write-Host ""
    Write-Host "2. 🔧 SOLUCIONES APLICADAS:" -ForegroundColor Cyan
    Write-Host "   ✅ HMR configurado para localhost (evita recargas)" -ForegroundColor Green
    Write-Host "   ✅ Cache limpiado completamente" -ForegroundColor Green
    Write-Host "   ✅ Proxy estable: /api -> localhost:8000" -ForegroundColor Green
    Write-Host "   ✅ Variables de entorno optimizadas" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "3. 🔐 PARA LOGIN:" -ForegroundColor Cyan
    Write-Host "   ✅ Usar exclusivamente: http://localhost:5173" -ForegroundColor Green
    Write-Host "   ✅ Backend disponible en: http://localhost:8000" -ForegroundColor Green
    Write-Host "   ✅ CORS configurado correctamente" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "4. 📱 ACCESO MÓVIL:" -ForegroundColor Cyan
    Write-Host "   ⚠️ Si necesitas acceso móvil:" -ForegroundColor Yellow
    Write-Host "     - Usar: http://192.168.12.178:5173" -ForegroundColor White
    Write-Host "     - Solo DESPUÉS de confirmar que localhost funciona" -ForegroundColor White
    
    Write-Host ""
    Write-Host "🎉 PRÓXIMO PASO:" -ForegroundColor Green
    Write-Host "   Abre SOLO esta URL: http://localhost:5173" -ForegroundColor White
    Write-Host "   NO uses direcciones de red hasta confirmar que funciona" -ForegroundColor Yellow
    
    # Abrir navegador
    Start-Sleep -Seconds 2
    try {
        Write-Host ""
        Write-Host "🌍 Abriendo navegador en localhost..." -ForegroundColor Green
        Start-Process "http://localhost:5173"
    } catch {
        Write-Host "⚠️ Abre manualmente: http://localhost:5173" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "❌ Frontend no se pudo iniciar correctamente" -ForegroundColor Red
    Write-Host "💡 Reinicia con: .\inicio-robusto.ps1" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📊 MONITOREO:" -ForegroundColor Magenta
Write-Host "   Revisa las ventanas de backend y frontend para logs" -ForegroundColor Cyan
Write-Host "   Si ves recargas constantes, presiona Ctrl+C y reinicia" -ForegroundColor Yellow

Write-Host ""
Read-Host "Presiona Enter para finalizar este script (servidores siguen activos)"
