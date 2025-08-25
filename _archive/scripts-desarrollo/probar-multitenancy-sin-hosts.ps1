# 🧪 PROBAR MULTITENANCY SIN MODIFICAR HOSTS
# Packfy Cuba - Testing usando parámetros y headers

Write-Host "🇨🇺 PACKFY CUBA - TESTING MULTITENANCY AVANZADO" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host ""
Write-Host "📋 CREDENCIALES DE PRUEBA:" -ForegroundColor Magenta
Write-Host "   Email: admin@packfy.cu" -ForegroundColor Yellow
Write-Host "   Password: admin123" -ForegroundColor Yellow
Write-Host "   🌟 (Tiene acceso a TODAS las empresas)" -ForegroundColor Green

Write-Host ""
Write-Host "🌐 ABRIENDO SISTEMA MULTITENANCY..." -ForegroundColor Green

# Función para abrir Chrome con configuración específica
function Open-MultitenancyTest {
    param([string]$url, [string]$description, [string]$empresa)

    Write-Host "🌐 $description" -ForegroundColor Green
    Write-Host "   URL: $url" -ForegroundColor Yellow
    Write-Host "   Empresa: $empresa" -ForegroundColor Cyan

    try {
        Start-Process "chrome.exe" --new-tab, "$url"
        Start-Sleep -Seconds 2
    }
    catch {
        Write-Host "❌ Error abriendo Chrome: $url" -ForegroundColor Red
    }
    Write-Host ""
}

# 1. Admin principal
Open-MultitenancyTest "http://localhost:5173/login" "🏛️  ADMIN PRINCIPAL" "Administración general"

# 2. Simular empresa PackFy Express
Open-MultitenancyTest "http://localhost:5173/login?empresa=packfy-express" "📦 PACKFY EXPRESS" "packfy-express"

# 3. Simular empresa Cuba Fast Delivery
Open-MultitenancyTest "http://localhost:5173/login?empresa=cuba-fast-delivery" "🚚 CUBA FAST DELIVERY" "cuba-fast-delivery"

# 4. Simular empresa Habana Cargo
Open-MultitenancyTest "http://localhost:5173/login?empresa=habana-cargo" "🏢 HABANA CARGO" "habana-cargo"

Write-Host "📱 TESTING CON DEVTOOLS:" -ForegroundColor Magenta
Write-Host "1. Abre DevTools en cualquier pestaña (F12)" -ForegroundColor White
Write-Host "2. Ve a la pestaña Console" -ForegroundColor White
Write-Host "3. Busca logs que comiencen con '🌐 TenantContext'" -ForegroundColor White
Write-Host "4. Verifica que detecte las empresas correctamente" -ForegroundColor White

Write-Host ""
Write-Host "🔧 TESTING MANUAL ADICIONAL:" -ForegroundColor Magenta
Write-Host "En la consola del navegador, ejecuta:" -ForegroundColor White
Write-Host "   window.location.hostname" -ForegroundColor Gray
Write-Host "   localStorage.getItem('tenant_slug')" -ForegroundColor Gray

Write-Host ""
Write-Host "✅ PRUEBAS INICIADAS" -ForegroundColor Green
Write-Host "🔍 Verifica los logs en cada pestaña de Chrome" -ForegroundColor Yellow

Read-Host "Presiona Enter para continuar..."
