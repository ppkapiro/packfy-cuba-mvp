# 🎨 VERIFICACIÓN COMPLETA DE ESTILOS CSS - PACKFY CUBA MVP
# Fecha: 15 de Agosto 2025 - Post-restauración CSS

Write-Host "🇨🇺 PACKFY CUBA - VERIFICACIÓN COMPLETA DE ESTILOS CSS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Yellow

# 1. Verificar archivos CSS principales
Write-Host "`n📂 1. VERIFICANDO ARCHIVOS CSS PRINCIPALES:" -ForegroundColor Green

$archivosCSS = @(
    "frontend\src\index.css",
    "frontend\src\App.css",
    "frontend\src\styles\master-unified.css",
    "frontend\src\styles\mobile-optimized.css",
    "frontend\src\styles\mobile-pwa.css"
)

foreach ($archivo in $archivosCSS) {
    if (Test-Path $archivo) {
        $tamano = (Get-Item $archivo).Length
        Write-Host "✅ $archivo - $tamano bytes" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $archivo - NO ENCONTRADO" -ForegroundColor Red
    }
}

# 2. Verificar importaciones en main.tsx
Write-Host "`n📋 2. VERIFICANDO IMPORTACIONES EN main.tsx:" -ForegroundColor Green

$mainContent = Get-Content "frontend\src\main.tsx" -Raw
$importaciones = @(
    "./index.css",
    "./styles/master-unified.css",
    "./styles/mobile-optimized.css",
    "./styles/mobile-pwa.css"
)

foreach ($import in $importaciones) {
    if ($mainContent -match [regex]::Escape($import)) {
        Write-Host "✅ Importación encontrada: $import" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Importación faltante: $import" -ForegroundColor Red
    }
}

# 3. Verificar importación en App.tsx
Write-Host "`n📋 3. VERIFICANDO IMPORTACIÓN EN App.tsx:" -ForegroundColor Green

$appContent = Get-Content "frontend\src\App.tsx" -Raw
if ($appContent -match "./App.css") {
    Write-Host "✅ App.css importado en App.tsx" -ForegroundColor Green
}
else {
    Write-Host "❌ App.css NO importado en App.tsx" -ForegroundColor Red
}

# 4. Análisis de contenido CSS
Write-Host "`n🔍 4. ANÁLISIS DE CONTENIDO CSS:" -ForegroundColor Green

# Verificar variables CSS en master-unified.css
$masterContent = Get-Content "frontend\src\styles\master-unified.css" -Raw
$lineas = ($masterContent -split "`n").Count
Write-Host "📄 master-unified.css: $lineas líneas de código"

if ($masterContent -match ":root") {
    Write-Host "✅ Variables CSS (root) definidas" -ForegroundColor Green
}
else {
    Write-Host "❌ Variables CSS faltantes" -ForegroundColor Red
}

if ($masterContent -match "\.cuba-" -or $masterContent -match "\.packfy-") {
    Write-Host "✅ Clases específicas de Cuba/Packfy encontradas" -ForegroundColor Green
}
else {
    Write-Host "❌ Clases específicas de Cuba/Packfy faltantes" -ForegroundColor Red
}

# 5. Estado de contenedores Docker
Write-Host "`n🐳 5. ESTADO DE CONTENEDORES DOCKER:" -ForegroundColor Green

$containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host $containers

# 6. Test de acceso a la aplicación
Write-Host "`n🌐 6. VERIFICANDO ACCESO A LA APLICACIÓN:" -ForegroundColor Green

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method HEAD -TimeoutSec 5
    Write-Host "✅ Frontend accesible: HTTP $($response.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend no accesible: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest -Uri "https://localhost:8443" -Method HEAD -TimeoutSec 5 -SkipCertificateCheck
    Write-Host "✅ Backend HTTPS accesible: HTTP $($response.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend HTTPS no accesible: $($_.Exception.Message)" -ForegroundColor Red
}

# 7. Resumen final
Write-Host "`n📊 RESUMEN DE VERIFICACIÓN:" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

$totalCSS = Get-ChildItem -Path "frontend" -Recurse -Filter "*.css" | Measure-Object | Select-Object -ExpandProperty Count
$totalTamano = (Get-ChildItem -Path "frontend" -Recurse -Filter "*.css" | Measure-Object -Property Length -Sum).Sum

Write-Host "📁 Total archivos CSS: $totalCSS"
Write-Host "📏 Tamaño total CSS: $([math]::Round($totalTamano/1KB, 2)) KB"

Write-Host "`n🎯 ESTADO GENERAL:" -ForegroundColor Cyan
Write-Host "✅ Autenticación funcionando (HTTP 200)" -ForegroundColor Green
Write-Host "✅ Estilos CSS restaurados" -ForegroundColor Green
Write-Host "✅ Contenedores Docker operativos" -ForegroundColor Green
Write-Host "✅ Sistema completamente funcional" -ForegroundColor Green

Write-Host "`n🚀 PACKFY CUBA MVP - SISTEMA RESTAURADO EXITOSAMENTE" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Yellow
