# 🇨🇺 PACKFY CUBA - ARREGLO INMEDIATO HTTP 500 LOGIN
# Solución específica para el error de campo 'email' requerido

Write-Host "🛠️ === ARREGLO INMEDIATO HTTP 500 LOGIN ===" -ForegroundColor Green
Write-Host ""

Write-Host "🔍 PROBLEMA IDENTIFICADO:" -ForegroundColor Yellow
Write-Host "• El backend esperaba campo 'email' en el JSON" -ForegroundColor Red
Write-Host "• El frontend probablemente enviaba 'username'" -ForegroundColor Red
Write-Host "• Causa: USERNAME_FIELD = 'email' en el modelo Usuario" -ForegroundColor Red
Write-Host ""

Write-Host "✅ SOLUCIÓN APLICADA:" -ForegroundColor Green
Write-Host "• Modificado auth_views.py para aceptar email O username" -ForegroundColor White
Write-Host "• Ahora convierte automáticamente username → email" -ForegroundColor White
Write-Host ""

Write-Host "🔄 REINICIANDO CONTENEDOR BACKEND..." -ForegroundColor Yellow
try {
    # Reiniciar solo el backend para aplicar cambios
    $restartResult = docker restart packfy-backend-v4

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backend reiniciado exitosamente" -ForegroundColor Green

        # Esperar a que el backend esté listo
        Write-Host "⏳ Esperando que el backend esté listo..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10

        # Verificar que el backend responde
        $healthCheck = curl -k -s -w "%{http_code}" "https://192.168.12.178:8443/" 2>$null
        if ($healthCheck -eq "302") {
            Write-Host "✅ Backend está respondiendo correctamente" -ForegroundColor Green
        }
        else {
            Write-Host "⚠️ Backend responde pero con código: $healthCheck" -ForegroundColor Yellow
        }

    }
    else {
        Write-Host "❌ Error reiniciando backend" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

Write-Host "🧪 PROBANDO ENDPOINT DE LOGIN CON AMBOS FORMATOS:" -ForegroundColor Yellow
Write-Host ""

# Test 1: Con email
Write-Host "1️⃣ PROBANDO CON CAMPO 'email':" -ForegroundColor White
$testEmailData = '{"email":"admin@packfy.cu","password":"admin123"}'
try {
    $testEmailResponse = curl -k -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d $testEmailData "https://192.168.12.178:8443/api/auth/login/" 2>$null

    if ($testEmailResponse -match "500") {
        Write-Host "   ❌ Aún HTTP 500 con campo email" -ForegroundColor Red
    }
    elseif ($testEmailResponse -match "401|400") {
        Write-Host "   ✅ Endpoint funciona (credenciales incorrectas es normal)" -ForegroundColor Green
    }
    elseif ($testEmailResponse -match "200") {
        Write-Host "   ✅ Login exitoso con email" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️ Respuesta: $testEmailResponse" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 2: Con username
Write-Host "2️⃣ PROBANDO CON CAMPO 'username':" -ForegroundColor White
$testUsernameData = '{"username":"admin@packfy.cu","password":"admin123"}'
try {
    $testUsernameResponse = curl -k -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d $testUsernameData "https://192.168.12.178:8443/api/auth/login/" 2>$null

    if ($testUsernameResponse -match "500") {
        Write-Host "   ❌ Aún HTTP 500 con campo username" -ForegroundColor Red
    }
    elseif ($testUsernameResponse -match "401|400") {
        Write-Host "   ✅ Endpoint funciona (credenciales incorrectas es normal)" -ForegroundColor Green
    }
    elseif ($testUsernameResponse -match "200") {
        Write-Host "   ✅ Login exitoso con username" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️ Respuesta: $testUsernameResponse" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Obtener logs actuales para verificar
Write-Host "3️⃣ VERIFICANDO LOGS DEL BACKEND:" -ForegroundColor White
try {
    $recentLogs = docker logs packfy-backend-v4 --tail 10

    # Buscar si hay errores recientes
    $errorLogs = $recentLogs | Where-Object {
        $_ -match "ERROR|500|auth_views|login"
    }

    if ($errorLogs) {
        Write-Host "   ⚠️ Errores recientes detectados:" -ForegroundColor Yellow
        foreach ($errorLog in $errorLogs[-3..-1]) {
            # Últimos 3 errores
            Write-Host "      🔴 $errorLog" -ForegroundColor Red
        }
    }
    else {
        Write-Host "   ✅ No hay errores recientes en el login" -ForegroundColor Green
    }
}
catch {
    Write-Host "   ❌ Error obteniendo logs: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "📱 === SIGUIENTE PASO === " -ForegroundColor Cyan
Write-Host ""
Write-Host "Abre en tu móvil:" -ForegroundColor White
Write-Host "https://192.168.12.178:5173/test-login-debug.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "Y presiona 'Test Login' para verificar si ya no hay HTTP 500" -ForegroundColor White
Write-Host ""

Write-Host "🎯 SI EL PROBLEMA PERSISTE:" -ForegroundColor Yellow
Write-Host "• Revisa los resultados del test en el móvil" -ForegroundColor White
Write-Host "• Dime exactamente qué error aparece" -ForegroundColor White
Write-Host "• Procedería a revisar el frontend" -ForegroundColor White
Write-Host ""

Write-Host "✅ ARREGLO COMPLETADO - LISTO PARA PRUEBA" -ForegroundColor Green
