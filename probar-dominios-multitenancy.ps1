# 🌐 PROBAR SISTEMA MULTITENANCY CON DOMINIOS
# Packfy Cuba - Testing de Subdominios

Write-Host "🇨🇺 PACKFY CUBA - TESTING MULTITENANCY DOMINIOS" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Función para abrir URLs en Chrome
function Open-Chrome {
    param([string]$url, [string]$description)

    Write-Host "🌐 Abriendo: $description" -ForegroundColor Green
    Write-Host "   URL: $url" -ForegroundColor Yellow

    try {
        Start-Process "chrome.exe" -ArgumentList "--new-tab", "$url"
        Start-Sleep -Seconds 2
    }
    catch {
        Write-Host "❌ Error abriendo Chrome. Intenta manualmente: $url" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🔧 PREPARACIÓN:" -ForegroundColor Magenta
Write-Host "1. Asegúrate de que Docker esté corriendo" -ForegroundColor White
Write-Host "2. Backend debe estar en: http://localhost:8000" -ForegroundColor White
Write-Host "3. Frontend debe estar en: http://localhost:5173" -ForegroundColor White
Write-Host "4. Archivo hosts configurado (ver hosts-multitenancy.txt)" -ForegroundColor White

Write-Host ""
Write-Host "📋 CREDENCIALES DE PRUEBA:" -ForegroundColor Magenta
Write-Host "   Email: admin@packfy.cu" -ForegroundColor Yellow
Write-Host "   Password: admin123" -ForegroundColor Yellow
Write-Host "   🌟 (Tiene acceso a TODAS las empresas)" -ForegroundColor Green
Write-Host ""
Write-Host "   Alternativas:" -ForegroundColor Magenta
Write-Host "   • dueno@packfy.com / admin123 (Dueño principal)" -ForegroundColor Yellow
Write-Host "   • miami@packfy.com / admin123 (Operador Miami)" -ForegroundColor Yellow
Write-Host "   • cuba@packfy.com / admin123 (Operador Cuba)" -ForegroundColor Yellow

Write-Host ""
Write-Host "🚀 INICIANDO PRUEBAS..." -ForegroundColor Green

# Verificar si los servicios están corriendo
Write-Host ""
Write-Host "🔍 Verificando servicios..." -ForegroundColor Blue

try {
    $backend = Invoke-WebRequest -Uri "http://localhost:8000/api/sistema-info/" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Backend corriendo: http://localhost:8000" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend NO disponible en http://localhost:8000" -ForegroundColor Red
    Write-Host "   Ejecuta: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

try {
    $frontend = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Frontend corriendo: http://localhost:5173" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend NO disponible en http://localhost:5173" -ForegroundColor Red
    Write-Host "   Ejecuta: cd frontend && npm run dev" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🌐 ABRIENDO DOMINIOS DE PRUEBA..." -ForegroundColor Cyan

# 1. Dominio administrativo principal
Open-Chrome "http://localhost:5173/login" "🏛️  ADMIN PRINCIPAL - Login"

Start-Sleep -Seconds 3

# 2. Primer subdominio de empresa (REAL)
Open-Chrome "http://packfy-express.localhost:5173/login" "📦 PACKFY EXPRESS - Empresa principal"

Start-Sleep -Seconds 3

# 3. Segundo subdominio de empresa (REAL)
Open-Chrome "http://cuba-fast-delivery.localhost:5173/login" "� CUBA FAST DELIVERY - Empresa de Cuba"

Start-Sleep -Seconds 3

# 4. Tercer subdominio de empresa (REAL)
Open-Chrome "http://habana-cargo.localhost:5173/login" "🏢 HABANA CARGO - Logística Habana"

Start-Sleep -Seconds 3

# 5. Dominio administrativo alternativo
Open-Chrome "http://app.localhost:5173/admin" "⚙️  APP ADMIN - Panel administrativo"Write-Host ""
Write-Host "📝 PASOS DE PRUEBA:" -ForegroundColor Magenta
Write-Host "1. Haz login en CUALQUIERA de las pestañas" -ForegroundColor White
Write-Host "2. Observa los logs en DevTools (F12 → Console)" -ForegroundColor White
Write-Host "3. Busca mensajes: '🌐 TenantContext: Detectando dominio'" -ForegroundColor White
Write-Host "4. Verifica que cada dominio detecte la empresa correcta" -ForegroundColor White
Write-Host "5. Prueba navegar entre dominios usando el TenantSelector" -ForegroundColor White

Write-Host ""
Write-Host "🔍 LOGS ESPERADOS EN CONSOLE:" -ForegroundColor Magenta
Write-Host "🌐 TenantContext: Detectando dominio: packfy-express.localhost:5173" -ForegroundColor Gray
Write-Host "🏢 TenantContext: Subdominio de empresa detectado: packfy-express" -ForegroundColor Gray
Write-Host "✅ TenantContext: Empresa válida encontrada: PackFy Express" -ForegroundColor Gray

Write-Host ""
Write-Host "✅ PRUEBAS INICIADAS - Revisa las pestañas de Chrome abiertas" -ForegroundColor Green
Write-Host "📱 Para cerrar todas las pestañas: Ctrl+Shift+W" -ForegroundColor Yellow

Write-Host ""
Write-Host "🌐 DOMINIOS PROBADOS:" -ForegroundColor Green
Write-Host "• http://localhost:5173 → Admin general" -ForegroundColor White
Write-Host "• http://packfy-express.localhost:5173 → PackFy Express" -ForegroundColor White
Write-Host "• http://cuba-fast-delivery.localhost:5173 → Cuba Fast Delivery" -ForegroundColor White
Write-Host "• http://habana-cargo.localhost:5173 → Habana Cargo" -ForegroundColor White
Write-Host "• http://app.localhost:5173 → Panel administrativo" -ForegroundColor White

Write-Host ""
Write-Host "🔧 Si hay problemas:" -ForegroundColor Red
Write-Host "1. Verifica archivo hosts: C:\Windows\System32\drivers\etc\hosts" -ForegroundColor White
Write-Host "2. Reinicia Chrome completamente" -ForegroundColor White
Write-Host "3. Ejecuta: docker-compose restart" -ForegroundColor White
Write-Host "4. Verifica logs del backend: docker-compose logs backend" -ForegroundColor White

Read-Host "Presiona Enter para cerrar..."
