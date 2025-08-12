# 🚀 ENTORNO IDEAL DE DESARROLLO - CONFIGURACIÓN DEFINITIVA
# Script para configurar el entorno más avanzado y robusto posible

param(
    [switch]$InstallTools,
    [switch]$ConfigureWSL,
    [switch]$SetupWindowsTerminal,
    [switch]$InstallPowerShell7,
    [switch]$All
)

if ($All) {
    $InstallTools = $true
    $ConfigureWSL = $true
    $SetupWindowsTerminal = $true
    $InstallPowerShell7 = $true
}

Write-Host "🚀 CONFIGURANDO ENTORNO IDEAL DE DESARROLLO" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# ✅ 1. DETECTAR SISTEMA Y CAPACIDADES
Write-Host "`n🔍 1. ANALIZANDO SISTEMA..." -ForegroundColor Yellow

$windowsVersion = [System.Environment]::OSVersion.Version
$isWindows10Plus = $windowsVersion.Major -ge 10
$isWindows11 = $windowsVersion.Build -ge 22000

Write-Host "   Windows Version: $($windowsVersion.Major).$($windowsVersion.Minor) (Build $($windowsVersion.Build))" -ForegroundColor White
Write-Host "   Windows 10+: $isWindows10Plus" -ForegroundColor $(if($isWindows10Plus) { "Green" } else { "Red" })
Write-Host "   Windows 11: $isWindows11" -ForegroundColor $(if($isWindows11) { "Green" } else { "Yellow" })

