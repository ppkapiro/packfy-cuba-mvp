# 🇨🇺 PACKFY CUBA - ANÁLISIS ESPECÍFICO LOGIN HTTP 500
# Investigando problema en proceso de autenticación

Write-Host "🔍 === ANÁLISIS ESPECÍFICO LOGIN HTTP 500 ===" -ForegroundColor Red
Write-Host ""

Write-Host "📊 SITUACIÓN ACTUAL:" -ForegroundColor Yellow
Write-Host "• Página principal: CARGA (sin estilos)" -ForegroundColor Green
Write-Host "• Problema específico: LOGIN HTTP 500" -ForegroundColor Red
Write-Host "• Momento del error: Al hacer clic en 'Iniciar sesión'" -ForegroundColor White
Write-Host ""

Write-Host "🔍 INVESTIGANDO ENDPOINTS DE AUTENTICACIÓN:" -ForegroundColor Yellow
Write-Host ""

# 1. Verificar endpoint de login directamente
Write-Host "1. 🔑 PROBANDO ENDPOINT DE LOGIN DIRECTAMENTE:" -ForegroundColor Yellow

$loginEndpoints = @(
    "https://192.168.12.178:8443/api/auth/login/",
    "https://192.168.12.178:8443/api/login/",
    "https://192.168.12.178:8443/api/token/",
    "https://192.168.12.178:8443/api/users/login/"
)

