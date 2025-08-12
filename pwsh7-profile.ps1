# PROFILE POWERSHELL 7 - ENTORNO IDEAL PACKFY
# Configuracion automatica para desarrollo

# Importar modulos esenciales si existen
try {
    Import-Module PSReadLine -Force

    # Configurar PSReadLine (autocompletado avanzado)
    Set-PSReadLineOption -PredictionSource History
    Set-PSReadLineOption -PredictionViewStyle ListView
    Set-PSReadLineOption -EditMode Emacs
    Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
}
catch {
    Write-Host "PSReadLine no disponible" -ForegroundColor Yellow
}

# Configurar codificacion UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# Variables de entorno
$env:PYTHONIOENCODING = "utf-8"
$env:LC_ALL = "en_US.UTF-8"

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
    $location = Get-Location

    # Detectar Git branch
    $gitBranch = ""
    try {
        $branch = git branch --show-current 2>$null
        if ($branch) {
            $gitBranch = " ($branch)"
        }
    }
    catch { }

    # Detectar Python virtual environment
    $venvIndicator = ""
    if ($env:VIRTUAL_ENV) {
        $venvName = Split-Path $env:VIRTUAL_ENV -Leaf
        $venvIndicator = " ($venvName)"
    }

    # Detectar Node.js project
    $nodeIndicator = ""
    if (Test-Path "package.json") {
        $nodeIndicator = " [NPM]"
    }

    # Detectar Docker
    $dockerIndicator = ""
    if (Test-Path "docker-compose.yml" -or Test-Path "compose.yml") {
        $dockerIndicator = " [DOCKER]"
    }

    Write-Host "PS7 " -NoNewline -ForegroundColor Cyan
    Write-Host $location -NoNewline -ForegroundColor Green
    Write-Host $gitBranch -NoNewline -ForegroundColor Yellow
    Write-Host $venvIndicator -NoNewline -ForegroundColor Blue
    Write-Host $nodeIndicator -NoNewline -ForegroundColor Magenta
    Write-Host $dockerIndicator -NoNewline -ForegroundColor Cyan
    Write-Host ""
    return "> "
}

# Cargar configuracion especifica de Packfy si existe
if (Test-Path "scripts\powershell-config.ps1") {
    try {
        . "scripts\powershell-config.ps1"
        Write-Host "Configuracion Packfy cargada" -ForegroundColor Green
    }
    catch {
        Write-Host "Error cargando configuracion Packfy" -ForegroundColor Yellow
    }
}

Write-Host "PowerShell 7 - Entorno Ideal Configurado!" -ForegroundColor Green
Write-Host "Comandos utiles: dc, gs, ll, .., dcu, dcd" -ForegroundColor Cyan
