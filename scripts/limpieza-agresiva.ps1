# 🧹 LIMPIEZA AGRESIVA FASE 2 - PACKFY
# Segunda pasada para limpiar archivos que quedaron

Write-Host "🧹 FASE 2: LIMPIEZA AGRESIVA" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

# Verificar directorio
if (-not (Test-Path "compose.yml")) {
    Write-Host "❌ ERROR: No se encuentra compose.yml" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Directorio de proyecto confirmado" -ForegroundColor Green

# FASE 2A: Mover TODOS los scripts de testing/verificación
Write-Host "`n🧪 FASE 2A: Moviendo scripts de testing y verificación..." -ForegroundColor Yellow

$scriptsTesting = @(
    "testing-*.ps1",
    "verificar-*.ps1",
    "verificacion-*.ps1",
    "validacion-*.ps1",
    "probar-*.ps1",
    "prueba-*.ps1",
    "test-*.ps1",
    "test_*.py",
    "*_test.py",
    "TESTING-*.md",
    "VERIFICACION-*.json",
    "test-*.js",
    "test-*.html"
)

$movidosCount = 0
foreach ($pattern in $scriptsTesting) {
    $archivos = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Move-Item $archivo.FullName "_archive/scripts-desarrollo/" -Force
        Write-Host "  🧪 Movido: $($archivo.Name)" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount scripts de testing movidos" -ForegroundColor Green

# FASE 2B: Mover scripts de configuración/setup específicos
Write-Host "`n⚙️ FASE 2B: Moviendo scripts de configuración específicos..." -ForegroundColor Yellow

$scriptsConfig = @(
    "configurar-*.ps1",
    "configuracion-*.ps1",
    "setup-*.ps1",
    "instalar-*.ps1",
    "instrucciones-*.ps1",
    "inicio-*.ps1",
    "iniciar-*.ps1",
    "build-*.ps1",
    "rebuild-*.ps1",
    "reset-*.ps1",
    "reset_*.sh",
    "reset_*.py",
    "solucion-*.ps1",
    "fix-*.ps1",
    "corregir-*.ps1",
    "reload-*.ps1",
    "serve-*.ps1",
    "start-*.ps1",
    "stop-*.ps1"
)

$movidosCount = 0
foreach ($pattern in $scriptsConfig) {
    $archivos = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Move-Item $archivo.FullName "_archive/scripts-desarrollo/" -Force
        Write-Host "  ⚙️ Movido: $($archivo.Name)" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount scripts de configuración movidos" -ForegroundColor Green

# FASE 2C: Mover archivos de modo móvil/PWA específicos
Write-Host "`n📱 FASE 2C: Moviendo archivos de modo móvil y PWA..." -ForegroundColor Yellow

$scriptsMovil = @(
    "*movil*.ps1",
    "*mobile*.ps1",
    "*pwa*.ps1",
    "*chrome*.ps1",
    "*ngrok*.ps1",
    "*https*.ps1"
)

$movidosCount = 0
foreach ($pattern in $scriptsMovil) {
    $archivos = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Move-Item $archivo.FullName "_archive/scripts-desarrollo/" -Force
        Write-Host "  📱 Movido: $($archivo.Name)" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount scripts móviles movidos" -ForegroundColor Green

# FASE 2D: Mover documentación fragmentada restante
Write-Host "`n📚 FASE 2D: Moviendo documentación fragmentada..." -ForegroundColor Yellow

$docsFragmentados = @(
    "*COMPLETADO*.md",
    "*PROGRESO*.md",
    "*REPORTE*.md",
    "*RESUMEN*.md",
    "*PLAN*.md",
    "*ANALISIS*.md",
    "*IMPLEMENTACION*.md",
    "*MODERNIZACION*.md",
    "*ADMIN-*.md",
    "*DEBUG-*.md",
    "*COMIC-*.txt",
    "*MAPEO-*.md",
    "*SISTEMA-*.md",
    "*SOLUCION-*.md",
    "HEALTH-*.ps1"
)

$movidosCount = 0
foreach ($pattern in $docsFragmentados) {
    $archivos = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Move-Item $archivo.FullName "_archive/documentacion-obsoleta/" -Force
        Write-Host "  📚 Movido: $($archivo.Name)" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount documentos fragmentados movidos" -ForegroundColor Green

# FASE 2E: Mover archivos de comandos/utilidades específicas
Write-Host "`n🔧 FASE 2E: Moviendo utilidades y comandos específicos..." -ForegroundColor Yellow

$utilidades = @(
    "comandos-*.ps1",
    "aplicar-*.ps1",
    "ejecutar-*.ps1",
    "packfy.ps1",
    "start.ps1",
    "stop.ps1",
    "guia-*.ps1",
    "monitor-*.ps1",
    "modo-*.ps1",
    "organizar-*.ps1",
    "reorganizar-*.ps1",
    "resultado-*.ps1",
    "shell_*.py",
    "corregir_*.py",
    "verificar_*.py",
    "restaurar_*.py"
)

$movidosCount = 0
foreach ($pattern in $utilidades) {
    $archivos = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Move-Item $archivo.FullName "_archive/scripts-desarrollo/" -Force
        Write-Host "  🔧 Movido: $($archivo.Name)" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount utilidades movidas" -ForegroundColor Green

# FASE 2F: Consolidar archivos de configuración específicos
Write-Host "`n📄 FASE 2F: Moviendo archivos de configuración específicos..." -ForegroundColor Yellow

$configsEspecificos = @(
    "hosts-*.txt",
    "*.json" -and -not "*package*.json",
    "*.cfg",
    "*.toml",
    "*profile*.ps1",
    "mcp-*.json"
)

$movidosCount = 0

# Mover archivos de configuración específicos individualmente
$archivosConfig = @(
    "hosts-multitenancy.txt",
    "REPORTE-ESTADO-ACTUAL-SISTEMA.json",
    "VERIFICACION-ESTRUCTURA-NUEVA-COMPLETA.json",
    "VERIFICACION-FINAL-CORRECCION-COMPLETA.json",
    "VERIFICACION-LIMPIEZA-COMPLETADA.json",
    "test_login.json",
    "setup.cfg",
    "pyproject.toml",
    "pyrightconfig.json",
    "pwsh7-profile.ps1",
    "mcp-config.json"
)

foreach ($archivo in $archivosConfig) {
    if (Test-Path $archivo) {
        Move-Item $archivo "_archive/scripts-desarrollo/" -Force
        Write-Host "  📄 Movido: $archivo" -ForegroundColor Green
        $movidosCount++
    }
}
Write-Host "✅ $movidosCount archivos de configuración movidos" -ForegroundColor Green

# Resumen de limpieza agresiva
Write-Host "`n🎯 RESUMEN LIMPIEZA AGRESIVA:" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

$archivosRestantes = (Get-ChildItem *.ps1).Count
$archivosMarkdown = (Get-ChildItem *.md).Count
$archivosPython = (Get-ChildItem *.py).Count

Write-Host "📊 Archivos restantes en raíz:" -ForegroundColor White
Write-Host "   PowerShell: $archivosRestantes" -ForegroundColor $(if ($archivosRestantes -lt 10) { "Green" } else { "Yellow" })
Write-Host "   Markdown: $archivosMarkdown" -ForegroundColor $(if ($archivosMarkdown -lt 5) { "Green" } else { "Yellow" })
Write-Host "   Python: $archivosPython" -ForegroundColor $(if ($archivosPython -lt 5) { "Green" } else { "Yellow" })

if ($archivosRestantes -lt 10 -and $archivosMarkdown -lt 5 -and $archivosPython -lt 5) {
    Write-Host "`n🎉 ¡LIMPIEZA EXITOSA!" -ForegroundColor Green
    Write-Host "El proyecto está ahora mucho más organizado" -ForegroundColor Green
}
else {
    Write-Host "`n⚠️ Todavía hay archivos por organizar" -ForegroundColor Yellow
    Write-Host "Revisar manualmente los archivos restantes" -ForegroundColor Yellow
}

Write-Host "`n📋 Próximo paso:" -ForegroundColor Yellow
Write-Host "   Probar: docker-compose up -d" -ForegroundColor White
