#!/usr/bin/env pwsh
# Script para detener todos los servicios del proyecto Packfy Cuba

Write-Host "🛑 DETENIENDO SERVICIOS PACKFY CUBA" -ForegroundColor Red
Write-Host "===================================" -ForegroundColor Red

# Detener procesos de Node y Python
Write-Host "⏹️ Deteniendo procesos de Node.js y Python..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "node" -or $_.ProcessName -eq "python"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Limpiar puertos específicos
Write-Host "🧹 Liberando puertos..." -ForegroundColor Yellow
$ports = @(5173, 5174, 8000, 3000)
foreach ($port in $ports) {
    $processes = netstat -ano | findstr ":$port"
    if ($processes) {
        Write-Host "   Liberando puerto $port"
        $pids = ($processes | ForEach-Object { ($_ -split '\s+')[-1] }) | Where-Object { $_ -ne "0" -and $_ -ne "" } | Sort-Object -Unique
        foreach ($processId in $pids) {
            taskkill /PID $processId /F 2>$null
        }
    }
}

# Eliminar archivos batch temporales
if (Test-Path "start-backend.bat") { Remove-Item "start-backend.bat" -Force }
if (Test-Path "start-frontend.bat") { Remove-Item "start-frontend.bat" -Force }

Write-Host "✅ Todos los servicios han sido detenidos" -ForegroundColor Green
Write-Host "Para reiniciar, ejecuta: .\reset-completo.ps1" -ForegroundColor Cyan
