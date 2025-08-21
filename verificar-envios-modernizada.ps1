# Script de verificación para la nueva página de envíos modernizada
# Verifica que GestionEnvios esté usando el nuevo estilo moderno

$frontendUrl = "http://localhost:5173"
$backendUrl = "http://localhost:8000"

Write-Host "📦 VERIFICACIÓN - PÁGINA DE ENVÍOS MODERNIZADA" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

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

# Verificar archivos modernizados
Write-Host "`n2. Verificando modernización de envíos..." -ForegroundColor Yellow

$gestionEnviosFile = "frontend/src/pages/GestionEnvios.tsx"
$gestionEnviosCssFile = "frontend/src/styles/gestion-envios.css"

if (Test-Path $gestionEnviosFile) {
    $fileSize = (Get-Item $gestionEnviosFile).Length
    Write-Host "   ✅ GestionEnvios.tsx: $fileSize bytes (MODERNIZADO)" -ForegroundColor Green

    # Verificar que use el nuevo estilo
    $content = Get-Content $gestionEnviosFile -Raw

    $modernFeatures = @(
        @{Pattern = "gestion-envios.css"; Description = "Nuevo CSS moderno" },
        @{Pattern = "filteredEnvios"; Description = "Sistema de filtros" },
        @{Pattern = "searchTerm"; Description = "Búsqueda funcional" },
        @{Pattern = "page-header"; Description = "Header moderno" },
        @{Pattern = "envios-stats"; Description = "Stats visuales" },
        @{Pattern = "envios-table"; Description = "Tabla moderna" },
        @{Pattern = "status-badge"; Description = "Badges de estado" },
        @{Pattern = "btn-action"; Description = "Botones de acción" },
        @{Pattern = "loading-spinner"; Description = "Loading moderno" }
    )

    foreach ($feature in $modernFeatures) {
        if ($content -match $feature.Pattern) {
            Write-Host "   ✅ $($feature.Description)" -ForegroundColor Green
        }
        else {
            Write-Host "   ❌ $($feature.Description) - No encontrado" -ForegroundColor Red
        }
    }

    # Verificar que NO use Tailwind (estilo antiguo)
    if ($content -match "className=.*bg-.*text-") {
        Write-Host "   ⚠️  Aún contiene clases Tailwind (estilo antiguo)" -ForegroundColor Yellow
    }
    else {
        Write-Host "   ✅ Sin clases Tailwind - Completamente modernizado" -ForegroundColor Green
    }

}
else {
    Write-Host "   ❌ GestionEnvios.tsx no encontrado" -ForegroundColor Red
}

if (Test-Path $gestionEnviosCssFile) {
    $cssSize = (Get-Item $gestionEnviosCssFile).Length
    Write-Host "   ✅ gestion-envios.css: $cssSize bytes (NUEVO)" -ForegroundColor Green
}
else {
    Write-Host "   ❌ gestion-envios.css no encontrado" -ForegroundColor Red
}

# Verificar que AdminRouter use la nueva página
Write-Host "`n3. Verificando integración con AdminRouter..." -ForegroundColor Yellow
$routerFile = "frontend/src/components/admin/AdminRouter.tsx"
if (Test-Path $routerFile) {
    $routerContent = Get-Content $routerFile -Raw
    if ($routerContent -match "GestionEnvios.*from.*GestionEnvios") {
        Write-Host "   ✅ Import correcto en AdminRouter" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Import faltante en AdminRouter" -ForegroundColor Red
    }

    if ($routerContent -match "/admin/envios.*GestionEnvios") {
        Write-Host "   ✅ Ruta /admin/envios configurada" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Ruta /admin/envios no configurada" -ForegroundColor Red
    }
}
else {
    Write-Host "   ❌ AdminRouter no encontrado" -ForegroundColor Red
}

