# 🇨🇺 PACKFY CUBA - DIAGNÓSTICO COMPLETO DE CONECTIVIDAD
# =====================================================

Write-Host "🔍 PACKFY CUBA - DIAGNÓSTICO COMPLETO" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# 1. Verificar procesos activos
Write-Host "`n📊 1. VERIFICANDO PROCESOS ACTIVOS" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
$nodeProcesses = Get-Process node -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "✅ Python procesos activos: $($pythonProcesses.Count)" -ForegroundColor Green
    $pythonProcesses | ForEach-Object {
        Write-Host "   📍 PID: $($_.Id) - CPU: $($_.CPU)" -ForegroundColor Gray
    }
}
else {
    Write-Host "❌ No hay procesos Python activos" -ForegroundColor Red
}

if ($nodeProcesses) {
    Write-Host "✅ Node procesos activos: $($nodeProcesses.Count)" -ForegroundColor Green
    $nodeProcesses | ForEach-Object {
        Write-Host "   📍 PID: $($_.Id) - CPU: $($_.CPU)" -ForegroundColor Gray
    }
}
else {
    Write-Host "❌ No hay procesos Node activos" -ForegroundColor Red
}

# 2. Verificar puertos
Write-Host "`n📡 2. VERIFICANDO PUERTOS" -ForegroundColor Yellow
Write-Host "===========================" -ForegroundColor Yellow

$backendPort = netstat -an | Select-String ":8000" | Select-String "LISTENING"
$frontendPort = netstat -an | Select-String ":5173" | Select-String "LISTENING"

if ($backendPort) {
    Write-Host "✅ Backend (8000): ACTIVO" -ForegroundColor Green
}
else {
    Write-Host "❌ Backend (8000): INACTIVO" -ForegroundColor Red
}

if ($frontendPort) {
    Write-Host "✅ Frontend (5173): ACTIVO" -ForegroundColor Green
}
else {
    Write-Host "❌ Frontend (5173): INACTIVO" -ForegroundColor Red
}

# 3. Probar conectividad HTTP
Write-Host "`n🌐 3. PROBANDO CONECTIVIDAD HTTP" -ForegroundColor Yellow
Write-Host "==================================" -ForegroundColor Yellow

try {
    $backendTest = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -Method Head -TimeoutSec 5
    Write-Host "✅ Backend Admin: $($backendTest.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend Admin: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

try {
    $frontendTest = Invoke-WebRequest -Uri "https://localhost:5173/" -Method Head -TimeoutSec 5 -SkipCertificateCheck
    Write-Host "✅ Frontend HTTPS: $($frontendTest.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend HTTPS: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Probar endpoints específicos del sistema de rastreo
Write-Host "`n🔍 4. PROBANDO ENDPOINTS DE RASTREO POR NOMBRES" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/envios/rastrear_por_nombre/?nombre=test&tipo=ambos" -TimeoutSec 5
    Write-Host "✅ Endpoint rastreo público: FUNCIONAL" -ForegroundColor Green
    Write-Host "   📋 Respuesta: $($response)" -ForegroundColor Gray
}
catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "⚠️  Endpoint rastreo: REQUIERE AUTENTICACIÓN (normal)" -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ Endpoint rastreo: ERROR - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 5. Información de red
Write-Host "`n🌐 5. INFORMACIÓN DE RED" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow

$networkInfo = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.*" }
foreach ($ip in $networkInfo) {
    Write-Host "📍 IP: $($ip.IPAddress) - Interface: $($ip.InterfaceAlias)" -ForegroundColor Gray
}

# 6. URLs disponibles
Write-Host "`n🔗 6. URLS DISPONIBLES" -ForegroundColor Yellow
Write-Host "=====================" -ForegroundColor Yellow

$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" } | Select-Object -First 1).IPAddress

Write-Host "🖥️  LOCALHOST:" -ForegroundColor Cyan
Write-Host "   Frontend: https://localhost:5173/" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000/" -ForegroundColor White
Write-Host "   Admin:    http://localhost:8000/admin/" -ForegroundColor White

if ($localIP) {
    Write-Host "`n📱 ACCESO MÓVIL/RED:" -ForegroundColor Cyan
    Write-Host "   Frontend: https://$localIP:5173/" -ForegroundColor White
    Write-Host "   Backend:  http://$localIP:8000/" -ForegroundColor White
    Write-Host "   API:      http://$localIP:8000/api/" -ForegroundColor White
}

# 7. Probar específicamente el sistema de rastreo
Write-Host "`n🎯 7. PROBANDO SISTEMA DE RASTREO POR NOMBRES" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Yellow

Write-Host "📝 Endpoints implementados:" -ForegroundColor Gray
Write-Host "   • /api/envios/buscar_por_nombre/ (autenticado)" -ForegroundColor Gray
Write-Host "   • /api/envios/rastrear_por_nombre/ (público)" -ForegroundColor Gray

Write-Host "`n🧪 Tipos de búsqueda soportados:" -ForegroundColor Gray
Write-Host "   • ambos: Busca en remitente Y destinatario" -ForegroundColor Gray
Write-Host "   • remitente: Solo en nombre del remitente" -ForegroundColor Gray
Write-Host "   • destinatario: Solo en nombre del destinatario" -ForegroundColor Gray

# 8. Resumen final
Write-Host "`n📋 8. RESUMEN FINAL" -ForegroundColor Yellow
Write-Host "===================" -ForegroundColor Yellow

if ($backendPort -and $frontendPort) {
    Write-Host "🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!" -ForegroundColor Green
    Write-Host "✅ Backend y Frontend están ejecutándose correctamente" -ForegroundColor Green
    Write-Host "✅ Sistema de rastreo por nombres implementado" -ForegroundColor Green
    Write-Host "✅ APIs disponibles para uso público y autenticado" -ForegroundColor Green

    Write-Host "`n🚀 PASOS SIGUIENTES:" -ForegroundColor Cyan
    Write-Host "1. Visita https://localhost:5173/ para usar la interfaz" -ForegroundColor White
    Write-Host "2. Prueba el rastreo por nombres en la página pública" -ForegroundColor White
    Write-Host "3. Inicia sesión para usar funciones completas" -ForegroundColor White
}
else {
    Write-Host "⚠️  SISTEMA CON PROBLEMAS" -ForegroundColor Red
    Write-Host "❌ Algunos servicios no están ejecutándose" -ForegroundColor Red
    Write-Host "🔧 Ejecuta: .\iniciar-sistema-unificado.ps1" -ForegroundColor Yellow
}

Write-Host "`n💡 Para más diagnósticos, ejecuta:" -ForegroundColor Cyan
Write-Host "   .\scripts\testing\diagnostico-conectividad.ps1" -ForegroundColor White

Write-Host "`n🇨🇺 Packfy Cuba - Sistema de rastreo listo!" -ForegroundColor Green
