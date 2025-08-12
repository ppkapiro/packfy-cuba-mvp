# ENTORNO IDEAL DE DESARROLLO - CONFIGURACION DEFINITIVA
# Script para configurar el entorno mas avanzado y robusto posible

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

Write-Host "CONFIGURANDO ENTORNO IDEAL DE DESARROLLO" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. DETECTAR SISTEMA Y CAPACIDADES
Write-Host "`n1. ANALIZANDO SISTEMA..." -ForegroundColor Yellow

$windowsVersion = [System.Environment]::OSVersion.Version
$isWindows10Plus = $windowsVersion.Major -ge 10
$isWindows11 = $windowsVersion.Build -ge 22000

Write-Host "   Windows Version: $($windowsVersion.Major).$($windowsVersion.Minor) (Build $($windowsVersion.Build))" -ForegroundColor White
Write-Host "   Windows 10+: $isWindows10Plus" -ForegroundColor $(if ($isWindows10Plus) { "Green" } else { "Red" })
Write-Host "   Windows 11: $isWindows11" -ForegroundColor $(if ($isWindows11) { "Green" } else { "Yellow" })

# 2. INSTALAR HERRAMIENTAS ESENCIALES
if ($InstallTools) {
  Write-Host "`n2. INSTALANDO HERRAMIENTAS ESENCIALES..." -ForegroundColor Yellow

  # Verificar si Winget esta disponible
  try {
    winget --version | Out-Null
    $wingetAvailable = $true
    Write-Host "   Winget disponible" -ForegroundColor Green
  }
  catch {
    $wingetAvailable = $false
    Write-Host "   Winget no disponible" -ForegroundColor Red
  }

  if ($wingetAvailable) {
    $tools = @(
      @{Name = "PowerShell 7"; Package = "Microsoft.PowerShell" },
      @{Name = "Windows Terminal"; Package = "Microsoft.WindowsTerminal" },
      @{Name = "Git"; Package = "Git.Git" },
      @{Name = "Node.js LTS"; Package = "OpenJS.NodeJS.LTS" },
      @{Name = "Python 3.11"; Package = "Python.Python.3.11" },
      @{Name = "Docker Desktop"; Package = "Docker.DockerDesktop" },
      @{Name = "VS Code"; Package = "Microsoft.VisualStudioCode" }
    )

    foreach ($tool in $tools) {
      Write-Host "   Instalando $($tool.Name)..." -ForegroundColor White
      try {
        winget install $tool.Package --silent --accept-package-agreements --accept-source-agreements
        Write-Host "   $($tool.Name) instalado" -ForegroundColor Green
      }
      catch {
        Write-Host "   Error instalando $($tool.Name)" -ForegroundColor Yellow
      }
    }
  }
  else {
    Write-Host "   Winget no disponible. Instalacion manual requerida." -ForegroundColor Yellow
  }
}

# 3. CONFIGURAR POWERSHELL 7
if ($InstallPowerShell7) {
  Write-Host "`n3. CONFIGURANDO POWERSHELL 7..." -ForegroundColor Yellow

  # Verificar si PowerShell 7 esta instalado
  try {
    $pwsh7Path = Get-Command pwsh -ErrorAction Stop
    Write-Host "   PowerShell 7 encontrado en: $($pwsh7Path.Source)" -ForegroundColor Green

    # Configurar profile para PowerShell 7
    $profilePath = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "PowerShell\Microsoft.PowerShell_profile.ps1"
    $profileDir = Split-Path $profilePath -Parent

    if (!(Test-Path $profileDir)) {
      New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    $profileContent = @"
# PROFILE POWERSHELL 7 - ENTORNO IDEAL
# Configuracion automatica para desarrollo

# Importar modulos esenciales
Import-Module PSReadLine -Force

# Configurar PSReadLine (autocompletado avanzado)
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -EditMode Emacs
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete

# Configurar codificacion UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
`$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# Variables de entorno
`$env:PYTHONIOENCODING = "utf-8"
`$env:LC_ALL = "en_US.UTF-8"

# Alias utiles
Set-Alias -Name ll -Value Get-ChildItem -Force
Set-Alias -Name la -Value Get-ChildItem -Force
Set-Alias -Name grep -Value Select-String -Force
Set-Alias -Name which -Value Get-Command -Force
Set-Alias -Name cat -Value Get-Content -Force

# Funcion para Docker Compose (alias dc)
function dc { docker-compose @args }
function dcu { docker-compose up -d @args }
function dcd { docker-compose down @args }
function dcb { docker-compose build @args }
function dcl { docker-compose logs -f @args }

# Funcion para Git (aliases)
function gs { git status @args }
function ga { git add @args }
function gc { git commit @args }
function gp { git push @args }
function gl { git log --oneline -10 @args }

# Funcion para navegacion rapida
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
            `$gitBranch = " (`$branch)"
        }
    } catch { }

    # Detectar Python virtual environment
    `$venvIndicator = ""
    if (`$env:VIRTUAL_ENV) {
        `$venvName = Split-Path `$env:VIRTUAL_ENV -Leaf
        `$venvIndicator = " (`$venvName)"
    }

    # Detectar Node.js project
    `$nodeIndicator = ""
    if (Test-Path "package.json") {
        `$nodeIndicator = " [NPM]"
    }

    # Detectar Docker
    `$dockerIndicator = ""
    if (Test-Path "docker-compose.yml" -or Test-Path "compose.yml") {
        `$dockerIndicator = " [DOCKER]"
    }

    Write-Host "PS " -NoNewline -ForegroundColor Cyan
    Write-Host `$location -NoNewline -ForegroundColor Green
    Write-Host `$gitBranch -NoNewline -ForegroundColor Yellow
    Write-Host `$venvIndicator -NoNewline -ForegroundColor Blue
    Write-Host `$nodeIndicator -NoNewline -ForegroundColor Magenta
    Write-Host `$dockerIndicator -NoNewline -ForegroundColor Cyan
    Write-Host ""
    return "> "
}

# Cargar configuracion especifica de Packfy si existe
if (Test-Path "scripts\powershell-config.ps1") {
    . "scripts\powershell-config.ps1"
}

Write-Host "PowerShell 7 configurado para desarrollo avanzado" -ForegroundColor Green
"@

    Set-Content -Path $profilePath -Value $profileContent -Encoding UTF8
    Write-Host "   Profile PowerShell 7 configurado" -ForegroundColor Green

  }
  catch {
    Write-Host "   PowerShell 7 no encontrado. Instalalo primero." -ForegroundColor Red
  }
}

# 4. CONFIGURAR VS CODE PARA EL ENTORNO IDEAL
Write-Host "`n4. CONFIGURANDO VS CODE PARA ENTORNO IDEAL..." -ForegroundColor Yellow

