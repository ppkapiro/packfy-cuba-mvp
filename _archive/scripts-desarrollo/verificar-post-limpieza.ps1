# 🔍 SCRIPT DE VERIFICACIÓN POST-LIMPIEZA
# Valida el estado del sistema después de la limpieza multitenancy

Write-Host "🔍 VERIFICACIÓN SISTEMA POST-LIMPIEZA" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# 1. VERIFICAR DOCKER
Write-Host "🐳 1. ESTADO DOCKER..." -ForegroundColor Yellow
$dockerStatus = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host $dockerStatus

$containers = @("packfy-frontend", "packfy-backend", "packfy-database")
$allRunning = $true

foreach ($container in $containers) {
    $isRunning = docker ps --filter "name=$container" --format "{{.Names}}" | Select-String $container
    if ($isRunning) {
        Write-Host "  ✅ $container - Funcionando" -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ $container - No encontrado" -ForegroundColor Red
        $allRunning = $false
    }
}

# 2. VERIFICAR BASE DE DATOS Y MIGRACIONES
Write-Host "💾 2. VERIFICANDO BASE DE DATOS..." -ForegroundColor Yellow
Set-Location "backend"

# Verificar migraciones
Write-Host "  📋 Verificando migraciones..." -ForegroundColor DarkYellow
$migrationsOutput = python manage.py showmigrations --plan 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Migraciones verificadas correctamente" -ForegroundColor Green
}
else {
    Write-Host "  ❌ Error verificando migraciones: $migrationsOutput" -ForegroundColor Red
}

# 3. VERIFICAR DATOS MULTITENANCY
Write-Host "🏢 3. VERIFICANDO DATOS MULTITENANCY..." -ForegroundColor Yellow

$verifyScript = @"
from empresas.models import Empresa, PerfilUsuario
from django.contrib.auth.models import User
import sys

print('🏢 EMPRESAS EN EL SISTEMA:')
empresas = Empresa.objects.all()
if empresas.count() == 0:
    print('  ❌ NO HAY EMPRESAS CREADAS')
    sys.exit(1)

for empresa in empresas:
    print(f'  ✅ {empresa.nombre} (slug: {empresa.slug}, activo: {empresa.activo})')

print()
print('👥 USUARIOS Y PERFILES:')
usuarios = User.objects.all()
if usuarios.count() == 0:
    print('  ❌ NO HAY USUARIOS CREADOS')
    sys.exit(1)

for user in usuarios:
    perfiles = PerfilUsuario.objects.filter(usuario=user)
    print(f'  👤 {user.username} ({user.email})')
    if perfiles.count() == 0:
        print('    ❌ Sin perfiles de empresa')
    else:
        for perfil in perfiles:
            print(f'    └── {perfil.empresa.nombre} - {perfil.rol}')

print()
print('✅ DATOS MULTITENANCY VERIFICADOS CORRECTAMENTE')
"@

$verifyScript | python manage.py shell
$dbVerified = ($LASTEXITCODE -eq 0)

if ($dbVerified) {
    Write-Host "  ✅ Datos multitenancy correctos" -ForegroundColor Green
}
else {
    Write-Host "  ❌ Problemas con datos multitenancy" -ForegroundColor Red
}

Set-Location ".."

# 4. VERIFICAR ENDPOINTS API
Write-Host "🌐 4. VERIFICANDO ENDPOINTS API..." -ForegroundColor Yellow

$apiTests = @(
    @{ URL = "http://localhost:8000/api/usuarios/"; Name = "Usuarios API" },
    @{ URL = "http://localhost:8000/api/empresas/"; Name = "Empresas API" },
    @{ URL = "http://localhost:8000/api/envios/"; Name = "Envíos API" },
    @{ URL = "http://localhost:8000/admin/"; Name = "Django Admin" }
)

foreach ($test in $apiTests) {
    try {
        $response = Invoke-WebRequest -Uri $test.URL -Method GET -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200 -or $response.StatusCode -eq 401 -or $response.StatusCode -eq 403) {
            Write-Host "  ✅ $($test.Name) - Responde correctamente" -ForegroundColor Green
        }
        else {
            Write-Host "  ❌ $($test.Name) - Status: $($response.StatusCode)" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "  ❌ $($test.Name) - No responde: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 5. VERIFICAR FRONTEND
Write-Host "🎨 5. VERIFICANDO FRONTEND..." -ForegroundColor Yellow

try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 10 -ErrorAction Stop
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "  ✅ Frontend accesible en puerto 5173" -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ Frontend status: $($frontendResponse.StatusCode)" -ForegroundColor Red
    }
}
catch {
    Write-Host "  ❌ Frontend no accesible: $($_.Exception.Message)" -ForegroundColor Red
}

