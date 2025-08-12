# 🚀 Packfy - Desarrollo Inteligente
# Script que detecta cambios y solo recarga lo necesario

param(
    [string]$Mode = "watch",  # watch, local, docker
    [switch]$Reset
)

Write-Host "🚀 PACKFY - DESARROLLO INTELIGENTE" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

function Show-Options {
    Write-Host ""
    Write-Host "📋 MODOS DISPONIBLES:" -ForegroundColor Cyan
    Write-Host "  1. 👁️  watch    - Docker con recarga automática" -ForegroundColor White
    Write-Host "  2. 🏠 local    - Desarrollo local nativo" -ForegroundColor White
    Write-Host "  3. 🐳 docker   - Docker completo (rebuild)" -ForegroundColor White
    Write-Host "  4. 🔌 mcp      - Servidor MCP para VS Code" -ForegroundColor White
    Write-Host ""
}

function Start-WatchMode {
    Write-Host "👁️ MODO WATCH: Recarga automática activada" -ForegroundColor Yellow

    # Iniciar servicios Docker
    Write-Host "🐳 Iniciando servicios..." -ForegroundColor Cyan
    docker-compose up -d

    # Configurar watch para backend
    Write-Host "🔧 Configurando watch para backend..." -ForegroundColor Cyan
    docker-compose exec -d backend python manage.py runserver 0.0.0.0:8000 --reload

    # Watch para frontend ya está configurado en Vite
    Write-Host "🌐 Frontend en modo watch automático" -ForegroundColor Cyan

    Write-Host "✅ Sistema iniciado en modo watch" -ForegroundColor Green
    Write-Host "💡 Los cambios se aplicarán automáticamente" -ForegroundColor Yellow
}

function Start-LocalMode {
    Write-Host "🏠 MODO LOCAL: Desarrollo nativo" -ForegroundColor Yellow

    # Solo BD en Docker
    docker-compose up -d database

    # Backend local
    Start-Job -ScriptBlock {
        Set-Location "backend"
        python manage.py runserver 127.0.0.1:8000
    } -Name "BackendLocal"

    # Frontend local
    Start-Job -ScriptBlock {
        Set-Location "frontend"
        npm run dev
    } -Name "FrontendLocal"

    Write-Host "✅ Desarrollo local iniciado" -ForegroundColor Green
}

function Start-DockerMode {
    Write-Host "🐳 MODO DOCKER: Reconstrucción completa" -ForegroundColor Yellow

    if ($Reset) {
        Write-Host "🧹 Limpiando Docker..." -ForegroundColor Red
        docker-compose down --volumes --remove-orphans
        docker system prune -f
    }

    Write-Host "🔨 Reconstruyendo servicios..." -ForegroundColor Cyan
    docker-compose build --no-cache
    docker-compose up -d

    Write-Host "✅ Docker reconstruido completamente" -ForegroundColor Green
}

function Start-MCPMode {
    Write-Host "🔌 MODO MCP: Servidor para VS Code" -ForegroundColor Yellow

    # Instalar dependencias MCP si no existen
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Python no encontrado" -ForegroundColor Red
        return
    }

    Write-Host "📦 Instalando/verificando dependencias MCP..." -ForegroundColor Cyan
    pip install mcp asyncio subprocess-run

    Write-Host "🚀 Iniciando servidor MCP..." -ForegroundColor Cyan
    python mcp-server.py
}

# Mostrar opciones si no se especifica modo
if (-not $Mode -or $Mode -eq "help") {
    Show-Options
    $Mode = Read-Host "Selecciona modo (watch/local/docker/mcp)"
}

# Ejecutar según el modo seleccionado
switch ($Mode.ToLower()) {
    "watch" { Start-WatchMode }
    "local" { Start-LocalMode }
    "docker" { Start-DockerMode }
    "mcp" { Start-MCPMode }
    default {
        Write-Host "❌ Modo no válido: $Mode" -ForegroundColor Red
        Show-Options
    }
}

Write-Host ""
Write-Host "🎯 URLs de desarrollo:" -ForegroundColor Yellow
Write-Host "   🌐 Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "   🔧 Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   📊 Base datos: localhost:5433" -ForegroundColor White
Write-Host ""
Write-Host "💡 Para cambiar modo, ejecuta: .\dev-smart.ps1 -Mode <modo>" -ForegroundColor Cyan