foreach ($endpoint in $loginEndpoints) {
    Write-Host "   🧪 Probando: $endpoint" -ForegroundColor White
    try {
        # Test GET primero
        $getResponse = curl -k -s -w "%{http_code}" "$endpoint" 2>$null
        Write-Host "      GET: $getResponse" -ForegroundColor Gray

        # Test POST con datos de prueba
        $postData = '{"username":"test","password":"test"}'
        $postResponse = curl -k -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d $postData "$endpoint" 2>$null

        if ($postResponse -eq "500") {
            Write-Host "      POST: $postResponse ❌ HTTP 500 DETECTADO" -ForegroundColor Red
        }
        elseif ($postResponse -eq "401" -or $postResponse -eq "400") {
            Write-Host "      POST: $postResponse ✅ Endpoint funciona (credenciales incorrectas)" -ForegroundColor Green
        }
        else {
            Write-Host "      POST: $postResponse ⚠️ Respuesta inesperada" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "      ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# 2. Verificar logs específicos del backend durante login
Write-Host "2. 📋 ANALIZANDO LOGS DEL BACKEND:" -ForegroundColor Yellow

try {
    $backendLogs = docker logs packfy-backend-v4 --tail 50

    # Buscar errores relacionados con autenticación
    $authErrors = $backendLogs | Where-Object {
        $_ -match "login|auth|token|500|error|Error|ERROR|exception|Exception|traceback|Traceback"
    }

    if ($authErrors) {
        Write-Host "   ❌ ERRORES DE AUTENTICACIÓN DETECTADOS:" -ForegroundColor Red
        foreach ($authError in $authErrors) {
            Write-Host "      🔴 $authError" -ForegroundColor Red
        }
    }
    else {
        Write-Host "   ✅ No hay errores evidentes en logs de backend" -ForegroundColor Green
    }
}
catch {
    Write-Host "   ❌ Error obteniendo logs: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 3. Verificar configuración de autenticación en Django
Write-Host "3. ⚙️ VERIFICANDO CONFIGURACIÓN DJANGO:" -ForegroundColor Yellow

$settingsFile = "backend/config/settings_development.py"
if (Test-Path $settingsFile) {
    $settings = Get-Content $settingsFile -Raw

    Write-Host "   📄 Verificando configuraciones críticas:" -ForegroundColor White

    # Verificar REST_FRAMEWORK
    if ($settings -match "REST_FRAMEWORK") {
        Write-Host "      ✅ REST_FRAMEWORK configurado" -ForegroundColor Green
    }
    else {
        Write-Host "      ❌ REST_FRAMEWORK no encontrado" -ForegroundColor Red
    }

    # Verificar JWT
    if ($settings -match "JWT|SimpleJWT") {
        Write-Host "      ✅ JWT configurado" -ForegroundColor Green
    }
    else {
        Write-Host "      ❌ JWT no configurado" -ForegroundColor Red
    }

    # Verificar CORS
    if ($settings -match "CORS") {
        Write-Host "      ✅ CORS configurado" -ForegroundColor Green
    }
    else {
        Write-Host "      ❌ CORS no configurado" -ForegroundColor Red
    }
}
else {
    Write-Host "   ❌ No se encontró archivo de configuración Django" -ForegroundColor Red
}

Write-Host ""

# 4. Crear test específico de login para móvil
Write-Host "4. 🧪 CREANDO TEST ESPECÍFICO DE LOGIN:" -ForegroundColor Yellow

$loginTest = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇨🇺 Packfy - Test Login HTTP 500</title>
    <style>
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
        .error { color: red; font-weight: bold; }
        .success { color: green; font-weight: bold; }
        .warning { color: orange; font-weight: bold; }
        input, button {
            display: block;
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 3px;
        }
        button {
            background: #007cba;
            color: white;
            cursor: pointer;
        }
        #log {
            background: #f8f8f8;
            padding: 10px;
            border: 1px solid #ddd;
            max-height: 300px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>🇨🇺 Packfy Cuba - Test Login HTTP 500</h1>
        <p class="warning">Diagnóstico específico del problema de login</p>
    </div>

    <div class="box">
        <h3>🔑 Test de Login</h3>
        <input type="text" id="username" placeholder="Usuario (ej: admin@packfy.cu)" value="admin@packfy.cu">
        <input type="password" id="password" placeholder="Contraseña" value="admin123">
        <button onclick="testLogin()">🧪 Test Login</button>
        <button onclick="testEndpoints()">🔍 Test Todos los Endpoints</button>
        <button onclick="clearLog()">🧹 Limpiar Log</button>
    </div>

    <div class="box">
        <h3>📊 Resultados del Test:</h3>
        <div id="log"></div>
    </div>

    <script>
        function log(message, type = 'info') {
            const logDiv = document.getElementById('log');
            const timestamp = new Date().toLocaleTimeString();
            const color = type === 'error' ? 'red' : type === 'success' ? 'green' : type === 'warning' ? 'orange' : 'black';

            logDiv.innerHTML += '<div style="color: ' + color + ';">' + timestamp + ' - ' + message + '</div>';
            logDiv.scrollTop = logDiv.scrollHeight;
            console.log(message);
        }

        function clearLog() {
            document.getElementById('log').innerHTML = '';
        }

        async function testLogin() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            log('🔄 Iniciando test de login...', 'info');
            log('Usuario: ' + username, 'info');

            const endpoints = [
                '/api/auth/login/',
                '/api/login/',
                '/api/token/',
                '/api/users/login/',
                '/api/auth/token/'
            ];

            for (let endpoint of endpoints) {
                await testSingleEndpoint(endpoint, username, password);
                await new Promise(resolve => setTimeout(resolve, 1000)); // Esperar 1 segundo entre tests
            }
        }

        async function testSingleEndpoint(endpoint, username, password) {
            log('📡 Probando endpoint: ' + endpoint, 'info');

            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password,
                        email: username // Por si usa email en lugar de username
                    })
                });

                const status = response.status;
                log('📊 Respuesta HTTP: ' + status, status === 500 ? 'error' : status === 200 ? 'success' : 'warning');

                if (status === 500) {
                    log('❌ HTTP 500 DETECTADO en ' + endpoint, 'error');

                    // Intentar obtener detalles del error
                    try {
                        const errorText = await response.text();
                        if (errorText) {
                            log('🔍 Error details: ' + errorText.substring(0, 200) + '...', 'error');
                        }
                    } catch (e) {
                        log('⚠️ No se pudo obtener detalles del error', 'warning');
                    }
                } else if (status === 200) {
                    log('✅ Login exitoso en ' + endpoint, 'success');
                    const data = await response.json();
                    log('📄 Response: ' + JSON.stringify(data).substring(0, 100) + '...', 'success');
                } else if (status === 401) {
                    log('🔑 Credenciales incorrectas en ' + endpoint + ' (pero endpoint funciona)', 'warning');
                } else if (status === 400) {
                    log('📝 Datos mal formados en ' + endpoint + ' (pero endpoint funciona)', 'warning');
                } else if (status === 404) {
                    log('❓ Endpoint no existe: ' + endpoint, 'warning');
                } else {
                    log('⚠️ Respuesta inesperada: ' + status + ' en ' + endpoint, 'warning');
                }

            } catch (error) {
                log('❌ Error de red: ' + error.message + ' en ' + endpoint, 'error');
            }
        }

        async function testEndpoints() {
            log('🔄 Probando todos los endpoints de autenticación...', 'info');

            const endpoints = [
                '/api/',
                '/api/health/',
                '/api/auth/',
                '/api/auth/login/',
                '/api/users/',
                '/api/token/',
                '/admin/'
            ];

            for (let endpoint of endpoints) {
                try {
                    const response = await fetch(endpoint, { method: 'GET' });
                    const status = response.status;
                    log('GET ' + endpoint + ': ' + status, status >= 400 ? 'error' : 'success');
                } catch (error) {
                    log('❌ Error GET ' + endpoint + ': ' + error.message, 'error');
                }
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }

        // Auto-test al cargar
        log('🇨🇺 Test de login iniciado', 'info');
        log('📱 Dispositivo: ' + navigator.userAgent, 'info');
        log('💡 Haz clic en "Test Login" para diagnosticar el problema HTTP 500', 'info');
    </script>
</body>
</html>
"@

$loginTest | Out-File -FilePath "frontend/public/test-login-debug.html" -Encoding UTF8
Write-Host "   ✅ Test de login creado: test-login-debug.html" -ForegroundColor Green

Write-Host ""

# 5. Verificar variables de entorno del backend
Write-Host "5. 🌐 VERIFICANDO VARIABLES DE ENTORNO:" -ForegroundColor Yellow

try {
    $envVars = docker exec packfy-backend-v4 env | Where-Object { $_ -match "DJANGO|SECRET|DEBUG|ALLOWED|CORS" }

    if ($envVars) {
        Write-Host "   📋 Variables de entorno críticas:" -ForegroundColor White
        foreach ($envVar in $envVars) {
            if ($envVar -match "SECRET") {
                Write-Host "      🔑 SECRET_KEY: [CONFIGURADA]" -ForegroundColor Green
            }
            else {
                Write-Host "      📄 $envVar" -ForegroundColor Gray
            }
        }
    }
    else {
        Write-Host "   ❌ No se encontraron variables de entorno Django" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error obteniendo variables de entorno: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 6. Verificar base de datos
Write-Host "6. 🗄️ VERIFICANDO CONEXIÓN A BASE DE DATOS:" -ForegroundColor Yellow

try {
    $dbCheck = docker exec packfy-backend-v4 python manage.py check --database default
    if ($dbCheck -match "System check identified no issues") {
        Write-Host "   ✅ Base de datos conectada correctamente" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Problemas con base de datos detectados:" -ForegroundColor Red
        Write-Host "      $dbCheck" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error verificando base de datos: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "🎯 === PRÓXIMOS PASOS PARA DIAGNÓSTICO ===" -ForegroundColor Magenta
Write-Host ""

Write-Host "📱 ABRE EN TU MÓVIL:" -ForegroundColor Red
Write-Host "https://192.168.12.178:5173/test-login-debug.html" -ForegroundColor Cyan
Write-Host ""

Write-Host "🧪 ESTE TEST TE DIRÁ:" -ForegroundColor Yellow
Write-Host "• ✅ Qué endpoints de login existen" -ForegroundColor White
Write-Host "• ❌ Cuál específicamente da HTTP 500" -ForegroundColor White
Write-Host "• 🔍 Detalles del error exacto" -ForegroundColor White
Write-Host ""

Write-Host "📊 BASADO EN LOS RESULTADOS:" -ForegroundColor Green
Write-Host "• Si /api/auth/login/ da 500 → Problema en Django REST Framework" -ForegroundColor White
Write-Host "• Si /api/token/ da 500 → Problema en JWT" -ForegroundColor White
Write-Host "• Si todos dan 500 → Problema en configuración Django" -ForegroundColor White
Write-Host ""

Write-Host "💡 Una vez que sepamos el endpoint exacto que falla," -ForegroundColor Green
Write-Host "   podré arreglar el problema específico." -ForegroundColor Green
Write-Host ""
