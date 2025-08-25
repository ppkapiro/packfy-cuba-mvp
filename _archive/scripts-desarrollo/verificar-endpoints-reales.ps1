# 🔍 VERIFICACIÓN DE ENDPOINTS REALES DISPONIBLES

Write-Host "🔍 VERIFICACIÓN DE ENDPOINTS REALES PACKFY" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
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
Write-Host "📋 ENDPOINTS CONFIRMADOS DISPONIBLES:" -ForegroundColor Yellow

# Endpoints básicos confirmados en urls.py
$endpoints_disponibles = @(
    @{url = "/api/empresas/"; nombre = "Empresas - Lista"; metodo = "GET" },
    @{url = "/api/empresas/mi_empresa/"; nombre = "Empresas - Mi Empresa"; metodo = "GET" },
    @{url = "/api/empresas/mis_perfiles/"; nombre = "Empresas - Mis Perfiles"; metodo = "GET" },
    @{url = "/api/usuarios/"; nombre = "Usuarios - Lista"; metodo = "GET" },
    @{url = "/api/usuarios/me/"; nombre = "Usuarios - Mi Perfil"; metodo = "GET" },
    @{url = "/api/envios/"; nombre = "Envíos - Lista"; metodo = "GET" },
    @{url = "/api/historial-estados/"; nombre = "Historial Estados"; metodo = "GET" },
    @{url = "/api/sistema-info/"; nombre = "Sistema Info"; metodo = "GET" },
    @{url = "/api/health/"; nombre = "Health Check"; metodo = "GET" }
)

foreach ($endpoint in $endpoints_disponibles) {
    try {
        switch ($endpoint.metodo) {
            "GET" { $response = Invoke-RestMethod -Uri "http://localhost:5173$($endpoint.url)" -Method GET -Headers $headers }
            "POST" { $response = Invoke-RestMethod -Uri "http://localhost:5173$($endpoint.url)" -Method POST -Headers $headers -Body "{}" }
        }

        if ($response -is [array]) {
            Write-Host "✅ $($endpoint.nombre) - $($response.Length) elementos" -ForegroundColor Green
        }
        elseif ($response.count -ne $null) {
            Write-Host "✅ $($endpoint.nombre) - $($response.count) elementos paginados" -ForegroundColor Green
        }
        elseif ($response.status -eq "ok") {
            Write-Host "✅ $($endpoint.nombre) - OK" -ForegroundColor Green
        }
        else {
            Write-Host "✅ $($endpoint.nombre) - Datos recibidos" -ForegroundColor Green
        }
    }
    catch {
        $statusCode = $null
        if ($_.Exception.Response) {
            $statusCode = $_.Exception.Response.StatusCode.value__
        }

        switch ($statusCode) {
            403 { Write-Host "🔒 $($endpoint.nombre) - Sin permisos (403)" -ForegroundColor Yellow }
            404 { Write-Host "❌ $($endpoint.nombre) - No encontrado (404)" -ForegroundColor Red }
            400 { Write-Host "⚠️ $($endpoint.nombre) - Bad Request (400)" -ForegroundColor Yellow }
            default { Write-Host "❌ $($endpoint.nombre) - Error: $($_.Exception.Message)" -ForegroundColor Red }
        }
    }
}

Write-Host ""
Write-Host "🧪 PROBANDO CREACIÓN DE DATOS..." -ForegroundColor Yellow

# Test crear usuario (si tiene permisos)
Write-Host "👤 Probando crear usuario..." -ForegroundColor White
try {
    $nuevoUsuario = @{
        email    = "test_$(Get-Random)@packfy.com"
        nombre   = "Usuario"
        apellido = "Prueba"
        telefono = "+53 5 999-9999"
        password = "test123"
    } | ConvertTo-Json

    $usuarioCreado = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/" -Method POST -Headers $headers -Body $nuevoUsuario
    Write-Host "✅ Usuario creado: $($usuarioCreado.email)" -ForegroundColor Green
}
catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "❌ Error crear usuario: HTTP $statusCode" -ForegroundColor Red
}

# Test crear envío (si tiene permisos)
Write-Host "📦 Probando crear envío..." -ForegroundColor White
try {
    $nuevoEnvio = @{
        remitente_nombre       = "Admin Test"
        remitente_telefono     = "+53 5 123-4567"
        remitente_direccion    = "Miami, FL"
        destinatario_nombre    = "Cliente Test"
        destinatario_telefono  = "+53 5 987-6543"
        destinatario_direccion = "La Habana, Cuba"
        descripcion            = "Paquete de prueba automática"
        peso                   = 1.5
        valor_declarado        = 50.00
    } | ConvertTo-Json

    $envioCreado = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method POST -Headers $headers -Body $nuevoEnvio
    Write-Host "✅ Envío creado: $($envioCreado.numero_guia)" -ForegroundColor Green
}
catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "❌ Error crear envío: HTTP $statusCode" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 VERIFICACIÓN COMPLETA DE ENDPOINTS REALES" -ForegroundColor Cyan
Write-Host "✅ = Funcionando | 🔒 = Sin permisos | ❌ = Error/No existe" -ForegroundColor White
Write-Host ""
