# 🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA

Write-Host "🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA PACKFY" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar contenedores
Write-Host "📦 CONTENEDORES DOCKER:" -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host ""

# 2. Verificar datos en PostgreSQL
Write-Host "🗄️ DATOS EN BASE DE DATOS:" -ForegroundColor Yellow
Write-Host "Empresas disponibles:"
docker exec packfy-database psql -U postgres -d packfy -c "SELECT id, nombre, slug FROM empresas_empresa;" 2>$null
Write-Host ""

Write-Host "Usuarios (primeros 5):"
docker exec packfy-database psql -U postgres -d packfy -c "SELECT id, email FROM usuarios_usuario LIMIT 5;" 2>$null
Write-Host ""

Write-Host "Perfiles de empresa (primeros 5):"
docker exec packfy-database psql -U postgres -d packfy -c "SELECT pu.id, u.email, e.slug, pu.rol FROM empresas_perfilusuario pu JOIN usuarios_usuario u ON pu.usuario_id = u.id JOIN empresas_empresa e ON pu.empresa_id = e.id LIMIT 5;" 2>$null
Write-Host ""

# 3. Probar login con diferentes usuarios
Write-Host "🔐 PROBANDO AUTENTICACIÓN:" -ForegroundColor Yellow

$usuarios_test = @(
    @{email = "dueno@packfy.com"; password = "dueno123!" },
    @{email = "admin@packfy.com"; password = "admin123" },
    @{email = "superadmin@packfy.com"; password = "admin123" }
)

foreach ($usuario in $usuarios_test) {
    Write-Host "Probando usuario: $($usuario.email)" -ForegroundColor White
    try {
        $loginBody = @{
            email    = $usuario.email
            password = $usuario.password
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "http://localhost:5173/api/auth/login/" -Method POST -ContentType "application/json" -Body $loginBody
        Write-Host "  ✅ Login exitoso - Token obtenido" -ForegroundColor Green

        # Guardamos el token para usar después
        $token = $response.access
        $usuarioValido = $usuario.email
        break
    }
    catch {
        Write-Host "  ❌ Login fallido: $($_.Exception.Message)" -ForegroundColor Red
    }
}

if ($token) {
    Write-Host ""
    Write-Host "🏢 PROBANDO ACCESO A EMPRESAS:" -ForegroundColor Yellow

    # Headers sin tenant
    $headersSimple = @{
        "Authorization" = "Bearer $token"
        "Content-Type"  = "application/json"
    }

    try {
        $empresas = Invoke-RestMethod -Uri "http://localhost:5173/api/empresas/" -Method GET -Headers $headersSimple
        Write-Host "✅ Empresas API funcionando - Encontradas: $($empresas.count)" -ForegroundColor Green

        if ($empresas.results -and $empresas.results.Length -gt 0) {
            foreach ($empresa in $empresas.results) {
                Write-Host "  🏢 $($empresa.nombre) - Slug: $($empresa.slug)" -ForegroundColor White
            }
        }
    }
    catch {
        Write-Host "❌ Error accediendo a empresas: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎯 DIAGNÓSTICO COMPLETADO" -ForegroundColor Cyan
