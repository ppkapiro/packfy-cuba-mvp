# 🚀 CONFIGURACIÓN OPTIMAL DE POWERSHELL PARA VS CODE
# Este script configura PowerShell para evitar problemas de codificación

Write-Host "🔧 CONFIGURANDO POWERSHELL PARA MEJOR EXPERIENCIA..." -ForegroundColor Cyan

# ✅ 1. CONFIGURAR CODIFICACIÓN UTF-8
Write-Host "📝 Configurando codificación UTF-8..." -ForegroundColor Yellow
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# ✅ 2. CONFIGURAR VARIABLES DE ENTORNO
Write-Host "🌐 Configurando variables de entorno..." -ForegroundColor Yellow
$env:PYTHONIOENCODING = "utf-8"
$env:LC_ALL = "en_US.UTF-8"

# ✅ 3. CONFIGURAR POWERSHELL EXECUTION POLICY
Write-Host "🔐 Configurando política de ejecución..." -ForegroundColor Yellow
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "✅ Política de ejecución configurada correctamente" -ForegroundColor Green
} catch {
    Write-Host "⚠️  No se pudo cambiar la política de ejecución" -ForegroundColor Yellow
}

# ✅ 4. CONFIGURAR ALIAS ÚTILES
Write-Host "🔗 Configurando alias útiles..." -ForegroundColor Yellow
Set-Alias -Name ll -Value Get-ChildItem -Force
Set-Alias -Name grep -Value Select-String -Force
Set-Alias -Name which -Value Get-Command -Force

# ✅ 5. FUNCIONES ÚTILES PARA DESARROLLO
function Start-DevEnvironment {
    Write-Host "🚀 Iniciando entorno de desarrollo..." -ForegroundColor Green
    # Activar entorno virtual Python si existe
    if (Test-Path "backend\venv\Scripts\Activate.ps1") {
        Write-Host "🐍 Activando entorno virtual Python..." -ForegroundColor Yellow
        & "backend\venv\Scripts\Activate.ps1"
    }

    # Verificar Docker
    try {
        docker --version | Out-Host
        Write-Host "🐳 Docker disponible" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Docker no disponible" -ForegroundColor Yellow
    }

    # Verificar Node.js
    try {
        node --version | Out-Host
        Write-Host "📦 Node.js disponible" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Node.js no disponible" -ForegroundColor Yellow
    }
}

function Test-Encoding {
    Write-Host "🧪 PROBANDO CODIFICACIÓN..." -ForegroundColor Cyan
    Write-Host "OutputEncoding: $([Console]::OutputEncoding.EncodingName)" -ForegroundColor White
    Write-Host "InputEncoding: $([Console]::InputEncoding.EncodingName)" -ForegroundColor White
    Write-Host "Página de código actual: $(chcp)" -ForegroundColor White
    Write-Host "Caracteres especiales: áéíóú ñÑ üÜ ¡¿" -ForegroundColor Green
    Write-Host "Emojis: 🚀 🐍 🔧 ✅ ⚠️" -ForegroundColor Green
}

function Start-PackfyServices {
    param(
        [switch]$Build,
        [switch]$Logs
    )

    Write-Host "🚀 INICIANDO SERVICIOS PACKFY..." -ForegroundColor Cyan

    if ($Build) {
        Write-Host "🔨 Construyendo servicios..." -ForegroundColor Yellow
        docker-compose build
    }

    Write-Host "▶️  Iniciando servicios..." -ForegroundColor Yellow
    docker-compose up -d

    Write-Host "📊 Estado de servicios:" -ForegroundColor Green
    docker-compose ps

    if ($Logs) {
        Write-Host "📝 Mostrando logs..." -ForegroundColor Yellow
        docker-compose logs -f
    }
}

function Stop-PackfyServices {
    Write-Host "🛑 DETENIENDO SERVICIOS PACKFY..." -ForegroundColor Red
    docker-compose down
    Write-Host "✅ Servicios detenidos" -ForegroundColor Green
}

function Test-PackfyAPI {
    Write-Host "🧪 PROBANDO API PACKFY..." -ForegroundColor Cyan

    $apiUrl = "http://localhost:8000/api"
    $frontendUrl = "https://localhost:5173"

    try {
        $response = Invoke-RestMethod -Uri "$apiUrl/health/" -Method Get -TimeoutSec 5
        Write-Host "✅ API Backend: FUNCIONANDO" -ForegroundColor Green
        Write-Host "   URL: $apiUrl" -ForegroundColor White
    } catch {
        Write-Host "❌ API Backend: NO DISPONIBLE" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    }

    try {
        $response = Invoke-WebRequest -Uri $frontendUrl -Method Head -TimeoutSec 5 -SkipCertificateCheck
        Write-Host "✅ Frontend: FUNCIONANDO" -ForegroundColor Green
        Write-Host "   URL: $frontendUrl" -ForegroundColor White
    } catch {
        Write-Host "❌ Frontend: NO DISPONIBLE" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    }
}

