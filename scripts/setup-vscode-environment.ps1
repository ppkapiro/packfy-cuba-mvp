# 🔧 CONFIGURACIÓN COMPLETA DE ENTORNO VS CODE PARA PACKFY
# Script de PowerShell para configurar entorno sin problemas de codificación

param(
    [switch]$InstallExtensions,
    [switch]$ConfigureGit,
    [switch]$TestAll
)

Write-Host "🚀 CONFIGURANDO ENTORNO ÓPTIMO VS CODE..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# ✅ 1. CONFIGURAR CODIFICACIÓN GLOBAL
Write-Host "`n📝 1. CONFIGURANDO CODIFICACIÓN UTF-8..." -ForegroundColor Yellow
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

$env:PYTHONIOENCODING = "utf-8"
$env:LC_ALL = "en_US.UTF-8"
$env:LANG = "en_US.UTF-8"

Write-Host "✅ Codificación UTF-8 configurada" -ForegroundColor Green

# ✅ 2. CONFIGURAR POLÍTICAS DE POWERSHELL
Write-Host "`n🔐 2. CONFIGURANDO POLÍTICAS DE POWERSHELL..." -ForegroundColor Yellow
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "✅ Política de ejecución configurada" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Advertencia: No se pudo cambiar la política de ejecución" -ForegroundColor Yellow
}

# ✅ 3. INSTALAR EXTENSIONES RECOMENDADAS (OPCIONAL)
if ($InstallExtensions) {
    Write-Host "`n📦 3. INSTALANDO EXTENSIONES RECOMENDADAS..." -ForegroundColor Yellow

    $extensions = @(
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-vscode.powershell",
        "eamodio.gitlens",
        "ms-azuretools.vscode-docker",
        "vscode-icons-team.vscode-icons",
        "davidanson.vscode-markdownlint",
        "ms-vscode.vscode-typescript-next"
    )

    foreach ($ext in $extensions) {
        try {
            Write-Host "  📌 Instalando $ext..." -ForegroundColor White
            code --install-extension $ext --force
        } catch {
            Write-Host "  ⚠️  Error instalando $ext" -ForegroundColor Yellow
        }
    }
    Write-Host "✅ Extensiones procesadas" -ForegroundColor Green
}

# ✅ 4. CONFIGURAR GIT (OPCIONAL)
if ($ConfigureGit) {
    Write-Host "`n🔧 4. CONFIGURANDO GIT..." -ForegroundColor Yellow
    try {
        git config core.autocrlf false
        git config core.safecrlf false
        git config core.filemode false
        git config core.precomposeunicode true
        git config core.quotepath false
        Write-Host "✅ Git configurado para mejor compatibilidad" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Git no disponible o error en configuración" -ForegroundColor Yellow
    }
}

# ✅ 5. CREAR PROFILE DE POWERSHELL PERSONALIZADO
Write-Host "`n⚙️  5. CONFIGURANDO PROFILE DE POWERSHELL..." -ForegroundColor Yellow

$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path $profilePath -Parent

