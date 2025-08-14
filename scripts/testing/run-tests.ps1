# 🇨🇺 PACKFY CUBA - Ejecutor de Tests v4.0

param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("all", "backend", "frontend", "e2e", "unit", "integration", "security", "performance")]
    [string]$TestType = "all",

    [Parameter(Mandatory = $false)]
    [switch]$Coverage,

    [Parameter(Mandatory = $false)]
    [switch]$Watch,

    [Parameter(Mandatory = $false)]
    [switch]$Verbose,

    [Parameter(Mandatory = $false)]
    [string]$Filter = "",

    [Parameter(Mandatory = $false)]
    [switch]$FailFast,

    [Parameter(Mandatory = $false)]
    [switch]$Parallel
)

# Configuración de colores y estilos
$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "PACKFY CUBA - Test Runner v4.0"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    switch ($Color) {
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Blue" { Write-Host $Message -ForegroundColor Blue }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        "Magenta" { Write-Host $Message -ForegroundColor Magenta }
        default { Write-Host $Message }
    }
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-ColorOutput "============================================" "Cyan"
    Write-ColorOutput "  $Title" "Cyan"
    Write-ColorOutput "============================================" "Cyan"
    Write-Host ""
}

function Test-Prerequisites {
    Write-Header "🔍 VERIFICANDO PRERREQUISITOS"

    $missingTools = @()

    # Verificar Python y pip
    try {
        $pythonVersion = python --version 2>&1
        Write-ColorOutput "✅ Python: $pythonVersion" "Green"
    }
    catch {
        $missingTools += "Python"
        Write-ColorOutput "❌ Python no encontrado" "Red"
    }

    # Verificar Node.js y npm
    try {
        $nodeVersion = node --version 2>&1
        $npmVersion = npm --version 2>&1
        Write-ColorOutput "✅ Node.js: $nodeVersion" "Green"
        Write-ColorOutput "✅ npm: v$npmVersion" "Green"
    }
    catch {
        $missingTools += "Node.js/npm"
        Write-ColorOutput "❌ Node.js/npm no encontrado" "Red"
    }

    # Verificar Docker
    try {
        $dockerVersion = docker --version 2>&1
        Write-ColorOutput "✅ Docker: $dockerVersion" "Green"
    }
    catch {
        Write-ColorOutput "⚠️  Docker no encontrado (opcional para algunos tests)" "Yellow"
    }

    if ($missingTools.Count -gt 0) {
        Write-ColorOutput "❌ Faltan herramientas: $($missingTools -join ', ')" "Red"
        Write-ColorOutput "Instale las herramientas faltantes antes de continuar." "Red"
        exit 1
    }

    Write-ColorOutput "✅ Todos los prerrequisitos están disponibles" "Green"
}

function Install-Dependencies {
    Write-Header "📦 INSTALANDO DEPENDENCIAS"

    # Backend dependencies
    if (Test-Path "backend/requirements.txt") {
        Write-ColorOutput "📥 Instalando dependencias de Python..." "Blue"
        Set-Location "backend"
        pip install -r requirements.txt
        pip install pytest pytest-django pytest-cov pytest-xdist bandit safety
        Set-Location ".."
        Write-ColorOutput "✅ Dependencias de Python instaladas" "Green"
    }

    # Frontend dependencies
    if (Test-Path "frontend/package.json") {
        Write-ColorOutput "📥 Instalando dependencias de Node.js..." "Blue"
        Set-Location "frontend"
        npm install

        # Instalar Playwright si es necesario
        if ($TestType -eq "all" -or $TestType -eq "e2e") {
            Write-ColorOutput "📥 Instalando navegadores de Playwright..." "Blue"
            npx playwright install
        }

        Set-Location ".."
        Write-ColorOutput "✅ Dependencias de Node.js instaladas" "Green"
    }
}

function Start-Services {
    Write-Header "🚀 INICIANDO SERVICIOS"

    # Verificar si Docker Compose está disponible
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        Write-ColorOutput "🐳 Iniciando servicios con Docker Compose..." "Blue"
        docker-compose -f compose.yml up -d postgres redis

        # Esperar a que los servicios estén listos
        Write-ColorOutput "⏳ Esperando a que los servicios estén listos..." "Yellow"
        Start-Sleep -Seconds 10

        Write-ColorOutput "✅ Servicios iniciados" "Green"
    }
    else {
        Write-ColorOutput "⚠️  Docker Compose no disponible, usando configuración local" "Yellow"
    }
}

