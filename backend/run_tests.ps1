Param(
    [switch]$Reinstall,
    [switch]$Lint,
    [switch]$Coverage,
    [switch]$NoInstall
)
$ErrorActionPreference = 'Stop'
Write-Host '🚀 Iniciando suite de pruebas Packfy (backend)'

# Iniciar transcript para capturar toda la salida en un archivo de log
try {
    if (-not (Test-Path 'logs')) { New-Item -ItemType Directory -Path 'logs' | Out-Null }
    $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $global:TestLogPath = Join-Path 'logs' ("test-$timestamp.log")
    Start-Transcript -Path $global:TestLogPath -Force | Out-Null
    Write-Host "📝 Log: $global:TestLogPath" -ForegroundColor Cyan
}
catch { Write-Warning "No se pudo iniciar transcript: $_" }

# Detectar python (python o python3)
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { Write-Error 'Python no encontrado en PATH'; exit 1 }


# Preferir reusar .venv de la raíz si existe para evitar reinstalaciones
$usingRootVenv = $false
$venvPath = '.venv'
$rootVenvPath = Join-Path (Resolve-Path '..') '.venv'
if ($Reinstall -and (Test-Path $venvPath)) { Remove-Item -Recurse -Force $venvPath }
if (-not (Test-Path $venvPath)) {
    if (Test-Path $rootVenvPath) {
        Write-Host "🔄 Reutilizando entorno virtual raíz: $rootVenvPath"
        $usingRootVenv = $true
    }
    else {
        Write-Host '📦 Creando entorno virtual (.venv)...'
        & $python.Path -m venv $venvPath
    }
}
# Ruta de Python dentro del venv (Windows vs Unix)
if ($IsWindows) {
    $venvPython = if ($usingRootVenv) { Join-Path $rootVenvPath 'Scripts/python.exe' } else { Join-Path $venvPath 'Scripts/python.exe' }
}
else {
    $venvPython = if ($usingRootVenv) { Join-Path $rootVenvPath 'bin/python' } else { Join-Path $venvPath 'bin/python' }
}

# Detectar si ya existen paquetes clave en el entorno
& $venvPython -c "import importlib.util,sys; sys.exit(0 if all(importlib.util.find_spec(m) for m in ('django','pytest')) else 1)"
$hasCorePkgs = ($LASTEXITCODE -eq 0)

if ($NoInstall -and -not $hasCorePkgs) {
    Write-Error 'NoInstall solicitado pero el entorno no tiene Django y/o Pytest. Por favor instala dependencias o ejecuta sin -NoInstall.'
    exit 3
}

if ($NoInstall -or $hasCorePkgs) {
    Write-Host '🧰 Dependencias ya disponibles; saltando instalación' -ForegroundColor Cyan
}
elseif (-not $usingRootVenv) {
    Write-Host '⬆️ Actualizando pip...'
    & $venvPython -m pip install --upgrade pip | Out-Null

    Write-Host '📥 Instalando dependencias (requirements.txt)...'
    & $venvPython -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { Write-Error 'Fallo instalación dependencias'; exit 2 }
}
else {
    Write-Host '🧰 Usando .venv de la raíz; saltando instalación de dependencias' -ForegroundColor Cyan
}

Write-Host '🔍 Verificando paquetes clave...'
& $venvPython -c "import pkgutil,sys;print('pytest?',bool(pkgutil.find_loader('pytest')),'django?',bool(pkgutil.find_loader('django')),'ruff?',bool(pkgutil.find_loader('ruff')));" || Write-Warning 'No se pudieron verificar paquetes'

Write-Host 'ℹ️ Versiones:'
& $venvPython -c "import sys, django, pkgutil;print('Python', sys.version);print('Django', django.get_version())"