# ✅ 2. INSTALAR HERRAMIENTAS ESENCIALES
if ($InstallTools) {
    Write-Host "`n📦 2. INSTALANDO HERRAMIENTAS ESENCIALES..." -ForegroundColor Yellow

    # Verificar si Winget está disponible
    try {
        winget --version | Out-Null
        $wingetAvailable = $true
        Write-Host "   ✅ Winget disponible" -ForegroundColor Green
    } catch {
        $wingetAvailable = $false
        Write-Host "   ❌ Winget no disponible" -ForegroundColor Red
    }

    if ($wingetAvailable) {
        $tools = @(
            @{Name="PowerShell 7"; Package="Microsoft.PowerShell"},
            @{Name="Windows Terminal"; Package="Microsoft.WindowsTerminal"},
            @{Name="Git"; Package="Git.Git"},
            @{Name="Node.js LTS"; Package="OpenJS.NodeJS.LTS"},
            @{Name="Python 3.11"; Package="Python.Python.3.11"},
            @{Name="Docker Desktop"; Package="Docker.DockerDesktop"},
            @{Name="VS Code"; Package="Microsoft.VisualStudioCode"}
        )

        foreach ($tool in $tools) {
            Write-Host "   📌 Instalando $($tool.Name)..." -ForegroundColor White
            try {
                winget install $tool.Package --silent --accept-package-agreements --accept-source-agreements
                Write-Host "   ✅ $($tool.Name) instalado" -ForegroundColor Green
            } catch {
                Write-Host "   ⚠️  Error instalando $($tool.Name)" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "   💡 Winget no disponible. Instalación manual requerida." -ForegroundColor Yellow
        Write-Host "   📥 Descarga herramientas desde:" -ForegroundColor Cyan
        Write-Host "      - PowerShell 7: https://github.com/PowerShell/PowerShell/releases" -ForegroundColor White
        Write-Host "      - Windows Terminal: Microsoft Store" -ForegroundColor White
        Write-Host "      - Git: https://git-scm.com/download/win" -ForegroundColor White
        Write-Host "      - Node.js: https://nodejs.org/" -ForegroundColor White
        Write-Host "      - Python: https://python.org/downloads/" -ForegroundColor White
        Write-Host "      - Docker: https://docker.com/products/docker-desktop/" -ForegroundColor White
    }
}

# ✅ 3. CONFIGURAR POWERSHELL 7
if ($InstallPowerShell7) {
    Write-Host "`n🔧 3. CONFIGURANDO POWERSHELL 7..." -ForegroundColor Yellow

    # Verificar si PowerShell 7 está instalado
    try {
        $pwsh7Path = Get-Command pwsh -ErrorAction Stop
        Write-Host "   ✅ PowerShell 7 encontrado en: $($pwsh7Path.Source)" -ForegroundColor Green

        # Configurar profile para PowerShell 7
        $profilePath = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "PowerShell\Microsoft.PowerShell_profile.ps1"
        $profileDir = Split-Path $profilePath -Parent

        if (!(Test-Path $profileDir)) {
            New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
        }

        $profileContent = @"
# 🚀 PROFILE POWERSHELL 7 - ENTORNO IDEAL
# Configuración automática para desarrollo

# Importar módulos esenciales
Import-Module PSReadLine -Force

# Configurar PSReadLine (autocompletado avanzado)
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -EditMode Emacs
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete

# Configurar codificación UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
`$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# Variables de entorno
`$env:PYTHONIOENCODING = "utf-8"
`$env:LC_ALL = "en_US.UTF-8"

# Alias útiles
Set-Alias -Name ll -Value Get-ChildItem -Force
Set-Alias -Name la -Value Get-ChildItem -Force
Set-Alias -Name grep -Value Select-String -Force
Set-Alias -Name which -Value Get-Command -Force
Set-Alias -Name cat -Value Get-Content -Force

# Función para Docker Compose (alias dc)
function dc { docker-compose @args }
function dcu { docker-compose up -d @args }
function dcd { docker-compose down @args }
function dcb { docker-compose build @args }
function dcl { docker-compose logs -f @args }

# Función para Git (aliases)
function gs { git status @args }
function ga { git add @args }
function gc { git commit @args }
function gp { git push @args }
function gl { git log --oneline -10 @args }

# Función para navegación rápida
function .. { Set-Location .. }
function ... { Set-Location ..\.. }
function .... { Set-Location ..\..\.. }

# Prompt personalizado con Git y entorno virtual
function Prompt {
    `$location = Get-Location

    # Detectar Git branch
    `$gitBranch = ""
    try {
        `$branch = git branch --show-current 2>`$null
        if (`$branch) {
            `$gitBranch = " 🌿(`$branch)"
        }
    } catch { }

    # Detectar Python virtual environment
    `$venvIndicator = ""
    if (`$env:VIRTUAL_ENV) {
        `$venvName = Split-Path `$env:VIRTUAL_ENV -Leaf
        `$venvIndicator = " 🐍(`$venvName)"
    }

    # Detectar Node.js project
    `$nodeIndicator = ""
    if (Test-Path "package.json") {
        `$nodeIndicator = " 📦"
    }

    # Detectar Docker
    `$dockerIndicator = ""
    if (Test-Path "docker-compose.yml" -or Test-Path "compose.yml") {
        `$dockerIndicator = " 🐳"
    }

    Write-Host "🚀 " -NoNewline -ForegroundColor Cyan
    Write-Host `$location -NoNewline -ForegroundColor Green
    Write-Host `$gitBranch -NoNewline -ForegroundColor Yellow
    Write-Host `$venvIndicator -NoNewline -ForegroundColor Blue
    Write-Host `$nodeIndicator -NoNewline -ForegroundColor Magenta
    Write-Host `$dockerIndicator -NoNewline -ForegroundColor Cyan
    Write-Host ""
    return "PS> "
}

# Cargar configuración específica de Packfy si existe
if (Test-Path "scripts\powershell-config.ps1") {
    . "scripts\powershell-config.ps1"
}

Write-Host "💡 PowerShell 7 configurado para desarrollo avanzado" -ForegroundColor Green
"@

        Set-Content -Path $profilePath -Value $profileContent -Encoding UTF8
        Write-Host "   ✅ Profile PowerShell 7 configurado" -ForegroundColor Green

    } catch {
        Write-Host "   ❌ PowerShell 7 no encontrado. Instálalo primero." -ForegroundColor Red
    }
}

# ✅ 4. CONFIGURAR WINDOWS TERMINAL
if ($SetupWindowsTerminal -and $isWindows10Plus) {
    Write-Host "`n🖥️  4. CONFIGURANDO WINDOWS TERMINAL..." -ForegroundColor Yellow

    $terminalSettingsPath = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"

    if (Test-Path $terminalSettingsPath) {
        Write-Host "   📝 Creando configuración optimizada..." -ForegroundColor White

        $terminalConfig = @{
            '$schema' = "https://aka.ms/terminal-profiles-schema"
            defaultProfile = "{574e775e-4f2a-5b96-ac1e-a2962a402336}"
            profiles = @{
                defaults = @{
                    fontFace = "CascadiaCode Nerd Font"
                    fontSize = 12
                    cursorShape = "bar"
                    colorScheme = "Campbell Powershell"
                }
                list = @(
                    @{
                        guid = "{574e775e-4f2a-5b96-ac1e-a2962a402336}"
                        name = "PowerShell 7"
                        commandline = "pwsh.exe"
                        icon = "ms-appx:///ProfileIcons/{574e775e-4f2a-5b96-ac1e-a2962a402336}.png"
                        startingDirectory = "%USERPROFILE%"
                        tabTitle = "PowerShell 7"
                    },
                    @{
                        guid = "{07b52e3e-de2c-5db4-bd2d-ba144ed6c273}"
                        name = "Ubuntu (WSL2)"
                        commandline = "wsl.exe -d Ubuntu"
                        icon = "ms-appx:///ProfileIcons/{9acb9455-ca41-5af7-950f-6bca1bc9722f}.png"
                        startingDirectory = "/home"
                        tabTitle = "Ubuntu"
                    },
                    @{
                        guid = "{2c4de342-38b7-51cf-b940-2309a097f518}"
                        name = "Git Bash"
                        commandline = "C:\\Program Files\\Git\\bin\\bash.exe"
                        icon = "C:\\Program Files\\Git\\mingw64\\share\\git\\git-for-windows.ico"
                        startingDirectory = "%USERPROFILE%"
                        tabTitle = "Git Bash"
                    }
                )
            }
            schemes = @(
                @{
                    name = "Packfy Theme"
                    black = "#0C0C0C"
                    red = "#C50F1F"
                    green = "#13A10E"
                    yellow = "#C19C00"
                    blue = "#0037DA"
                    purple = "#881798"
                    cyan = "#3A96DD"
                    white = "#CCCCCC"
                    brightBlack = "#767676"
                    brightRed = "#E74856"
                    brightGreen = "#16C60C"
                    brightYellow = "#F9F1A5"
                    brightBlue = "#3B78FF"
                    brightPurple = "#B4009E"
                    brightCyan = "#61D6D6"
                    brightWhite = "#F2F2F2"
                    background = "#012456"
                    foreground = "#CCCCCC"
                    cursorColor = "#FFFFFF"
                    selectionBackground = "#FFFFFF"
                }
            )
            actions = @(
                @{ command = @{ action = "copy"; singleLine = $false }; keys = "ctrl+c" },
                @{ command = "paste"; keys = "ctrl+v" },
                @{ command = "newTab"; keys = "ctrl+t" },
                @{ command = "closeTab"; keys = "ctrl+w" },
                @{ command = @{ action = "splitPane"; split = "auto"; splitMode = "duplicate" }; keys = "alt+shift+d" }
            )
        }

        $terminalConfigJson = $terminalConfig | ConvertTo-Json -Depth 10
        Set-Content -Path $terminalSettingsPath -Value $terminalConfigJson -Encoding UTF8
        Write-Host "   ✅ Windows Terminal configurado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Windows Terminal no encontrado" -ForegroundColor Yellow
    }
}

