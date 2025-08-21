# Script para verificar URLs exactas disponibles en DRF
Write-Host "🔍 VERIFICACIÓN DE URLS EXACTAS DRF" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

$frontendUrl = "http://localhost:5173"

# Credenciales correctas
$loginData = @{
    email    = "admin@packfy.com"
    password = "admin123"
}

Write-Host "`n🔐 AUTENTICACIÓN..." -ForegroundColor Yellow
try {
    $loginBody = $loginData | ConvertTo-Json
    $authResponse = Invoke-RestMethod -Uri "$frontendUrl/api/auth/login/" -Method POST -ContentType "application/json" -Body $loginBody
    $token = $authResponse.access
    Write-Host "✅ Autenticación exitosa" -ForegroundColor Green

    # Headers base
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type"  = "application/json"
        "X-Tenant-Slug" = "packfy-express"
    }

    Write-Host "`n📡 OBTENIENDO API ROOT..." -ForegroundColor Green
    $apiRoot = Invoke-RestMethod -Uri "$frontendUrl/api/" -Method GET -Headers $headers

    Write-Host "`n🌐 ENDPOINTS DISPONIBLES DESDE API ROOT:" -ForegroundColor Yellow
    $apiRoot.PSObject.Properties | ForEach-Object {
        Write-Host "   📍 $($_.Name): $($_.Value)" -ForegroundColor White
    }

    Write-Host "`n🧪 PROBANDO ENDPOINTS ESPECÍFICOS..." -ForegroundColor Green

    # Probar endpoints específicos con las URLs exactas
    $endpointsToTest = @(
        @{ name = "Empresas Lista"; url = "/api/empresas/" },
        @{ name = "Mi Empresa"; url = "/api/empresas/mi_empresa/" },
        @{ name = "Mis Perfiles"; url = "/api/empresas/mis_perfiles/" },
        @{ name = "Usuarios Lista"; url = "/api/usuarios/" },
        @{ name = "Mi Perfil"; url = "/api/usuarios/me/" },
        @{ name = "Envíos Lista"; url = "/api/envios/" },
        @{ name = "Historial Estados"; url = "/api/historial-estados/" },
        @{ name = "Sistema Info"; url = "/api/sistema-info/" },
        @{ name = "Health Check"; url = "/api/health/" }
    )

    foreach ($endpoint in $endpointsToTest) {
        try {
            Write-Host "`n🔗 Testing: $($endpoint.name) - $($endpoint.url)" -ForegroundColor Cyan
            $response = Invoke-RestMethod -Uri "$frontendUrl$($endpoint.url)" -Method GET -Headers $headers

            # Verificar tipo de respuesta
            if ($response.results) {
                Write-Host "   ✅ Paginado: $($response.results.Count) elementos" -ForegroundColor Green
                Write-Host "   📊 Total: $($response.count)" -ForegroundColor Gray
            }
            elseif ($response.Count -gt 0) {
                Write-Host "   ✅ Array: $($response.Count) elementos" -ForegroundColor Green
            }
            elseif ($response) {
                Write-Host "   ✅ Objeto individual" -ForegroundColor Green
                if ($response.PSObject.Properties) {
                    $keys = ($response.PSObject.Properties | Select-Object -First 5).Name -join ", "
                    Write-Host "   🔑 Keys: $keys..." -ForegroundColor Gray
                }
            }
        }
        catch {
            $statusCode = $_.Exception.Response.StatusCode.value__
            if ($statusCode -eq 404) {
                Write-Host "   ❌ 404 - Endpoint no encontrado" -ForegroundColor Red
            }
            elseif ($statusCode -eq 403) {
                Write-Host "   🔒 403 - Sin permisos" -ForegroundColor Yellow
            }
            else {
                Write-Host "   ⚠️ Error $statusCode - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }

    Write-Host "`n🎯 TAMBIÉN PROBANDO VARIANTES CON GUIONES..." -ForegroundColor Green

    $variantesToTest = @(
        @{ name = "Mi Empresa (guión)"; url = "/api/empresas/mi-empresa/" },
        @{ name = "Mis Perfiles (guión)"; url = "/api/empresas/mis-perfiles/" },
        @{ name = "Mi Perfil (guión)"; url = "/api/usuarios/mi-perfil/" }
    )

    foreach ($variant in $variantesToTest) {
        try {
            Write-Host "`n🔗 Testing variante: $($variant.name) - $($variant.url)" -ForegroundColor Cyan
            $response = Invoke-RestMethod -Uri "$frontendUrl$($variant.url)" -Method GET -Headers $headers
            Write-Host "   ✅ Funciona con guión!" -ForegroundColor Green
        }
        catch {
            $statusCode = $_.Exception.Response.StatusCode.value__
            Write-Host "   ❌ No funciona con guión ($statusCode)" -ForegroundColor Red
        }
    }

}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎯 RESUMEN:" -ForegroundColor Cyan
Write-Host "- Verificar qué URLs están realmente disponibles" -ForegroundColor White
Write-Host "- DRF puede usar underscore (_) o guión (-) según configuración" -ForegroundColor White
Write-Host "- Algunos endpoints pueden necesitar implementación adicional" -ForegroundColor White
