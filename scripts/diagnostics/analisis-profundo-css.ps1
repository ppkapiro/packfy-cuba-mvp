# 🇨🇺 PACKFY CUBA - ANÁLISIS PROFUNDO SISTEMA CSS
# Diagnóstico completo: Por qué se perdieron todos los estilos después del arreglo HTTP 500

Write-Host "🎨 === ANÁLISIS PROFUNDO SISTEMA CSS ===" -ForegroundColor Magenta
Write-Host ""

Write-Host "📊 SITUACIÓN ACTUAL:" -ForegroundColor Red
Write-Host "• ✅ Login HTTP 500: SOLUCIONADO" -ForegroundColor Green
Write-Host "• ❌ Estilos CSS: PERDIDOS COMPLETAMENTE" -ForegroundColor Red
Write-Host "• 🔍 Necesidad: Análisis profundo del sistema de estilos" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔍 === FASE 1: INVENTARIO COMPLETO DE ARCHIVOS CSS ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "📁 BUSCANDO TODOS LOS ARCHIVOS CSS EN EL PROYECTO:" -ForegroundColor Yellow

try {
    # Buscar todos los archivos CSS en el frontend
    $cssFiles = Get-ChildItem -Path "frontend" -Recurse -Filter "*.css" -ErrorAction SilentlyContinue

    if ($cssFiles) {
        Write-Host "   📄 ARCHIVOS CSS ENCONTRADOS:" -ForegroundColor White
        foreach ($file in $cssFiles) {
            $relativePath = $file.FullName.Replace((Get-Location).Path + "\", "")
            $size = [math]::Round($file.Length / 1KB, 2)
            Write-Host "      • $relativePath ($size KB)" -ForegroundColor Gray
        }
        Write-Host "   📊 Total archivos CSS: $($cssFiles.Count)" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ NO SE ENCONTRARON ARCHIVOS CSS" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error buscando archivos CSS: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "🔍 === FASE 2: ANÁLISIS ARCHIVO MAIN.TSX === " -ForegroundColor Cyan
Write-Host "📄 Revisando imports de CSS en main.tsx (punto de entrada React):" -ForegroundColor Yellow

try {
    if (Test-Path "frontend/src/main.tsx") {
        $mainContent = Get-Content "frontend/src/main.tsx" -Raw

        # Buscar imports de CSS
        $cssImports = $mainContent | Select-String "import.*\.css" -AllMatches

        if ($cssImports.Matches) {
            Write-Host "   📋 IMPORTS CSS EN MAIN.TSX:" -ForegroundColor White
            foreach ($match in $cssImports.Matches) {
                Write-Host "      • $($match.Value)" -ForegroundColor Gray
            }
        }
        else {
            Write-Host "   ❌ NO HAY IMPORTS CSS EN MAIN.TSX" -ForegroundColor Red
        }

        # Mostrar contenido completo para análisis
        Write-Host "   📄 CONTENIDO COMPLETO DE MAIN.TSX:" -ForegroundColor White
        Write-Host $mainContent -ForegroundColor Gray

    }
    else {
        Write-Host "   ❌ ARCHIVO main.tsx NO ENCONTRADO" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error leyendo main.tsx: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "🔍 === FASE 3: ANÁLISIS ARCHIVOS CSS CRÍTICOS ===" -ForegroundColor Cyan
Write-Host ""

# Lista de archivos CSS críticos para revisar
$criticalCssFiles = @(
    "frontend/src/styles/master-unified.css",
    "frontend/src/styles/mobile-optimized.css",
    "frontend/src/styles/mobile-safe.css",
    "frontend/src/styles/reset.css",
    "frontend/src/styles/index.css",
    "frontend/src/index.css",
    "frontend/src/App.css"
)

foreach ($cssFile in $criticalCssFiles) {
    Write-Host "📄 ANALIZANDO: $cssFile" -ForegroundColor Yellow

    if (Test-Path $cssFile) {
        $fileSize = (Get-Item $cssFile).Length
        $sizeKB = [math]::Round($fileSize / 1KB, 2)

        Write-Host "   ✅ Existe - Tamaño: $sizeKB KB" -ForegroundColor Green

        # Verificar si el archivo tiene contenido válido
        $content = Get-Content $cssFile -Raw -ErrorAction SilentlyContinue

        if ($content -and $content.Length -gt 100) {
            Write-Host "   ✅ Contiene CSS válido" -ForegroundColor Green

            # Buscar reglas CSS importantes
            $cssRules = ($content | Select-String "^\s*[.#]" -AllMatches).Matches.Count
            Write-Host "   📊 Reglas CSS detectadas: $cssRules" -ForegroundColor Gray

            # Mostrar primeras líneas para verificar integridad
            $firstLines = ($content -split "`n")[0..4] -join "`n"
            Write-Host "   📄 Primeras líneas:" -ForegroundColor Gray
            Write-Host "      $firstLines..." -ForegroundColor DarkGray

        }
        else {
            Write-Host "   ❌ ARCHIVO VACÍO O CORRUPTO" -ForegroundColor Red
        }
    }
    else {
        Write-Host "   ❌ NO EXISTE" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "🔍 === FASE 4: VERIFICACIÓN VITE CONFIG ===" -ForegroundColor Cyan
Write-Host ""

$viteConfigs = @(
    "frontend/vite.config.ts",
    "frontend/vite.config.mobile.ts",
    "frontend/vite.config.docker.ts"
)

foreach ($viteConfig in $viteConfigs) {
    Write-Host "⚙️ VERIFICANDO: $viteConfig" -ForegroundColor Yellow

    if (Test-Path $viteConfig) {
        Write-Host "   ✅ Existe" -ForegroundColor Green

        $viteContent = Get-Content $viteConfig -Raw

        # Buscar configuraciones relacionadas con CSS
        if ($viteContent -match "css") {
            Write-Host "   📄 Configuraciones CSS encontradas:" -ForegroundColor White
            $cssConfig = $viteContent | Select-String "css.*:" -Context 2
            if ($cssConfig) {
                foreach ($config in $cssConfig) {
                    Write-Host "      • $($config.Line)" -ForegroundColor Gray
                }
            }
        }
        else {
            Write-Host "   ⚠️ No hay configuraciones CSS específicas" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "   ❌ NO EXISTE" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "🔍 === FASE 5: VERIFICACIÓN DOCKER CSS ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 VERIFICANDO CSS EN CONTENEDOR FRONTEND:" -ForegroundColor Yellow

try {
    # Verificar archivos CSS dentro del contenedor
    $containerCssCheck = docker exec packfy-frontend-mobile-v4.0 ls -la /app/src/styles/ 2>$null

    if ($containerCssCheck) {
        Write-Host "   📁 Archivos CSS en contenedor:" -ForegroundColor White
        Write-Host $containerCssCheck -ForegroundColor Gray
    }
    else {
        Write-Host "   ❌ No se pueden listar archivos CSS en contenedor" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error verificando contenedor: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "🔍 === FASE 6: VERIFICACIÓN NETWORK/CARGA CSS ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "🌐 PROBANDO CARGA DE ARCHIVOS CSS:" -ForegroundColor Yellow

# Probar carga de archivos CSS específicos
$cssUrls = @(
    "https://192.168.12.178:5173/src/styles/master-unified.css",
    "https://192.168.12.178:5173/src/styles/mobile-optimized.css",
    "https://192.168.12.178:5173/src/styles/mobile-safe.css",
    "https://192.168.12.178:5173/src/index.css"
)

foreach ($cssUrl in $cssUrls) {
    try {
        $response = curl -k -s -w "%{http_code}" $cssUrl 2>$null

        if ($response -eq "200") {
            Write-Host "   ✅ $cssUrl: HTTP 200" -ForegroundColor Green
        }
        else {
            Write-Host "   ❌ $cssUrl: HTTP $response" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "   ❌ $cssUrl: Error de conexión" -ForegroundColor Red
    }
}

Write-Host ""

Write-Host "📋 === RESUMEN DE DIAGNÓSTICO ===" -ForegroundColor Magenta
Write-Host ""

Write-Host "🎯 PROBLEMAS IDENTIFICADOS:" -ForegroundColor Red
Write-Host "1. Verificar integridad de archivos CSS" -ForegroundColor White
Write-Host "2. Confirmar imports correctos en main.tsx" -ForegroundColor White
Write-Host "3. Verificar que Vite está sirviendo CSS" -ForegroundColor White
Write-Host "4. Comprobar que Docker incluye archivos CSS" -ForegroundColor White
Write-Host ""

Write-Host "📋 PRÓXIMOS PASOS BASADOS EN HALLAZGOS:" -ForegroundColor Green
Write-Host "• Ejecutaré análisis específico según los resultados" -ForegroundColor White
Write-Host "• Restauraré archivos CSS faltantes/corruptos" -ForegroundColor White
Write-Host "• Corregiré configuraciones de Vite si es necesario" -ForegroundColor White
Write-Host "• Rebuilder contenedores si CSS no está incluido" -ForegroundColor White
Write-Host ""
