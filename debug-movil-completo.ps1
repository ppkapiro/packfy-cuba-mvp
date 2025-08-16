# 🇨🇺 PACKFY CUBA - Modo Debug Móvil v4.0
# Depuración específica para resolver el HTTP 500 en móvil

Write-Host "🔍 === MODO DEBUG MÓVIL ACTIVADO ===" -ForegroundColor Red
Write-Host ""

# 1. Verificar todas las IPs posibles
Write-Host "1. 🌐 VERIFICANDO TODAS LAS IPs DISPONIBLES:" -ForegroundColor Yellow

$ipConfig = ipconfig | Select-String -Pattern "IPv4.*192\.168\."
if ($ipConfig) {
    $currentIP = ($ipConfig -split ":")[1].Trim()
    Write-Host "   IP actual detectada: $currentIP" -ForegroundColor Cyan
}
else {
    $currentIP = "192.168.12.178"
    Write-Host "   Usando IP por defecto: $currentIP" -ForegroundColor Yellow
}

Write-Host ""

# 2. Test desde diferentes puertos y protocolos
Write-Host "2. 🧪 TESTING MÚLTIPLES CONFIGURACIONES:" -ForegroundColor Yellow

Write-Host "   🔒 HTTPS:" -ForegroundColor Cyan
$httpsStatus = curl -k -s -o /dev/null -w "%{http_code}" "https://$currentIP:5173"
Write-Host "     https://$currentIP:5173 → HTTP $httpsStatus" -ForegroundColor $(if ($httpsStatus -eq "200") { "Green" } else { "Red" })

Write-Host "   🔓 HTTP:" -ForegroundColor Cyan
$httpStatus = curl -s -o /dev/null -w "%{http_code}" "http://$currentIP:5173" 2>$null
Write-Host "     http://$currentIP:5173 → HTTP $httpStatus" -ForegroundColor $(if ($httpStatus -eq "200") { "Green" } else { "Red" })

Write-Host "   🐳 Docker IP:" -ForegroundColor Cyan
$dockerIP = docker inspect packfy-frontend-mobile-v4.0 | ConvertFrom-Json | Select-Object -ExpandProperty NetworkSettings | Select-Object -ExpandProperty Networks | Select-Object -First 1 -ExpandProperty IPAddress
if ($dockerIP) {
    $dockerStatus = curl -k -s -o /dev/null -w "%{http_code}" "https://$dockerIP:5173" 2>$null
    Write-Host "     https://$dockerIP:5173 → HTTP $dockerStatus" -ForegroundColor $(if ($dockerStatus -eq "200") { "Green" } else { "Red" })
}

Write-Host ""

# 3. Crear página de debug simple
Write-Host "3. 📄 CREANDO PÁGINA DE DEBUG SIMPLE:" -ForegroundColor Yellow

