# Verificar routing de admin después de cambios
Write-Host "🔄 VERIFICANDO ROUTING ADMIN ACTUALIZADO" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

Write-Host "`n🏷️  INFORMACIÓN DEL TEST:" -ForegroundColor Yellow
Write-Host "Usuario: admin@packfy.com (rol: dueno)" -ForegroundColor Gray
Write-Host "Empresa: packfy-express" -ForegroundColor Gray
Write-Host "Cambio: Rutas /admin/* ahora van a AdminRouter" -ForegroundColor Gray

$baseUrl = "http://localhost:8000"
$frontendUrl = "http://localhost:5173"

Write-Host "`n🔐 PASO 1: Autenticación como dueño..." -ForegroundColor Green

$loginBody = @{
    email    = "admin@packfy.com"
    password = "packfy123"
    tenant   = "packfy-express"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login/" -Method POST -Body $loginBody -Headers $headers
    $token = $loginResponse.access_token

    Write-Host "✅ Login exitoso" -ForegroundColor Green
    Write-Host "   Token: $($token.Substring(0,20))..." -ForegroundColor Gray
    Write-Host "   Usuario: $($loginResponse.user.nombre) $($loginResponse.user.apellidos)" -ForegroundColor Gray
    Write-Host "   Rol: $($loginResponse.user.perfil_actual.rol)" -ForegroundColor Gray

    # Headers con autenticación
    $authHeaders = @{
        "Authorization" = "Bearer $token"
        "X-Tenant-ID"   = "packfy-express"
        "Content-Type"  = "application/json"
    }

    Write-Host "`n📊 PASO 2: Verificando endpoints principales..." -ForegroundColor Green

    # Verificar endpoint de perfil
    $profile = Invoke-RestMethod -Uri "$baseUrl/auth/perfil/" -Method GET -Headers $authHeaders
    Write-Host "✅ Perfil verificado - Rol: $($profile.rol)" -ForegroundColor Green

    # Verificar envíos
    $envios = Invoke-RestMethod -Uri "$baseUrl/envios/" -Method GET -Headers $authHeaders
    Write-Host "✅ Envíos cargados: $($envios.results.Count) encontrados" -ForegroundColor Green

    Write-Host "`n🌐 PASO 3: URLs de testing del frontend..." -ForegroundColor Green
    Write-Host "Frontend principal: $frontendUrl" -ForegroundColor White
    Write-Host "Login directo: $frontendUrl/login" -ForegroundColor White
    Write-Host "Dashboard admin: $frontendUrl/admin/dashboard" -ForegroundColor Yellow
    Write-Host "Envíos admin: $frontendUrl/admin/envios" -ForegroundColor Yellow
    Write-Host "Usuarios admin: $frontendUrl/admin/usuarios" -ForegroundColor Yellow

    Write-Host "`n🔍 PASO 4: Instrucciones de verificación manual..." -ForegroundColor Green
    Write-Host "1. Abrir: $frontendUrl" -ForegroundColor White
    Write-Host "2. Hacer login con admin@packfy.com / packfy123" -ForegroundColor White
    Write-Host "3. Verificar que la navegación muestra opciones de admin" -ForegroundColor White
    Write-Host "4. Hacer clic en 'Envíos' en la navegación superior" -ForegroundColor White
    Write-Host "5. ¡Ahora debería ir a /admin/envios y mostrar la interfaz de admin!" -ForegroundColor Yellow

    Write-Host "`n📝 CAMBIOS IMPLEMENTADOS:" -ForegroundColor Magenta
    Write-Host "✅ AdminNavigation actualizada para usar rutas /admin/*" -ForegroundColor White
    Write-Host "✅ AdminRouter creado para manejar rutas de admin" -ForegroundColor White
    Write-Host "✅ App.tsx configurado con ruta /admin/* → AdminRouter" -ForegroundColor White
    Write-Host "✅ AdminRouter detecta ruta y muestra componente apropiado" -ForegroundColor White

    Write-Host "`n🎯 EXPECTATIVA:" -ForegroundColor Cyan
    Write-Host "Cuando el usuario admin hace clic en 'Envíos' debe:" -ForegroundColor White
    Write-Host "• Navegar a /admin/envios" -ForegroundColor White
    Write-Host "• AdminRouter detectar la ruta" -ForegroundColor White
    Write-Host "• Mostrar GestionEnvios pero en contexto de admin" -ForegroundColor White
    Write-Host "• Ver navegación de admin (no la básica)" -ForegroundColor White

}
catch {
    Write-Host "❌ Error en autenticación: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n🚀 ¡Listo para probar la interfaz actualizada!" -ForegroundColor Green