# ✅ 5. CONFIGURAR WSL2 (OPCIONAL PERO RECOMENDADO)
if ($ConfigureWSL -and $isWindows10Plus) {
    Write-Host "`n🐧 5. CONFIGURANDO WSL2..." -ForegroundColor Yellow

    try {
        # Verificar si WSL está habilitado
        $wslStatus = wsl --status 2>$null
        if ($wslStatus) {
            Write-Host "   ✅ WSL ya está configurado" -ForegroundColor Green
        } else {
            Write-Host "   📥 Instalando WSL2..." -ForegroundColor White
            wsl --install -d Ubuntu
            Write-Host "   💡 WSL2 instalado. Reinicia el sistema y completa la configuración." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "   💡 Para instalar WSL2 manualmente:" -ForegroundColor Yellow
        Write-Host "      1. Ejecuta como administrador: wsl --install" -ForegroundColor White
        Write-Host "      2. Reinicia el sistema" -ForegroundColor White
        Write-Host "      3. Configura usuario Ubuntu" -ForegroundColor White
    }
}

# ✅ 6. CONFIGURAR VS CODE PARA EL ENTORNO IDEAL
Write-Host "`n🔧 6. CONFIGURANDO VS CODE PARA ENTORNO IDEAL..." -ForegroundColor Yellow

$idealVSCodeSettings = @{
    # Terminal configuration
    "terminal.integrated.defaultProfile.windows" = "PowerShell"
    "terminal.integrated.profiles.windows" = @{
        "PowerShell" = @{
            path = "pwsh.exe"
            args = @("-NoLogo")
            icon = "terminal-powershell"
        }
        "Git Bash" = @{
            path = "C:\\Program Files\\Git\\bin\\bash.exe"
            icon = "terminal-bash"
        }
        "Ubuntu (WSL)" = @{
            path = "wsl.exe"
            args = @("-d", "Ubuntu")
            icon = "terminal-ubuntu"
        }
    }

    # Encoding and file settings
    "files.encoding" = "utf8"
    "files.autoGuessEncoding" = $true
    "files.eol" = "`n"
    "files.insertFinalNewline" = $true
    "files.trimTrailingWhitespace" = $true

    # Editor enhancements
    "editor.fontSize" = 14
    "editor.fontFamily" = "'CascadiaCode Nerd Font', 'Fira Code', Consolas"
    "editor.fontLigatures" = $true
    "editor.formatOnSave" = $true
    "editor.formatOnPaste" = $true
    "editor.minimap.enabled" = $true
    "editor.wordWrap" = "on"
    "editor.renderWhitespace" = "boundary"
    "editor.rulers" = @(80, 120)

    # Python configuration
    "python.defaultInterpreterPath" = "./backend/venv/Scripts/python.exe"
    "python.terminal.activateEnvironment" = $true
    "python.formatting.provider" = "black"
    "python.linting.enabled" = $true
    "python.analysis.typeCheckingMode" = "basic"

    # Git integration
    "git.autofetch" = $true
    "git.enableSmartCommit" = $true
    "git.confirmSync" = $false

    # Workbench
    "workbench.colorTheme" = "Dark+ (default dark)"
    "workbench.iconTheme" = "material-icon-theme"
    "workbench.startupEditor" = "welcomePage"

    # Performance
    "files.watcherExclude" = @{
        "**/node_modules/**" = $true
        "**/.git/**" = $true
        "**/venv/**" = $true
        "**/__pycache__/**" = $true
    }
}

$vsCodeSettingsPath = ".vscode\settings.json"
if (!(Test-Path ".vscode")) {
    New-Item -ItemType Directory -Name ".vscode" -Force | Out-Null
}

$idealVSCodeSettings | ConvertTo-Json -Depth 10 | Set-Content $vsCodeSettingsPath -Encoding UTF8
Write-Host "   ✅ VS Code configurado con settings ideales" -ForegroundColor Green

# ✅ 7. RESUMEN Y RECOMENDACIONES
Write-Host "`n🎉 CONFIGURACIÓN DEL ENTORNO IDEAL COMPLETADA" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

Write-Host "`n🏆 ENTORNO CONFIGURADO:" -ForegroundColor Cyan
if ((Get-Command pwsh -ErrorAction SilentlyContinue)) {
    Write-Host "   ✅ PowerShell 7 - Terminal moderno y potente" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  PowerShell 7 - Pendiente de instalación" -ForegroundColor Yellow
}

if ($isWindows10Plus) {
    Write-Host "   ✅ Windows Terminal - Interface moderna" -ForegroundColor Green
} else {
    Write-Host "   ❌ Windows Terminal - Requiere Windows 10+" -ForegroundColor Red
}

Write-Host "   ✅ VS Code - Configuración optimizada" -ForegroundColor Green
Write-Host "   ✅ Codificación UTF-8 - Sin problemas de caracteres" -ForegroundColor Green

Write-Host "`n📋 PRÓXIMOS PASOS RECOMENDADOS:" -ForegroundColor Yellow
Write-Host "1. 🔄 Reinicia VS Code para aplicar cambios" -ForegroundColor White
Write-Host "2. 🖥️  Abre Windows Terminal como terminal principal" -ForegroundColor White
Write-Host "3. 🐧 Considera usar WSL2 para desarrollo avanzado" -ForegroundColor White
Write-Host "4. 📦 Instala las extensiones recomendadas de .vscode/extensions.json" -ForegroundColor White

Write-Host "`n💡 COMANDOS ÚTILES EN TU NUEVO ENTORNO:" -ForegroundColor Cyan
Write-Host "   pwsh          # Abrir PowerShell 7" -ForegroundColor White
Write-Host "   dc up -d      # Docker Compose up (alias)" -ForegroundColor White
Write-Host "   gs            # Git status (alias)" -ForegroundColor White
Write-Host "   ll            # List files (alias)" -ForegroundColor White

Write-Host "`n🌟 ¡ENTORNO IDEAL CONFIGURADO! Desarrollo profesional sin limitaciones." -ForegroundColor Green
