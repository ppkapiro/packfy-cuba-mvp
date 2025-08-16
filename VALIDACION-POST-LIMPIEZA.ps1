# 🔍 SCRIPT DE VALIDACIÓN POST-LIMPIEZA
# Fecha: 15 de Agosto de 2025
# Objetivo: Verificar que el proyecto funciona correctamente después de la limpieza

Write-Host "🇨🇺 PACKFY CUBA - VALIDACIÓN POST-LIMPIEZA" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray
Write-Host ""

$projectRoot = "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"
$errors = @()
$warnings = @()

# FASE 1: VERIFICAR ESTRUCTURA DE ARCHIVOS
Write-Host "📁 FASE 1: Verificando estructura de archivos" -ForegroundColor Green
Write-Host "-" * 40

# Verificar archivos críticos
$criticalFiles = @(
    "frontend\package.json",
    "frontend\src\main.tsx",
    "frontend\src\App.tsx",
    "backend\manage.py",
    "backend\requirements.txt",
    "compose.yml",
    "README.md"
)

foreach ($file in $criticalFiles) {
    $fullPath = Join-Path $projectRoot $file
    if (Test-Path $fullPath) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ $file (FALTA)" -ForegroundColor Red
        $errors += "Archivo crítico faltante: $file"
    }
}

# Verificar que no queden archivos BACKUP o UNIFICADO
Write-Host ""
Write-Host "🔍 Verificando eliminación de archivos duplicados..." -ForegroundColor Cyan

$backupFiles = Get-ChildItem -Path "$projectRoot\frontend\src" -Recurse -Name "*BACKUP*" -ErrorAction SilentlyContinue
$unificadoFiles = Get-ChildItem -Path "$projectRoot\frontend\src" -Recurse -Name "*UNIFICADO*" -ErrorAction SilentlyContinue

if ($backupFiles.Count -eq 0) {
    Write-Host "  ✅ No hay archivos BACKUP restantes" -ForegroundColor Green
}
else {
    Write-Host "  ⚠️  Archivos BACKUP encontrados: $($backupFiles.Count)" -ForegroundColor Yellow
    $warnings += "Archivos BACKUP aún presentes: $($backupFiles -join ', ')"
}

if ($unificadoFiles.Count -eq 0) {
    Write-Host "  ✅ No hay archivos UNIFICADO restantes" -ForegroundColor Green
}
else {
    Write-Host "  ⚠️  Archivos UNIFICADO encontrados: $($unificadoFiles.Count)" -ForegroundColor Yellow
    $warnings += "Archivos UNIFICADO aún presentes: $($unificadoFiles -join ', ')"
}

# FASE 2: VERIFICAR FUNCIONALIDAD FRONTEND
Write-Host ""
Write-Host "⚛️  FASE 2: Verificando funcionalidad del frontend" -ForegroundColor Green
Write-Host "-" * 40

Set-Location "$projectRoot\frontend"

# Verificar que las dependencias están instaladas
if (Test-Path "node_modules") {
    Write-Host "  ✅ Dependencias instaladas" -ForegroundColor Green
}
else {
    Write-Host "  ⚠️  Instalando dependencias..." -ForegroundColor Yellow
    npm install --silent
}

# Ejecutar linting
Write-Host "  🔍 Ejecutando linting..." -ForegroundColor Cyan
try {
    $lintResult = npm run lint --silent 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Linting: Sin errores" -ForegroundColor Green
    }
    else {
        Write-Host "  ⚠️  Linting: Con warnings" -ForegroundColor Yellow
        $warnings += "Linting produjo warnings"
    }
}
catch {
    Write-Host "  ❌ Linting: Error" -ForegroundColor Red
    $errors += "Error en linting: $($_.Exception.Message)"
}

# Verificar type checking
Write-Host "  🔎 Verificando tipos TypeScript..." -ForegroundColor Cyan
try {
    $typeResult = npm run type-check --silent 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ TypeScript: Sin errores de tipos" -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ TypeScript: Errores de tipos encontrados" -ForegroundColor Red
        $errors += "Errores de TypeScript detectados"
    }
}
catch {
    Write-Host "  ❌ TypeScript: Error en verificación" -ForegroundColor Red
    $errors += "Error en type-check: $($_.Exception.Message)"
}

# Intentar build
Write-Host "  🏗️  Verificando build..." -ForegroundColor Cyan
try {
    $buildResult = npm run build --silent 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Build: Exitoso" -ForegroundColor Green

        # Verificar que se generó el directorio dist
        if (Test-Path "dist") {
            Write-Host "  ✅ Directorio dist generado" -ForegroundColor Green
        }
        else {
            Write-Host "  ⚠️  Directorio dist no encontrado" -ForegroundColor Yellow
            $warnings += "Build exitoso pero dist no encontrado"
        }
    }
    else {
        Write-Host "  ❌ Build: Falló" -ForegroundColor Red
        $errors += "Build del frontend falló"
    }
}
catch {
    Write-Host "  ❌ Build: Error crítico" -ForegroundColor Red
    $errors += "Error crítico en build: $($_.Exception.Message)"
}

# FASE 3: VERIFICAR CONTAINERS DOCKER
Write-Host ""
Write-Host "🐳 FASE 3: Verificando contenedores Docker" -ForegroundColor Green
Write-Host "-" * 40

