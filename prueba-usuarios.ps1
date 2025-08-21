# Script de prueba rápida para la página de usuarios
# Verifica el estado y conectividad

$frontendUrl = "http://localhost:5173"
$backendUrl = "http://localhost:8000"

Write-Host "🔍 PRUEBA RÁPIDA - PÁGINA DE USUARIOS" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Verificar servicios básicos
Write-Host "`n1. Verificando servicios..." -ForegroundColor Yellow
try {
    $frontendResponse = Invoke-WebRequest -Uri $frontendUrl -Method GET -TimeoutSec 5
    Write-Host "   ✅ Frontend: Status $($frontendResponse.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Frontend: $($_.Exception.Message)" -ForegroundColor Red
    return
}

try {
    $backendResponse = Invoke-WebRequest -Uri "$backendUrl/api/health/" -Method GET -TimeoutSec 5
    Write-Host "   ✅ Backend: Status $($backendResponse.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Backend: $($_.Exception.Message)" -ForegroundColor Red
    return
}

# Verificar archivo GestionUsuarios.tsx
Write-Host "`n2. Verificando archivo GestionUsuarios..." -ForegroundColor Yellow
$usuariosFile = "frontend/src/components/admin/GestionUsuarios.tsx"
if (Test-Path $usuariosFile) {
    $fileSize = (Get-Item $usuariosFile).Length
    Write-Host "   ✅ GestionUsuarios.tsx: $fileSize bytes" -ForegroundColor Green

    # Verificar contenido básico
    $content = Get-Content $usuariosFile -Raw
    if ($content -match "export default GestionUsuarios") {
        Write-Host "   ✅ Export correcto" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Export incorrecto" -ForegroundColor Red
    }

    if ($content -match "Gestión de Usuarios") {
        Write-Host "   ✅ Título presente" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Título faltante" -ForegroundColor Red
    }
}
else {
    Write-Host "   ❌ Archivo no encontrado" -ForegroundColor Red
    return
}

# Verificar AdminRouter
Write-Host "`n3. Verificando AdminRouter..." -ForegroundColor Yellow
$routerFile = "frontend/src/components/admin/AdminRouter.tsx"
if (Test-Path $routerFile) {
    $routerContent = Get-Content $routerFile -Raw
    if ($routerContent -match "GestionUsuarios.*from.*GestionUsuarios") {
        Write-Host "   ✅ Import GestionUsuarios correcto" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Import GestionUsuarios faltante" -ForegroundColor Red
    }

    if ($routerContent -match "/admin/usuarios.*GestionUsuarios") {
        Write-Host "   ✅ Ruta /admin/usuarios configurada" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Ruta /admin/usuarios no configurada" -ForegroundColor Red
    }
}
else {
    Write-Host "   ❌ AdminRouter no encontrado" -ForegroundColor Red
}

# Probar endpoint usuarios con autenticación
Write-Host "`n4. Probando endpoint de usuarios..." -ForegroundColor Yellow

$loginData = @{
    email    = "admin@packfy.com"
    password = "admin123"
    empresa  = "packfy-express"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$backendUrl/api/auth/login/" -Method POST -Body $loginData -ContentType "application/json"
    $token = $loginResponse.access
    Write-Host "   ✅ Login exitoso" -ForegroundColor Green

    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type"  = "application/json"
    }

    $usuariosResponse = Invoke-RestMethod -Uri "$backendUrl/api/usuarios/" -Method GET -Headers $headers
    $usuarios = $usuariosResponse.results || $usuariosResponse
    Write-Host "   ✅ Endpoint usuarios: $($usuarios.Count) usuarios encontrados" -ForegroundColor Green

    if ($usuarios.Count -gt 0) {
        $primerUsuario = $usuarios[0]
        Write-Host "   📋 Primer usuario: $($primerUsuario.nombre) $($primerUsuario.apellidos) ($($primerUsuario.email))" -ForegroundColor Gray
    }

}
catch {
    Write-Host "   ❌ Error probando endpoint: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎯 URLs PARA PROBAR:" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
Write-Host "🔗 Login: $frontendUrl/login" -ForegroundColor White
Write-Host "🔗 Admin Dashboard: $frontendUrl/admin" -ForegroundColor White
Write-Host "🔗 Gestión Usuarios: $frontendUrl/admin/usuarios" -ForegroundColor White
Write-Host "🔗 Configuración: $frontendUrl/admin/configuracion" -ForegroundColor White
Write-Host "🔗 Reportes: $frontendUrl/admin/reportes" -ForegroundColor White

Write-Host "`n💡 INSTRUCCIONES:" -ForegroundColor Cyan
Write-Host "1. Abrir navegador en: $frontendUrl" -ForegroundColor White
Write-Host "2. Login: admin@packfy.com / admin123" -ForegroundColor White
Write-Host "3. Ir a Admin → Usuarios" -ForegroundColor White
Write-Host "4. Verificar que aparezca la lista de usuarios" -ForegroundColor White
Write-Host "5. Abrir DevTools (F12) para ver logs de consola" -ForegroundColor White

Write-Host "`n🔧 Si la página está en blanco:" -ForegroundColor Yellow
Write-Host "- Verificar logs en DevTools (F12 → Console)" -ForegroundColor Gray
Write-Host "- Verificar que el token sea válido" -ForegroundColor Gray
Write-Host "- Verificar que la API responda correctamente" -ForegroundColor Gray

Write-Host "`n✅ Sistema listo para pruebas!" -ForegroundColor Green