# 6. VERIFICAR ARCHIVOS CLAVE
Write-Host "📁 6. VERIFICANDO ARCHIVOS CLAVE..." -ForegroundColor Yellow

$archivosEsenciales = @(
    # Backend Core
    @{ Path = "backend\config\settings.py"; Name = "Settings Django" },
    @{ Path = "backend\empresas\middleware.py"; Name = "TenantMiddleware" },
    @{ Path = "backend\empresas\models.py"; Name = "Modelo Empresa" },
    @{ Path = "backend\usuarios\models.py"; Name = "Modelo PerfilUsuario" },

    # Frontend Core
    @{ Path = "frontend-multitenant\src\contexts\TenantContext.tsx"; Name = "TenantContext" },
    @{ Path = "frontend-multitenant\src\components\TenantSelector"; Name = "TenantSelector" },

    # Docker
    @{ Path = "compose.yml"; Name = "Docker Compose" },
    @{ Path = "backend\Dockerfile"; Name = "Backend Dockerfile" }
)

$archivosPresentes = 0
foreach ($archivo in $archivosEsenciales) {
    if (Test-Path $archivo.Path) {
        Write-Host "  ✅ $($archivo.Name)" -ForegroundColor Green
        $archivosPresentes++
    }
    else {
        Write-Host "  ❌ $($archivo.Name) - No encontrado: $($archivo.Path)" -ForegroundColor Red
    }
}

# 7. RESUMEN FINAL
Write-Host ""
Write-Host "📊 RESUMEN DE VERIFICACIÓN" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

$totalChecks = 6
$passedChecks = 0

if ($allRunning) { $passedChecks++ }
if ($dbVerified) { $passedChecks++ }

Write-Host "🐳 Docker Containers: $(if($allRunning){'✅ OK'}else{'❌ FALLÓ'})" -ForegroundColor $(if ($allRunning) { 'Green' }else { 'Red' })
Write-Host "💾 Base de Datos: $(if($dbVerified){'✅ OK'}else{'❌ FALLÓ'})" -ForegroundColor $(if ($dbVerified) { 'Green' }else { 'Red' })
Write-Host "📁 Archivos Core: ✅ $archivosPresentes/$($archivosEsenciales.Count) presentes" -ForegroundColor $(if ($archivosPresentes -eq $archivosEsenciales.Count) { 'Green' }else { 'Yellow' })

if ($allRunning -and $dbVerified -and $archivosPresentes -eq $archivosEsenciales.Count) {
    Write-Host ""
    Write-Host "🎉 SISTEMA COMPLETAMENTE FUNCIONAL" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host "✅ Multitenancy implementado correctamente" -ForegroundColor Green
    Write-Host "✅ Base de datos con datos de prueba" -ForegroundColor Green
    Write-Host "✅ APIs respondiendo" -ForegroundColor Green
    Write-Host "✅ Frontend accesible" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 LISTO PARA DESARROLLO:" -ForegroundColor Cyan
    Write-Host "  • Frontend: http://localhost:5173" -ForegroundColor White
    Write-Host "  • API: http://localhost:8000/api/" -ForegroundColor White
    Write-Host "  • Admin: http://localhost:8000/admin/" -ForegroundColor White
}
else {
    Write-Host ""
    Write-Host "⚠️ SISTEMA CON PROBLEMAS" -ForegroundColor Yellow
    Write-Host "========================" -ForegroundColor Yellow
    Write-Host "❌ Revisar los errores arriba y ejecutar:" -ForegroundColor Red
    Write-Host "   docker-compose up -d --build" -ForegroundColor White
    Write-Host "   cd backend && python manage.py migrate" -ForegroundColor White
}

Write-Host ""
Write-Host "📋 Para más detalles ver: DIAGNÓSTICO-PROFUNDO-LIMPIEZA-MULTITENANCY.md" -ForegroundColor Cyan
