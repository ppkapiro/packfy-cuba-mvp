# 🚀 VALIDACIÓN NAVEGACIÓN DUEÑO - COMPLETA
# Packfy Cuba v3.0 - Sistema Unificado
# Fecha: $(Get-Date -Format "yyyy-MM-dd HH:mm")

Write-Host "🇨🇺 PACKFY CUBA - VALIDACIÓN NAVEGACIÓN DUEÑO" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# Configuración
$projectRoot = "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"
$frontendRoot = "$projectRoot\frontend"

# Función para verificar archivos
function Test-ComponentFile {
    param([string]$FilePath, [string]$ComponentName)

    Write-Host "📁 Verificando $ComponentName..." -ForegroundColor Yellow

    if (Test-Path $FilePath) {
        $content = Get-Content $FilePath -Raw
        $size = (Get-Item $FilePath).Length

        Write-Host "   ✅ Archivo existe: $FilePath" -ForegroundColor Green
        Write-Host "   📊 Tamaño: $([math]::Round($size/1KB, 2)) KB" -ForegroundColor Cyan

        # Verificar imports importantes
        if ($content -match "import.*React") {
            Write-Host "   ✅ React importado correctamente" -ForegroundColor Green
        }

        if ($content -match "export default") {
            Write-Host "   ✅ Componente exportado correctamente" -ForegroundColor Green
        }

        return $true
    }
    else {
        Write-Host "   ❌ Archivo no existe: $FilePath" -ForegroundColor Red
        return $false
    }
}

# Función para verificar rutas
function Test-RouteConfiguration {
    param([string]$AppTsxPath)

    Write-Host "🛣️ Verificando configuración de rutas..." -ForegroundColor Yellow

    if (Test-Path $AppTsxPath) {
        $content = Get-Content $AppTsxPath -Raw

        # Verificar import de AdminDashboard
        if ($content -match "import.*AdminDashboard") {
            Write-Host "   ✅ AdminDashboard importado en App.tsx" -ForegroundColor Green
        }
        else {
            Write-Host "   ❌ AdminDashboard NO importado en App.tsx" -ForegroundColor Red
        }

        # Verificar ruta admin/dashboard
        if ($content -match 'path="admin/dashboard"') {
            Write-Host "   ✅ Ruta admin/dashboard configurada" -ForegroundColor Green
        }
        else {
            Write-Host "   ❌ Ruta admin/dashboard NO configurada" -ForegroundColor Red
        }

        return $true
    }
    else {
        Write-Host "   ❌ App.tsx no encontrado" -ForegroundColor Red
        return $false
    }
}

# Función para verificar estilos
function Test-StylesConfiguration {
    param([array]$StylePaths)

    Write-Host "🎨 Verificando archivos de estilos..." -ForegroundColor Yellow

    foreach ($stylePath in $StylePaths) {
        if (Test-Path $stylePath) {
            $size = (Get-Item $stylePath).Length
            Write-Host "   ✅ Estilo existe: $(Split-Path $stylePath -Leaf) ($([math]::Round($size/1KB, 2)) KB)" -ForegroundColor Green
        }
        else {
            Write-Host "   ❌ Estilo faltante: $(Split-Path $stylePath -Leaf)" -ForegroundColor Red
        }
    }
}

# Función para análisis TypeScript
function Test-TypeScriptSyntax {
    param([string]$TsxFile)

    Write-Host "🔍 Analizando sintaxis TypeScript: $(Split-Path $TsxFile -Leaf)..." -ForegroundColor Yellow

    if (Test-Path $TsxFile) {
        $content = Get-Content $TsxFile -Raw

        # Verificar sintaxis básica
        $issues = @()

        # Verificar interfaces
        if ($content -match "interface\s+\w+\s*{") {
            Write-Host "   ✅ Interfaces TypeScript definidas" -ForegroundColor Green
        }

        # Verificar hooks de React
        if ($content -match "useState|useEffect|useContext") {
            Write-Host "   ✅ Hooks de React utilizados" -ForegroundColor Green
        }

        # Verificar manejo de errores
        if ($content -match "try\s*{.*catch") {
            Write-Host "   ✅ Manejo de errores implementado" -ForegroundColor Green
        }

        # Verificar async/await
        if ($content -match "async.*await") {
            Write-Host "   ✅ Operaciones asíncronas implementadas" -ForegroundColor Green
        }

        return $true
    }
    else {
        Write-Host "   ❌ Archivo no encontrado" -ForegroundColor Red
        return $false
    }
}

Write-Host ""
Write-Host "🔍 INICIANDO VALIDACIÓN COMPLETA..." -ForegroundColor Cyan
Write-Host ""

# 1. Verificar componentes principales
Write-Host "1️⃣ COMPONENTES DE NAVEGACIÓN" -ForegroundColor Magenta
Write-Host "-" * 40

