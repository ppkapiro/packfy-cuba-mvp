# 🧹 SCRIPT DE LIMPIEZA AUTOMATIZADA - PACKFY
# Ejecuta la limpieza gradual del proyecto de forma segura

Write-Host "🧹 INICIANDO LIMPIEZA PROFUNDA DE PACKFY" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "compose.yml")) {
    Write-Host "❌ ERROR: No se encuentra compose.yml" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde el directorio raíz del proyecto" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Directorio de proyecto confirmado" -ForegroundColor Green

# FASE 1: Documentación obsoleta a archivo
Write-Host "`n📚 FASE 1: Moviendo documentación obsoleta..." -ForegroundColor Yellow

$docsObsoletos = @(
    "ANALISIS-PROFUNDO-ESTADO-ACTUAL-COMPLETO.md",
    "ANALISIS-PROFUNDO-LIMPIEZA-v3.0.md",
    "APIS-MULTI-TENANT-COMPLETADAS.md",
    "BUSQUEDA-COMPLETA-IMPLEMENTADA.md",
    "COMMIT-FINAL-v2.0.0.md",
    "COMPILACION-EXITOSA.txt",
    "CONEXION-MOVIL-COMPLETA.md",
    "CONFIGURACION-ROBUSTA-COMPLETA.md",
    "CREDENCIALES-TESTING.md",
    "DIAGNÓSTICO_Y_PLAN_MULTITENANCY.md",
    "DISEÑO-PREMIUM-COMPLETADO.md",
    "DISEÑO-PREMIUM-IMPLEMENTADO.md",
    "DOCKER-BUILD-ESTADO.md",
    "ENTORNO-IDEAL-COMPLETADO.md",
    "ESTADO-ACTUAL-COMPLETO.md",
    "ESTADO-FINAL-V2.0.0.md",
    "ESTADO-SISTEMA-ACTUAL.md",
    "MULTITENANCY-COMPLETADO.md"
)

$movidosCount = 0
foreach ($archivo in $docsObsoletos) {
    if (Test-Path $archivo) {
        Move-Item $archivo "_archive/documentacion-obsoleta/" -Force
        Write-Host "  📄 Movido: $archivo" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount archivos de documentación movidos" -ForegroundColor Green

# FASE 2: Scripts de diagnóstico obsoletos
Write-Host "`n🔍 FASE 2: Moviendo scripts de diagnóstico obsoletos..." -ForegroundColor Yellow

$scriptsObsoletos = @(
    "diagnostico-*.ps1",
    "debug-*.ps1",
    "check_*.py",
    "auditoria_*.py",
    "investigar_*.py",
    "mapear_*.py",
    "explorar_*.py"
)

$movidosCount = 0
foreach ($pattern in $scriptsObsoletos) {
    $archivos = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Move-Item $archivo.FullName "_archive/scripts-desarrollo/" -Force
        Write-Host "  🔧 Movido: $($archivo.Name)" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount scripts de diagnóstico movidos" -ForegroundColor Green

# FASE 3: Scripts de desarrollo/fix temporales
Write-Host "`n🔧 FASE 3: Moviendo scripts de desarrollo temporales..." -ForegroundColor Yellow

$scriptsFix = @(
    "aplicar_*.py",
    "arreglar_*.py",
    "blindar_*.py",
    "configurar_*.py",
    "crear_*.py",
    "fix_*.py",
    "limpieza_*.py",
    "proteger_*.py",
    "completar_*.py",
    "agregar_*.py",
    "eliminar_*.py",
    "otorgar_*.py"
)

$movidosCount = 0
foreach ($pattern in $scriptsFix) {
    $archivos = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Move-Item $archivo.FullName "_archive/scripts-desarrollo/" -Force
        Write-Host "  🐍 Movido: $($archivo.Name)" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount scripts de desarrollo movidos" -ForegroundColor Green

# FASE 4: Archivos temporales/basura
Write-Host "`n🗑️ FASE 4: Eliminando archivos temporales..." -ForegroundColor Yellow

$archivosTemporales = @(
    "diagnostico_*.json",
    "diagnostico_*.html",
    "estado-sistema-*.html",
    "BD_PROTECTION_STATUS.lock",
    "temp-*.txt"
)

$eliminadosCount = 0
foreach ($pattern in $archivosTemporales) {
    $archivos = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Remove-Item $archivo.FullName -Force
        Write-Host "  🗑️ Eliminado: $($archivo.Name)" -ForegroundColor Red
        $eliminadosCount++
    }
}
Write-Host "✅ $eliminadosCount archivos temporales eliminados" -ForegroundColor Green

# FASE 5: Reorganización de scripts útiles
Write-Host "`n📁 FASE 5: Reorganizando scripts útiles..." -ForegroundColor Yellow

$scriptsUtiles = @{
    "dev.ps1"          = "scripts/dev.ps1"
    "deploy.ps1"       = "scripts/deploy.ps1"
    "ABRIR-PACKFY.ps1" = "scripts/start.ps1"
    "ABRIR-PACKFY.bat" = "scripts/start.bat"
}

$reorganizadosCount = 0
foreach ($origen in $scriptsUtiles.Keys) {
    if (Test-Path $origen) {
        $destino = $scriptsUtiles[$origen]
        Move-Item $origen $destino -Force
        Write-Host "  📁 Reorganizado: $origen → $destino" -ForegroundColor Green
        $reorganizadosCount++
    }
}
Write-Host "✅ $reorganizadosCount scripts reorganizados" -ForegroundColor Green

# FASE 6: Consolidación de documentación
Write-Host "`n📚 FASE 6: Consolidando documentación útil..." -ForegroundColor Yellow

$docsMantener = @{
    "auditoria-README.md" = "docs/auditoria.md"
    "CHANGELOG.md"        = "docs/changelog.md"
}

$consolidadosCount = 0
foreach ($origen in $docsMantener.Keys) {
    if (Test-Path $origen) {
        $destino = $docsMantener[$origen]
        Move-Item $origen $destino -Force
        Write-Host "  📚 Consolidado: $origen → $destino" -ForegroundColor Green
        $consolidadosCount++
    }
}
Write-Host "✅ $consolidadosCount documentos consolidados" -ForegroundColor Green

# FASE 7: Verificación final
Write-Host "`n🔍 FASE 7: Verificación del sistema..." -ForegroundColor Yellow

Write-Host "Verificando que Docker sigue funcionando..." -ForegroundColor White
try {
    $containers = docker-compose ps --services
    if ($containers -contains "backend" -and $containers -contains "frontend") {
        Write-Host "✅ Docker Compose configuración intacta" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️ Verificar configuración Docker" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "⚠️ Error verificando Docker, revisar manualmente" -ForegroundColor Yellow
}

# Resumen final
Write-Host "`n🎉 LIMPIEZA COMPLETADA!" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host "📁 Estructura final:" -ForegroundColor White
Write-Host "   ├── backend/ (Django - intacto)" -ForegroundColor Green
Write-Host "   ├── frontend/ (React - intacto)" -ForegroundColor Green
Write-Host "   ├── scripts/ (scripts útiles organizados)" -ForegroundColor Blue
Write-Host "   ├── docs/ (documentación consolidada)" -ForegroundColor Blue
Write-Host "   ├── _archive/ (archivos históricos)" -ForegroundColor Gray
Write-Host "   └── compose.yml (intacto)" -ForegroundColor Green

Write-Host "`n📋 Próximos pasos:" -ForegroundColor Yellow
Write-Host "   1. Probar: docker-compose up -d" -ForegroundColor White
Write-Host "   2. Verificar SuperAdminPanel funciona" -ForegroundColor White
Write-Host "   3. Testear multitenancy" -ForegroundColor White
Write-Host "   4. Si todo funciona: git add . && git commit" -ForegroundColor White

Write-Host "`n🔄 Para revertir: git checkout backup/pre-cleanup-audit" -ForegroundColor Cyan
