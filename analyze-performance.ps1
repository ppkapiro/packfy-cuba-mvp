# 🇨🇺 PACKFY CUBA - ANÁLISIS DE RENDIMIENTO VS CODE (SIN ELIMINAR NADA)
# Diagnóstico completo para identificar causas de lentitud

Write-Host "🔍 INICIANDO ANÁLISIS DE RENDIMIENTO (SOLO LECTURA)..." -ForegroundColor Cyan
Write-Host "⚠️  NO SE ELIMINARÁ NI MOVERÁ NINGÚN ARCHIVO" -ForegroundColor Yellow
Write-Host ""

# 1. ANÁLISIS DE TAMAÑO DEL PROYECTO
Write-Host "📊 ANÁLISIS DE TAMAÑO DEL PROYECTO" -ForegroundColor Green
Write-Host "=" * 50

$totalFiles = (Get-ChildItem -Recurse -File | Measure-Object).Count
$totalSize = [math]::Round(((Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB), 2)
$totalFolders = (Get-ChildItem -Recurse -Directory | Measure-Object).Count

Write-Host "📁 Total archivos: $totalFiles"
Write-Host "💾 Tamaño total: $totalSize MB"
Write-Host "📂 Total carpetas: $totalFolders"
Write-Host ""

# 2. ANÁLISIS POR TIPO DE ARCHIVO
Write-Host "📄 ANÁLISIS POR TIPO DE ARCHIVO" -ForegroundColor Green
Write-Host "=" * 50

$fileTypes = Get-ChildItem -Recurse -File | Group-Object Extension | Sort-Object Count -Descending | Select-Object -First 15
foreach ($type in $fileTypes) {
    $ext = if ($type.Name) { $type.Name } else { "(sin extensión)" }
    $size = [math]::Round((($type.Group | Measure-Object -Property Length -Sum).Sum / 1MB), 2)
    Write-Host "  $ext : $($type.Count) archivos, $size MB"
}
Write-Host ""

# 3. CARPETAS MÁS PESADAS
Write-Host "📁 CARPETAS MÁS PESADAS" -ForegroundColor Green
Write-Host "=" * 50

$folders = Get-ChildItem -Directory | ForEach-Object {
    $folderSize = [math]::Round(((Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB), 2)
    $fileCount = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
    [PSCustomObject]@{
        Nombre   = $_.Name
        Tamaño   = $folderSize
        Archivos = $fileCount
    }
} | Sort-Object Tamaño -Descending

foreach ($folder in $folders) {
    Write-Host "  $($folder.Nombre): $($folder.Tamaño) MB ($($folder.Archivos) archivos)"
}
Write-Host ""

# 4. ARCHIVOS GRANDES INDIVIDUALES
Write-Host "🗃️  ARCHIVOS INDIVIDUALES MÁS GRANDES" -ForegroundColor Green
Write-Host "=" * 50

$largeFiles = Get-ChildItem -Recurse -File | Sort-Object Length -Descending | Select-Object -First 10
foreach ($file in $largeFiles) {
    $size = [math]::Round(($file.Length / 1MB), 2)
    Write-Host "  $($file.Name): $size MB"
}
Write-Host ""

# 5. DOCUMENTACIÓN EN RAÍZ
Write-Host "📝 ARCHIVOS DE DOCUMENTACIÓN EN RAÍZ" -ForegroundColor Green
Write-Host "=" * 50

$docsInRoot = Get-ChildItem -File | Where-Object { $_.Extension -eq ".md" -or $_.Name -like "*.txt" -or $_.Name -like "README*" }
Write-Host "  Total documentos en raíz: $($docsInRoot.Count)"
foreach ($doc in $docsInRoot) {
    $size = [math]::Round(($doc.Length / 1KB), 1)
    $lastWrite = $doc.LastWriteTime.ToString("yyyy-MM-dd")
    Write-Host "    $($doc.Name) ($size KB, modificado: $lastWrite)"
}
Write-Host ""

# 6. SCRIPTS EN RAÍZ
Write-Host "📜 SCRIPTS EN RAÍZ" -ForegroundColor Green
Write-Host "=" * 50

$scriptsInRoot = Get-ChildItem -File | Where-Object { $_.Extension -eq ".ps1" -or $_.Extension -eq ".py" -or $_.Extension -eq ".sh" }
Write-Host "  Total scripts en raíz: $($scriptsInRoot.Count)"
foreach ($script in $scriptsInRoot) {
    $size = [math]::Round(($script.Length / 1KB), 1)
    $lastWrite = $script.LastWriteTime.ToString("yyyy-MM-dd")
    Write-Host "    $($script.Name) ($size KB, modificado: $lastWrite)"
}
Write-Host ""

# 7. ARCHIVOS DOCKER
Write-Host "🐳 ARCHIVOS DOCKER" -ForegroundColor Green
Write-Host "=" * 50

$dockerFiles = Get-ChildItem -File | Where-Object { $_.Name -like "*docker*" -or $_.Name -like "*compose*" }
Write-Host "  Total archivos Docker: $($dockerFiles.Count)"
foreach ($docker in $dockerFiles) {
    $lastWrite = $docker.LastWriteTime.ToString("yyyy-MM-dd")
    Write-Host "    $($docker.Name) (modificado: $lastWrite)"
}
Write-Host ""

# 8. ANÁLISIS DE NODE_MODULES
Write-Host "📦 ANÁLISIS NODE_MODULES" -ForegroundColor Green
Write-Host "=" * 50

if (Test-Path "frontend\node_modules") {
    $nodeModulesSize = [math]::Round(((Get-ChildItem "frontend\node_modules" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB), 2)
    $nodeModulesFiles = (Get-ChildItem "frontend\node_modules" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host "  node_modules: $nodeModulesSize MB ($nodeModulesFiles archivos)"
}
else {
    Write-Host "  node_modules: No encontrado"
}
Write-Host ""

# 9. ANÁLISIS DE .GIT
Write-Host "🔄 ANÁLISIS REPOSITORIO GIT" -ForegroundColor Green
Write-Host "=" * 50

if (Test-Path ".git") {
    $gitSize = [math]::Round(((Get-ChildItem ".git" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB), 2)
    Write-Host "  .git: $gitSize MB"
}
else {
    Write-Host "  .git: No encontrado"
}
Write-Host ""

# 10. RECOMENDACIONES PRELIMINARES
Write-Host "💡 OBSERVACIONES INICIALES" -ForegroundColor Yellow
Write-Host "=" * 50

if ($totalFiles -gt 5000) {
    Write-Host "  ⚠️  Proyecto tiene muchos archivos ($totalFiles) - puede causar lentitud" -ForegroundColor Yellow
}

if ($totalSize -gt 500) {
    Write-Host "  ⚠️  Proyecto es muy grande ($totalSize MB) - considerar limpieza" -ForegroundColor Yellow
}

$mdFilesInRoot = ($docsInRoot | Where-Object { $_.Extension -eq ".md" }).Count
if ($mdFilesInRoot -gt 10) {
    Write-Host "  ⚠️  Muchos archivos .md en raíz ($mdFilesInRoot) - considerar reorganizar" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ ANÁLISIS COMPLETADO - NINGÚN ARCHIVO FUE MODIFICADO" -ForegroundColor Green