Set-Location $projectRoot

try {
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}" | Where-Object { $_ -like "*packfy*" }

    if ($containers) {
        Write-Host "  📊 Contenedores encontrados:" -ForegroundColor Cyan
        $containers | ForEach-Object {
            if ($_ -like "*Up*") {
                Write-Host "  ✅ $_" -ForegroundColor Green
            }
            else {
                Write-Host "  ⚠️  $_" -ForegroundColor Yellow
                $warnings += "Contenedor no está ejecutándose: $_"
            }
        }
    }
    else {
        Write-Host "  ⚠️  No se encontraron contenedores de Packfy" -ForegroundColor Yellow
        $warnings += "Contenedores Docker no están ejecutándose"
    }
}
catch {
    Write-Host "  ❌ Error verificando Docker" -ForegroundColor Red
    $errors += "Error en verificación Docker: $($_.Exception.Message)"
}

# FASE 4: VERIFICAR ENDPOINTS
Write-Host ""
Write-Host "🌐 FASE 4: Verificando endpoints" -ForegroundColor Green
Write-Host "-" * 40

$endpoints = @(
    @{ Url = "https://localhost:5173"; Name = "Frontend" },
    @{ Url = "https://localhost:8443"; Name = "Backend" },
    @{ Url = "https://localhost:8443/api"; Name = "API" }
)

foreach ($endpoint in $endpoints) {
    try {
        Write-Host "  🔍 Verificando $($endpoint.Name)..." -ForegroundColor Cyan

        # Usar curl para verificar endpoint (más confiable que Invoke-WebRequest con HTTPS self-signed)
        $curlResult = curl -k -s -o /dev/null -w "%{http_code}" $endpoint.Url --connect-timeout 5

        if ($curlResult -eq "200") {
            Write-Host "  ✅ $($endpoint.Name): Respondiendo (HTTP 200)" -ForegroundColor Green
        }
        elseif ($curlResult -eq "000") {
            Write-Host "  ⚠️  $($endpoint.Name): No disponible" -ForegroundColor Yellow
            $warnings += "$($endpoint.Name) no está respondiendo"
        }
        else {
            Write-Host "  ⚠️  $($endpoint.Name): HTTP $curlResult" -ForegroundColor Yellow
            $warnings += "$($endpoint.Name) respondió con código $curlResult"
        }
    }
    catch {
        Write-Host "  ❌ $($endpoint.Name): Error de conexión" -ForegroundColor Red
        $warnings += "Error conectando a $($endpoint.Name)"
    }
}

# FASE 5: VERIFICAR NUEVA ESTRUCTURA
Write-Host ""
Write-Host "📂 FASE 5: Verificando nueva estructura organizacional" -ForegroundColor Green
Write-Host "-" * 40

$expectedDirs = @(
    "scripts\development",
    "scripts\diagnostics",
    "scripts\deployment",
    "docs\setup",
    "docs\api",
    "docs\deployment",
    "archive\legacy_docs"
)

foreach ($dir in $expectedDirs) {
    $fullPath = Join-Path $projectRoot $dir
    if (Test-Path $fullPath) {
        $fileCount = (Get-ChildItem $fullPath -File).Count
        Write-Host "  ✅ $dir ($fileCount archivos)" -ForegroundColor Green
    }
    else {
        Write-Host "  ⚠️  $dir (no existe)" -ForegroundColor Yellow
        $warnings += "Directorio esperado no existe: $dir"
    }
}

# Verificar archivos nuevos
$newFiles = @("CHANGELOG.md", "STATUS.md", "ANALISIS-ESTADO-PROYECTO-COMPLETO.md")
foreach ($file in $newFiles) {
    $fullPath = Join-Path $projectRoot $file
    if (Test-Path $fullPath) {
        Write-Host "  ✅ $file creado" -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ $file (falta)" -ForegroundColor Red
        $errors += "Archivo requerido no creado: $file"
    }
}

# RESUMEN FINAL
Write-Host ""
Write-Host "📋 RESUMEN DE VALIDACIÓN" -ForegroundColor Cyan
Write-Host "=" * 50

if ($errors.Count -eq 0) {
    Write-Host "✅ SIN ERRORES CRÍTICOS" -ForegroundColor Green
}
else {
    Write-Host "❌ ERRORES ENCONTRADOS ($($errors.Count)):" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  • $error" -ForegroundColor Red
    }
}

if ($warnings.Count -eq 0) {
    Write-Host "✅ SIN WARNINGS" -ForegroundColor Green
}
else {
    Write-Host "⚠️  WARNINGS ($($warnings.Count)):" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "  • $warning" -ForegroundColor Yellow
    }
}

Write-Host ""
if ($errors.Count -eq 0) {
    Write-Host "🎉 VALIDACIÓN EXITOSA - PROYECTO LISTO" -ForegroundColor Green
    Write-Host "🚀 Puedes continuar con el desarrollo normalmente" -ForegroundColor Cyan
}
else {
    Write-Host "⚠️  VALIDACIÓN CON ERRORES - REVISAR ANTES DE CONTINUAR" -ForegroundColor Red
    Write-Host "🔧 Corrige los errores antes de continuar" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📞 Validación completada - $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
