# 🇨🇺 PACKFY CUBA - Diagnóstico Automático Móvil
# Simulamos el comportamiento del móvil desde la PC

Write-Host "🔍 === DIAGNÓSTICO AUTOMÁTICO MÓVIL ===" -ForegroundColor Cyan
Write-Host ""

# 1. Simulando User-Agent de móvil
Write-Host "1. 📱 SIMULANDO NAVEGADOR MÓVIL DESDE PC:" -ForegroundColor Yellow

$mobileUserAgents = @(
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
)

foreach ($userAgent in $mobileUserAgents) {
    $deviceType = if ($userAgent -match "iPhone") { "📱 iPhone" } elseif ($userAgent -match "Android") { "🤖 Android" } else { "📱 Móvil" }

    Write-Host "   Testing $deviceType..." -ForegroundColor White

    try {
        $response = curl -k -s -w "%{http_code}|%{time_total}|%{size_download}" -H "User-Agent: $userAgent" "https://192.168.12.178:5173"
        $parts = $response -split '\|'
        $statusCode = $parts[-3]
        $time = $parts[-2]
        $size = $parts[-1]

        $status = if ($statusCode -eq "200") { "✅ OK" } elseif ($statusCode -eq "500") { "❌ HTTP 500" } else { "⚠️ HTTP $statusCode" }
        Write-Host "     $status (${time}s, ${size} bytes)" -ForegroundColor $(if ($statusCode -eq "200") { "Green" } elseif ($statusCode -eq "500") { "Red" } else { "Yellow" })

        if ($statusCode -eq "500") {
            Write-Host "     🔍 ENCONTRADO HTTP 500 CON $deviceType" -ForegroundColor Red

            # Obtener detalles del error 500
            $errorDetails = curl -k -s -H "User-Agent: $userAgent" "https://192.168.12.178:5173"
            if ($errorDetails -match "DisallowedHost|ALLOWED_HOSTS") {
                Write-Host "     🎯 Error: ALLOWED_HOSTS" -ForegroundColor Red
            }
            elseif ($errorDetails -match "Certificate|SSL|TLS") {
                Write-Host "     🎯 Error: Certificado SSL" -ForegroundColor Red
            }
            elseif ($errorDetails -match "CORS") {
                Write-Host "     🎯 Error: CORS" -ForegroundColor Red
            }
            else {
                Write-Host "     🎯 Error: Desconocido" -ForegroundColor Red
            }
        }
    }
    catch {
        Write-Host "     ❌ Error de conexión: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# 2. Verificar logs del servidor en tiempo real
Write-Host "2. 📊 VERIFICANDO LOGS DEL SERVIDOR:" -ForegroundColor Yellow

Write-Host "   • Logs recientes del frontend..." -ForegroundColor White
$frontendLogs = docker-compose logs frontend --tail=5 2>$null
if ($frontendLogs -match "error|Error|ERROR") {
    Write-Host "     ❌ Errores encontrados en frontend:" -ForegroundColor Red
    $frontendLogs | Select-String -Pattern "error|Error|ERROR" | ForEach-Object {
        Write-Host "       $_" -ForegroundColor Red
    }
}
else {
    Write-Host "     ✅ Frontend sin errores críticos" -ForegroundColor Green
}

Write-Host "   • Logs recientes del backend..." -ForegroundColor White
$backendLogs = docker-compose logs backend --tail=5 2>$null
if ($backendLogs -match "error|Error|ERROR|DisallowedHost|500") {
    Write-Host "     ❌ Errores encontrados en backend:" -ForegroundColor Red
    $backendLogs | Select-String -Pattern "error|Error|ERROR|DisallowedHost|500" | ForEach-Object {
        Write-Host "       $_" -ForegroundColor Red
    }
}
else {
    Write-Host "     ✅ Backend sin errores críticos" -ForegroundColor Green
}

Write-Host ""

# 3. Verificar configuraciones específicas para móvil
Write-Host "3. ⚙️ VERIFICANDO CONFIGURACIONES MÓVIL:" -ForegroundColor Yellow

# Verificar vite.config.mobile.ts
Write-Host "   • Configuración Vite móvil..." -ForegroundColor White
if (Test-Path "frontend/vite.config.mobile.ts") {
    $viteConfig = Get-Content "frontend/vite.config.mobile.ts" -Raw
    if ($viteConfig -match "192\.168\.12\.178") {
        Write-Host "     ✅ IP móvil configurada en Vite" -ForegroundColor Green
    }
    else {
        Write-Host "     ❌ IP móvil NO configurada en Vite" -ForegroundColor Red
    }

    if ($viteConfig -match "localhost\.crt") {
        Write-Host "     ✅ Certificados configurados en Vite" -ForegroundColor Green
    }
    else {
        Write-Host "     ❌ Certificados NO configurados en Vite" -ForegroundColor Red
    }
}
else {
    Write-Host "     ❌ Archivo vite.config.mobile.ts no encontrado" -ForegroundColor Red
}

# Verificar settings de Django
Write-Host "   • Configuración Django..." -ForegroundColor White
$djangoSettings = Get-Content "backend/config/settings_development.py" -Raw 2>$null
if ($djangoSettings -match "192\.168\.12\.178") {
    Write-Host "     ✅ IP móvil en ALLOWED_HOSTS" -ForegroundColor Green
}
else {
    Write-Host "     ❌ IP móvil NO en ALLOWED_HOSTS" -ForegroundColor Red
}

Write-Host ""

# 4. Test directo con headers móviles específicos
Write-Host "4. 🧪 TEST DIRECTO CON HEADERS MÓVILES:" -ForegroundColor Yellow

$mobileHeaders = @{
    "User-Agent"                = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
    "Accept"                    = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    "Accept-Language"           = "es-ES,es;q=0.9,en;q=0.8"
    "Accept-Encoding"           = "gzip, deflate, br"
    "Connection"                = "keep-alive"
    "Upgrade-Insecure-Requests" = "1"
}

Write-Host "   • Simulando petición móvil exacta..." -ForegroundColor White

try {
    # Crear archivo temporal para headers
    $headerFile = "temp_headers.txt"
    $mobileHeaders.GetEnumerator() | ForEach-Object {
        "$($_.Key): $($_.Value)" | Out-File -FilePath $headerFile -Append -Encoding UTF8
    }

    $mobileResponse = curl -k -s -w "STATUS:%{http_code}|TIME:%{time_total}|SIZE:%{size_download}" -H "@$headerFile" "https://192.168.12.178:5173"

    if ($mobileResponse -match "STATUS:(\d+)") {
        $statusCode = $matches[1]
        if ($statusCode -eq "500") {
            Write-Host "     ❌ CONFIRMADO: HTTP 500 con headers móviles" -ForegroundColor Red

            # Obtener el contenido del error
            $errorContent = curl -k -s -H "@$headerFile" "https://192.168.12.178:5173" 2>$null

            # Analizar el tipo de error
            if ($errorContent -match "DisallowedHost") {
                Write-Host "     🎯 CAUSA: DisallowedHost - Problema de ALLOWED_HOSTS" -ForegroundColor Red
                Write-Host "     💡 SOLUCIÓN: Actualizar ALLOWED_HOSTS en Django" -ForegroundColor Yellow
            }
            elseif ($errorContent -match "ssl|SSL|certificate") {
                Write-Host "     🎯 CAUSA: Problema de certificado SSL" -ForegroundColor Red
                Write-Host "     💡 SOLUCIÓN: Regenerar certificados" -ForegroundColor Yellow
            }
            elseif ($errorContent -match "CORS") {
                Write-Host "     🎯 CAUSA: Problema de CORS" -ForegroundColor Red
                Write-Host "     💡 SOLUCIÓN: Actualizar configuración CORS" -ForegroundColor Yellow
            }
            else {
                Write-Host "     🎯 CAUSA: Error desconocido" -ForegroundColor Red
                # Guardar error para análisis
                $errorContent | Out-File -FilePath "error_movil_500.html" -Encoding UTF8
                Write-Host "     📄 Error guardado en: error_movil_500.html" -ForegroundColor Cyan
            }
        }
        else {
            Write-Host "     ✅ OK: HTTP $statusCode con headers móviles" -ForegroundColor Green
        }
    }

    Remove-Item $headerFile -Force 2>$null
}
catch {
    Write-Host "     ❌ Error en test móvil: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 5. Monitoreo en tiempo real
Write-Host "5. 📡 INICIANDO MONITOREO EN TIEMPO REAL:" -ForegroundColor Yellow
Write-Host "   Presiona Ctrl+C para parar el monitoreo" -ForegroundColor Gray
Write-Host ""

for ($i = 1; $i -le 5; $i++) {
    Write-Host "   Monitor #$i - $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray

    # Test rápido
    $quickTest = curl -k -s -w "%{http_code}" -H "User-Agent: Mozilla/5.0 (iPhone)" "https://192.168.12.178:5173" 2>$null
    $statusIcon = if ($quickTest -eq "200") { "✅" } elseif ($quickTest -eq "500") { "❌" } else { "⚠️" }

    Write-Host "     Frontend: HTTP $quickTest $statusIcon" -ForegroundColor $(if ($quickTest -eq "200") { "Green" } elseif ($quickTest -eq "500") { "Red" } else { "Yellow" })

    Start-Sleep 2
}

Write-Host ""
Write-Host "🎯 === RESUMEN DEL DIAGNÓSTICO ===" -ForegroundColor Magenta
Write-Host ""

# Verificar si encontramos el problema
if (Test-Path "error_movil_500.html") {
    Write-Host "❌ HTTP 500 CONFIRMADO - Error guardado en error_movil_500.html" -ForegroundColor Red
    Write-Host "🔍 Revisa el archivo para ver el error exacto" -ForegroundColor Yellow
}
else {
    Write-Host "✅ No se detectó HTTP 500 desde PC" -ForegroundColor Green
    Write-Host "💡 El problema podría ser específico del móvil o la red" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. Revisar el archivo error_movil_500.html si existe" -ForegroundColor White
Write-Host "2. Verificar configuración de red móvil" -ForegroundColor White
Write-Host "3. Aplicar solución específica basada en el error encontrado" -ForegroundColor White
Write-Host ""
