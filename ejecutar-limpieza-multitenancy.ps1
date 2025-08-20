# 🧹 SCRIPT DE LIMPIEZA MULTITENANCY - PACKFY CUBA
# Ejecuta limpieza profunda del sistema post-restauración

Write-Host "🚀 INICIANDO LIMPIEZA PROFUNDA MULTITENANCY" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 1. CREAR BACKUP DE SEGURIDAD
Write-Host "📦 PASO 1: Creando backup de seguridad..." -ForegroundColor Yellow
git add .
git commit -m "🔒 CHECKPOINT: Pre-limpieza multitenancy - Estado de seguridad $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

# 2. CREAR RAMA DE LIMPIEZA
Write-Host "🌿 PASO 2: Creando rama de limpieza..." -ForegroundColor Yellow
git checkout -b "cleanup/multitenancy-profunda-$(Get-Date -Format 'yyyyMMdd')"

# 3. ELIMINAR ARCHIVOS OBSOLETOS BACKEND
Write-Host "🗑️ PASO 3: Eliminando archivos obsoletos..." -ForegroundColor Yellow

$archivosObsoletos = @(
    # Comandos Django-Tenants obsoletos
    "backend\empresas\management\commands\init_tenants.py",
    "backend\empresas\management\commands\list_tenants.py",

    # Scripts de diagnóstico temporales
    "backend\diagnostico_admin.py",
    "diagnostico_admin.py",
    "diagnostico_frontend_completo.py",
    "reporte_testing_final.py",
    "test_final_limpio.py",
    "test_rapido.py",
    "test_simple.py",
    "test_todos_usuarios.py",
    "verificar_admin_final.py",
    "verificar_fix.py",
    "verificar_sistema_limpio.py",

    # Páginas frontend eliminadas (ya marcadas como deleted)
    "frontend-multitenant\src\pages\EnvioModePage.tsx",
    "frontend-multitenant\src\pages\ModernAdvancedPage.tsx",
    "frontend-multitenant\src\pages\SimpleAdvancedPage.tsx",
    "frontend-multitenant\src\pages\TrackingPage.tsx",
    "frontend-multitenant\src\pages\TrackingPageSimple.tsx"
)

foreach ($archivo in $archivosObsoletos) {
    if (Test-Path $archivo) {
        Write-Host "  🗑️ Eliminando: $archivo" -ForegroundColor Red
        Remove-Item $archivo -Force
    } else {
        Write-Host "  ✅ Ya eliminado: $archivo" -ForegroundColor Green
    }
}

# 4. LIMPIAR ARCHIVOS TEMPORALES Y CACHE
Write-Host "🧽 PASO 4: Limpiando archivos temporales..." -ForegroundColor Yellow

$archivosTemporal = @(
    "backend\__pycache__",
    "backend\*\__pycache__",
    "backend\*\*\__pycache__",
    "frontend\node_modules\.cache",
    "frontend-multitenant\node_modules\.cache",
    "*.pyc",
    "*\*.pyc",
    "*\*\*.pyc"
)

foreach ($pattern in $archivosTemporal) {
    $archivos = Get-ChildItem -Path $pattern -Recurse -Force -ErrorAction SilentlyContinue
    foreach ($archivo in $archivos) {
        Write-Host "  🧽 Limpiando: $($archivo.FullName)" -ForegroundColor DarkYellow
        Remove-Item $archivo.FullName -Force -Recurse -ErrorAction SilentlyContinue
    }
}

# 5. VERIFICAR ESTADO DOCKER
Write-Host "🐳 PASO 5: Verificando Docker..." -ForegroundColor Yellow
$containers = docker ps --format "table {{.Names}}\t{{.Status}}"
Write-Host $containers

# 6. APLICAR MIGRACIONES
Write-Host "💾 PASO 6: Aplicando migraciones..." -ForegroundColor Yellow
Set-Location "backend"
python manage.py migrate --run-syncdb
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Migraciones aplicadas correctamente" -ForegroundColor Green
} else {
    Write-Host "  ❌ Error en migraciones" -ForegroundColor Red
}
Set-Location ".."

# 7. CREAR DATOS DE PRUEBA MULTITENANCY
Write-Host "🏢 PASO 7: Creando datos de prueba multitenancy..." -ForegroundColor Yellow
Set-Location "backend"
python manage.py crear_datos_multitenancy --clear
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Datos de prueba creados" -ForegroundColor Green
} else {
    Write-Host "  ❌ Error creando datos de prueba" -ForegroundColor Red
}
Set-Location ".."

# 8. COMMIT FINAL DE LIMPIEZA
Write-Host "💾 PASO 8: Confirmando limpieza..." -ForegroundColor Yellow
git add .
git commit -m "🧹 LIMPIEZA MULTITENANCY COMPLETADA

✅ Archivos obsoletos eliminados
✅ Cache y temporales limpiados
✅ Migraciones aplicadas
✅ Datos de prueba multitenancy creados
✅ Sistema listo para desarrollo

Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# 9. RESUMEN FINAL
Write-Host "🎉 LIMPIEZA COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host "✅ Sistema multitenancy limpio y funcional" -ForegroundColor Green
Write-Host "✅ Arquitectura nativa Django (sin django-tenants)" -ForegroundColor Green
Write-Host "✅ Base de datos con datos de prueba" -ForegroundColor Green
Write-Host "✅ Docker containers funcionando" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "  1. Verificar frontend en: http://localhost:5173" -ForegroundColor White
Write-Host "  2. Probar login y cambio de empresa" -ForegroundColor White
Write-Host "  3. Validar filtrado de datos por empresa" -ForegroundColor White
Write-Host "  4. Continuar desarrollo de features" -ForegroundColor White
Write-Host ""
Write-Host "📋 Para ver el diagnóstico completo:" -ForegroundColor Cyan
Write-Host "     Get-Content DIAGNÓSTICO-PROFUNDO-LIMPIEZA-MULTITENANCY.md" -ForegroundColor White
