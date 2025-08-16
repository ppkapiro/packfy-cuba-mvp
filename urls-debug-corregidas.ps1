# 🇨🇺 PACKFY CUBA - URLs Debug Móvil Corregidas
# URLs específicas de debug con IP correcta

$timestamp = Get-Date -Format "yyyyMMddHHmmss"

Write-Host "🔍 === URLS DEBUG MÓVIL CORREGIDAS ===" -ForegroundColor Red
Write-Host ""

Write-Host "📱 URLS DE DEBUG PARA TU MÓVIL:" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔍 PÁGINA DE DEBUG (úsala primero):" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/debug.html?t=$timestamp" -ForegroundColor White
Write-Host ""

Write-Host "🔍 APLICACIÓN PRINCIPAL:" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/?debug=true&t=$timestamp" -ForegroundColor White
Write-Host ""

Write-Host "🔍 URL DE EMERGENCIA:" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/debug.html?emergency=true" -ForegroundColor White
Write-Host ""

# Verificar que el debug.html existe
if (Test-Path "frontend/public/debug.html") {
    Write-Host "✅ Archivo debug.html creado correctamente" -ForegroundColor Green
}
else {
    Write-Host "❌ Creando archivo debug.html..." -ForegroundColor Red

    if (!(Test-Path "frontend/public")) {
        New-Item -ItemType Directory -Path "frontend/public" -Force
    }

    $debugHTML = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>🇨🇺 Debug Móvil - Packfy</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: linear-gradient(135deg, #001122, #003366);
            color: white;
            min-height: 100vh;
            margin: 0;
        }
        .container { max-width: 400px; margin: 0 auto; }
        .success { color: #00ff88; font-weight: bold; }
        .error { color: #ff4444; font-weight: bold; }
        .info { color: #44aaff; }
        .warning { color: #ffaa44; }
        .test-item {
            margin: 15px 0;
            padding: 15px;
            border: 1px solid #444;
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
        }
        button {
            background: #0066cc;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        button:hover { background: #0055aa; }
        a { color: #44aaff; text-decoration: none; }
        a:hover { color: #66ccff; }
        .big-button {
            display: block;
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            font-size: 18px;
            background: #00aa44;
        }
        .big-button:hover { background: #009933; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🇨🇺 Packfy Cuba</h1>
        <h2>Debug Móvil v4.0</h2>

        <div class="test-item">
            <p class="success">✅ Página de debug cargada exitosamente</p>
            <p class="info">Si ves este mensaje, la conexión básica funciona</p>
        </div>

        <div class="test-item">
            <h3>📱 Tu dispositivo:</h3>
            <p id="userAgent" class="info"></p>
            <p id="screenInfo" class="info"></p>
            <p id="timeInfo" class="info"></p>
        </div>

        <div class="test-item">
            <h3>🌐 Test de conectividad:</h3>
            <button onclick="testBackend()">🔧 Test Backend API</button>
            <p id="backendResult" class="info">Clic para probar</p>
        </div>

        <div class="test-item">
            <h3>🚀 Ir a la aplicación:</h3>
            <a href="/?t=$timestamp" class="big-button">🇨🇺 Abrir Packfy Cuba</a>
            <p class="warning">⚠️ Si esto da error HTTP 500, hay un problema en la aplicación principal</p>
        </div>

        <div class="test-item">
            <h3>📊 Información técnica:</h3>
            <p class="info">URL: <span id="currentUrl"></span></p>
            <p class="info">Timestamp: $timestamp</p>
            <p class="info">Servidor: 192.168.12.178:5173</p>
        </div>

        <div class="test-item">
            <h3>🔧 Acciones de emergencia:</h3>
            <button onclick="clearCache()">🧹 Limpiar Cache</button>
            <button onclick="reloadPage()">🔄 Recargar</button>
            <button onclick="testConnection()">📡 Test Conexión</button>
        </div>

        <div class="test-item">
            <h3>📝 Log de pruebas:</h3>
            <div id="logOutput" style="background: #000; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 12px; max-height: 200px; overflow-y: auto;"></div>
        </div>
    </div>

    <script>
        function log(message) {
            const logOutput = document.getElementById('logOutput');
            const timestamp = new Date().toLocaleTimeString();
            logOutput.innerHTML += timestamp + ': ' + message + '<br>';
            logOutput.scrollTop = logOutput.scrollHeight;
            console.log('DEBUG:', message);
        }

        // Información del dispositivo
        document.getElementById('userAgent').textContent = navigator.userAgent;
        document.getElementById('screenInfo').textContent = 'Pantalla: ' + screen.width + 'x' + screen.height + ' (ratio: ' + window.devicePixelRatio + ')';
        document.getElementById('timeInfo').textContent = 'Hora: ' + new Date().toLocaleString();
        document.getElementById('currentUrl').textContent = window.location.href;

        log('🇨🇺 Packfy Cuba Debug iniciado');
        log('Dispositivo: ' + (navigator.userAgent.includes('Mobile') ? 'Móvil' : 'Escritorio'));
        log('Pantalla: ' + screen.width + 'x' + screen.height);

        // Test del backend
        function testBackend() {
            const result = document.getElementById('backendResult');
            result.textContent = '⏳ Probando backend...';
            result.className = 'info';
            log('🔧 Iniciando test de backend...');

            fetch('/api/', {
                method: 'GET',
                cache: 'no-cache'
            })
            .then(response => {
                const status = response.status;
                if (status === 401) {
                    result.textContent = '✅ Backend OK (HTTP 401 - Auth requerida)';
                    result.className = 'success';
                    log('✅ Backend responde correctamente: HTTP ' + status);
                } else {
                    result.textContent = '⚠️ Backend responde: HTTP ' + status;
                    result.className = 'warning';
                    log('⚠️ Backend respuesta inesperada: HTTP ' + status);
                }
            })
            .catch(error => {
                result.textContent = '❌ Error: ' + error.message;
                result.className = 'error';
                log('❌ Error de backend: ' + error.message);
            });
        }

        function clearCache() {
            log('🧹 Intentando limpiar cache...');
            if ('caches' in window) {
                caches.keys().then(function(names) {
                    for (let name of names) {
                        caches.delete(name);
                    }
                    log('🧹 Cache del navegador limpiado');
                });
            }
            location.reload(true);
        }

        function reloadPage() {
            log('🔄 Recargando página...');
            location.reload(true);
        }

        function testConnection() {
            log('📡 Probando conexión...');
            fetch('/', { method: 'HEAD', cache: 'no-cache' })
                .then(() => log('📡 Conexión OK'))
                .catch(error => log('📡 Error de conexión: ' + error.message));
        }

        // Auto-test al cargar
        setTimeout(() => {
            log('🤖 Ejecutando auto-test...');
            testBackend();
        }, 1000);
    </script>
</body>
</html>
"@

    $debugHTML | Out-File -FilePath "frontend/public/debug.html" -Encoding UTF8
    Write-Host "✅ Archivo debug.html creado" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 INSTRUCCIONES PARA TU MÓVIL:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 🧹 Limpia cache del navegador móvil primero" -ForegroundColor Yellow
Write-Host "2. 🔒 Usa modo incógnito/privado" -ForegroundColor Yellow
Write-Host "3. 📱 Abre esta URL de debug:" -ForegroundColor Yellow
Write-Host "   https://192.168.12.178:5173/debug.html?t=$timestamp" -ForegroundColor White
Write-Host ""
Write-Host "4. ✅ Si la página de debug carga:" -ForegroundColor Green
Write-Host "   - Toca 'Test Backend API'" -ForegroundColor White
Write-Host "   - Debe decir 'Backend OK'" -ForegroundColor White
Write-Host "   - Luego toca 'Abrir Packfy Cuba'" -ForegroundColor White
Write-Host ""
Write-Host "5. ❌ Si la página de debug NO carga:" -ForegroundColor Red
Write-Host "   - El problema es de conectividad WiFi" -ForegroundColor White
Write-Host "   - Verifica que estés en la misma red" -ForegroundColor White
Write-Host "   - Prueba con diferentes navegadores" -ForegroundColor White
Write-Host ""

# Verificar servidor
Write-Host "🔍 VERIFICANDO SERVIDOR:" -ForegroundColor Yellow
$serverStatus = curl -k -s -o /dev/null -w "%{http_code}" "https://192.168.12.178:5173/debug.html"
Write-Host "Debug page: HTTP $serverStatus $(if($serverStatus -eq '200') { '✅' } else { '❌' })" -ForegroundColor $(if ($serverStatus -eq '200') { 'Green' } else { 'Red' })

Write-Host ""
Write-Host "🎯 EMPIEZA POR LA PÁGINA DE DEBUG:" -ForegroundColor Red
Write-Host "https://192.168.12.178:5173/debug.html?t=$timestamp" -ForegroundColor White
Write-Host ""
