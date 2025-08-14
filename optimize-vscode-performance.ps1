# 🇨🇺 PACKFY CUBA - Limpieza de Rendimiento VS Code
# Script para optimizar el proyecto y mejorar velocidad

Write-Host "🚀 INICIANDO OPTIMIZACIÓN DE RENDIMIENTO..." -ForegroundColor Cyan

# 1. Limpiar archivos de documentación obsoletos
Write-Host "📝 Moviendo documentación obsoleta..." -ForegroundColor Yellow
$docsToMove = @(
    "ANALISIS-ESTILOS-MODERNOS.md",
    "BACKUP-CSS-ANTES-UNIFICACION.md",
    "CLEANUP-SUMMARY-v4.0.md",
    "ELIMINACION-MENU-RASTREAR-COMPLETADO.md",
    "ESTILOS-APLICADOS-TODAS-PAGINAS.md",
    "ETAPA-6-IA-COMPLETADA.md",
    "ETAPA-7-ESCALABILIDAD-GLOBAL-COMPLETADA.md",
    "HTTPS-CONFIGURADO-EXITOSAMENTE.md",
    "MODERNIZACION-EXITOSA-v4.0.md",
    "MODERNIZACION-GLOBAL-COMPLETADA-v4.0.md",
    "MODERNIZACION-VISUAL-COMPLETADA.md",
    "REPORTE-FINAL-MEJORAS-v3.3.md",
    "REPORTE-FINAL-OPTIMIZACION-CSS.md",
    "REPOSITORY-SYNC-COMPLETE-v4.0.md"
)

# Crear directorio archive/legacy_docs si no existe
if (!(Test-Path "archive\legacy_docs")) {
    New-Item -ItemType Directory -Path "archive\legacy_docs" -Force
}

foreach ($doc in $docsToMove) {
    if (Test-Path $doc) {
        Move-Item $doc "archive\legacy_docs\" -Force
        Write-Host "  ✅ Movido: $doc" -ForegroundColor Green
    }
}

# 2. Limpiar caches
Write-Host "🧹 Limpiando caches..." -ForegroundColor Yellow
if (Test-Path "__pycache__") { Remove-Item "__pycache__" -Recurse -Force }
if (Test-Path ".pytest_cache") { Remove-Item ".pytest_cache" -Recurse -Force }
if (Test-Path "backend\__pycache__") { Remove-Item "backend\__pycache__" -Recurse -Force }
if (Test-Path "frontend\node_modules\.cache") { Remove-Item "frontend\node_modules\.cache" -Recurse -Force }
if (Test-Path "frontend\dist") { Remove-Item "frontend\dist" -Recurse -Force }

# 3. Consolidar scripts
Write-Host "📜 Consolidando scripts obsoletos..." -ForegroundColor Yellow
$scriptsToMove = @(
    "crear_datos_cuba.py",
    "crear_envios_api.ps1",
    "create_admin.py",
    "diagnostico_auth.py",
    "fix_auth.ps1",
    "fix_auth.py",
    "fix_fast.ps1",
    "install-pwa.ps1",
    "quick_fix.ps1",
    "rebuild_clean.ps1",
    "script_correcto_envios.py",
    "script_familias_cubanas.py",
    "test_quick.ps1"
)

# Crear directorio archive/scripts_legacy si no existe
if (!(Test-Path "archive\scripts_legacy")) {
    New-Item -ItemType Directory -Path "archive\scripts_legacy" -Force
}

foreach ($script in $scriptsToMove) {
    if (Test-Path $script) {
        Move-Item $script "archive\scripts_legacy\" -Force
        Write-Host "  ✅ Movido: $script" -ForegroundColor Green
    }
}

Write-Host "✨ LIMPIEZA COMPLETADA" -ForegroundColor Green
Write-Host "📊 Archivos reorganizados para mejor rendimiento" -ForegroundColor Cyan
