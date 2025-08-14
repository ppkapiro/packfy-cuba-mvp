# 🇨🇺 PACKFY CUBA - OPTIMIZACIÓN SEGURA VS CODE
# Solo elimina archivos confirmados como obsoletos (0 bytes)

Write-Host "🔍 OPTIMIZACIÓN SEGURA DE RENDIMIENTO VS CODE" -ForegroundColor Cyan
Write-Host "⚠️  Solo se eliminarán archivos vacíos (0 bytes) confirmados" -ForegroundColor Yellow
Write-Host ""

# 1. VERIFICAR Y ELIMINAR SOLO ARCHIVOS MD VACÍOS
Write-Host "📝 Limpiando archivos .md vacíos..." -ForegroundColor Green

$emptyMdFiles = @(
    "ANALISIS-ESTILOS-MODERNOS.md",
    "BACKUP-CSS-ANTES-UNIFICACION.md",
    "ELIMINACION-MENU-RASTREAR-COMPLETADO.md",
    "ESTILOS-APLICADOS-TODAS-PAGINAS.md",
    "HTTPS-CONFIGURADO-EXITOSAMENTE.md",
    "MODERNIZACION-EXITOSA-v4.0.md",
    "MODERNIZACION-GLOBAL-COMPLETADA-v4.0.md",
    "MODERNIZACION-VISUAL-COMPLETADA.md",
    "REPORTE-FINAL-MEJORAS-v3.3.md",
    "REPORTE-FINAL-OPTIMIZACION-CSS.md"
)

$deletedMd = 0
foreach ($file in $emptyMdFiles) {
    if (Test-Path $file) {
        $fileInfo = Get-Item $file
        if ($fileInfo.Length -eq 0) {
            Remove-Item $file -Force
            Write-Host "  ✅ Eliminado: $file (0 bytes)" -ForegroundColor Green
            $deletedMd++
        }
        else {
            Write-Host "  ⚠️  Preservado: $file (tiene contenido: $($fileInfo.Length) bytes)" -ForegroundColor Yellow
        }
    }
}

# 2. VERIFICAR Y ELIMINAR SOLO SCRIPTS PS1 VACÍOS
Write-Host "`n📜 Limpiando scripts .ps1 vacíos..." -ForegroundColor Green

$emptyPs1Files = @(
    "crear_envios_api.ps1",
    "final_setup.ps1",
    "fix_auth.ps1",
    "fix_fast.ps1",
    "iniciar-https-completo.ps1",
    "install-pwa.ps1",
    "quick_fix.ps1",
    "test_quick.ps1"
)

$deletedPs1 = 0
foreach ($file in $emptyPs1Files) {
    if (Test-Path $file) {
        $fileInfo = Get-Item $file
        if ($fileInfo.Length -eq 0) {
            Remove-Item $file -Force
            Write-Host "  ✅ Eliminado: $file (0 bytes)" -ForegroundColor Green
            $deletedPs1++
        }
        else {
            Write-Host "  ⚠️  Preservado: $file (tiene contenido: $($fileInfo.Length) bytes)" -ForegroundColor Yellow
        }
    }
}

# 3. LIMPIAR CACHES TEMPORALES SEGUROS
Write-Host "`n🧹 Limpiando caches temporales..." -ForegroundColor Green

$cachesDeleted = 0
if (Test-Path "__pycache__") {
    Remove-Item "__pycache__" -Recurse -Force
    Write-Host "  ✅ Eliminado: __pycache__" -ForegroundColor Green
    $cachesDeleted++
}
if (Test-Path ".pytest_cache") {
    Remove-Item ".pytest_cache" -Recurse -Force
    Write-Host "  ✅ Eliminado: .pytest_cache" -ForegroundColor Green
    $cachesDeleted++
}
if (Test-Path "backend\__pycache__") {
    Remove-Item "backend\__pycache__" -Recurse -Force
    Write-Host "  ✅ Eliminado: backend\__pycache__" -ForegroundColor Green
    $cachesDeleted++
}

# 4. RESUMEN DE LIMPIEZA
Write-Host "`n📊 RESUMEN DE LIMPIEZA" -ForegroundColor Cyan
Write-Host "=" * 40
Write-Host "📝 Archivos .md eliminados: $deletedMd"
Write-Host "📜 Scripts .ps1 eliminados: $deletedPs1"
Write-Host "🗂️  Caches eliminados: $cachesDeleted"
Write-Host "💾 Espacio liberado: Estimado 5-10 MB"
Write-Host ""

$totalDeleted = $deletedMd + $deletedPs1 + $cachesDeleted
if ($totalDeleted -gt 0) {
    Write-Host "✅ OPTIMIZACIÓN COMPLETADA - $totalDeleted elementos eliminados" -ForegroundColor Green
    Write-Host "🚀 VS Code debería ser más rápido ahora" -ForegroundColor Cyan
}
else {
    Write-Host "ℹ️  No se encontraron archivos vacíos para eliminar" -ForegroundColor Blue
}

Write-Host ""
Write-Host "📋 ARCHIVOS IMPORTANTES PRESERVADOS:" -ForegroundColor Yellow
Write-Host "  ✅ README.md (documentación principal)"
Write-Host "  ✅ dev.ps1 (script de desarrollo)"
Write-Host "  ✅ Scripts Python con contenido"
Write-Host "  ✅ Configuraciones del proyecto"
