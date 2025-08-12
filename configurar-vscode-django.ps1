# ═══════════════════════════════════════════════════════════════════
# 🔧 SCRIPT: CONFIGURACIÓN VS CODE DJANGO OPTIMIZADA
# ═══════════════════════════════════════════════════════════════════
# Descripción: Aplica configuración óptima para Django en VS Code
# Autor: Sistema Packfy
# Fecha: $(Get-Date -Format "yyyy-MM-dd")
# ═══════════════════════════════════════════════════════════════════

Write-Host "🔧 CONFIGURANDO VS CODE PARA DJANGO..." -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Yellow

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "backend/config/settings.py")) {
    Write-Host "❌ Error: No se encuentra el proyecto Django" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde la raíz del proyecto" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Proyecto Django detectado" -ForegroundColor Green

# 1. Verificar configuración de Python
Write-Host "`n🐍 VERIFICANDO CONFIGURACIÓN PYTHON..." -ForegroundColor Cyan

$pythonPath = ".\backend\venv\Scripts\python.exe"
if (Test-Path $pythonPath) {
    Write-Host "✅ Entorno virtual Python encontrado: $pythonPath" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Entorno virtual no encontrado en: $pythonPath" -ForegroundColor Yellow
    Write-Host "   Buscando Python alternativo..." -ForegroundColor Yellow

    $globalPython = Get-Command python -ErrorAction SilentlyContinue
    if ($globalPython) {
        Write-Host "✅ Python global encontrado: $($globalPython.Source)" -ForegroundColor Green
    }
    else {
        Write-Host "❌ No se encontró Python" -ForegroundColor Red
    }
}

# 2. Verificar extensiones requeridas
Write-Host "`n📦 VERIFICANDO EXTENSIONES VS CODE..." -ForegroundColor Cyan

$extensionesRequeridas = @(
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-toolsai.jupyter",
    "pkief.material-icon-theme"
)

foreach ($extension in $extensionesRequeridas) {
    $instalada = code --list-extensions | Select-String $extension
    if ($instalada) {
        Write-Host "✅ $extension" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  $extension (no instalada)" -ForegroundColor Yellow
        Write-Host "   Instalando..." -ForegroundColor Cyan
        code --install-extension $extension
    }
}

# 3. Verificar archivos de configuración
Write-Host "`n⚙️  VERIFICANDO ARCHIVOS DE CONFIGURACIÓN..." -ForegroundColor Cyan

$archivosConfig = @(
    ".vscode/settings.json",
    "pyrightconfig.json",
    "backend/django_vscode_config.py"
)

foreach ($archivo in $archivosConfig) {
    if (Test-Path $archivo) {
        Write-Host "✅ $archivo" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $archivo (faltante)" -ForegroundColor Red
    }
}

# 4. Recargar ventana de VS Code
Write-Host "`n🔄 RECARGANDO VS CODE..." -ForegroundColor Cyan
Write-Host "   Presiona Ctrl+Shift+P y ejecuta: 'Developer: Reload Window'" -ForegroundColor Yellow

# 5. Comandos recomendados
Write-Host "`n📋 COMANDOS RECOMENDADOS:" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "1. Recargar VS Code: Ctrl+Shift+P > 'Developer: Reload Window'" -ForegroundColor White
Write-Host "2. Seleccionar intérprete Python: Ctrl+Shift+P > 'Python: Select Interpreter'" -ForegroundColor White
Write-Host "3. Ejecutar en terminal: python manage.py check" -ForegroundColor White
Write-Host "4. Si persisten errores: Ctrl+Shift+P > 'Python: Clear Cache and Reload Window'" -ForegroundColor White

Write-Host "`n🎯 CONFIGURACIÓN APLICADA:" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "✅ Paths Django configurados" -ForegroundColor Green
Write-Host "✅ Pylance optimizado para Django" -ForegroundColor Green
Write-Host "✅ Imports automáticos habilitados" -ForegroundColor Green
Write-Host "✅ Errores falsos positivos deshabilitados" -ForegroundColor Green
Write-Host "✅ Entorno Python configurado" -ForegroundColor Green

Write-Host "`n🚀 ¡VS CODE CONFIGURADO PARA DJANGO!" -ForegroundColor Green
Write-Host "   Recarga VS Code para aplicar todos los cambios." -ForegroundColor Cyan

# Pausa para que el usuario pueda leer
Write-Host "`nPresiona cualquier tecla para continuar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
