# Script de desarrollo para Packfy MVP
# Utiliza verbos aprobados de PowerShell y maneja variables correctamente
# Última actualización: Julio 2025 - Todos los errores de PSScriptAnalyzer resueltos

param(
    [string]$Action = "start",
    [switch]$Clean,
    [switch]$Build,
    [switch]$Logs
)

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Test-DockerRunning {
    try {
        docker info 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

function Start-ApplicationServices {
    Write-ColorOutput "🚀 Iniciando servicios de desarrollo..." "Green"
    
    if (-not (Test-DockerRunning)) {
        Write-ColorOutput "❌ Docker no está ejecutándose. Por favor, inicia Docker Desktop." "Red"
        return $false
    }
    
    # Construcción y inicio de servicios
    Write-ColorOutput "📦 Construyendo e iniciando contenedores..." "Yellow"
    
    try {
        docker-compose up -d --build
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Servicios iniciados correctamente" "Green"
            Write-ColorOutput "🌐 Frontend: http://localhost:3000" "Cyan"
            Write-ColorOutput "🔧 Backend API: http://localhost:8000" "Cyan"
            return $true
        } else {
            Write-ColorOutput "❌ Error al iniciar los servicios" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error al ejecutar docker-compose: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Stop-ApplicationServices {
    Write-ColorOutput "🛑 Deteniendo servicios..." "Yellow"
    
    try {
        docker-compose down
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Servicios detenidos correctamente" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Error al detener los servicios" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error al detener servicios: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Clear-ApplicationData {
    Write-ColorOutput "🧹 Limpiando datos de la aplicación..." "Yellow"
    
    try {
        # Detener servicios primero
        docker-compose down -v
        
        # Limpiar imágenes huérfanas
        docker image prune -f
        
        # Limpiar volúmenes huérfanos
        docker volume prune -f
        
        Write-ColorOutput "✅ Limpieza completada" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "❌ Error durante la limpieza: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Invoke-ApplicationBuild {
    Write-ColorOutput "🔨 Construyendo aplicación..." "Yellow"
    
    try {
        # Rebuild sin cache
        docker-compose build --no-cache
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Construcción completada" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Error en la construcción" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error durante la construcción: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Show-ApplicationLogs {
    Write-ColorOutput "📋 Mostrando logs de la aplicación..." "Cyan"
    
    try {
        docker-compose logs -f
    }
    catch {
        Write-ColorOutput "❌ Error al mostrar logs: $($_.Exception.Message)" "Red"
    }
}

function Show-Help {
    Write-ColorOutput "📖 Packfy MVP - Script de Desarrollo" "Cyan"
    Write-ColorOutput ""
    Write-ColorOutput "Uso:" "White"
    Write-ColorOutput "  .\dev.ps1 [start|stop|restart|status] [-Clean] [-Build] [-Logs]" "Gray"
    Write-ColorOutput ""
    Write-ColorOutput "Acciones:" "White"
    Write-ColorOutput "  start     - Inicia los servicios (por defecto)" "Gray"
    Write-ColorOutput "  stop      - Detiene los servicios" "Gray"
    Write-ColorOutput "  restart   - Reinicia los servicios" "Gray"
    Write-ColorOutput "  status    - Muestra el estado de los servicios" "Gray"
    Write-ColorOutput ""
    Write-ColorOutput "Parámetros:" "White"
    Write-ColorOutput "  -Clean    - Limpia datos antes de la acción" "Gray"
    Write-ColorOutput "  -Build    - Fuerza reconstrucción" "Gray"
    Write-ColorOutput "  -Logs     - Muestra logs después de la acción" "Gray"
    Write-ColorOutput ""
    Write-ColorOutput "Ejemplos:" "White"
    Write-ColorOutput "  .\dev.ps1 start" "Gray"
    Write-ColorOutput "  .\dev.ps1 restart -Clean -Build" "Gray"
    Write-ColorOutput "  .\dev.ps1 start -Logs" "Gray"
}

# Lógica principal
switch ($Action.ToLower()) {
    "start" {
        if ($Clean) {
            $cleanResult = Clear-ApplicationData
            if (-not $cleanResult) {
                exit 1
            }
        }
        
        if ($Build) {
            $buildResult = Invoke-ApplicationBuild
            if (-not $buildResult) {
                exit 1
            }
        }
        
        $startResult = Start-ApplicationServices
        if (-not $startResult) {
            exit 1
        }
        
        if ($Logs) {
            Show-ApplicationLogs
        }
    }
    
    "stop" {
        $stopResult = Stop-ApplicationServices
        if (-not $stopResult) {
            exit 1
        }
    }
    
    "restart" {
        if ($Clean) {
            $cleanResult = Clear-ApplicationData
            if (-not $cleanResult) {
                exit 1
            }
        }
        
        $stopResult = Stop-ApplicationServices
        if (-not $stopResult) {
            exit 1
        }
        
        if ($Build) {
            $buildResult = Invoke-ApplicationBuild
            if (-not $buildResult) {
                exit 1
            }
        }
        
        $startResult = Start-ApplicationServices
        if (-not $startResult) {
            exit 1
        }
        
        if ($Logs) {
            Show-ApplicationLogs
        }
    }
    
    "status" {
        Write-ColorOutput "📊 Estado de los servicios:" "Cyan"
        docker-compose ps
    }
    
    "help" {
        Show-Help
    }
    
    default {
        Write-ColorOutput "❌ Acción no reconocida: $Action" "Red"
        Show-Help
        exit 1
    }
}