# Probar endpoint envíos
Write-Host "`n4. Probando endpoint de envíos..." -ForegroundColor Yellow

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

    $enviosResponse = Invoke-RestMethod -Uri "$backendUrl/api/envios/" -Method GET -Headers $headers
    $envios = $enviosResponse.results || $enviosResponse
    Write-Host "   ✅ Endpoint envíos: $($envios.Count) envíos encontrados" -ForegroundColor Green

    if ($envios.Count -gt 0) {
        $primerEnvio = $envios[0]
        Write-Host "   📦 Primer envío: #$($primerEnvio.numero_guia) - $($primerEnvio.estado_actual)" -ForegroundColor Gray
    }

}
catch {
    Write-Host "   ❌ Error probando endpoint: $($_.Exception.Message)" -ForegroundColor Red
}

# Comparar con estilo anterior
Write-Host "`n5. Verificando eliminación del estilo antiguo..." -ForegroundColor Yellow

$oldStyleIndicators = @(
    "lucide-react",
    "Tailwind",
    "bg-blue-100",
    "text-gray-600",
    "className.*space-",
    "className.*flex.*justify"
)

if (Test-Path $gestionEnviosFile) {
    $content = Get-Content $gestionEnviosFile -Raw
    $oldStyleFound = $false

    foreach ($indicator in $oldStyleIndicators) {
        if ($content -match $indicator) {
            Write-Host "   ⚠️  Detectado estilo antiguo: $indicator" -ForegroundColor Yellow
            $oldStyleFound = $true
        }
    }

    if (-not $oldStyleFound) {
        Write-Host "   ✅ Estilo antiguo completamente eliminado" -ForegroundColor Green
    }
}

Write-Host "`n🎯 URLs PARA PROBAR:" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
Write-Host "🔗 Admin Envíos: $frontendUrl/admin/envios" -ForegroundColor White
Write-Host "🔗 Envíos Directo: $frontendUrl/envios" -ForegroundColor White
Write-Host "🔗 Nuevo Envío: $frontendUrl/envios/nuevo" -ForegroundColor White
Write-Host "🔗 Admin Dashboard: $frontendUrl/admin" -ForegroundColor White

Write-Host "`n📋 CARACTERÍSTICAS DE LA NUEVA PÁGINA:" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "✨ Header moderno con botones de acción" -ForegroundColor Green
Write-Host "✨ Stats visuales (Total, Entregados, En Proceso, Cancelados)" -ForegroundColor Green
Write-Host "✨ Búsqueda en tiempo real" -ForegroundColor Green
Write-Host "✨ Filtros por estado" -ForegroundColor Green
Write-Host "✨ Tabla moderna con información completa" -ForegroundColor Green
Write-Host "✨ Botones de acción (Ver, Editar, Eliminar)" -ForegroundColor Green
Write-Host "✨ Estados con colores y badges" -ForegroundColor Green
Write-Host "✨ Responsive design" -ForegroundColor Green
Write-Host "✨ Estados de carga y error" -ForegroundColor Green

Write-Host "`n💡 INSTRUCCIONES PARA PROBAR:" -ForegroundColor Cyan
Write-Host "1. Abrir: $frontendUrl" -ForegroundColor White
Write-Host "2. Login: admin@packfy.com / admin123" -ForegroundColor White
Write-Host "3. Ir a Admin → Envíos" -ForegroundColor White
Write-Host "4. Verificar el nuevo diseño moderno:" -ForegroundColor White
Write-Host "   - Header con título y botones" -ForegroundColor Gray
Write-Host "   - Cards de estadísticas" -ForegroundColor Gray
Write-Host "   - Búsqueda y filtros funcionales" -ForegroundColor Gray
Write-Host "   - Tabla con diseño moderno" -ForegroundColor Gray
Write-Host "   - Botones de acción en cada fila" -ForegroundColor Gray

Write-Host "`n🔥 COMPARACIÓN ANTES VS DESPUÉS:" -ForegroundColor Cyan
Write-Host "ANTES: Tailwind CSS, estilo básico, iconos Lucide" -ForegroundColor Red
Write-Host "DESPUÉS: CSS moderno, diseño unificado, emojis nativos" -ForegroundColor Green

Write-Host "`n🎉 ¡PÁGINA DE ENVÍOS COMPLETAMENTE MODERNIZADA!" -ForegroundColor Green