if (!(Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$profileContent = @"
# 🚀 PROFILE PERSONALIZADO PARA DESARROLLO PACKFY
# Auto-generado por setup-vscode-environment.ps1

# Configurar codificación UTF-8 automáticamente
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# Variables de entorno
`$env:PYTHONIOENCODING = "utf-8"
`$env:LC_ALL = "en_US.UTF-8"

# Alias útiles
Set-Alias -Name ll -Value Get-ChildItem -Force
Set-Alias -Name grep -Value Select-String -Force
Set-Alias -Name which -Value Get-Command -Force

# Función para cargar configuración de proyecto Packfy
function Load-PackfyConfig {
    if (Test-Path "scripts\powershell-config.ps1") {
        . "scripts\powershell-config.ps1"
        Write-Host "✅ Configuración Packfy cargada" -ForegroundColor Green
    }
}

# Auto-cargar si estamos en directorio Packfy
if (Test-Path "compose.yml") {
    Load-PackfyConfig
}

Write-Host "💡 PowerShell configurado para desarrollo" -ForegroundColor Cyan
"@

Set-Content -Path $profilePath -Value $profileContent -Encoding UTF8
Write-Host "✅ Profile de PowerShell configurado en: $profilePath" -ForegroundColor Green

# ✅ 6. VERIFICAR HERRAMIENTAS NECESARIAS
Write-Host "`n🔍 6. VERIFICANDO HERRAMIENTAS..." -ForegroundColor Yellow

$tools = @{
    "Node.js" = { node --version }
    "Python" = { python --version }
    "Docker" = { docker --version }
    "Git" = { git --version }
    "VS Code" = { code --version }
}

foreach ($tool in $tools.Keys) {
    try {
        $version = & $tools[$tool] 2>$null
        if ($version) {
            Write-Host "  ✅ $tool`: $($version[0])" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $tool`: NO DISPONIBLE" -ForegroundColor Red
        }
    } catch {
        Write-Host "  ❌ $tool`: NO DISPONIBLE" -ForegroundColor Red
    }
}

# ✅ 7. PROBAR CODIFICACIÓN
Write-Host "`n🧪 7. PROBANDO CODIFICACIÓN..." -ForegroundColor Yellow
Write-Host "  Caracteres especiales: áéíóú ñÑ üÜ ¡¿" -ForegroundColor White
Write-Host "  Emojis: 🚀 🐍 🔧 ✅ ⚠️ 📦 🌐" -ForegroundColor White
Write-Host "  Encoding: $([Console]::OutputEncoding.EncodingName)" -ForegroundColor White

# ✅ 8. PROBAR TODO SI SE SOLICITA
if ($TestAll) {
    Write-Host "`n🧪 8. EJECUTANDO PRUEBAS COMPLETAS..." -ForegroundColor Yellow

    # Probar servicios Docker
    try {
        Write-Host "  🐳 Probando Docker..." -ForegroundColor White
        docker-compose ps 2>$null
        Write-Host "  ✅ Docker Compose funcional" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  Docker Compose no disponible" -ForegroundColor Yellow
    }

    # Probar Python
    try {
        if (Test-Path "backend\venv\Scripts\python.exe") {
            Write-Host "  🐍 Probando Python virtual env..." -ForegroundColor White
            & "backend\venv\Scripts\python.exe" --version
            Write-Host "  ✅ Python virtual env funcional" -ForegroundColor Green
        }
    } catch {
        Write-Host "  ⚠️  Python virtual env no disponible" -ForegroundColor Yellow
    }

    # Probar Node.js en frontend
    try {
        Push-Location "frontend"
        Write-Host "  📦 Probando Node.js en frontend..." -ForegroundColor White
        npm --version | Out-Host
        Write-Host "  ✅ Node.js en frontend funcional" -ForegroundColor Green
        Pop-Location
    } catch {
        Pop-Location
        Write-Host "  ⚠️  Node.js en frontend no disponible" -ForegroundColor Yellow
    }
}

# ✅ 9. RESUMEN Y SIGUIENTE PASOS
Write-Host "`n🎉 ¡CONFIGURACIÓN COMPLETADA!" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green
Write-Host "✅ Codificación UTF-8 configurada" -ForegroundColor White
Write-Host "✅ PowerShell profile personalizado creado" -ForegroundColor White
Write-Host "✅ Variables de entorno configuradas" -ForegroundColor White

Write-Host "`n📋 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. 🔄 Reinicia VS Code para aplicar cambios" -ForegroundColor White
Write-Host "2. 📁 Abre el terminal integrado (Ctrl+`)" -ForegroundColor White
Write-Host "3. 🧪 Ejecuta 'Test-Encoding' para verificar" -ForegroundColor White
Write-Host "4. 🚀 Ejecuta 'Show-PackfyInfo' para ver info del proyecto" -ForegroundColor White

Write-Host "`n💡 COMANDOS ÚTILES DISPONIBLES:" -ForegroundColor Yellow
Write-Host "   Load-PackfyConfig       # Cargar configuración Packfy" -ForegroundColor White
Write-Host "   Start-PackfyServices    # Iniciar servicios" -ForegroundColor White
Write-Host "   Test-PackfyAPI         # Probar API" -ForegroundColor White

Write-Host "`n🔗 CONFIGURACIÓN APLICADA EN:" -ForegroundColor Cyan
Write-Host "   PowerShell Profile: $profilePath" -ForegroundColor White
Write-Host "   VS Code Settings: .vscode\settings.json" -ForegroundColor White
Write-Host "   VS Code Extensions: .vscode\extensions.json" -ForegroundColor White

if (!$InstallExtensions) {
    Write-Host "`n💡 TIP: Ejecuta con -InstallExtensions para instalar extensiones automáticamente" -ForegroundColor Yellow
}

if (!$ConfigureGit) {
    Write-Host "💡 TIP: Ejecuta con -ConfigureGit para optimizar configuración de Git" -ForegroundColor Yellow
}

Write-Host "`n🎯 ¡Entorno listo para desarrollo sin problemas de codificación!" -ForegroundColor Green