$debugHTML = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>🇨🇺 Packfy Cuba - Debug Móvil</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #001122; color: white; }
        .success { color: #00ff00; }
        .error { color: #ff0000; }
        .info { color: #0099ff; }
        .container { max-width: 400px; margin: 0 auto; }
        .test-item { margin: 10px 0; padding: 10px; border: 1px solid #333; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🇨🇺 Packfy Cuba - Debug Móvil</h1>
        <p class="success">✅ Página de debug cargada exitosamente</p>

        <div class="test-item">
            <h3>📱 Información del dispositivo:</h3>
            <p id="userAgent" class="info"></p>
            <p id="screenInfo" class="info"></p>
            <p id="connectionInfo" class="info"></p>
        </div>

        <div class="test-item">
            <h3>🌐 Test de conectividad:</h3>
            <button onclick="testBackend()" style="padding: 10px; margin: 5px;">Test Backend</button>
            <p id="backendResult"></p>
        </div>

        <div class="test-item">
            <h3>📍 URLs disponibles:</h3>
            <p><a href="/" style="color: #00ff00;">Aplicación principal</a></p>
            <p><a href="/?debug=true" style="color: #0099ff;">Aplicación con debug</a></p>
        </div>

        <div class="test-item">
            <h3>🔧 Información técnica:</h3>
            <p>Timestamp: <span id="timestamp" class="info"></span></p>
            <p>URL actual: <span id="currentUrl" class="info"></span></p>
        </div>
    </div>

    <script>
        // Mostrar información del dispositivo
        document.getElementById('userAgent').textContent = 'User Agent: ' + navigator.userAgent;
        document.getElementById('screenInfo').textContent = 'Pantalla: ' + screen.width + 'x' + screen.height;
        document.getElementById('currentUrl').textContent = window.location.href;
        document.getElementById('timestamp').textContent = new Date().toISOString();

        // Información de conexión
        if (navigator.connection) {
            document.getElementById('connectionInfo').textContent = 'Conexión: ' + navigator.connection.effectiveType;
        } else {
            document.getElementById('connectionInfo').textContent = 'Info de conexión no disponible';
        }

        // Test del backend
        function testBackend() {
            const result = document.getElementById('backendResult');
            result.textContent = 'Probando backend...';
            result.className = 'info';

            fetch('/api/')
                .then(response => {
                    result.textContent = 'Backend responde: HTTP ' + response.status;
                    result.className = response.status === 401 ? 'success' : 'error';
                })
                .catch(error => {
                    result.textContent = 'Error: ' + error.message;
                    result.className = 'error';
                });
        }

        console.log('🇨🇺 Packfy Cuba Debug - Página cargada');
        console.log('Dispositivo:', navigator.userAgent);
        console.log('URL:', window.location.href);
    </script>
</body>
</html>
"@

$debugHTML | Out-File -FilePath "frontend/public/debug.html" -Encoding UTF8
Write-Host "   ✅ Página de debug creada en: /debug.html" -ForegroundColor Green

Write-Host ""

# 4. URLs de debug para móvil
Write-Host "4. 📱 URLS DE DEBUG PARA TU MÓVIL:" -ForegroundColor Red
Write-Host ""

$timestamp = Get-Date -Format "yyyyMMddHHmmss"

Write-Host "🔍 URL DE DEBUG PRINCIPAL:" -ForegroundColor Yellow
Write-Host "https://$currentIP:5173/debug.html?t=$timestamp" -ForegroundColor White
Write-Host ""

Write-Host "🔍 URL ALTERNATIVA:" -ForegroundColor Yellow
Write-Host "https://$currentIP:5173/debug.html" -ForegroundColor White
Write-Host ""

Write-Host "🔍 URL CON FORZADO DE RECARGA:" -ForegroundColor Yellow
Write-Host "https://$currentIP:5173/debug.html?nocache=true&v=$timestamp" -ForegroundColor White
Write-Host ""

# 5. Instrucciones específicas
Write-Host "5. 📋 INSTRUCCIONES PARA DEBUG EN MÓVIL:" -ForegroundColor Red
Write-Host ""

Write-Host "✅ PASO 1: Prueba la página de debug primero" -ForegroundColor Green
Write-Host "   URL: https://$currentIP:5173/debug.html?t=$timestamp" -ForegroundColor Cyan
Write-Host "   Esta página es más simple y debería cargar sin problemas" -ForegroundColor White
Write-Host ""

Write-Host "✅ PASO 2: Si la página de debug carga:" -ForegroundColor Green
Write-Host "   - Toca el botón 'Test Backend'" -ForegroundColor White
Write-Host "   - Verifica que diga 'Backend responde: HTTP 401'" -ForegroundColor White
Write-Host "   - Luego ve a la aplicación principal" -ForegroundColor White
Write-Host ""

Write-Host "❌ PASO 3: Si la página de debug NO carga:" -ForegroundColor Red
Write-Host "   - El problema es de conectividad de red" -ForegroundColor White
Write-Host "   - Verifica que estés en la misma WiFi" -ForegroundColor White
Write-Host "   - Prueba reiniciar tu router WiFi" -ForegroundColor White
Write-Host ""

# 6. Reiniciar frontend para aplicar debug
Write-Host "6. 🔄 APLICANDO MODO DEBUG..." -ForegroundColor Yellow
docker-compose restart frontend

Write-Host ""
Write-Host "🎯 === MODO DEBUG ACTIVADO ===" -ForegroundColor Green
Write-Host ""
Write-Host "📱 PRUEBA AHORA EN TU MÓVIL:" -ForegroundColor Cyan
Write-Host "https://$currentIP:5173/debug.html?t=$timestamp" -ForegroundColor White
Write-Host ""
Write-Host "📊 Esta página te dirá exactamente qué está fallando" -ForegroundColor Yellow
Write-Host ""
