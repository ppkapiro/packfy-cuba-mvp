# 🔒 VERIFICACIÓN ACCESO HTTPS - PACKFY CUBA MVP
# Verificando acceso correcto a las URLs HTTPS

Write-Host "🇨🇺 PACKFY CUBA - VERIFICACIÓN ACCESO HTTPS" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Yellow

Write-Host "`n🔍 Verificando servicios HTTPS..." -ForegroundColor Green

# 1. Frontend HTTPS
Write-Host "`n📱 1. FRONTEND HTTPS (puerto 5173):" -ForegroundColor Green
try {
    $frontendResponse = Invoke-WebRequest -Uri "https://localhost:5173" -Method HEAD -TimeoutSec 10 -SkipCertificateCheck
    Write-Host "✅ Frontend HTTPS accesible: HTTP $($frontendResponse.StatusCode)" -ForegroundColor Green
    Write-Host "🌐 URL correcta: https://localhost:5173" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Frontend HTTPS no accesible: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "⚠️  Verificando HTTP como respaldo..." -ForegroundColor Yellow
    try {
        $httpResponse = Invoke-WebRequest -Uri "http://localhost:5173" -Method HEAD -TimeoutSec 5
        Write-Host "⚠️  Frontend HTTP accesible: HTTP $($httpResponse.StatusCode)" -ForegroundColor Yellow
        Write-Host "📝 Nota: Usar HTTPS para funcionalidad completa" -ForegroundColor Yellow
    }
    catch {
        Write-Host "❌ Frontend HTTP tampoco accesible" -ForegroundColor Red
    }
}

# 2. Backend HTTPS
Write-Host "`n🔧 2. BACKEND HTTPS (puerto 8443):" -ForegroundColor Green
try {
    $backendResponse = Invoke-WebRequest -Uri "https://localhost:8443/admin/" -Method HEAD -TimeoutSec 10 -SkipCertificateCheck
    Write-Host "✅ Backend HTTPS accesible: HTTP $($backendResponse.StatusCode)" -ForegroundColor Green
    Write-Host "🌐 URL correcta: https://localhost:8443" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Backend HTTPS no accesible: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Estado de contenedores
Write-Host "`n🐳 3. ESTADO DE CONTENEDORES:" -ForegroundColor Green
$containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host $containers

# 4. Verificar certificados
Write-Host "`n🔒 4. VERIFICANDO CERTIFICADOS SSL:" -ForegroundColor Green
if (Test-Path "frontend\certs") {
    $certs = Get-ChildItem "frontend\certs" -Filter "*.pem" -ErrorAction SilentlyContinue
    if ($certs) {
        Write-Host "✅ Certificados SSL encontrados:" -ForegroundColor Green
        foreach ($cert in $certs) {
            Write-Host "   📄 $($cert.Name) - $($cert.Length) bytes" -ForegroundColor Cyan
        }
    }
    else {
        Write-Host "⚠️  No se encontraron certificados .pem" -ForegroundColor Yellow
    }
}
else {
    Write-Host "❌ Directorio de certificados no encontrado" -ForegroundColor Red
}

# 5. URLs de acceso
Write-Host "`n🌐 5. URLS DE ACCESO CORRETAS:" -ForegroundColor Yellow
Write-Host "==============================" -ForegroundColor Yellow
Write-Host "📱 Frontend (Dashboard):  https://localhost:5173" -ForegroundColor Cyan
Write-Host "🔧 Backend API:          https://localhost:8443" -ForegroundColor Cyan
Write-Host "🔐 Admin Django:         https://localhost:8443/admin/" -ForegroundColor Cyan
Write-Host "📊 Login API:            https://localhost:8443/api/auth/login/" -ForegroundColor Cyan

Write-Host "`n⚠️  IMPORTANTE:" -ForegroundColor Red
Write-Host "   • Siempre usar HTTPS (no HTTP)" -ForegroundColor Yellow
Write-Host "   • Los estilos CSS requieren HTTPS para cargarse correctamente" -ForegroundColor Yellow
Write-Host "   • El sistema está configurado para SSL/TLS" -ForegroundColor Yellow

Write-Host "`n🎯 ACCESO RECOMENDADO:" -ForegroundColor Magenta
Write-Host "   👉 Abrir: https://localhost:5173" -ForegroundColor Green
Write-Host "   👉 Usuario: admin@packfy.cu / admin" -ForegroundColor Green
Write-Host "   👉 Verificar estilos CSS funcionando" -ForegroundColor Green

Write-Host "`n🚀 SISTEMA HTTPS VERIFICADO" -ForegroundColor Magenta
Write-Host "=============================================" -ForegroundColor Yellow
