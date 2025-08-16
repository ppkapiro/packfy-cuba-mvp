# 🇨🇺 PACKFY CUBA - TEST RÁPIDO SSL vs HTTP
# Verificación inmediata del problema SSL

Write-Host "⚡ === TEST RÁPIDO SSL vs HTTP ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "🎯 VERIFICACIÓN INMEDIATA: ¿Es problema SSL?" -ForegroundColor Yellow
Write-Host ""

# 1. Test directo backend HTTP (puerto 8000)
Write-Host "1. 🔍 TEST BACKEND HTTP DIRECTO:" -ForegroundColor Yellow

try {
    $backendHTTP = curl -k -s -w "Status: %{http_code}\nTime: %{time_total}s\n" "http://192.168.12.178:8000"
    Write-Host "   Backend HTTP (puerto 8000):" -ForegroundColor White
    Write-Host "   $backendHTTP" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Error backend HTTP: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 2. Test directo backend HTTPS (puerto 8443)
Write-Host "2. 🔒 TEST BACKEND HTTPS DIRECTO:" -ForegroundColor Yellow

try {
    $backendHTTPS = curl -k -s -w "Status: %{http_code}\nTime: %{time_total}s\n" "https://192.168.12.178:8443"
    Write-Host "   Backend HTTPS (puerto 8443):" -ForegroundColor White
    Write-Host "   $backendHTTPS" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Error backend HTTPS: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 3. Crear página de test simple sin Docker
Write-Host "3. 📄 CREANDO TEST SIMPLE SIN DOCKER:" -ForegroundColor Yellow

$simpleTest = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇨🇺 Packfy - Test SSL vs HTTP</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #001122;
            color: white;
            text-align: center;
        }
        .test-box {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            border: 2px solid #0066cc;
        }
        .success { color: #00ff00; }
        .error { color: #ff0000; }
        .warning { color: #ff6600; }
        .button {
            display: inline-block;
            padding: 12px 24px;
            margin: 10px;
            background: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover { background: #3385d6; }
        #results { margin-top: 20px; text-align: left; }
    </style>
</head>
<body>
    <h1>🇨🇺 Packfy Cuba - Test SSL vs HTTP</h1>

    <div class="test-box">
        <h3>📱 Información del Móvil</h3>
        <p><strong>Dispositivo:</strong> <span id="device"></span></p>
        <p><strong>Hora:</strong> <span id="time"></span></p>
        <p><strong>Protocolo actual:</strong> <span id="protocol"></span></p>
    </div>

    <div class="test-box">
        <h3>🧪 Tests de Conectividad</h3>
        <button class="button" onclick="testHTTP()">Test HTTP (Puerto 8000)</button>
        <button class="button" onclick="testHTTPS()">Test HTTPS (Puerto 8443)</button>
        <button class="button" onclick="testFrontend()">Test Frontend HTTPS</button>
    </div>

    <div id="results"></div>

    <div class="test-box">
        <h3>💡 Interpretación de Resultados</h3>
        <p><strong>Si HTTP funciona pero HTTPS no:</strong> <span class="warning">Problema SSL confirmado</span></p>
        <p><strong>Si ambos fallan:</strong> <span class="error">Problema de red/conectividad</span></p>
        <p><strong>Si ambos funcionan:</strong> <span class="success">Problema en otra parte</span></p>
    </div>

    <script>
        // Mostrar información inicial
        document.getElementById('device').textContent = navigator.userAgent;
        document.getElementById('time').textContent = new Date().toLocaleString();
        document.getElementById('protocol').textContent = window.location.protocol;

        function log(message, type = 'info') {
            const results = document.getElementById('results');
            const color = type === 'success' ? '#00ff00' : type === 'error' ? '#ff0000' : type === 'warning' ? '#ff6600' : '#ffffff';
            results.innerHTML += '<div style="color: ' + color + '; margin: 5px 0;">' + message + '</div>';
            console.log(message);
        }

        async function testHTTP() {
            log('🔄 Probando HTTP (puerto 8000)...');
            try {
                const response = await fetch('http://192.168.12.178:8000', {
                    method: 'GET',
                    mode: 'no-cors'
                });
                log('✅ HTTP: Conexión exitosa', 'success');
            } catch (error) {
                log('❌ HTTP: Error - ' + error.message, 'error');
            }
        }

        async function testHTTPS() {
            log('🔄 Probando HTTPS (puerto 8443)...');
            try {
                const response = await fetch('https://192.168.12.178:8443', {
                    method: 'GET',
                    mode: 'no-cors'
                });
                log('✅ HTTPS: Conexión exitosa', 'success');
            } catch (error) {
                log('❌ HTTPS: Error - ' + error.message, 'error');
            }
        }

        async function testFrontend() {
            log('🔄 Probando Frontend HTTPS (puerto 5173)...');
            try {
                const response = await fetch('https://192.168.12.178:5173', {
                    method: 'GET',
                    mode: 'no-cors'
                });
                log('✅ Frontend HTTPS: Conexión exitosa', 'success');
            } catch (error) {
                log('❌ Frontend HTTPS: Error - ' + error.message, 'error');
            }
        }

        // Test automático al cargar
        setTimeout(() => {
            log('🚀 Iniciando tests automáticos...');
            testHTTP();
            setTimeout(() => testHTTPS(), 2000);
            setTimeout(() => testFrontend(), 4000);
        }, 1000);
    </script>
</body>
</html>
"@

$simpleTest | Out-File -FilePath "frontend/public/test-ssl-rapido.html" -Encoding UTF8
Write-Host "   ✅ Test rápido creado: test-ssl-rapido.html" -ForegroundColor Green

Write-Host ""
Write-Host "4. 🌐 SIRVIENDO TEST DESDE FRONTEND ACTUAL:" -ForegroundColor Yellow

# Verificar si el frontend actual está funcionando
try {
    $frontendStatus = curl -k -s -w "%{http_code}" "https://192.168.12.178:5173" 2>$null
    if ($frontendStatus -eq "200") {
        Write-Host "   ✅ Frontend actual funcionando (Estado: $frontendStatus)" -ForegroundColor Green
        Write-Host ""
        Write-Host "📱 TEST RÁPIDO DISPONIBLE AHORA:" -ForegroundColor Red
        Write-Host "https://192.168.12.178:5173/test-ssl-rapido.html" -ForegroundColor White
        Write-Host ""
        Write-Host "🧪 ESTE TEST TE DIRÁ INMEDIATAMENTE:" -ForegroundColor Yellow
        Write-Host "• ✅ Si HTTP funciona pero HTTPS no → Problema SSL" -ForegroundColor Green
        Write-Host "• ❌ Si ambos fallan → Problema de red" -ForegroundColor Red
        Write-Host "• ⚠️  Si ambos funcionan → Problema en otra parte" -ForegroundColor Yellow
    }
    else {
        Write-Host "   ❌ Frontend no disponible (Estado: $frontendStatus)" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error verificando frontend" -ForegroundColor Red
}

Write-Host ""
Write-Host "5. 📊 MIENTRAS TANTO - VERIFICACIÓN DESDE PC:" -ForegroundColor Yellow

# Test desde PC para comparar
Write-Host "   🖥️ Resultado desde PC (referencia):" -ForegroundColor White

try {
    $pcHTTP = curl -k -s -w "%{http_code}" "http://192.168.12.178:8000" 2>$null
    $pcHTTPS = curl -k -s -w "%{http_code}" "https://192.168.12.178:8443" 2>$null
    $pcFrontend = curl -k -s -w "%{http_code}" "https://192.168.12.178:5173" 2>$null

    Write-Host "   • HTTP Backend (8000): $pcHTTP" -ForegroundColor $(if ($pcHTTP -eq "200") { "Green" }else { "Red" })
    Write-Host "   • HTTPS Backend (8443): $pcHTTPS" -ForegroundColor $(if ($pcHTTPS -eq "200") { "Green" }else { "Red" })
    Write-Host "   • HTTPS Frontend (5173): $pcFrontend" -ForegroundColor $(if ($pcFrontend -eq "200") { "Green" }else { "Red" })
}
catch {
    Write-Host "   ❌ Error en verificación desde PC" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 === INSTRUCCIONES FINALES ===" -ForegroundColor Red
Write-Host ""
Write-Host "1. 📱 Abre en tu móvil:" -ForegroundColor White
Write-Host "   https://192.168.12.178:5173/test-ssl-rapido.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 📊 El test se ejecutará automáticamente" -ForegroundColor White
Write-Host ""
Write-Host "3. 🎯 Reporta los resultados:" -ForegroundColor White
Write-Host "   • ¿Carga la página?" -ForegroundColor White
Write-Host "   • ¿Qué dicen los tests HTTP/HTTPS?" -ForegroundColor White
Write-Host "   • ¿Hay errores específicos?" -ForegroundColor White
Write-Host ""
Write-Host "💡 ESTO NOS DARÁ LA RESPUESTA DEFINITIVA" -ForegroundColor Green
Write-Host ""