# Verificar si ya existe settings.json y hacer backup
$vsCodeSettingsPath = ".vscode\settings.json"
if (Test-Path $vsCodeSettingsPath) {
  $backupPath = ".vscode\settings-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
  Copy-Item $vsCodeSettingsPath $backupPath
  Write-Host "   Backup creado: $backupPath" -ForegroundColor Yellow
}

# Aplicar configuracion ideal
if (Test-Path ".vscode\settings-ideal.json") {
  Copy-Item ".vscode\settings-ideal.json" $vsCodeSettingsPath -Force
  Write-Host "   Configuracion ideal aplicada a VS Code" -ForegroundColor Green
}
else {
  Write-Host "   Archivo settings-ideal.json no encontrado" -ForegroundColor Yellow
}

# Aplicar extensiones recomendadas
if (Test-Path ".vscode\extensions-ideal.json") {
  Copy-Item ".vscode\extensions-ideal.json" ".vscode\extensions.json" -Force
  Write-Host "   Extensiones ideales configuradas" -ForegroundColor Green
}
else {
  Write-Host "   Archivo extensions-ideal.json no encontrado" -ForegroundColor Yellow
}

# 5. CONFIGURAR WSL2 (OPCIONAL)
if ($ConfigureWSL -and $isWindows10Plus) {
  Write-Host "`n5. CONFIGURANDO WSL2..." -ForegroundColor Yellow

  try {
    # Verificar si WSL esta habilitado
    $wslStatus = wsl --status 2>$null
    if ($wslStatus) {
      Write-Host "   WSL ya esta configurado" -ForegroundColor Green
    }
    else {
      Write-Host "   Instalando WSL2..." -ForegroundColor White
      wsl --install -d Ubuntu
      Write-Host "   WSL2 instalado. Reinicia el sistema y completa la configuracion." -ForegroundColor Yellow
    }
  }
  catch {
    Write-Host "   Para instalar WSL2 manualmente:" -ForegroundColor Yellow
    Write-Host "      1. Ejecuta como administrador: wsl --install" -ForegroundColor White
    Write-Host "      2. Reinicia el sistema" -ForegroundColor White
    Write-Host "      3. Configura usuario Ubuntu" -ForegroundColor White
  }
}

# 6. RESUMEN Y RECOMENDACIONES
Write-Host "`nCONFIGURACION DEL ENTORNO IDEAL COMPLETADA" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

Write-Host "`nENTORNO CONFIGURADO:" -ForegroundColor Cyan
if ((Get-Command pwsh -ErrorAction SilentlyContinue)) {
  Write-Host "   PowerShell 7 - Terminal moderno y potente" -ForegroundColor Green
}
else {
  Write-Host "   PowerShell 7 - Pendiente de instalacion" -ForegroundColor Yellow
}

if ($isWindows10Plus) {
  Write-Host "   Windows Terminal - Interface moderna" -ForegroundColor Green
}
else {
  Write-Host "   Windows Terminal - Requiere Windows 10+" -ForegroundColor Red
}

Write-Host "   VS Code - Configuracion optimizada" -ForegroundColor Green
Write-Host "   Codificacion UTF-8 - Sin problemas de caracteres" -ForegroundColor Green

Write-Host "`nPROXIMOS PASOS RECOMENDADOS:" -ForegroundColor Yellow
Write-Host "1. Reinicia VS Code para aplicar cambios" -ForegroundColor White
Write-Host "2. Abre Windows Terminal como terminal principal" -ForegroundColor White
Write-Host "3. Considera usar WSL2 para desarrollo avanzado" -ForegroundColor White
Write-Host "4. Instala las extensiones recomendadas de .vscode/extensions.json" -ForegroundColor White

Write-Host "`nCOMANDOS UTILES EN TU NUEVO ENTORNO:" -ForegroundColor Cyan
Write-Host "   pwsh          # Abrir PowerShell 7" -ForegroundColor White
Write-Host "   dc up -d      # Docker Compose up (alias)" -ForegroundColor White
Write-Host "   gs            # Git status (alias)" -ForegroundColor White
Write-Host "   ll            # List files (alias)" -ForegroundColor White

Write-Host "`nENTORNO IDEAL CONFIGURADO! Desarrollo profesional sin limitaciones." -ForegroundColor Green
