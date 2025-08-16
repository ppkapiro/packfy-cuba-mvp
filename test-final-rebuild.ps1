# 🇨🇺 PACKFY CUBA - TEST FINAL DESPUÉS DEL REBUILD
# Verificación completa del arreglo HTTP 500 login

Write-Host "🧪 === TEST FINAL DESPUÉS DEL REBUILD ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 VERIFICANDO ESTADO DE LOS CONTENEDORES:" -ForegroundColor Yellow
try {
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    Write-Host $containers -ForegroundColor White

    # Verificar específicamente que backend esté healthy
    $backendStatus = docker ps --filter "name=packfy-backend-v4" --format "{{.Status}}"
    if ($backendStatus -match "healthy") {
        Write-Host "✅ Backend está healthy" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️ Backend status: $backendStatus" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Error verificando contenedores: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "🔍 PROBANDO ENDPOINTS DESPUÉS DEL REBUILD:" -ForegroundColor Yellow
Write-Host ""

# Test 1: Backend general
Write-Host "1️⃣ Backend general:" -ForegroundColor White
try {
    $backendResponse = curl -k -s -w "%{http_code}" "https://192.168.12.178:8443/" 2>$null
    if ($backendResponse -eq "302") {
        Write-Host "   ✅ Backend: HTTP 302 (redirecto normal)" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️ Backend: $backendResponse" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Login con email (formato correcto)
Write-Host "2️⃣ Login con email:" -ForegroundColor White
try {
    $emailLogin = curl -k -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"email":"admin@packfy.cu","password":"admin123"}' "https://192.168.12.178:8443/api/auth/login/" 2>$null

    if ($emailLogin -match "200") {
        Write-Host "   ✅ Login email: HTTP 200 (EXITOSO)" -ForegroundColor Green
    }
    elseif ($emailLogin -match "401") {
        Write-Host "   ✅ Login email: HTTP 401 (Credenciales incorrectas - endpoint funciona)" -ForegroundColor Green
    }
    elseif ($emailLogin -match "500") {
        Write-Host "   ❌ Login email: HTTP 500 (PROBLEMA PERSISTE)" -ForegroundColor Red
    }
    else {
        Write-Host "   ⚠️ Login email: $emailLogin" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Login con username (formato arreglado)
Write-Host "3️⃣ Login con username:" -ForegroundColor White
try {
    $usernameLogin = curl -k -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"username":"admin@packfy.cu","password":"admin123"}' "https://192.168.12.178:8443/api/auth/login/" 2>$null

    if ($usernameLogin -match "200") {
        Write-Host "   ✅ Login username: HTTP 200 (EXITOSO)" -ForegroundColor Green
    }
    elseif ($usernameLogin -match "401") {
        Write-Host "   ✅ Login username: HTTP 401 (Credenciales incorrectas - endpoint funciona)" -ForegroundColor Green
    }
    elseif ($usernameLogin -match "500") {
        Write-Host "   ❌ Login username: HTTP 500 (PROBLEMA PERSISTE)" -ForegroundColor Red
    }
    else {
        Write-Host "   ⚠️ Login username: $usernameLogin" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $(_Exception.Message)" -ForegroundColor Red
}

# Test 4: Frontend
Write-Host "4️⃣ Frontend principal:" -ForegroundColor White
try {
    $frontendResponse = curl -k -s -w "%{http_code}" "https://192.168.12.178:5173/" 2>$null
    if ($frontendResponse -eq "200") {
        Write-Host "   ✅ Frontend: HTTP 200" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️ Frontend: $frontendResponse" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Archivo de test nuevo
Write-Host "5️⃣ Test de login arreglado:" -ForegroundColor White
try {
    $testLoginResponse = curl -k -s -w "%{http_code}" "https://192.168.12.178:5173/login-arreglado.html" 2>$null
    if ($testLoginResponse -eq "200") {
        Write-Host "   ✅ login-arreglado.html: HTTP 200" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️ login-arreglado.html: $testLoginResponse" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "🔍 VERIFICANDO LOGS DEL BACKEND:" -ForegroundColor Yellow
try {
    $recentLogs = docker logs packfy-backend-v4 --tail 20

    # Buscar errores específicos de login
    $loginErrors = $recentLogs | Where-Object {
        $_ -match "login|auth|500|ERROR"
    }

    if ($loginErrors) {
        Write-Host "   📋 Logs relevantes de login:" -ForegroundColor White
        foreach ($log in $loginErrors[-5..-1]) {
            # Últimos 5
            if ($log -match "ERROR|500") {
                Write-Host "      🔴 $log" -ForegroundColor Red
            }
            else {
                Write-Host "      📄 $log" -ForegroundColor Gray
            }
        }
    }
    else {
        Write-Host "   ✅ No hay errores de login en logs recientes" -ForegroundColor Green
    }
}
catch {
    Write-Host "   ❌ Error obteniendo logs: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "📱 === RESULTADO FINAL ===" -ForegroundColor Magenta
Write-Host ""

# Crear un resumen de resultados
$testResults = @()
if ($emailLogin -match "200|401") { $testResults += "✅ Email login funciona" }
else { $testResults += "❌ Email login falla" }

if ($usernameLogin -match "200|401") { $testResults += "✅ Username login funciona" }
else { $testResults += "❌ Username login falla" }

if ($frontendResponse -eq "200") { $testResults += "✅ Frontend carga" }
else { $testResults += "❌ Frontend falla" }

foreach ($result in $testResults) {
    Write-Host $result -ForegroundColor $(if ($result -match "✅") { "Green" } else { "Red" })
}

Write-Host ""

if ($emailLogin -match "200|401" -and $usernameLogin -match "200|401") {
    Write-Host "🎉 ARREGLO EXITOSO: El problema HTTP 500 del login está SOLUCIONADO" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 PRUEBA EN TU MÓVIL:" -ForegroundColor Cyan
    Write-Host "https://192.168.12.178:5173/login-arreglado.html" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Deberías poder iniciar sesión sin errores HTTP 500" -ForegroundColor White
}
else {
    Write-Host "⚠️ Hay problemas que requieren atención adicional" -ForegroundColor Yellow
    Write-Host "Revisa los logs y resultados arriba para más detalles" -ForegroundColor White
}

Write-Host ""
