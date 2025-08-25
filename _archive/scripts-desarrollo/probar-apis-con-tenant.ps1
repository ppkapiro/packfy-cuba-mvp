# 🔧 SCRIPT DE PRUEBAS CON TENANT HEADER

Write-Host "🚀 PROBANDO APIs CON TENANT HEADER..." -ForegroundColor Green
Write-Host ""

# 1. Probar Login y obtener token
Write-Host "🔐 Obteniendo token..." -ForegroundColor Yellow
try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:5173/api/auth/login/" -Method POST -ContentType "application/json" -Body '{"email":"admin@packfy.com","password":"admin123"}'

    $accessToken = $loginResponse.access
    Write-Host "✅ Token obtenido" -ForegroundColor Green

    # Headers con autenticación y tenant
    $headers = @{
        "Authorization" = "Bearer $accessToken"
        "Content-Type"  = "application/json"
        "X-Tenant-Slug" = "packfy-express"  # Slug real según BD
    }

}
catch {
    Write-Host "❌ Error en login: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 2. Primero obtener las empresas para saber el slug correcto
Write-Host "🏢 Obteniendo empresas (sin tenant header)..." -ForegroundColor Yellow
try {
    $headersSimple = @{
        "Authorization" = "Bearer $accessToken"
        "Content-Type"  = "application/json"
    }

    $empresas = Invoke-RestMethod -Uri "http://localhost:5173/api/empresas/" -Method GET -Headers $headersSimple
    Write-Host "✅ Empresas obtenidas: $($empresas.count)" -ForegroundColor Green

    if ($empresas.results -and $empresas.results.Length -gt 0) {
        $primerEmpresa = $empresas.results[0]
        $tenantSlug = $primerEmpresa.slug
        Write-Host "🏢 Primera empresa: $($primerEmpresa.nombre) - Slug: $tenantSlug" -ForegroundColor White

        # Actualizar headers con el slug correcto
        $headers["X-Tenant-Slug"] = $tenantSlug
    }

}
catch {
    Write-Host "⚠️ Error obteniendo empresas: $($_.Exception.Message)" -ForegroundColor Yellow
    # Continuar con slug por defecto
}

Write-Host ""

# 3. Probar Usuario Actual con tenant
Write-Host "👤 Probando Usuario Actual con tenant..." -ForegroundColor Yellow
try {
    $usuarioActual = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/me/" -Method GET -Headers $headers
    Write-Host "✅ Usuario actual: $($usuarioActual.email)" -ForegroundColor Green
    if ($usuarioActual.rol) {
        Write-Host "🎭 Rol: $($usuarioActual.rol)" -ForegroundColor White
    }
}
catch {
    Write-Host "❌ Error obteniendo usuario actual: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 4. Probar Mis Perfiles con tenant
Write-Host "🎭 Probando Mis Perfiles con tenant..." -ForegroundColor Yellow
try {
    $perfiles = Invoke-RestMethod -Uri "http://localhost:5173/api/empresas/mis_perfiles/" -Method GET -Headers $headers
    Write-Host "✅ Perfiles obtenidos: $($perfiles.Length)" -ForegroundColor Green

    if ($perfiles -and $perfiles.Length -gt 0) {
        foreach ($perfil in $perfiles) {
            Write-Host "👤 Perfil: $($perfil.rol) en $($perfil.empresa.nombre)" -ForegroundColor White
        }
    }
}
catch {
    Write-Host "❌ Error obteniendo perfiles: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 5. Probar Usuarios con tenant
Write-Host "👥 Probando Lista Usuarios con tenant..." -ForegroundColor Yellow
try {
    $usuarios = Invoke-RestMethod -Uri "http://localhost:5173/api/usuarios/" -Method GET -Headers $headers
    Write-Host "✅ Usuarios obtenidos: $($usuarios.count)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error obteniendo usuarios: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 6. Probar Envíos con tenant
Write-Host "📦 Probando Envíos con tenant..." -ForegroundColor Yellow
try {
    $envios = Invoke-RestMethod -Uri "http://localhost:5173/api/envios/" -Method GET -Headers $headers
    Write-Host "✅ Envíos obtenidos: $($envios.count)" -ForegroundColor Green

    if ($envios.results -and $envios.results.Length -gt 0) {
        $primerEnvio = $envios.results[0]
        Write-Host "📄 Primer envío: $($primerEnvio.numero_guia) - Estado: $($primerEnvio.estado_actual)" -ForegroundColor White
    }
}
catch {
    Write-Host "❌ Error obteniendo envíos: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 PRUEBAS CON TENANT COMPLETADAS" -ForegroundColor Cyan
Write-Host "Tenant usado: $($headers['X-Tenant-Slug'])" -ForegroundColor White
Write-Host ""
