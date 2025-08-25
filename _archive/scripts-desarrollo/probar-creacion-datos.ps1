# 🔧 PRUEBA DE CREACIÓN CON DATOS CORRECTOS

Write-Host "🔧 PRUEBA DE CREACIÓN DE USUARIOS Y ENVÍOS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
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
Write-Host "👤 PROBANDO CREACIÓN DE USUARIO..." -ForegroundColor Yellow

# Datos de usuario según UsuarioSerializer
$nuevoUsuario = @{
    username   = "test_user_$(Get-Random)"
    email      = "test_user_$(Get-Random)@packfy.com"
    first_name = "Usuario"
    last_name  = "Prueba"
    password   = "testpass123!"
    telefono   = "+53 5 999-8888"
    cargo      = "Tester"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/" -Method POST -Headers $headers -Body $nuevoUsuario
    Write-Host "✅ Usuario creado exitosamente!" -ForegroundColor Green
    Write-Host "   📧 Email: $($response.email)" -ForegroundColor White
    Write-Host "   🆔 ID: $($response.id)" -ForegroundColor White
}
catch {
    Write-Host "❌ Error creando usuario:" -ForegroundColor Red
    if ($_.Exception.Response) {
        $errorDetails = $_.Exception.Response.GetResponseStream()
        $reader = [System.IO.StreamReader]::new($errorDetails)
        $errorText = $reader.ReadToEnd()
        Write-Host "   📋 Detalles: $errorText" -ForegroundColor Yellow
    }
    Write-Host "   🔍 Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📦 PROBANDO CREACIÓN DE ENVÍO..." -ForegroundColor Yellow

# Datos de envío según EnvioSerializer
$nuevoEnvio = @{
    descripcion            = "Paquete de prueba automática"
    peso                   = 2.5
    valor_declarado        = 100.00
    remitente_nombre       = "Carlos Rodriguez"
    remitente_direccion    = "1234 Calle Principal, Miami, FL 33101"
    remitente_telefono     = "+1 305 555-0123"
    remitente_email        = "carlos@example.com"
    destinatario_nombre    = "Maria Gonzalez"
    destinatario_direccion = "Calle 23 #456, Vedado, La Habana, Cuba"
    destinatario_telefono  = "+53 5 123-4567"
    destinatario_email     = "maria@example.com"
    notas                  = "Entregar en horario de oficina"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method POST -Headers $headers -Body $nuevoEnvio
    Write-Host "✅ Envío creado exitosamente!" -ForegroundColor Green
    Write-Host "   📋 Número de guía: $($response.numero_guia)" -ForegroundColor White
    Write-Host "   🆔 ID: $($response.id)" -ForegroundColor White
    Write-Host "   📊 Estado: $($response.estado_actual)" -ForegroundColor White
}
catch {
    Write-Host "❌ Error creando envío:" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "   🔢 Código HTTP: $statusCode" -ForegroundColor Yellow

        try {
            $errorDetails = $_.Exception.Response.GetResponseStream()
            $reader = [System.IO.StreamReader]::new($errorDetails)
            $errorText = $reader.ReadToEnd()
            Write-Host "   📋 Detalles: $errorText" -ForegroundColor Yellow
        }
        catch {
            Write-Host "   📋 No se pudo leer detalles del error" -ForegroundColor Yellow
        }
    }
    Write-Host "   🔍 Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📊 VERIFICANDO RESULTADOS..." -ForegroundColor Yellow

# Verificar usuarios después de la creación
try {
    $usuarios = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/" -Method GET -Headers $headers
    Write-Host "✅ Total usuarios después de prueba: $($usuarios.count)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error verificando usuarios" -ForegroundColor Red
}

# Verificar envíos después de la creación
try {
    $envios = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method GET -Headers $headers
    Write-Host "✅ Total envíos después de prueba: $($envios.count)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error verificando envíos" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 PRUEBA DE CREACIÓN COMPLETADA" -ForegroundColor Cyan
Write-Host ""
