# 🎭 CREAR DATOS DE PRUEBA ADICIONALES PARA DEMO

Write-Host "🎭 CREANDO DATOS ADICIONALES PARA DEMO COMPLETA" -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Magenta
Write-Host ""

# Credenciales del dueño
$loginData = @{
    email    = "admin@packfy.com"
    password = "admin123"
}

Write-Host "🔐 Autenticando como dueño..." -ForegroundColor Yellow
$loginBody = $loginData | ConvertTo-Json
$authResponse = Invoke-RestMethod -Uri "http://localhost:5173/api/auth/login/" -Method POST -ContentType "application/json" -Body $loginBody
$token = $authResponse.access
Write-Host "✅ Autenticado como admin@packfy.com" -ForegroundColor Green

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type"  = "application/json"
    "X-Tenant-Slug" = "packfy-express"
}

Write-Host ""
Write-Host "👥 CREANDO USUARIOS ADICIONALES..." -ForegroundColor Yellow

# Crear algunos usuarios adicionales para demo
$usuariosDemo = @(
    @{
        username   = "operador_miami"
        email      = "operador.miami@packfy.com"
        first_name = "Juan"
        last_name  = "Operador"
        password   = "operador123"
        telefono   = "+13055551234"
        cargo      = "Operador Miami"
    },
    @{
        username   = "operador_cuba"
        email      = "operador.cuba@packfy.com"
        first_name = "Ana"
        last_name  = "Rodriguez"
        password   = "operador123"
        telefono   = "+5351234567"
        cargo      = "Operador Cuba"
    },
    @{
        username   = "cliente_frecuente"
        email      = "cliente.frecuente@gmail.com"
        first_name = "Pedro"
        last_name  = "Martinez"
        password   = "cliente123"
        telefono   = "+5359876543"
        cargo      = "Cliente Frecuente"
    }
)

$usuariosCreados = @()
foreach ($usuario in $usuariosDemo) {
    try {
        $usuarioJson = $usuario | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/" -Method POST -Headers $headers -Body $usuarioJson
        $usuariosCreados += $response
        Write-Host "✅ Usuario creado: $($response.email) - $($response.first_name) $($response.last_name)" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️ Usuario ya existe o error: $($usuario.email)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📦 CREANDO ENVÍOS ADICIONALES..." -ForegroundColor Yellow

# Crear varios envíos para demo con diferentes estados
$enviosDemo = @(
    @{
        descripcion            = "Paquete documentos importantes"
        peso                   = 0.5
        valor_declarado        = 25.00
        remitente_nombre       = "Juan Operador"
        remitente_direccion    = "8th Street, Miami, FL"
        remitente_telefono     = "+13055551234"
        remitente_email        = "operador.miami@packfy.com"
        destinatario_nombre    = "Carmen Lopez"
        destinatario_direccion = "Calle 1ra, Centro Habana, Cuba"
        destinatario_telefono  = "+5351111111"
        destinatario_email     = "carmen@example.com"
        notas                  = "Documentos urgentes - manejar con cuidado"
    },
    @{
        descripcion            = "Medicamentos y productos de salud"
        peso                   = 3.2
        valor_declarado        = 180.00
        remitente_nombre       = "Ana Rodriguez"
        remitente_direccion    = "Brickell Ave, Miami, FL"
        remitente_telefono     = "+13055552345"
        remitente_email        = "operador.cuba@packfy.com"
        destinatario_nombre    = "Dr. Roberto Silva"
        destinatario_direccion = "Hospital Nacional, La Habana, Cuba"
        destinatario_telefono  = "+5352222222"
        destinatario_email     = "dr.silva@hospital.cu"
        notas                  = "Medicamentos - mantener refrigerado"
    },
    @{
        descripcion            = "Ropa y accesorios familiares"
        peso                   = 5.8
        valor_declarado        = 120.00
        remitente_nombre       = "Pedro Martinez"
        remitente_direccion    = "Kendall, Miami, FL"
        remitente_telefono     = "+13055553456"
        remitente_email        = "cliente.frecuente@gmail.com"
        destinatario_nombre    = "Maria Martinez"
        destinatario_direccion = "Vedado, La Habana, Cuba"
        destinatario_telefono  = "+5353333333"
        destinatario_email     = "maria.martinez@gmail.com"
        notas                  = "Ropa para toda la familia"
    },
    @{
        descripcion            = "Equipos electrónicos y componentes"
        peso                   = 4.1
        valor_declarado        = 450.00
        remitente_nombre       = "Tech Store Miami"
        remitente_direccion    = "Downtown Miami, FL"
        remitente_telefono     = "+13055554567"
        remitente_email        = "admin@packfy.com"
        destinatario_nombre    = "Carlos Ingeniero"
        destinatario_direccion = "Miramar, La Habana, Cuba"
        destinatario_telefono  = "+5354444444"
        destinatario_email     = "carlos.ing@gmail.com"
        notas                  = "Equipos delicados - no doblar"
    }
)

$enviosCreados = @()
foreach ($envio in $enviosDemo) {
    try {
        $envioJson = $envio | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method POST -Headers $headers -Body $envioJson
        $enviosCreados += $response
        Write-Host "✅ Envío creado: $($response.numero_guia) - $($response.remitente_nombre) → $($response.destinatario_nombre)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Error creando envío: $($envio.descripcion)" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📊 RESUMEN DE DATOS CREADOS:" -ForegroundColor Yellow

# Verificar totales finales
try {
    $usuarios = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/" -Method GET -Headers $headers
    $envios = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method GET -Headers $headers

    Write-Host "👥 Total usuarios: $($usuarios.count)" -ForegroundColor Green
    Write-Host "📦 Total envíos: $($envios.count)" -ForegroundColor Green

    if ($envios.results -and $envios.results.Count -gt 0) {
        Write-Host ""
        Write-Host "📋 Envíos disponibles para probar:" -ForegroundColor White
        foreach ($envio in $envios.results) {
            Write-Host "  🚚 $($envio.numero_guia) - $($envio.estado_actual) - $($envio.descripcion.Substring(0, [Math]::Min(30, $envio.descripcion.Length)))..." -ForegroundColor Cyan
        }
    }
}
catch {
    Write-Host "❌ Error verificando totales" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 ¡DATOS DE DEMO CREADOS!" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 AHORA PUEDES PROBAR EN LA WEB:" -ForegroundColor Yellow
Write-Host "   🌐 http://localhost:5173" -ForegroundColor White
Write-Host "   📧 admin@packfy.com" -ForegroundColor White
Write-Host "   🔑 admin123" -ForegroundColor White
Write-Host ""
Write-Host "💡 CON DATOS REALES PARA EXPLORAR:" -ForegroundColor Yellow
Write-Host "   👥 Múltiples usuarios en el sistema" -ForegroundColor White
Write-Host "   📦 Varios envíos con diferentes características" -ForegroundColor White
Write-Host "   🎭 Perfiles y roles configurados" -ForegroundColor White
Write-Host "   📊 Métricas con datos reales" -ForegroundColor White
Write-Host ""
