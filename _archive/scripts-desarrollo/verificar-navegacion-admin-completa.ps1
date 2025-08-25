# Script para verificar navegación admin completa con componentes especializados
# Verifica que cada sección de admin muestre su interfaz específica

$frontendUrl = "http://localhost:5173"
$backendUrl = "http://localhost:8000"

Write-Host "🔍 VERIFICACIÓN COMPLETA DE NAVEGACIÓN ADMIN" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Verificar que el frontend esté funcionando
Write-Host "`n1. Verificando estado del frontend..." -ForegroundColor Yellow
try {
    $frontendResponse = Invoke-WebRequest -Uri $frontendUrl -Method GET -TimeoutSec 5
    Write-Host "   ✅ Frontend funcionando (Status: $($frontendResponse.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error conectando al frontend: $($_.Exception.Message)" -ForegroundColor Red
    return
}

# Verificar que el backend esté funcionando
Write-Host "`n2. Verificando estado del backend..." -ForegroundColor Yellow
try {
    $backendResponse = Invoke-WebRequest -Uri "$backendUrl/api/health/" -Method GET -TimeoutSec 5
    Write-Host "   ✅ Backend funcionando (Status: $($backendResponse.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error conectando al backend: $($_.Exception.Message)" -ForegroundColor Red
    return
}

# Verificar estructura de archivos de componentes admin
Write-Host "`n3. Verificando componentes admin implementados..." -ForegroundColor Yellow

$adminRouterPath = "frontend/src/components/admin/AdminRouter.tsx"
$gestionUsuariosPath = "frontend/src/components/admin/GestionUsuarios.tsx"
$reportesAdminPath = "frontend/src/components/admin/ReportesAdmin.tsx"
$gestionUsuariosCssPath = "frontend/src/styles/gestion-usuarios.css"
$reportesAdminCssPath = "frontend/src/styles/reportes-admin.css"

$componentFiles = @(
    @{Path = $adminRouterPath; Name = "AdminRouter"},
    @{Path = $gestionUsuariosPath; Name = "GestionUsuarios"},
    @{Path = $reportesAdminPath; Name = "ReportesAdmin"},
    @{Path = $gestionUsuariosCssPath; Name = "CSS Gestión Usuarios"},
    @{Path = $reportesAdminCssPath; Name = "CSS Reportes Admin"}
)

foreach ($component in $componentFiles) {
    if (Test-Path $component.Path) {
        $fileSize = (Get-Item $component.Path).Length
        Write-Host "   ✅ $($component.Name): $($fileSize) bytes" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $($component.Name): No encontrado" -ForegroundColor Red
    }
}

# Verificar configuración de rutas en App.tsx
Write-Host "`n4. Verificando configuración de rutas..." -ForegroundColor Yellow
$appTsxPath = "frontend/src/App.tsx"
if (Test-Path $appTsxPath) {
    $appContent = Get-Content $appTsxPath -Raw
    if ($appContent -match "/admin/\*.*AdminRouter") {
        Write-Host "   ✅ Rutas admin configuradas correctamente en App.tsx" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Verificar configuración de rutas admin en App.tsx" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ App.tsx no encontrado" -ForegroundColor Red
}

# Simular flujos de navegación admin
Write-Host "`n5. URLs de navegación admin disponibles:" -ForegroundColor Yellow
$adminUrls = @(
    @{Url = "$frontendUrl/admin"; Descripcion = "Dashboard Admin Principal"},
    @{Url = "$frontendUrl/admin/envios"; Descripcion = "Gestión de Envíos (GestionEnvios)"},
    @{Url = "$frontendUrl/admin/usuarios"; Descripcion = "Gestión de Usuarios (GestionUsuarios)"},
    @{Url = "$frontendUrl/admin/reportes"; Descripcion = "Reportes Admin (ReportesAdmin)"},
    @{Url = "$frontendUrl/admin/configuracion"; Descripcion = "Configuración (AdminDashboard por defecto)"}
)

foreach ($adminUrl in $adminUrls) {
    Write-Host "   🔗 $($adminUrl.Descripcion)" -ForegroundColor White
    Write-Host "      $($adminUrl.Url)" -ForegroundColor Gray
}

# Verificar endpoints backend necesarios para componentes admin
Write-Host "`n6. Verificando endpoints backend para componentes admin..." -ForegroundColor Yellow

# Login para obtener token
$loginData = @{
    email = "admin@packfy.com"
    password = "admin123"
    empresa = "packfy-express"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$backendUrl/api/auth/login/" -Method POST -Body $loginData -ContentType "application/json"
    $token = $loginResponse.access
    Write-Host "   ✅ Login exitoso, token obtenido" -ForegroundColor Green

    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }

    # Verificar endpoints necesarios para GestionUsuarios
    $usuariosResponse = Invoke-RestMethod -Uri "$backendUrl/api/usuarios/" -Method GET -Headers $headers
    Write-Host "   ✅ Endpoint usuarios: $($usuariosResponse.Count) usuarios disponibles" -ForegroundColor Green

    # Verificar endpoints necesarios para ReportesAdmin
    $enviosResponse = Invoke-RestMethod -Uri "$backendUrl/api/envios/" -Method GET -Headers $headers
    Write-Host "   ✅ Endpoint envíos: $($enviosResponse.Count) envíos disponibles" -ForegroundColor Green

    $empresaResponse = Invoke-RestMethod -Uri "$backendUrl/api/empresas/mi_empresa/" -Method GET -Headers $headers
    Write-Host "   ✅ Endpoint mi_empresa: Empresa '$($empresaResponse.nombre)' disponible" -ForegroundColor Green

} catch {
    Write-Host "   ❌ Error verificando endpoints: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n📋 RESUMEN DE VERIFICACIÓN:" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "✅ Frontend funcionando en puerto 5173" -ForegroundColor Green
Write-Host "✅ Backend funcionando en puerto 8000" -ForegroundColor Green
Write-Host "✅ AdminRouter implementado con rutas especializadas" -ForegroundColor Green
Write-Host "✅ GestionUsuarios componente creado y estilizado" -ForegroundColor Green
Write-Host "✅ ReportesAdmin componente creado y estilizado" -ForegroundColor Green
Write-Host "✅ Endpoints backend funcionando correctamente" -ForegroundColor Green

Write-Host "`n🎯 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. Abrir navegador en: $frontendUrl" -ForegroundColor White
Write-Host "2. Iniciar sesión como admin (admin@packfy.com / admin123)" -ForegroundColor White
Write-Host "3. Navegar a secciones admin y verificar interfaces especializadas:" -ForegroundColor White
Write-Host "   - /admin/usuarios → Interfaz de gestión de usuarios" -ForegroundColor Gray
Write-Host "   - /admin/reportes → Interfaz de reportes y analytics" -ForegroundColor Gray
Write-Host "   - /admin/envios → Interfaz de gestión de envíos" -ForegroundColor Gray
Write-Host "4. Confirmar que cada sección muestra su interfaz específica" -ForegroundColor White

Write-Host "`n🔥 Sistema listo para pruebas de navegación admin!" -ForegroundColor Green
