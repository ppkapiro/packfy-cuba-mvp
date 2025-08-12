#!/usr/bin/env pwsh
# Script simplificado de monitoreo Packfy

Write-Host "SISTEMA DE MONITOREO PACKFY" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

function Test-ServiceHealth {
    Write-Host "`nVerificando conectividad..." -ForegroundColor Cyan

    # Frontend
    try {
        $frontend = Invoke-WebRequest -Uri "https://localhost:5173" -Method Head -TimeoutSec 5 -SkipCertificateCheck -ErrorAction Stop
        Write-Host "Frontend (HTTPS): CONECTADO" -ForegroundColor Green
    }
    catch {
        Write-Host "Frontend (HTTPS): ERROR" -ForegroundColor Red
    }

    # Backend
    try {
        $backend = Invoke-WebRequest -Uri "http://localhost:8000/api/health/" -Method Head -TimeoutSec 5 -ErrorAction Stop
        Write-Host "Backend Health: CONECTADO" -ForegroundColor Green
    }
    catch {
        Write-Host "Backend Health: ERROR" -ForegroundColor Red
    }

    # API General
    try {
        $api = Invoke-WebRequest -Uri "http://localhost:8000" -Method Head -TimeoutSec 5 -ErrorAction Stop
        Write-Host "Backend API: CONECTADO" -ForegroundColor Green
    }
    catch {
        Write-Host "Backend API: ERROR" -ForegroundColor Red
    }
}

function Show-DockerStatus {
    Write-Host "`nEstado de contenedores:" -ForegroundColor Cyan
    docker compose ps
}

function Quick-Fix {
    Write-Host "`nEjecutando reparacion rapida..." -ForegroundColor Yellow

    Write-Host "Reiniciando frontend..." -ForegroundColor White
    docker compose restart frontend
    Start-Sleep 10

    Write-Host "Reiniciando backend..." -ForegroundColor White
    docker compose restart backend
    Start-Sleep 15

    Write-Host "Verificando..." -ForegroundColor White
    Test-ServiceHealth
}

# Ejecucion principal
Show-DockerStatus
Test-ServiceHealth

Write-Host "`nComandos disponibles:" -ForegroundColor Cyan
Write-Host "  .\monitor-simple.ps1 -Fix    # Reparacion rapida" -ForegroundColor White
Write-Host "  docker compose ps            # Estado contenedores" -ForegroundColor White
Write-Host "  docker compose restart       # Reiniciar todos" -ForegroundColor White

param([switch]$Fix)

if ($Fix) {
    Quick-Fix
}

Write-Host "`nURLs de acceso:" -ForegroundColor Green
Write-Host "  Frontend: https://localhost:5173" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Health:   http://localhost:8000/api/health/" -ForegroundColor Cyan
