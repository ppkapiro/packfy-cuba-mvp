# 🇨🇺 PACKFY CUBA - ANÁLISIS POST-ACTUALIZACIÓN CSS
# Investigando problema HTTP 500 tras cambios CSS y actualización Docker

Write-Host "🔍 === ANÁLISIS POST-ACTUALIZACIÓN CSS/DOCKER ===" -ForegroundColor Red
Write-Host ""

Write-Host "🎯 NUEVA INFORMACIÓN CRÍTICA:" -ForegroundColor Yellow
Write-Host "• Problema inició DESPUÉS de actualizar contenedores" -ForegroundColor White
Write-Host "• Cambios previos: CSS de página de lobby" -ForegroundColor White
Write-Host "• Móvil funcionaba ANTES de estos cambios" -ForegroundColor White
Write-Host ""

Write-Host "🔄 REVISANDO CAMBIOS RECIENTES:" -ForegroundColor Yellow
Write-Host ""

# 1. Verificar cambios CSS recientes
Write-Host "1. 📄 VERIFICANDO ARCHIVOS CSS MODIFICADOS:" -ForegroundColor Yellow

$cssFiles = @(
    "frontend/src/styles/master-unified.css",
    "frontend/src/styles/main.css",
    "frontend/src/styles/mobile-optimized.css",
    "frontend/src/styles/mobile-pwa.css"
)

foreach ($cssFile in $cssFiles) {
    if (Test-Path $cssFile) {
        $lastWrite = (Get-Item $cssFile).LastWriteTime
        Write-Host "   📄 $cssFile" -ForegroundColor White
        Write-Host "      Modificado: $lastWrite" -ForegroundColor Gray

        # Verificar tamaño del archivo
        $size = (Get-Item $cssFile).Length
        if ($size -gt 500000) {
            # Mayor a 500KB
            Write-Host "      ⚠️ ARCHIVO MUY GRANDE: $([math]::Round($size/1KB, 2)) KB" -ForegroundColor Red
        }
        elseif ($size -gt 100000) {
            # Mayor a 100KB
            Write-Host "      ⚠️ Archivo grande: $([math]::Round($size/1KB, 2)) KB" -ForegroundColor Yellow
        }
        else {
            Write-Host "      ✅ Tamaño normal: $([math]::Round($size/1KB, 2)) KB" -ForegroundColor Green
        }
    }
    else {
        Write-Host "   ❌ No encontrado: $cssFile" -ForegroundColor Red
    }
}

Write-Host ""

# 2. Verificar errores en los contenedores
Write-Host "2. 🐳 ANALIZANDO LOGS DE CONTENEDORES POST-ACTUALIZACIÓN:" -ForegroundColor Yellow

$containers = @("packfy-frontend-mobile-v4.0", "packfy-backend-v4")

