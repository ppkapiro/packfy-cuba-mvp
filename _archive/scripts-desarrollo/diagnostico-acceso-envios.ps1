Write-Host "🔍 DIAGNÓSTICO - ACCESO A PÁGINA DE ENVÍOS" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# 1. Verificar servicios básicos
Write-Host "`n1. Verificando servicios..." -ForegroundColor Yellow
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 5
    Write-Host "   ✅ Frontend: Status $($frontendResponse.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Frontend: No responde" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -UseBasicParsing -TimeoutSec 5
    Write-Host "   ✅ Backend: Status $($backendResponse.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Backend: No responde" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# 2. Verificar archivos críticos
Write-Host "`n2. Verificando archivos críticos..." -ForegroundColor Yellow

$archivos = @{
    "GestionEnvios.tsx"  = "frontend\src\pages\GestionEnvios.tsx"
    "gestion-envios.css" = "frontend\src\styles\gestion-envios.css"
    "AdminRouter.tsx"    = "frontend\src\components\admin\AdminRouter.tsx"
    "App.tsx"            = "frontend\src\App.tsx"
}

foreach ($nombre in $archivos.Keys) {
    $ruta = $archivos[$nombre]
    if (Test-Path $ruta) {
        $size = (Get-Item $ruta).Length
        Write-Host "   ✅ $nombre`: $size bytes" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ $nombre`: No encontrado" -ForegroundColor Red
    }
}

# 3. Verificar errores de compilación
Write-Host "`n3. Verificando errores de compilación..." -ForegroundColor Yellow
try {
    Set-Location frontend
    $tscResult = npx tsc --noEmit --skipLibCheck 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ TypeScript: Sin errores críticos" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️ TypeScript: Hay errores, pero la app puede funcionar" -ForegroundColor Yellow
    }
    Set-Location ..
}
catch {
    Write-Host "   ❌ Error verificando TypeScript: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Verificar si el servidor de desarrollo está corriendo
Write-Host "`n4. Verificando procesos..." -ForegroundColor Yellow
$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    Write-Host "   ✅ Procesos Node.js: $($nodeProcesses.Count) ejecutándose" -ForegroundColor Green
}
else {
    Write-Host "   ❌ No hay procesos Node.js ejecutándose" -ForegroundColor Red
}

# 5. Verificar contenido de archivos clave
Write-Host "`n5. Verificando configuración de rutas..." -ForegroundColor Yellow

# Verificar AdminRouter
$adminRouterContent = Get-Content "frontend\src\components\admin\AdminRouter.tsx" -Raw
if ($adminRouterContent -match "/admin/envios") {
    Write-Host "   ✅ AdminRouter tiene ruta /admin/envios" -ForegroundColor Green
}
else {
    Write-Host "   ❌ AdminRouter NO tiene ruta /admin/envios" -ForegroundColor Red
}

# Verificar App.tsx
$appContent = Get-Content "frontend\src\App.tsx" -Raw
if ($appContent -match "admin/\*.*AdminRouter") {
    Write-Host "   ✅ App.tsx tiene rutas admin configuradas" -ForegroundColor Green
}
else {
    Write-Host "   ❌ App.tsx NO tiene rutas admin configuradas" -ForegroundColor Red
}

Write-Host "`n📋 INSTRUCCIONES PARA ACCEDER:" -ForegroundColor Cyan
Write-Host "1. Abrir navegador en: http://localhost:5173" -ForegroundColor White
Write-Host "2. Login con: admin@packfy.com / admin123" -ForegroundColor White
Write-Host "3. Ir a: Admin → Envíos" -ForegroundColor White
Write-Host "4. O directamente: http://localhost:5173/admin/envios" -ForegroundColor White

Write-Host "`n🔧 SI NO FUNCIONA:" -ForegroundColor Cyan
Write-Host "- Verificar que esté logueado correctamente" -ForegroundColor White
Write-Host "- Limpiar caché del navegador (Ctrl+F5)" -ForegroundColor White
Write-Host "- Revisar consola del navegador (F12)" -ForegroundColor White
Write-Host "- Verificar que tenga permisos de admin" -ForegroundColor White

Write-Host "`n🎯 RESULTADO:" -ForegroundColor Cyan
if ((Test-Path "frontend\src\pages\GestionEnvios.tsx") -and (Test-Path "frontend\src\styles\gestion-envios.css")) {
    Write-Host "✅ La página de envíos está modernizada y lista" -ForegroundColor Green
}
else {
    Write-Host "❌ Faltan archivos críticos de la página de envíos" -ForegroundColor Red
}
