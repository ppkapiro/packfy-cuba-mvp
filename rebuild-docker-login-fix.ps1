# 🇨🇺 PACKFY CUBA - REBUILD DOCKER PARA APLICAR ARREGLO LOGIN
# Reconstrucción completa de contenedores con cambios del arreglo HTTP 500

Write-Host "🐳 === REBUILD DOCKER PARA ARREGLO LOGIN ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "📝 CAMBIOS APLICADOS QUE NECESITAN REBUILD:" -ForegroundColor Yellow
Write-Host "• ✅ auth_views.py modificado para aceptar email/username" -ForegroundColor Green
Write-Host "• ✅ login-arreglado.html creado para test final" -ForegroundColor Green
Write-Host "• ⚠️ Contenedores Docker NO actualizados" -ForegroundColor Red
Write-Host ""

Write-Host "🔄 DETENIENDO CONTENEDORES ACTUALES..." -ForegroundColor Yellow
try {
    docker-compose down
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Contenedores detenidos exitosamente" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️ Error deteniendo contenedores (continuando...)" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "⚠️ Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

Write-Host "🧹 LIMPIANDO CACHE DOCKER..." -ForegroundColor Yellow
try {
    # Limpiar imágenes no utilizadas y cache de build
    docker system prune -f
    Write-Host "✅ Cache Docker limpiado" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ Error limpiando cache: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

Write-Host "🔨 RECONSTRUYENDO BACKEND CON CAMBIOS..." -ForegroundColor Yellow
try {
    # Rebuild específico del backend donde están los cambios
    docker-compose build --no-cache backend

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backend reconstruido exitosamente" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Error reconstruyendo backend" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

Write-Host "🔨 RECONSTRUYENDO FRONTEND CON NUEVOS ARCHIVOS..." -ForegroundColor Yellow
try {
    # Rebuild del frontend para incluir login-arreglado.html
    docker-compose build --no-cache frontend

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Frontend reconstruido exitosamente" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Error reconstruyendo frontend" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

Write-Host "🚀 INICIANDO CONTENEDORES ACTUALIZADOS..." -ForegroundColor Yellow
try {
    docker-compose up -d

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Contenedores iniciados exitosamente" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Error iniciando contenedores" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

Write-Host "⏳ ESPERANDO QUE LOS SERVICIOS ESTÉN LISTOS..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host ""

Write-Host "🩺 VERIFICANDO ESTADO DE LOS CONTENEDORES:" -ForegroundColor Yellow
try {
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    Write-Host $containers -ForegroundColor White
}
catch {
    Write-Host "❌ Error verificando contenedores: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "🧪 PROBANDO BACKEND ACTUALIZADO:" -ForegroundColor Yellow

# Test 1: Health check general
Write-Host "1️⃣ Health check backend:" -ForegroundColor White
try {
    $healthResponse = curl -k -s -w "%{http_code}" "https://192.168.12.178:8443/" 2>$null
    if ($healthResponse -eq "302") {
        Write-Host "   ✅ Backend responde correctamente (HTTP 302)" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️ Backend responde con: $healthResponse" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Login con email
Write-Host "2️⃣ Probando login con email:" -ForegroundColor White
try {
    $emailLoginResponse = curl -k -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"email":"admin@packfy.cu","password":"admin123"}' "https://192.168.12.178:8443/api/auth/login/" 2>$null

    if ($emailLoginResponse -match "200") {
        Write-Host "   ✅ Login con email: HTTP 200 (EXITOSO)" -ForegroundColor Green
    }
    elseif ($emailLoginResponse -match "401") {
        Write-Host "   ✅ Login con email: HTTP 401 (Credenciales incorrectas - endpoint funciona)" -ForegroundColor Green
    }
    elseif ($emailLoginResponse -match "500") {
        Write-Host "   ❌ Login con email: HTTP 500 (AÚN HAY PROBLEMA)" -ForegroundColor Red
    }
    else {
        Write-Host "   ⚠️ Login con email: $emailLoginResponse" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Login con username
Write-Host "3️⃣ Probando login con username:" -ForegroundColor White
try {
    $usernameLoginResponse = curl -k -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"username":"admin@packfy.cu","password":"admin123"}' "https://192.168.12.178:8443/api/auth/login/" 2>$null

    if ($usernameLoginResponse -match "200") {
        Write-Host "   ✅ Login con username: HTTP 200 (EXITOSO)" -ForegroundColor Green
    }
    elseif ($usernameLoginResponse -match "401") {
        Write-Host "   ✅ Login con username: HTTP 401 (Credenciales incorrectas - endpoint funciona)" -ForegroundColor Green
    }
    elseif ($usernameLoginResponse -match "500") {
        Write-Host "   ❌ Login con username: HTTP 500 (AÚN HAY PROBLEMA)" -ForegroundColor Red
    }
    else {
        Write-Host "   ⚠️ Login con username: $usernameLoginResponse" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "🧪 VERIFICANDO FRONTEND ACTUALIZADO:" -ForegroundColor Yellow

# Test 4: Frontend principal
Write-Host "4️⃣ Frontend principal:" -ForegroundColor White
try {
    $frontendResponse = curl -k -s -w "%{http_code}" "https://192.168.12.178:5173/" 2>$null
    if ($frontendResponse -eq "200") {
        Write-Host "   ✅ Frontend principal: HTTP 200" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️ Frontend principal: $frontendResponse" -ForegroundColor Yellow
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

Write-Host "📱 === PRUEBA FINAL EN MÓVIL ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Abre estas URLs en tu móvil para confirmar que el arreglo funciona:" -ForegroundColor White
Write-Host ""
Write-Host "🎯 TEST PRINCIPAL:" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/login-arreglado.html" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔍 TEST DETALLADO:" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/test-login-debug.html" -ForegroundColor Yellow
Write-Host ""
Write-Host "🏠 APLICACIÓN PRINCIPAL:" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/" -ForegroundColor Yellow
Write-Host ""

Write-Host "🎉 RESULTADO ESPERADO:" -ForegroundColor Green
Write-Host "• ❌ NO más HTTP 500 en login" -ForegroundColor White
Write-Host "• ✅ Login exitoso con tokens JWT" -ForegroundColor White
Write-Host "• ✅ Usuario autenticado correctamente" -ForegroundColor White
Write-Host ""

Write-Host "✅ REBUILD DOCKER COMPLETADO - CAMBIOS APLICADOS" -ForegroundColor Green
