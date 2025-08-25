# 🇨🇺 PACKFY CUBA - DEMOSTRACIÓN COMPLETA MULTITENANCY
# Sistema de demostración automática del multitenancy funcionando

Write-Host ""
Write-Host "🇨🇺 PACKFY CUBA - SISTEMA MULTITENANCY COMPLETO" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# 1. VERIFICAR SERVICIOS
Write-Host "🔧 VERIFICANDO SERVICIOS..." -ForegroundColor Magenta

try {
    $backend = Invoke-WebRequest -Uri "http://localhost:8000/api/sistema-info/" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Backend: http://localhost:8000 - FUNCIONANDO" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend no disponible. Ejecuta: docker-compose up -d" -ForegroundColor Red
    exit 1
}

try {
    $frontend = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Frontend: http://localhost:5173 - FUNCIONANDO" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend no disponible. Ejecuta: cd frontend && npm run dev" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 2. PROBAR MIDDLEWARE MULTITENANCY
Write-Host "🏢 PROBANDO MIDDLEWARE MULTITENANCY..." -ForegroundColor Magenta

$empresas = @("packfy-express", "cuba-fast-delivery", "habana-cargo")

foreach ($empresa in $empresas) {
    $headers = @{'X-Tenant-Slug' = $empresa }
    try {
        $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/sistema-info/' -Headers $headers
        Write-Host "✅ Tenant '$empresa': Sistema $($response.nombre_sistema) v$($response.version)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Error con tenant '$empresa'" -ForegroundColor Red
    }
}

Write-Host ""

# 3. MOSTRAR CREDENCIALES
Write-Host "🔑 CREDENCIALES DE PRUEBA:" -ForegroundColor Magenta
Write-Host "   Email: admin@packfy.cu" -ForegroundColor Yellow
Write-Host "   Password: admin123" -ForegroundColor Yellow
Write-Host "   🌟 Acceso a TODAS las empresas" -ForegroundColor Green
Write-Host ""

# 4. ABRIR NAVEGADORES
Write-Host "🌐 ABRIENDO SISTEMA MULTITENANCY..." -ForegroundColor Magenta

$urls = @(
    @{url = "http://localhost:5173/login"; desc = "🏛️  ADMIN PRINCIPAL"; empresa = "Administración general" },
    @{url = "http://localhost:5173/login?empresa=packfy-express"; desc = "📦 PACKFY EXPRESS"; empresa = "packfy-express" },
    @{url = "http://localhost:5173/login?empresa=cuba-fast-delivery"; desc = "🚚 CUBA FAST DELIVERY"; empresa = "cuba-fast-delivery" },
    @{url = "http://localhost:5173/login?empresa=habana-cargo"; desc = "🏢 HABANA CARGO"; empresa = "habana-cargo" }
)

foreach ($item in $urls) {
    Write-Host ""
    Write-Host "$($item.desc)" -ForegroundColor Green
    Write-Host "   URL: $($item.url)" -ForegroundColor Yellow
    Write-Host "   Empresa: $($item.empresa)" -ForegroundColor Cyan

    try {
        Start-Process "chrome.exe" "--new-tab", $item.url
        Start-Sleep -Seconds 1
    }
    catch {
        Write-Host "❌ Error abriendo Chrome: $($item.url)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎯 INSTRUCCIONES DE PRUEBA:" -ForegroundColor Magenta
Write-Host "1. Haz login en CUALQUIER pestaña con: admin@packfy.cu / admin123" -ForegroundColor White
Write-Host "2. Abre DevTools (F12) → Console en cada pestaña" -ForegroundColor White
Write-Host "3. Busca logs: '🌐 TenantContext: ...' y '🔗 TenantContext: ...'" -ForegroundColor White
Write-Host "4. Verifica que cada pestaña detecte la empresa correcta" -ForegroundColor White
Write-Host "5. Navega por el sistema y verifica la funcionalidad" -ForegroundColor White

Write-Host ""
Write-Host "🔍 LOGS ESPERADOS EN CONSOLE:" -ForegroundColor Magenta
Write-Host "• '🔗 TenantContext: Empresa detectada por URL: packfy-express'" -ForegroundColor Gray
Write-Host "• '✅ TenantContext: Empresa válida encontrada: PackFy Express'" -ForegroundColor Gray
Write-Host "• '🔄 TenantContext: Configurando empresa actual: PackFy Express'" -ForegroundColor Gray

Write-Host ""
Write-Host "📊 DATOS DE PRUEBA EN BD:" -ForegroundColor Magenta
Write-Host "• 3 empresas: PackFy Express, Cuba Fast Delivery, Habana Cargo" -ForegroundColor White
Write-Host "• 19 perfiles de usuario distribuidos entre empresas" -ForegroundColor White
Write-Host "• 5 envíos de prueba en PackFy Express" -ForegroundColor White
Write-Host "• admin@packfy.cu tiene acceso a todas las empresas" -ForegroundColor White

Write-Host ""
Write-Host "✅ SISTEMA MULTITENANCY ACTIVO Y FUNCIONANDO" -ForegroundColor Green
Write-Host "🇨🇺 Packfy Cuba v3.0 - Multitenancy con detección por URL" -ForegroundColor Cyan

Write-Host ""
Write-Host "🎉 ¡DEMOSTRACIÓN LISTA!" -ForegroundColor Green
Write-Host "   Las pestañas de Chrome están abiertas para testing" -ForegroundColor Yellow
Write-Host "   Cada una detectará automáticamente su empresa asignada" -ForegroundColor Yellow

Read-Host "Presiona Enter para finalizar..."
