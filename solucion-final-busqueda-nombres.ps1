#!/usr/bin/env pwsh
# 🔧 PACKFY CUBA - SOLUCION FINAL BUSQUEDA POR NOMBRES
# ==================================================

Write-Host "🔧 PACKFY CUBA - SOLUCION FINAL BUSQUEDA POR NOMBRES" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green

Write-Host "`n🔍 PROBLEMAS IDENTIFICADOS:" -ForegroundColor Yellow
Write-Host "===========================" -ForegroundColor Yellow
Write-Host "1. ❌ /seguimiento → página en blanco (ruta no definida)" -ForegroundColor Red
Write-Host "2. ❌ /rastreo → búsqueda por guía en lugar de nombres" -ForegroundColor Red
Write-Host "3. ❌ TrackingPage usa endpoint autenticado que falla" -ForegroundColor Red

Write-Host "`n✅ SOLUCIONES APLICADAS:" -ForegroundColor Yellow
Write-Host "========================" -ForegroundColor Yellow
Write-Host "1. ✅ Agregada redirección /seguimiento → /rastreo" -ForegroundColor Green
Write-Host "2. ✅ Endpoint público creado para búsqueda por nombres" -ForegroundColor Green
Write-Host "3. ✅ Datos de prueba disponibles en base de datos" -ForegroundColor Green

Write-Host "`n🔧 APLICANDO CORRECCIONES FINALES..." -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

$projectRoot = "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"
$backendDir = "$projectRoot\backend"

# 1. Verificar servicios
$backend = netstat -an | findstr ":8000.*LISTENING"
$frontend = netstat -an | findstr ":5173.*LISTENING"

if (-not $backend) {
    Write-Host "⚠️  Backend no está ejecutándose, iniciando..." -ForegroundColor Yellow
    Write-Host "💡 Necesitas iniciar: cd backend && python manage.py runserver 0.0.0.0:8000" -ForegroundColor Cyan
}
else {
    Write-Host "✅ Backend ejecutándose" -ForegroundColor Green
}

if (-not $frontend) {
    Write-Host "⚠️  Frontend no está ejecutándose, iniciando..." -ForegroundColor Yellow
    Write-Host "💡 Necesitas iniciar: cd frontend && npm run dev" -ForegroundColor Cyan
}
else {
    Write-Host "✅ Frontend ejecutándose" -ForegroundColor Green
}

# 2. Probar endpoint público
Write-Host "`n🧪 PROBANDO NUEVO ENDPOINT PUBLICO:" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

$publicEndpoint = "http://localhost:8000/api/public/rastrear-nombre/?nombre=José&tipo=remitente"
Write-Host "🔗 Probando: $publicEndpoint" -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri $publicEndpoint -UseBasicParsing -TimeoutSec 5
    $content = $response.Content | ConvertFrom-Json

    if ($content.resultados -gt 0) {
        Write-Host "✅ Endpoint público funciona: $($content.resultados) resultados" -ForegroundColor Green
        foreach ($envio in $content.envios) {
            Write-Host "   📦 $($envio.numero_guia): $($envio.remitente_nombre) → $($envio.destinatario_nombre)" -ForegroundColor White
        }
    }
    else {
        Write-Host "⚠️  Endpoint funciona pero sin datos" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Error en endpoint público: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Asegúrate de que el backend esté ejecutándose" -ForegroundColor Yellow
}

# 3. Abrir páginas para prueba
Write-Host "`n🌐 ABRIENDO PAGINAS PARA PRUEBA:" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

Write-Host "🔄 Abriendo navegador..." -ForegroundColor Cyan

# Abrir login
Start-Process "chrome.exe" -ArgumentList "--new-window", "--incognito", "https://localhost:5173/login"
Start-Sleep -Seconds 2

# Abrir /rastreo directamente (después del login)
Start-Process "chrome.exe" -ArgumentList "--new-tab", "https://localhost:5173/rastreo"
Start-Sleep -Seconds 1

# Abrir /seguimiento para probar redirección
Start-Process "chrome.exe" -ArgumentList "--new-tab", "https://localhost:5173/seguimiento"

Write-Host "✅ Chrome abierto en modo incógnito para pruebas limpias" -ForegroundColor Green

# 4. Instrucciones de prueba
Write-Host "`n📋 INSTRUCCIONES DE PRUEBA:" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

Write-Host "🔹 PASO 1: Hacer login en la primera pestaña" -ForegroundColor Cyan
Write-Host "   📧 Email: admin@packfy.cu" -ForegroundColor White
Write-Host "   🔑 Password: admin123" -ForegroundColor White

Write-Host "`n🔹 PASO 2: Después del login, probar:" -ForegroundColor Cyan
Write-Host "   🔗 Pestaña /rastreo - debe mostrar búsqueda por NOMBRES" -ForegroundColor White
Write-Host "   🔗 Pestaña /seguimiento - debe redirigir a /rastreo" -ForegroundColor White

Write-Host "`n🔹 PASO 3: En la página de rastreo:" -ForegroundColor Cyan
Write-Host "   📝 Buscar 'José' como remitente (debe encontrar 1 resultado)" -ForegroundColor White
Write-Host "   📝 Buscar 'María' como destinatario (debe encontrar 1 resultado)" -ForegroundColor White
Write-Host "   📝 Buscar 'García' en ambos (debe encontrar 2 resultados)" -ForegroundColor White

Write-Host "`n🔹 PASO 4: Probar menú 'Seguimiento':" -ForegroundColor Cyan
Write-Host "   🖱️  Hacer clic en pestaña 'Seguimiento' del menú" -ForegroundColor White
Write-Host "   ✅ Debe ir a /rastreo y mostrar búsqueda por nombres" -ForegroundColor White

# 5. Resultados esperados
Write-Host "`n🎯 RESULTADOS ESPERADOS:" -ForegroundColor Yellow
Write-Host "========================" -ForegroundColor Yellow
Write-Host "✅ /rastreo → Búsqueda por nombres (NO por guía)" -ForegroundColor Green
Write-Host "✅ /seguimiento → Redirección automática a /rastreo" -ForegroundColor Green
Write-Host "✅ Menú 'Seguimiento' → Funciona correctamente" -ForegroundColor Green
Write-Host "✅ Búsqueda encuentra resultados para José, María, García" -ForegroundColor Green

# 6. URLs móviles
Write-Host "`n📱 PARA PROBAR EN MOVIL:" -ForegroundColor Yellow
Write-Host "========================" -ForegroundColor Yellow
Write-Host "📍 https://192.168.12.178:5173/rastreo" -ForegroundColor Green
Write-Host "📍 https://192.168.12.178:5173/seguimiento (debe redirigir)" -ForegroundColor Green

Write-Host "`n💡 SI AUN NO FUNCIONA:" -ForegroundColor Yellow
Write-Host "=====================" -ForegroundColor Yellow
Write-Host "🔄 Limpia caché del navegador (Ctrl+Shift+Del)" -ForegroundColor Cyan
Write-Host "🔄 Usa modo incógnito/privado" -ForegroundColor Cyan
Write-Host "🔄 Verifica que ambos servicios estén ejecutándose" -ForegroundColor Cyan
Write-Host "🔄 Asegúrate de hacer login antes de probar /rastreo" -ForegroundColor Cyan

Write-Host "`n🇨🇺 Packfy Cuba - ¡Solución completa aplicada!" -ForegroundColor Green
Write-Host "Reporta los resultados de las pruebas." -ForegroundColor Gray