$env:DJANGO_SETTINGS_MODULE = 'config.settings_test'
Write-Host '🧪 Ejecutando tests básicos (smoke + métricas + estadísticas + cache + paginación + logging)...'
Write-Host '🔧 Pytest versión:'
& $venvPython -m pytest --version || Write-Warning 'Pytest no disponible'
function Invoke-Pytest {
    param([string[]]$pytestArgs)
    if (-not $script:timestamp) { $script:timestamp = Get-Date -Format 'yyyyMMdd-HHmmss' }
    $pytestOut = Join-Path 'logs' ("pytest-$($script:timestamp)-out.txt")
    $pytestErr = Join-Path 'logs' ("pytest-$($script:timestamp)-err.txt")
    Write-Host "🧪 Ejecutando: pytest $($pytestArgs -join ' ')" -ForegroundColor Yellow
    $argList = @('-m', 'pytest') + $pytestArgs
    $proc = Start-Process -FilePath $venvPython -ArgumentList $argList -NoNewWindow -Wait -PassThru -RedirectStandardOutput $pytestOut -RedirectStandardError $pytestErr
    # Combinar stdout y stderr en un único archivo 'pytest_latest.txt'
    try {
        $combined = Join-Path 'logs' 'pytest_latest.txt'
        if (Test-Path $combined) { Remove-Item $combined -Force }
        Add-Content -Path $combined -Value "##### STDOUT #####"
        if (Test-Path $pytestOut) { Get-Content $pytestOut | Add-Content -Path $combined }
        Add-Content -Path $combined -Value "`n##### STDERR #####"
        if (Test-Path $pytestErr) { Get-Content $pytestErr | Add-Content -Path $combined }
    }
    catch {}
    return $proc.ExitCode
}

# Lint opcional (Ruff)
if ($Lint) {
    Write-Host '🧹 Lint (ruff) en backend...' -ForegroundColor Cyan
    # Instalar ruff si no está
    & $venvPython -m pip show ruff | Out-Null
    if ($LASTEXITCODE -ne 0) { & $venvPython -m pip install ruff | Out-Null }
    $ruffOut = Join-Path 'logs' ("ruff-$timestamp.txt")
    $ruffArgs = @('run', '--quiet', '--exit-non-zero-on-fix', '--fix', '--unsafe-fixes', '--preview', '.')
    # Ejecutar ruff como módulo si está disponible
    $proc = Start-Process -FilePath $venvPython -ArgumentList @('-m', 'ruff') + $ruffArgs -NoNewWindow -Wait -PassThru -RedirectStandardOutput $ruffOut -RedirectStandardError $ruffOut
    if ($proc.ExitCode -eq 0) { Write-Host '✅ Lint OK' } else { Write-Warning "⚠️ Lint reportó issues (ver $ruffOut)" }
}

$pytestArgsBase = @('-vv')
if ($Coverage) {
    $covXml = Join-Path 'logs' 'coverage.xml'
    $covHtmlDir = Join-Path 'logs' 'htmlcov'
    $pytestArgsBase = @(
        '-vv',
        '--cov=.',
        '--cov-report=term-missing',
        "--cov-report=xml:$covXml",
        "--cov-report=html:$covHtmlDir"
    )
}

$selCode = Invoke-Pytest -pytestArgs ($pytestArgsBase + @('tests/test_smoke.py', 'tests/test_metrics_rate_limit.py', 'tests/test_envios_estadisticas.py', 'tests/test_cache_rastrear.py', 'tests/test_pagination_limits.py', 'tests/test_logging_request_id.py', 'tests/test_permissions_and_notifications.py'))
if ($selCode -ne 0) { $failed = $true }
if ($failed) {
    Write-Warning '❗ Reintentando suite completa en carpeta tests'
    $selCode = Invoke-Pytest -pytestArgs ($pytestArgsBase + @('tests'))
}
$code = $selCode
if ($code -eq 0) { Write-Host '✅ Tests básicos OK'; } else { Write-Error "❌ Fallos en tests básicos (exit $code)" }

# Etapa adicional: ejecutar tests de envíos para validar CRUD y permisos
Write-Host '📦 Ejecutando tests de Envíos (API)...'
$enviosCode = Invoke-Pytest -pytestArgs ($pytestArgsBase + @('tests/test_envios_api.py'))
if ($enviosCode -eq 0) {
    Write-Host '✅ Tests de Envíos OK'
}
else {
    Write-Error "❌ Fallos en tests de Envíos (exit $enviosCode)"
}
$code = [Math]::Max($code, $enviosCode)

if ($code -eq 0) { Write-Host '✅ Suite completa OK'; } else { Write-Error "❌ Fallos en la suite (exit $code)" }
try {
    if ($global:TestLogPath) { Copy-Item $global:TestLogPath 'logs/test_latest.log' -Force }
    Stop-Transcript | Out-Null
}
catch { Write-Warning "No se pudo finalizar transcript: $_" }
exit $code
