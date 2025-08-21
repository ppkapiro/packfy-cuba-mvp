# 🐛 DEBUG DETALLADO DE CREACIÓN DE ENVÍO

Write-Host "🐛 DEBUG DETALLADO - CREACIÓN DE ENVÍO" -ForegroundColor Red
Write-Host "=====================================" -ForegroundColor Red
Write-Host ""

# Credenciales
$loginData = @{
    email    = "admin@packfy.com"
    password = "admin123"
}

Write-Host "🔐 Autenticando..." -ForegroundColor Yellow
try {
    $loginBody = $loginData | ConvertTo-Json
    $authResponse = Invoke-RestMethod -Uri "http://localhost:5173/api/auth/login/" -Method POST -ContentType "application/json" -Body $loginBody
    $token = $authResponse.access
    Write-Host "✅ Token obtenido" -ForegroundColor Green

    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type"  = "application/json"
        "X-Tenant-Slug" = "packfy-express"
    }
}
catch {
    Write-Host "❌ Error en login: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 DEBUG CREACIÓN DE ENVÍO..." -ForegroundColor Yellow

# Datos mínimos para envío
$nuevoEnvio = @{
    descripcion            = "Debug test envío"
    peso                   = 1.0
    valor_declarado        = 50.00
    remitente_nombre       = "Test Remitente"
    remitente_direccion    = "Test Address Miami"
    remitente_telefono     = "+1 305 555-0123"
    destinatario_nombre    = "Test Destinatario"
    destinatario_direccion = "Test Address Habana"
    destinatario_telefono  = "+53 5 123-4567"
}

$envioJson = $nuevoEnvio | ConvertTo-Json
Write-Host "📋 JSON a enviar:" -ForegroundColor White
Write-Host $envioJson -ForegroundColor Cyan

Write-Host ""
Write-Host "🚀 Enviando request..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method POST -Headers $headers -Body $envioJson
    Write-Host "✅ ¡ENVÍO CREADO!" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 3) -ForegroundColor Green
}
catch {
    Write-Host "❌ ERROR DETALLADO:" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Yellow

    # Intentar leer el cuerpo de la respuesta de error
    try {
        $responseBody = $_.ErrorDetails.Message
        if ($responseBody) {
            Write-Host "Cuerpo de error:" -ForegroundColor Yellow
            Write-Host $responseBody -ForegroundColor Red

            # Intentar parsear JSON de error
            try {
                $errorJson = $responseBody | ConvertFrom-Json
                Write-Host ""
                Write-Host "Errores específicos:" -ForegroundColor Yellow
                foreach ($key in $errorJson.PSObject.Properties.Name) {
                    Write-Host "  $key : $($errorJson.$key)" -ForegroundColor Red
                }
            }
            catch {
                Write-Host "No se pudo parsear JSON de error" -ForegroundColor Yellow
            }
        }
    }
    catch {
        Write-Host "No se pudo leer detalles del error" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "Exception completa:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 DEBUG COMPLETADO" -ForegroundColor Red
Write-Host ""
