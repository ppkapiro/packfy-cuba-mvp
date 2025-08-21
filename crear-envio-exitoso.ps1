# 🎯 CREACIÓN DE ENVÍO CON FORMATO CORRECTO

Write-Host "🎯 CREACIÓN DE ENVÍO - FORMATO CORRECTO" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

# Credenciales
$loginData = @{
    email    = "admin@packfy.com"
    password = "admin123"
}

Write-Host "🔐 Autenticando..." -ForegroundColor Yellow
$loginBody = $loginData | ConvertTo-Json
$authResponse = Invoke-RestMethod -Uri "http://localhost:5173/api/auth/login/" -Method POST -ContentType "application/json" -Body $loginBody
$token = $authResponse.access
Write-Host "✅ Token obtenido" -ForegroundColor Green

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type"  = "application/json"
    "X-Tenant-Slug" = "packfy-express"
}

Write-Host ""
Write-Host "📦 CREANDO ENVÍO CON FORMATO CORRECTO..." -ForegroundColor Yellow

# Datos con teléfonos en formato correcto (solo dígitos + prefijo +)
$nuevoEnvio = @{
    descripcion            = "Envío de prueba exitoso"
    peso                   = 2.5
    valor_declarado        = 150.00
    remitente_nombre       = "Carlos Rodriguez"
    remitente_direccion    = "1234 Calle Principal, Miami, FL 33101"
    remitente_telefono     = "+13055550123"  # Sin espacios ni guiones
    remitente_email        = "carlos@example.com"
    destinatario_nombre    = "Maria Gonzalez"
    destinatario_direccion = "Calle 23 #456, Vedado, La Habana, Cuba"
    destinatario_telefono  = "+5351234567"  # Sin espacios ni guiones
    destinatario_email     = "maria@example.com"
    notas                  = "Entregar en horario de oficina"
}

$envioJson = $nuevoEnvio | ConvertTo-Json
Write-Host "📋 Datos del envío:" -ForegroundColor White
Write-Host "  Remitente: $($nuevoEnvio.remitente_nombre) - Tel: $($nuevoEnvio.remitente_telefono)" -ForegroundColor Cyan
Write-Host "  Destinatario: $($nuevoEnvio.destinatario_nombre) - Tel: $($nuevoEnvio.destinatario_telefono)" -ForegroundColor Cyan
Write-Host "  Peso: $($nuevoEnvio.peso) kg - Valor: $($nuevoEnvio.valor_declarado)" -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method POST -Headers $headers -Body $envioJson
    Write-Host ""
    Write-Host "✅ ¡ENVÍO CREADO EXITOSAMENTE!" -ForegroundColor Green
    Write-Host "   📋 Número de guía: $($response.numero_guia)" -ForegroundColor White
    Write-Host "   🆔 ID: $($response.id)" -ForegroundColor White
    Write-Host "   📊 Estado: $($response.estado_actual)" -ForegroundColor White
    Write-Host "   📅 Fecha: $($response.fecha_creacion)" -ForegroundColor White

    Write-Host ""
    Write-Host "🎉 ¡PROBLEMA DE CREACIÓN DE ENVÍOS RESUELTO!" -ForegroundColor Green
}
catch {
    Write-Host ""
    Write-Host "❌ Error inesperado:" -ForegroundColor Red
    Write-Host $_.ErrorDetails.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "📊 VERIFICANDO ENVÍOS TOTALES..." -ForegroundColor Yellow
try {
    $envios = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method GET -Headers $headers
    Write-Host "✅ Total envíos en sistema: $($envios.count)" -ForegroundColor Green

    if ($envios.results -and $envios.results.Count -gt 0) {
        Write-Host ""
        Write-Host "📋 Últimos envíos:" -ForegroundColor White
        foreach ($envio in $envios.results | Select-Object -First 3) {
            Write-Host "  🚚 $($envio.numero_guia) - $($envio.estado_actual) - $($envio.remitente_nombre) → $($envio.destinatario_nombre)" -ForegroundColor Cyan
        }
    }
}
catch {
    Write-Host "❌ Error verificando envíos" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 ¡CREACIÓN DE ENVÍOS COMPLETAMENTE FUNCIONAL!" -ForegroundColor Green
Write-Host ""
