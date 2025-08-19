# 🇨🇺 PACKFY CUBA - Script de Restauración y Verificación
# Restaura el estado estable del proyecto

Write-Host "🔄 INICIANDO PROCESO DE RESTAURACIÓN Y VERIFICACIÓN..." -ForegroundColor Cyan
Write-Host ""

# 1. Verificar estado actual
Write-Host "📊 ESTADO ACTUAL DEL PROYECTO" -ForegroundColor Green
Write-Host "=" * 50

$dockerContainers = docker ps --format "table {{.Names}}\t{{.Status}}" 2>$null
if ($dockerContainers) {
    Write-Host "🐳 Contenedores Docker:"
    $dockerContainers
}
else {
    Write-Host "❌ Docker no está ejecutándose o no hay contenedores"
}

Write-Host ""

# 2. Verificar servicios web
Write-Host "🌐 VERIFICANDO SERVICIOS WEB" -ForegroundColor Green
Write-Host "=" * 50

try {
    $frontendTest = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Frontend (5173): FUNCIONANDO - Status $($frontendTest.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend (5173): NO RESPONDE" -ForegroundColor Red
}

try {
    $backendTest = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Backend (8000): FUNCIONANDO - Status $($backendTest.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend (8000): NO RESPONDE" -ForegroundColor Red
}

Write-Host ""

# 3. Verificar archivos críticos
Write-Host "📁 VERIFICANDO ARCHIVOS CRÍTICOS" -ForegroundColor Green
Write-Host "=" * 50

$criticalFiles = @(
    "compose.yml",
    "backend\Dockerfile",
    "frontend\Dockerfile",
    "backend\requirements.txt",
    "frontend\package.json",
    ".vscode\settings.json"
)

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "✅ $file ($size bytes)" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $file - FALTA" -ForegroundColor Red
    }
}

Write-Host ""

# 4. Mostrar opciones de restauración
Write-Host "🛠️  OPCIONES DE RESTAURACIÓN" -ForegroundColor Yellow
Write-Host "=" * 50
Write-Host "Si algo no funciona, puedes ejecutar:"
Write-Host ""
Write-Host "📌 Para restaurar configuración VS Code:"
Write-Host "   Copy-Item .vscode\settings.json.backup .vscode\settings.json -Force"
Write-Host ""
Write-Host "📌 Para restaurar archivos eliminados:"
Write-Host "   git restore <archivo>"
Write-Host ""
Write-Host "📌 Para reiniciar Docker:"
Write-Host "   docker-compose -f compose.yml down"
Write-Host "   docker-compose -f compose.yml up -d"
Write-Host ""
Write-Host "📌 Para limpiar y reconstruir:"
Write-Host "   .\rebuild_clean.ps1"
Write-Host ""

# 5. Detectar problemas comunes
Write-Host "🔍 DIAGNÓSTICO AUTOMÁTICO" -ForegroundColor Yellow
Write-Host "=" * 50

# Verificar archivos vacíos problemáticos
$emptyFiles = Get-ChildItem -Recurse -File | Where-Object { $_.Length -eq 0 -and $_.Name -like "*.py" -or $_.Name -like "*.tsx" -or $_.Name -like "*.ts" }
if ($emptyFiles) {
    Write-Host "⚠️  Archivos vacíos detectados (pueden causar errores):" -ForegroundColor Yellow
    foreach ($file in $emptyFiles) {
        Write-Host "   - $($file.FullName)" -ForegroundColor Yellow
    }
}

# Verificar node_modules
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "⚠️  node_modules falta - ejecutar: cd frontend && npm install" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ VERIFICACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "📋 Revisa los resultados arriba para identificar problemas" -ForegroundColor Cyan
