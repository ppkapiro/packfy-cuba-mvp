# Script completo para verificar rutas del dashboard y endpoints
Write-Host "🔍 VERIFICACIÓN COMPLETA DE RUTAS Y ENDPOINTS PACKFY" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"
$frontendUrl = "http://localhost:5173"

Write-Host "`n🔐 PASO 1: Autenticación..." -ForegroundColor Green

$loginBody = @{
    email    = "admin@packfy.com"
    password = "admin123"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $loginResponse = Invoke-RestMethod -Uri "$frontendUrl/api/auth/login/" -Method POST -Body $loginBody -Headers $headers
    $token = $loginResponse.access

    Write-Host "✅ Autenticación exitosa" -ForegroundColor Green
    Write-Host "   Usuario: $($loginResponse.user.nombre) $($loginResponse.user.apellidos)" -ForegroundColor Gray
    Write-Host "   Rol: $($loginResponse.user.perfil_actual.rol)" -ForegroundColor Gray
    Write-Host "   Empresa: $($loginResponse.user.perfil_actual.empresa.nombre)" -ForegroundColor Gray

    # Headers con autenticación
    $authHeaders = @{
        "Authorization" = "Bearer $token"
        "X-Tenant-Slug" = "packfy-express"
        "Content-Type"  = "application/json"
    }

    Write-Host "`n📊 PASO 2: Verificando TODOS los endpoints principales..." -ForegroundColor Green

    # Array de endpoints para verificar
    $endpoints = @(
        @{ url = "/api/empresas/"; name = "Empresas - Lista" },
        @{ url = "/api/empresas/mi_empresa/"; name = "Mi Empresa" },
        @{ url = "/api/empresas/mis_perfiles/"; name = "Mis Perfiles" },
        @{ url = "/api/usuarios/"; name = "Usuarios - Lista" },
        @{ url = "/api/usuarios/me/"; name = "Mi Perfil" },
        @{ url = "/api/envios/"; name = "Envíos - Lista" },
        @{ url = "/api/historial-estados/"; name = "Historial Estados" },
        @{ url = "/api/sistema-info/"; name = "Info del Sistema" },
        @{ url = "/api/health/"; name = "Health Check" }
    )

    $endpointsOk = 0
    $endpointsTotal = $endpoints.Count

    foreach ($endpoint in $endpoints) {
        try {
            $response = Invoke-RestMethod -Uri "$frontendUrl$($endpoint.url)" -Method GET -Headers $authHeaders

            # Determinar la cantidad de elementos
            $count = 0
            if ($response.results) {
                $count = $response.results.Count
            }
            elseif ($response.Count) {
                $count = $response.Count
            }
            elseif ($response) {
                $count = 1
            }

            Write-Host "✅ $($endpoint.name) - $count elementos" -ForegroundColor Green
            $endpointsOk++
        }
        catch {
            Write-Host "❌ $($endpoint.name) - Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }

    Write-Host "`n📈 RESUMEN DE ENDPOINTS:" -ForegroundColor Cyan
    Write-Host "✅ Funcionando: $endpointsOk/$endpointsTotal" -ForegroundColor Green

    Write-Host "`n🌐 PASO 3: Verificando rutas del frontend..." -ForegroundColor Green

    # URLs principales del frontend que debemos verificar
    $frontendRoutes = @(
        @{ url = "$frontendUrl"; name = "Página Principal"; description = "Debe redirigir a /dashboard" },
        @{ url = "$frontendUrl/login"; name = "Login"; description = "Formulario de login" },
        @{ url = "$frontendUrl/dashboard"; name = "Dashboard Base"; description = "DashboardRouter decide admin/user" },
        @{ url = "$frontendUrl/admin/dashboard"; name = "Dashboard Admin"; description = "Dashboard ejecutivo para dueños" },
        @{ url = "$frontendUrl/admin/envios"; name = "Envíos Admin"; description = "GestionEnvios en contexto admin" },
        @{ url = "$frontendUrl/admin/usuarios"; name = "Usuarios Admin"; description = "Gestión de usuarios admin" },
        @{ url = "$frontendUrl/admin/reportes"; name = "Reportes Admin"; description = "Reportes y análisis" },
        @{ url = "$frontendUrl/envios"; name = "Envíos Básico"; description = "GestionEnvios básico" },
        @{ url = "$frontendUrl/envios/nuevo"; name = "Nuevo Envío"; description = "Formulario crear envío" }
    )

    Write-Host "`n📍 RUTAS DEL FRONTEND A VERIFICAR MANUALMENTE:" -ForegroundColor Yellow
    foreach ($route in $frontendRoutes) {
        Write-Host "🔗 $($route.name): $($route.url)" -ForegroundColor White
        Write-Host "   Debe mostrar: $($route.description)" -ForegroundColor Gray
    }

    Write-Host "`n🎯 PASO 4: Verificación de routing admin específico..." -ForegroundColor Green

    Write-Host "`n📋 NAVEGACIÓN ADMIN - VERIFICAR ESTOS LINKS:" -ForegroundColor Magenta
    Write-Host "• Dashboard Ejecutivo → /admin/dashboard" -ForegroundColor White
    Write-Host "• Envíos → /admin/envios (¡NO /envios!)" -ForegroundColor Yellow
    Write-Host "• Usuarios → /admin/usuarios" -ForegroundColor White
    Write-Host "• Reportes → /admin/reportes" -ForegroundColor White
    Write-Host "• Configuración → /admin/configuracion" -ForegroundColor White

    Write-Host "`n🔍 PASO 5: Lista de verificación para testing manual..." -ForegroundColor Green
    Write-Host "1. ✅ Abrir $frontendUrl" -ForegroundColor White
    Write-Host "2. ✅ Login: admin@packfy.com / admin123" -ForegroundColor White
    Write-Host "3. ✅ Verificar que aparece navegación de admin (Dashboard, Envíos, Usuarios, etc.)" -ForegroundColor White
    Write-Host "4. ✅ Hacer clic en cada elemento del menú admin:" -ForegroundColor White
    Write-Host "   - Dashboard → /admin/dashboard" -ForegroundColor Gray
    Write-Host "   - Envíos → /admin/envios" -ForegroundColor Gray
    Write-Host "   - Usuarios → /admin/usuarios" -ForegroundColor Gray
    Write-Host "5. ✅ Verificar que cada ruta muestra la interfaz correcta" -ForegroundColor White
    Write-Host "6. ✅ Verificar que la URL en el navegador sea correcta" -ForegroundColor White

    Write-Host "`n🚨 PROBLEMAS ANTERIORES QUE DEBERIAN ESTAR SOLUCIONADOS:" -ForegroundColor Red
    Write-Host "❌ Admin hacía clic en 'Envíos' → iba a /envios (básico)" -ForegroundColor White
    Write-Host "✅ Ahora admin hace clic en 'Envíos' → va a /admin/envios (admin)" -ForegroundColor Green

    Write-Host "`n📊 ENDPOINTS ADICIONALES PARA VERIFICAR EN EL FUTURO:" -ForegroundColor Yellow
    $futureEndpoints = @(
        "/api/admin/metricas/",
        "/api/admin/reportes/",
        "/api/admin/usuarios/roles/",
        "/api/admin/configuracion/",
        "/api/envios/estadisticas/",
        "/api/usuarios/por-rol/"
    )

    foreach ($futureEndpoint in $futureEndpoints) {
        Write-Host "🔮 $futureEndpoint - (Implementar si no existe)" -ForegroundColor Cyan
    }

    Write-Host "`n🎉 VERIFICACIÓN COMPLETA - TODO LISTO PARA TESTING" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Verifica que los contenedores estén funcionando:" -ForegroundColor Yellow
    Write-Host "docker-compose ps" -ForegroundColor Gray
}

Write-Host "🚀 ¡INSTRUCCIONES FINALES!" -ForegroundColor Cyan
Write-Host "1. Abre Chrome en: $frontendUrl" -ForegroundColor White
Write-Host "2. Haz login como admin (admin@packfy.com / admin123)" -ForegroundColor White
Write-Host "3. Verifica CADA link de la navegación admin" -ForegroundColor White
Write-Host "4. ¡Los usuarios admin ahora deberían ver la interfaz correcta!" -ForegroundColor Green