function Run-BackendTests {
    Write-Header "🐍 EJECUTANDO TESTS DE BACKEND"

    Set-Location "backend"

    # Configurar variables de entorno para testing
    $env:DJANGO_SETTINGS_MODULE = "config.settings_testing"
    $env:SECRET_KEY = "test-secret-key-for-testing"
    $env:DEBUG = "False"

    # Preparar base de datos de testing
    Write-ColorOutput "🗄️  Preparando base de datos de testing..." "Blue"
    python manage.py migrate --settings=config.settings_testing

    # Construir comando pytest
    $pytestArgs = @()

    if ($Coverage) {
        $pytestArgs += "--cov=."
        $pytestArgs += "--cov-report=html"
        $pytestArgs += "--cov-report=xml"
        $pytestArgs += "--cov-config=.coveragerc"
    }

    if ($Parallel) {
        $pytestArgs += "-n"
        $pytestArgs += "auto"
    }

    if ($Verbose) {
        $pytestArgs += "-v"
    }

    if ($FailFast) {
        $pytestArgs += "-x"
    }

    if ($Filter) {
        $pytestArgs += "-k"
        $pytestArgs += $Filter
    }

    # Ejecutar tests específicos según tipo
    switch ($TestType) {
        "unit" { $pytestArgs += "-m"; $pytestArgs += "unit" }
        "integration" { $pytestArgs += "-m"; $pytestArgs += "integration" }
        "security" { $pytestArgs += "-m"; $pytestArgs += "security" }
    }

    Write-ColorOutput "🧪 Ejecutando tests de backend..." "Blue"
    $backendResult = & pytest @pytestArgs
    $backendExitCode = $LASTEXITCODE

    if ($backendExitCode -eq 0) {
        Write-ColorOutput "✅ Tests de backend completados exitosamente" "Green"
    }
    else {
        Write-ColorOutput "❌ Tests de backend fallaron" "Red"
    }

    # Ejecutar análisis de seguridad
    if ($TestType -eq "all" -or $TestType -eq "security") {
        Write-ColorOutput "🔒 Ejecutando análisis de seguridad..." "Blue"
        bandit -r . -f json -o bandit-report.json
        safety check --json --output safety-report.json
        Write-ColorOutput "✅ Análisis de seguridad completado" "Green"
    }

    Set-Location ".."
    return $backendExitCode
}

function Run-FrontendTests {
    Write-Header "⚛️  EJECUTANDO TESTS DE FRONTEND"

    Set-Location "frontend"

    # Ejecutar linting
    Write-ColorOutput "🔍 Ejecutando linting..." "Blue"
    npm run lint

    # Ejecutar type checking
    Write-ColorOutput "🏷️  Verificando tipos..." "Blue"
    npm run type-check

    # Construir comando de test
    $testScript = if ($Coverage) { "test:coverage" } else { "test" }

    if ($Watch) {
        $testScript = "test:watch"
    }

    Write-ColorOutput "🧪 Ejecutando tests de frontend..." "Blue"

    if ($Filter) {
        $env:VITEST_FILTER = $Filter
    }

    npm run $testScript
    $frontendExitCode = $LASTEXITCODE

    if ($frontendExitCode -eq 0) {
        Write-ColorOutput "✅ Tests de frontend completados exitosamente" "Green"
    }
    else {
        Write-ColorOutput "❌ Tests de frontend fallaron" "Red"
    }

    Set-Location ".."
    return $frontendExitCode
}

function Run-E2ETests {
    Write-Header "🎭 EJECUTANDO TESTS E2E"

    # Iniciar servicios
    Write-ColorOutput "🚀 Iniciando servicios para E2E..." "Blue"

    # Iniciar backend
    Set-Location "backend"
    $env:DJANGO_SETTINGS_MODULE = "config.settings_testing"
    Start-Process python -ArgumentList "manage.py", "runserver", "8000" -PassThru
    $backendProcess = $Global:LASTEXITCODE
    Set-Location ".."

    # Iniciar frontend
    Set-Location "frontend"
    Start-Process npm -ArgumentList "run", "preview", "--", "--port", "5173" -PassThru
    $frontendProcess = $Global:LASTEXITCODE

    # Esperar a que los servicios estén listos
    Write-ColorOutput "⏳ Esperando a que los servicios estén listos..." "Yellow"
    Start-Sleep -Seconds 15

    # Ejecutar tests E2E
    Write-ColorOutput "🎭 Ejecutando tests E2E..." "Blue"

    $playwrightArgs = @()
    if ($Verbose) {
        $playwrightArgs += "--reporter=line"
    }

    if ($Filter) {
        $playwrightArgs += "--grep"
        $playwrightArgs += $Filter
    }

    npx playwright test @playwrightArgs
    $e2eExitCode = $LASTEXITCODE

    # Detener servicios
    Write-ColorOutput "🛑 Deteniendo servicios..." "Blue"
    if ($backendProcess) { Stop-Process -Id $backendProcess -ErrorAction SilentlyContinue }
    if ($frontendProcess) { Stop-Process -Id $frontendProcess -ErrorAction SilentlyContinue }

    Set-Location ".."

    if ($e2eExitCode -eq 0) {
        Write-ColorOutput "✅ Tests E2E completados exitosamente" "Green"
    }
    else {
        Write-ColorOutput "❌ Tests E2E fallaron" "Red"
    }

    return $e2eExitCode
}

