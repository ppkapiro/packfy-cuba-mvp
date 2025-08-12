#!/usr/bin/env pwsh
# Script de diagnóstico y recuperación automática de conectividad
# Packfy Cuba MVP - Sistema robusto contra desconexiones

param(
    [switch]$Monitor,
    [switch]$Repair,
    [switch]$Full
)

Write-Host "🔧 DIAGNÓSTICO Y RECUPERACIÓN AUTOMÁTICA - PACKFY" -ForegroundColor Green -BackgroundColor Black
Write-Host "=================================================" -ForegroundColor Green

function Test-ServiceConnectivity {
    param($ServiceName, $Url, $ExpectedStatus = 200)

    try {
        if ($Url -like "https://*") {
            $response = Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec 5 -SkipCertificateCheck -ErrorAction SilentlyContinue
        } else {
            $response = Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec 5 -ErrorAction SilentlyContinue
        }

        if ($response.StatusCode -eq $ExpectedStatus -or $response.StatusCode -eq 302) {
            Write-Host "✅ $ServiceName : CONECTADO" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️  $ServiceName : RESPUESTA INESPERADA ($($response.StatusCode))" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "❌ $ServiceName : DESCONECTADO" -ForegroundColor Red
        return $false
    }
}

function Test-AllServices {
    Write-Host "`n🔍 VERIFICANDO CONECTIVIDAD..." -ForegroundColor Cyan

    $frontend = Test-ServiceConnectivity "Frontend (HTTPS)" "https://localhost:5173"
    $backend = Test-ServiceConnectivity "Backend (HTTP)" "http://localhost:8000"
    $database = Test-ServiceConnectivity "Database" "http://localhost:5433" -ExpectedStatus 0  # DB no responde HTTP

    return @{
        Frontend = $frontend
        Backend = $backend
        AllHealthy = $frontend -and $backend
    }
}

function Get-DockerStatus {
    Write-Host "`n📊 ESTADO DE CONTENEDORES:" -ForegroundColor Cyan

    try {
        $containers = docker compose ps --format json | ConvertFrom-Json
        foreach ($container in $containers) {
            $status = $container.State
            $health = if ($container.Health) { $container.Health } else { "N/A" }

            if ($status -eq "running" -and ($health -eq "healthy" -or $health -eq "N/A")) {
                Write-Host "✅ $($container.Service): $status ($health)" -ForegroundColor Green
            } elseif ($status -eq "running") {
                Write-Host "⚠️  $($container.Service): $status ($health)" -ForegroundColor Yellow
            } else {
                Write-Host "❌ $($container.Service): $status ($health)" -ForegroundColor Red
            }
        }
        return $true
    } catch {
        Write-Host "❌ Error obteniendo estado de Docker" -ForegroundColor Red
        return $false
    }
}

function Repair-Services {
    Write-Host "`n🔧 INICIANDO REPARACIÓN AUTOMÁTICA..." -ForegroundColor Yellow

    # Paso 1: Reiniciar servicios suavemente
    Write-Host "   1️⃣  Reiniciando frontend..." -ForegroundColor White
    docker compose restart frontend | Out-Null
    Start-Sleep 5

    Write-Host "   2️⃣  Reiniciando backend..." -ForegroundColor White
    docker compose restart backend | Out-Null
    Start-Sleep 10

    # Paso 2: Verificar que estén saludables
    Write-Host "   3️⃣  Verificando health checks..." -ForegroundColor White
    $maxWait = 30
    $waited = 0

    do {
        Start-Sleep 2
        $waited += 2
        $status = docker compose ps --format json | ConvertFrom-Json
        $allHealthy = $true

        foreach ($container in $status) {
            if ($container.State -ne "running" -or ($container.Health -and $container.Health -ne "healthy")) {
                $allHealthy = $false
                break
            }
        }

        Write-Host "   ⏳ Esperando... ($waited/$maxWait seg)" -ForegroundColor Gray

    } while (-not $allHealthy -and $waited -lt $maxWait)

    if ($allHealthy) {
        Write-Host "   ✅ Servicios reparados exitosamente" -ForegroundColor Green
        return $true
    } else {
        Write-Host "   ⚠️  Reparación parcial - algunos servicios pueden necesitar más tiempo" -ForegroundColor Yellow
        return $false
    }
}

function Monitor-Services {
    Write-Host "`n👁️  MODO MONITOR ACTIVADO - Presiona Ctrl+C para salir" -ForegroundColor Magenta

    $checkCount = 0
    $failureCount = 0

    while ($true) {
        $checkCount++
        Clear-Host

        Write-Host "🔧 MONITOR PACKFY - Check #$checkCount" -ForegroundColor Green -BackgroundColor Black
        Write-Host "Failures detected: $failureCount" -ForegroundColor $(if($failureCount -eq 0){"Green"}else{"Red"})
        Write-Host "Last check: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
        Write-Host "=" * 50

        $services = Test-AllServices

        if (-not $services.AllHealthy) {
            $failureCount++
            Write-Host "`n🚨 PROBLEMA DETECTADO - Iniciando reparación automática..." -ForegroundColor Red

            if (Repair-Services) {
                Write-Host "✅ Problema resuelto automáticamente" -ForegroundColor Green
            } else {
                Write-Host "❌ Reparación falló - intervención manual requerida" -ForegroundColor Red
            }
        } else {
            Write-Host "`n✅ Todos los servicios funcionando correctamente" -ForegroundColor Green
        }

        Write-Host "`nPróxima verificación en 30 segundos..." -ForegroundColor Gray
        Start-Sleep 30
    }
}

# === EJECUCIÓN PRINCIPAL ===

if ($Monitor) {
    Monitor-Services
} elseif ($Repair) {
    Repair-Services
    Test-AllServices
} elseif ($Full) {
    Get-DockerStatus
    $services = Test-AllServices

    if (-not $services.AllHealthy) {
        Write-Host "`n🔧 Detectando problemas - iniciando reparación..." -ForegroundColor Yellow
        Repair-Services
        Write-Host "`n🔍 Re-verificando servicios..." -ForegroundColor Cyan
        Test-AllServices
    }
} else {
    # Diagnóstico básico
    Get-DockerStatus
    Test-AllServices

    Write-Host "`n📋 COMANDOS DISPONIBLES:" -ForegroundColor Cyan
    Write-Host "   ./diagnostico-y-recuperacion.ps1 -Repair    # Reparar servicios" -ForegroundColor White
    Write-Host "   ./diagnostico-y-recuperacion.ps1 -Monitor   # Monitor continuo" -ForegroundColor White
    Write-Host "   ./diagnostico-y-recuperacion.ps1 -Full      # Diagnóstico + reparación" -ForegroundColor White
}

Write-Host "`n🎯 Diagnóstico completado" -ForegroundColor Green