function Open-PackfyUrls {
    Write-Host "🌐 ABRIENDO URLS DE PACKFY..." -ForegroundColor Cyan

    # PC Desktop
    Start-Process "https://localhost:5173"
    Write-Host "📱 Abriendo PC Desktop: https://localhost:5173" -ForegroundColor Green

    # Admin Django
    Start-Process "http://localhost:8000/admin"
    Write-Host "⚙️  Abriendo Admin Django: http://localhost:8000/admin" -ForegroundColor Green

    Write-Host "📲 URL para móvil: https://192.168.12.178:5173" -ForegroundColor Yellow
}

function Show-PackfyInfo {
    Write-Host "`n🎯 INFORMACIÓN RÁPIDA PACKFY" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "📱 PC Desktop:    https://localhost:5173" -ForegroundColor Green
    Write-Host "📲 Móvil:         https://192.168.12.178:5173" -ForegroundColor Green
    Write-Host "🔧 API Backend:   http://localhost:8000/api" -ForegroundColor Green
    Write-Host "⚙️  Admin Django:  http://localhost:8000/admin" -ForegroundColor Green
    Write-Host "`n🔐 CREDENCIALES:" -ForegroundColor Yellow
    Write-Host "   Admin: admin@packfy.cu / admin123" -ForegroundColor White
    Write-Host "   Test:  test@packfy.cu / test123" -ForegroundColor White
    Write-Host "`n🚀 COMANDOS ÚTILES:" -ForegroundColor Yellow
    Write-Host "   Start-PackfyServices     # Iniciar servicios" -ForegroundColor White
    Write-Host "   Stop-PackfyServices      # Detener servicios" -ForegroundColor White
    Write-Host "   Test-PackfyAPI          # Probar API" -ForegroundColor White
    Write-Host "   Open-PackfyUrls         # Abrir URLs" -ForegroundColor White
    Write-Host "   Test-Encoding           # Probar codificación" -ForegroundColor White
}

# ✅ 6. CONFIGURAR PROMPT PERSONALIZADO
function Prompt {
    $location = Get-Location
    $gitBranch = ""

    # Detectar rama de Git si estamos en un repositorio
    try {
        $gitBranch = git branch --show-current 2>$null
        if ($gitBranch) {
            $gitBranch = " 🌿($gitBranch)"
        }
    } catch {
        # Ignorar errores si no hay Git
    }

    # Detectar si estamos en entorno virtual Python
    $venvIndicator = ""
    if ($env:VIRTUAL_ENV) {
        $venvName = Split-Path $env:VIRTUAL_ENV -Leaf
        $venvIndicator = " 🐍($venvName)"
    }

    Write-Host "🚀 " -NoNewline -ForegroundColor Cyan
    Write-Host $location -NoNewline -ForegroundColor Green
    Write-Host $gitBranch -NoNewline -ForegroundColor Yellow
    Write-Host $venvIndicator -NoNewline -ForegroundColor Blue
    Write-Host ""
    return "PS> "
}

# ✅ 7. MENSAJE DE BIENVENIDA
Write-Host "`n🎉 ¡POWERSHELL CONFIGURADO CORRECTAMENTE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✅ Codificación UTF-8 activada" -ForegroundColor White
Write-Host "✅ Variables de entorno configuradas" -ForegroundColor White
Write-Host "✅ Funciones de desarrollo cargadas" -ForegroundColor White
Write-Host "✅ Prompt personalizado activado" -ForegroundColor White

Write-Host "`n💡 Ejecuta 'Show-PackfyInfo' para ver información del proyecto" -ForegroundColor Cyan
Write-Host "💡 Ejecuta 'Test-Encoding' para verificar codificación" -ForegroundColor Cyan

# ✅ 8. AUTO-CONFIGURAR DIRECTORIO SI ESTAMOS EN PACKFY
if (Test-Path "compose.yml") {
    Write-Host "`n🎯 Detectado proyecto Packfy - Configurando entorno..." -ForegroundColor Yellow
    Start-DevEnvironment
}