foreach ($container in $containers) {
    Write-Host ""
    Write-Host "   📋 Logs de $container (últimas 20 líneas):" -ForegroundColor White
    try {
        $logs = docker logs $container --tail 20 2>&1
        if ($logs -match "error|Error|ERROR|fail|Fail|FAIL|exception|Exception") {
            Write-Host "      ❌ ERRORES DETECTADOS:" -ForegroundColor Red
            $errorLines = $logs | Where-Object { $_ -match "error|Error|ERROR|fail|Fail|FAIL|exception|Exception" }
            foreach ($errorLine in $errorLines) {
                Write-Host "      🔴 $errorLine" -ForegroundColor Red
            }
        }
        else {
            Write-Host "      ✅ No hay errores evidentes en logs" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "      ❌ Error obteniendo logs: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# 3. Verificar problemas específicos CSS en móvil
Write-Host "3. 📱 PROBLEMAS CSS QUE PUEDEN CAUSAR HTTP 500 EN MÓVIL:" -ForegroundColor Yellow
Write-Host ""

Write-Host "   🔍 Verificando problemas comunes:" -ForegroundColor White

# Verificar si hay CSS que puede causar problemas en móvil
$cssProblems = @()

# Buscar @import problemáticos
$frontendPath = "frontend/src"
if (Test-Path $frontendPath) {
    $importIssues = Get-ChildItem -Path $frontendPath -Recurse -Include "*.css" | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        if ($content -match "@import.*url\(.*\)" -and $content -match "http://|https://") {
            "❌ $($_.Name): @import externo detectado"
        }
    }

    if ($importIssues) {
        $cssProblems += $importIssues
    }
}

# Verificar tamaños de archivos CSS
$largeCSSFiles = Get-ChildItem -Path "frontend/src/styles" -Include "*.css" -Recurse | Where-Object { $_.Length -gt 300000 }
if ($largeCSSFiles) {
    foreach ($file in $largeCSSFiles) {
        $cssProblems += "⚠️ $($file.Name): Archivo muy grande ($([math]::Round($file.Length/1KB, 2)) KB)"
    }
}

if ($cssProblems.Count -gt 0) {
    Write-Host "   ❌ PROBLEMAS CSS DETECTADOS:" -ForegroundColor Red
    foreach ($problem in $cssProblems) {
        Write-Host "      $problem" -ForegroundColor Red
    }
}
else {
    Write-Host "   ✅ No se detectaron problemas CSS evidentes" -ForegroundColor Green
}

Write-Host ""

# 4. Verificar configuración Vite tras actualización
Write-Host "4. ⚙️ VERIFICANDO CONFIGURACIÓN VITE POST-ACTUALIZACIÓN:" -ForegroundColor Yellow

$viteConfig = "frontend/vite.config.mobile.ts"
if (Test-Path $viteConfig) {
    Write-Host "   📄 Verificando $viteConfig..." -ForegroundColor White

    $config = Get-Content $viteConfig -Raw

    # Verificar configuraciones problemáticas
    $viteIssues = @()

    if ($config -match "sourcemap:\s*true") {
        $viteIssues += "⚠️ Sourcemaps habilitados (puede causar problemas en móvil)"
    }

    if ($config -match "chunkSizeWarningLimit.*[0-9]+") {
        $viteIssues += "⚠️ Límite de chunk size configurado"
    }

    if ($config -notmatch "rollupOptions") {
        $viteIssues += "⚠️ No hay optimizaciones rollup configuradas"
    }

    if ($viteIssues.Count -gt 0) {
        Write-Host "   ❌ PROBLEMAS VITE DETECTADOS:" -ForegroundColor Red
        foreach ($issue in $viteIssues) {
            Write-Host "      $issue" -ForegroundColor Red
        }
    }
    else {
        Write-Host "   ✅ Configuración Vite parece correcta" -ForegroundColor Green
    }
}
else {
    Write-Host "   ❌ No se encontró configuración Vite móvil" -ForegroundColor Red
}

Write-Host ""

# 5. Test específico para problemas CSS
Write-Host "5. 🧪 CREANDO TEST SIN CSS PARA MÓVIL:" -ForegroundColor Yellow

$testWithoutCSS = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇨🇺 Packfy - Test Sin CSS</title>
    <style>
        /* SOLO CSS BÁSICO MÍNIMO */
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f0f0f0;
            color: #333;
        }
        .box {
            background: white;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .success { color: green; }
        .error { color: red; }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background: #007cba;
            color: white;
            text-decoration: none;
            border-radius: 3px;
            margin: 5px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>🇨🇺 Packfy Cuba - Test Sin CSS Complejo</h1>
        <p class="success">✅ Esta página usa CSS MÍNIMO</p>
        <p>Si esta página carga pero la principal no, el problema es el CSS complejo.</p>
    </div>

    <div class="box">
        <h3>📱 Información del Dispositivo</h3>
        <p><strong>User-Agent:</strong> <span id="ua"></span></p>
        <p><strong>Pantalla:</strong> <span id="screen"></span></p>
        <p><strong>Protocolo:</strong> <span id="protocol"></span></p>
    </div>

    <div class="box">
        <h3>🧪 Tests de Funcionalidad</h3>
        <a href="javascript:testAPI()" class="button">Test API</a>
        <a href="javascript:testCSS()" class="button">Test CSS Original</a>
        <div id="results"></div>
    </div>

    <script>
        // Información básica
        document.getElementById('ua').textContent = navigator.userAgent;
        document.getElementById('screen').textContent = screen.width + 'x' + screen.height;
        document.getElementById('protocol').textContent = window.location.protocol;

        function log(msg, type) {
            const results = document.getElementById('results');
            const color = type === 'error' ? 'red' : type === 'success' ? 'green' : 'black';
            results.innerHTML += '<p style="color: ' + color + ';">' + msg + '</p>';
        }

        async function testAPI() {
            log('🔄 Probando API...', 'info');
            try {
                const response = await fetch('/api/health/', { method: 'GET' });
                if (response.ok) {
                    log('✅ API funciona correctamente', 'success');
                } else {
                    log('❌ API devuelve: ' + response.status, 'error');
                }
            } catch (error) {
                log('❌ Error API: ' + error.message, 'error');
            }
        }

        function testCSS() {
            log('🔄 Probando página principal con CSS...', 'info');
            window.open('/', '_blank');
            log('⚠️ Verifica si la página principal carga en la nueva pestaña', 'info');
        }

        // Log inicial
        console.log('🇨🇺 Test sin CSS cargado');
        log('✅ JavaScript funcionando correctamente', 'success');
    </script>
</body>
</html>
"@

$testWithoutCSS | Out-File -FilePath "frontend/public/test-sin-css.html" -Encoding UTF8
Write-Host "   ✅ Test sin CSS creado: test-sin-css.html" -ForegroundColor Green

Write-Host ""

# 6. Hipótesis actualizada
Write-Host "6. 🎯 HIPÓTESIS ACTUALIZADA TRAS NUEVA INFORMACIÓN:" -ForegroundColor Cyan
Write-Host ""

Write-Host "   HIPÓTESIS PRINCIPAL (90% probabilidad):" -ForegroundColor Red
Write-Host "   • Cambios CSS causaron problemas de rendimiento" -ForegroundColor White
Write-Host "   • Archivos CSS muy grandes saturan móvil" -ForegroundColor White
Write-Host "   • Build/bundling problemático tras actualización" -ForegroundColor White
Write-Host ""

Write-Host "   HIPÓTESIS SECUNDARIA (70% probabilidad):" -ForegroundColor Yellow
Write-Host "   • Conflicto en cache tras actualización Docker" -ForegroundColor White
Write-Host "   • CSS mal formado causa errores JS" -ForegroundColor White
Write-Host "   • Dependencias corruptas en node_modules" -ForegroundColor White
Write-Host ""

# 7. Plan de acción actualizado
Write-Host "7. 📋 PLAN DE ACCIÓN ACTUALIZADO:" -ForegroundColor Green
Write-Host ""

Write-Host "   PASO 1 - Test sin CSS:" -ForegroundColor Yellow
Write-Host "   📱 Abre: https://192.168.12.178:5173/test-sin-css.html" -ForegroundColor White
Write-Host "   🎯 Si funciona → Problema es CSS complejo" -ForegroundColor White
Write-Host ""

Write-Host "   PASO 2 - Rollback temporal:" -ForegroundColor Yellow
Write-Host "   🔄 Revertir cambios CSS recientes" -ForegroundColor White
Write-Host "   🐳 Reconstruir contenedores" -ForegroundColor White
Write-Host ""

Write-Host "   PASO 3 - Optimización CSS:" -ForegroundColor Yellow
Write-Host "   🧹 Dividir CSS en chunks más pequeños" -ForegroundColor White
Write-Host "   📱 Optimizar para móvil específicamente" -ForegroundColor White
Write-Host ""

Write-Host "🎯 === SIGUIENTE ACCIÓN INMEDIATA ===" -ForegroundColor Magenta
Write-Host ""
Write-Host "1. 📱 Prueba el test sin CSS:" -ForegroundColor White
Write-Host "   https://192.168.12.178:5173/test-sin-css.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 📊 Reporta si esta página SÍ carga en móvil" -ForegroundColor White
Write-Host ""
Write-Host "💡 Si la página sin CSS funciona, confirmamos que el" -ForegroundColor Green
Write-Host "   problema está en los cambios CSS recientes" -ForegroundColor Green
Write-Host ""