function Run-PerformanceTests {
    Write-Header "⚡ EJECUTANDO TESTS DE PERFORMANCE"

    Set-Location "frontend"

    # Lighthouse CI
    if (Get-Command lhci -ErrorAction SilentlyContinue) {
        Write-ColorOutput "💡 Ejecutando Lighthouse..." "Blue"
        lhci autorun
    }
    else {
        Write-ColorOutput "⚠️  Lighthouse CI no encontrado, instalando..." "Yellow"
        npm install -g @lhci/cli
        lhci autorun
    }

    # Artillery load tests
    if (Test-Path "performance/load-test.yml") {
        Write-ColorOutput "🏹 Ejecutando tests de carga..." "Blue"
        if (Get-Command artillery -ErrorAction SilentlyContinue) {
            artillery run performance/load-test.yml
        }
        else {
            npm install -g artillery
            artillery run performance/load-test.yml
        }
    }

    Set-Location ".."
    Write-ColorOutput "✅ Tests de performance completados" "Green"
    return 0
}

function Show-TestSummary {
    param([hashtable]$Results)

    Write-Header "📊 RESUMEN DE RESULTADOS"

    $totalTests = 0
    $passedTests = 0

    foreach ($test in $Results.Keys) {
        $result = $Results[$test]
        $status = if ($result -eq 0) { "✅ PASÓ" } else { "❌ FALLÓ" }
        $color = if ($result -eq 0) { "Green" } else { "Red" }

        Write-ColorOutput "$test`: $status" $color

        $totalTests++
        if ($result -eq 0) { $passedTests++ }
    }

    Write-Host ""
    $successRate = [math]::Round(($passedTests / $totalTests) * 100, 2)
    Write-ColorOutput "Tasa de éxito: $successRate% ($passedTests/$totalTests)" $(if ($successRate -eq 100) { "Green" } else { "Yellow" })

    if ($Coverage) {
        Write-Host ""
        Write-ColorOutput "📈 Reportes de cobertura generados:" "Blue"
        if (Test-Path "backend/htmlcov/index.html") {
            Write-ColorOutput "  - Backend: backend/htmlcov/index.html" "Cyan"
        }
        if (Test-Path "frontend/coverage/index.html") {
            Write-ColorOutput "  - Frontend: frontend/coverage/index.html" "Cyan"
        }
    }
}

# FUNCIÓN PRINCIPAL
function Main {
    Write-Header "🇨🇺 PACKFY CUBA - TEST RUNNER v4.0"

    Write-ColorOutput "Configuración de ejecución:" "Blue"
    Write-ColorOutput "  - Tipo de test: $TestType" "Cyan"
    Write-ColorOutput "  - Cobertura: $(if ($Coverage) { 'Sí' } else { 'No' })" "Cyan"
    Write-ColorOutput "  - Modo watch: $(if ($Watch) { 'Sí' } else { 'No' })" "Cyan"
    Write-ColorOutput "  - Paralelo: $(if ($Parallel) { 'Sí' } else { 'No' })" "Cyan"
    if ($Filter) { Write-ColorOutput "  - Filtro: $Filter" "Cyan" }

    # Verificar prerrequisitos
    Test-Prerequisites

    # Instalar dependencias
    Install-Dependencies

    # Iniciar servicios si es necesario
    if ($TestType -eq "all" -or $TestType -eq "integration" -or $TestType -eq "e2e") {
        Start-Services
    }

    # Ejecutar tests según el tipo
    $results = @{}

    switch ($TestType) {
        "all" {
            $results["Backend"] = Run-BackendTests
            $results["Frontend"] = Run-FrontendTests
            $results["E2E"] = Run-E2ETests
            $results["Performance"] = Run-PerformanceTests
        }
        "backend" {
            $results["Backend"] = Run-BackendTests
        }
        "frontend" {
            $results["Frontend"] = Run-FrontendTests
        }
        "e2e" {
            $results["E2E"] = Run-E2ETests
        }
        "unit" {
            $results["Backend Unit"] = Run-BackendTests
            $results["Frontend Unit"] = Run-FrontendTests
        }
        "integration" {
            $results["Backend Integration"] = Run-BackendTests
        }
        "security" {
            $results["Security"] = Run-BackendTests
        }
        "performance" {
            $results["Performance"] = Run-PerformanceTests
        }
    }

    # Mostrar resumen
    Show-TestSummary $results

    # Determinar código de salida
    $overallResult = ($results.Values | Measure-Object -Maximum).Maximum

    if ($overallResult -eq 0) {
        Write-ColorOutput "`n🎉 ¡Todos los tests completados exitosamente!" "Green"
    }
    else {
        Write-ColorOutput "`n💥 Algunos tests fallaron. Revise los resultados arriba." "Red"
    }

    exit $overallResult
}

# Ejecutar función principal
Main
