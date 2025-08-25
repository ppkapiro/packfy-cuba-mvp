# 🔍 VERIFICACIÓN COMPLETA DE TODOS LOS FLUJOS DEL SISTEMA

Write-Host "🔍 VERIFICACIÓN COMPLETA DE FLUJOS PACKFY" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Credenciales correctas confirmadas
$loginData = @{
    email    = "admin@packfy.com"
    password = "admin123"
}

Write-Host "🔐 AUTENTICACIÓN..." -ForegroundColor Yellow
try {
    $loginBody = $loginData | ConvertTo-Json
    $authResponse = Invoke-RestMethod -Uri "http://localhost:5173/api/auth/login/" -Method POST -ContentType "application/json" -Body $loginBody
    $token = $authResponse.access
    Write-Host "✅ Autenticación exitosa" -ForegroundColor Green

    # Headers base
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type"  = "application/json"
        "X-Tenant-Slug" = "packfy-express"
    }
}
catch {
    Write-Host "❌ Error en autenticación: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🏢 VERIFICANDO MÓDULO EMPRESAS..." -ForegroundColor Yellow

# Test 1: Listar empresas
try {
    $empresas = Invoke-RestMethod -Uri "http://localhost:5173/api/empresas/" -Method GET -Headers $headers
    Write-Host "✅ GET /empresas/ - $($empresas.count) empresas" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /empresas/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Mis perfiles
try {
    $perfiles = Invoke-RestMethod -Uri "http://localhost:5173/api/empresas/mis_perfiles/" -Method GET -Headers $headers
    Write-Host "✅ GET /empresas/mis_perfiles/ - $($perfiles.Length) perfiles" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /empresas/mis_perfiles/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "👥 VERIFICANDO MÓDULO USUARIOS..." -ForegroundColor Yellow

# Test 3: Usuario actual
try {
    $usuarioActual = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/me/" -Method GET -Headers $headers
    Write-Host "✅ GET /usuarios/me/ - Usuario: $($usuarioActual.email)" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /usuarios/me/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Lista de usuarios
try {
    $usuarios = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/" -Method GET -Headers $headers
    Write-Host "✅ GET /usuarios/ - $($usuarios.count) usuarios" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /usuarios/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Crear usuario (verificar endpoint)
try {
    $nuevoUsuario = @{
        email    = "test_usuario_$(Get-Random)@packfy.com"
        nombre   = "Usuario"
        apellido = "Prueba"
        telefono = "+53 5 999-9999"
        password = "test123"
    } | ConvertTo-Json

    $usuarioCreado = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/" -Method POST -Headers $headers -Body $nuevoUsuario
    Write-Host "✅ POST /usuarios/ - Usuario creado: $($usuarioCreado.email)" -ForegroundColor Green
}
catch {
    Write-Host "❌ POST /usuarios/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📦 VERIFICANDO MÓDULO ENVÍOS..." -ForegroundColor Yellow

# Test 6: Lista de envíos
try {
    $envios = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method GET -Headers $headers
    Write-Host "✅ GET /envios/ - $($envios.count) envíos" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /envios/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 7: Crear envío (verificar endpoint)
try {
    $nuevoEnvio = @{
        remitente_email    = "admin@packfy.com"
        destinatario_email = "cliente1@packfy.com"
        descripcion        = "Paquete de prueba"
        peso               = 1.5
        valor_declarado    = 50.00
        direccion_origen   = "Miami, FL"
        direccion_destino  = "La Habana, Cuba"
    } | ConvertTo-Json

    $envioCreado = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method POST -Headers $headers -Body $nuevoEnvio
    Write-Host "✅ POST /envios/ - Envío creado: $($envioCreado.numero_guia)" -ForegroundColor Green
}
catch {
    Write-Host "❌ POST /envios/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "💰 VERIFICANDO MÓDULO FINANZAS..." -ForegroundColor Yellow

# Test 8: Tarifas
try {
    $tarifas = Invoke-RestMethod -Uri "http://localhost:5173/api/finanzas/tarifas/" -Method GET -Headers $headers
    Write-Host "✅ GET /finanzas/tarifas/ - $($tarifas.count) tarifas" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /finanzas/tarifas/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 9: Reportes financieros
try {
    $reportes = Invoke-RestMethod -Uri "http://localhost:5173/api/finanzas/reportes/" -Method GET -Headers $headers
    Write-Host "✅ GET /finanzas/reportes/ - Reportes disponibles" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /finanzas/reportes/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📊 VERIFICANDO MÓDULO REPORTES..." -ForegroundColor Yellow

# Test 10: Dashboard stats
try {
    $stats = Invoke-RestMethod -Uri "http://localhost:5173/api/reportes/dashboard/" -Method GET -Headers $headers
    Write-Host "✅ GET /reportes/dashboard/ - Stats obtenidas" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /reportes/dashboard/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 11: Reportes de envíos
try {
    $reporteEnvios = Invoke-RestMethod -Uri "http://localhost:5173/api/reportes/envios/" -Method GET -Headers $headers
    Write-Host "✅ GET /reportes/envios/ - Reporte de envíos" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /reportes/envios/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔧 VERIFICANDO ENDPOINTS ADMIN..." -ForegroundColor Yellow

# Test 12: Admin stats
try {
    $adminStats = Invoke-RestMethod -Uri "http://localhost:5173/api/admin/stats/" -Method GET -Headers $headers
    Write-Host "✅ GET /admin/stats/ - Stats de admin" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /admin/stats/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 13: Admin usuarios
try {
    $adminUsuarios = Invoke-RestMethod -Uri "http://localhost:5173/api/admin/usuarios/" -Method GET -Headers $headers
    Write-Host "✅ GET /admin/usuarios/ - Gestión de usuarios" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /admin/usuarios/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔍 VERIFICANDO ENDPOINTS DE BÚSQUEDA..." -ForegroundColor Yellow

# Test 14: Buscar envíos
try {
    $busqueda = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/buscar/?q=test" -Method GET -Headers $headers
    Write-Host "✅ GET /envios/buscar/ - Búsqueda funcionando" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /envios/buscar/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 15: Buscar usuarios
try {
    $busquedaUsuarios = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/buscar/?q=admin" -Method GET -Headers $headers
    Write-Host "✅ GET /usuarios/buscar/ - Búsqueda de usuarios" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /usuarios/buscar/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📱 VERIFICANDO ENDPOINTS MOBILE..." -ForegroundColor Yellow

# Test 16: Mobile API
try {
    $mobileStats = Invoke-RestMethod -Uri "http://localhost:5173/api/mobile/stats/" -Method GET -Headers $headers
    Write-Host "✅ GET /mobile/stats/ - API móvil funcionando" -ForegroundColor Green
}
catch {
    Write-Host "❌ GET /mobile/stats/ - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 RESUMEN DE VERIFICACIÓN COMPLETA" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✅ = Funcionando correctamente" -ForegroundColor Green
Write-Host "❌ = Necesita reparación" -ForegroundColor Red
Write-Host ""