$adminNavPath = "$frontendRoot\src\components\navigation\AdminNavigation.tsx"
$standardNavPath = "$frontendRoot\src\components\navigation\StandardNavigation.tsx"
$layoutPath = "$frontendRoot\src\components\Layout.tsx"

Test-ComponentFile $adminNavPath "AdminNavigation"
Test-ComponentFile $standardNavPath "StandardNavigation"
Test-ComponentFile $layoutPath "Layout (modificado)"

Write-Host ""

# 2. Verificar dashboard administrativo
Write-Host "2️⃣ DASHBOARD ADMINISTRATIVO" -ForegroundColor Magenta
Write-Host "-" * 40

$adminDashboardPath = "$frontendRoot\src\pages\AdminDashboard.tsx"
Test-ComponentFile $adminDashboardPath "AdminDashboard"
Test-TypeScriptSyntax $adminDashboardPath

Write-Host ""

# 3. Verificar configuración de rutas
Write-Host "3️⃣ CONFIGURACIÓN DE RUTAS" -ForegroundColor Magenta
Write-Host "-" * 40

$appTsxPath = "$frontendRoot\src\App.tsx"
Test-RouteConfiguration $appTsxPath

Write-Host ""

# 4. Verificar estilos
Write-Host "4️⃣ ARCHIVOS DE ESTILOS" -ForegroundColor Magenta
Write-Host "-" * 40

$stylePaths = @(
    "$frontendRoot\src\styles\admin-dashboard.css",
    "$frontendRoot\src\styles\admin-navigation.css"
)
Test-StylesConfiguration $stylePaths

Write-Host ""

# 5. Verificar estructura de archivos
Write-Host "5️⃣ ESTRUCTURA DE ARCHIVOS" -ForegroundColor Magenta
Write-Host "-" * 40

$requiredFiles = @(
    @{Path = "$frontendRoot\src\pages\AdminDashboard.tsx"; Name = "AdminDashboard Component" },
    @{Path = "$frontendRoot\src\components\navigation\AdminNavigation.tsx"; Name = "AdminNavigation Component" },
    @{Path = "$frontendRoot\src\components\navigation\StandardNavigation.tsx"; Name = "StandardNavigation Component" },
    @{Path = "$frontendRoot\src\styles\admin-dashboard.css"; Name = "Admin Dashboard Styles" },
    @{Path = "$frontendRoot\src\styles\admin-navigation.css"; Name = "Admin Navigation Styles" },
    @{Path = "$projectRoot\docs\ANALISIS-NAVEGACION-DUENO.md"; Name = "Análisis de Navegación" }
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file.Path) {
        $size = (Get-Item $file.Path).Length
        Write-Host "   ✅ $($file.Name) ($([math]::Round($size/1KB, 2)) KB)" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ $($file.Name) - FALTANTE" -ForegroundColor Red
        $allFilesExist = $false
    }
}

Write-Host ""

# 6. Verificar integraciones
Write-Host "6️⃣ INTEGRACIONES Y DEPENDENCIAS" -ForegroundColor Magenta
Write-Host "-" * 40

# Verificar contexts utilizados
$contextFiles = @(
    "$frontendRoot\src\contexts\AuthContext.tsx",
    "$frontendRoot\src\contexts\TenantContext.tsx"
)

foreach ($contextFile in $contextFiles) {
    if (Test-Path $contextFile) {
        Write-Host "   ✅ Context disponible: $(Split-Path $contextFile -Leaf)" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Context faltante: $(Split-Path $contextFile -Leaf)" -ForegroundColor Red
    }
}

# Verificar servicios API
$apiServicePath = "$frontendRoot\src\services\api.ts"
if (Test-Path $apiServicePath) {
    Write-Host "   ✅ API Service disponible" -ForegroundColor Green
}
else {
    Write-Host "   ❌ API Service faltante" -ForegroundColor Red
}

Write-Host ""

# 7. Resumen final
Write-Host "🎯 RESUMEN DE VALIDACIÓN" -ForegroundColor Cyan
Write-Host "=" * 50

if ($allFilesExist) {
    Write-Host "✅ ESTRUCTURA COMPLETA - Todos los archivos existen" -ForegroundColor Green
}
else {
    Write-Host "⚠️ ESTRUCTURA INCOMPLETA - Algunos archivos faltan" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 SIGUIENTES PASOS RECOMENDADOS:" -ForegroundColor Cyan
Write-Host "1. Probar navegación en modo dueño" -ForegroundColor White
Write-Host "2. Verificar dashboard administrativo" -ForegroundColor White
Write-Host "3. Validar métricas y datos" -ForegroundColor White
Write-Host "4. Probar responsive design" -ForegroundColor White
Write-Host "5. Validar accesibilidad" -ForegroundColor White

Write-Host ""
Write-Host "🚀 VALIDACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
