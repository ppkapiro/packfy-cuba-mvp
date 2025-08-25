# 🔍 PACKFY CUBA - DIAGNÓSTICO COMPLETO MÓVIL
# Verifica todos los aspectos de conectividad móvil

Write-Host "🔍 DIAGNÓSTICO COMPLETO PACKFY MÓVIL" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

# 1. Verificar IP actual
Write-Host "`n1️⃣ IP de la máquina:" -ForegroundColor Cyan
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress
Write-Host "   IP actual: $ip" -ForegroundColor White

# 2. Verificar servicios Docker
Write-Host "`n2️⃣ Estado de servicios Docker:" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 3. Verificar puertos abiertos
Write-Host "`n3️⃣ Puertos en uso:" -ForegroundColor Cyan
try {
    $port5173 = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
    $port8000 = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    
    if ($port5173) { Write-Host "   ✅ Puerto 5173 (Frontend) activo" -ForegroundColor Green }
    else { Write-Host "   ❌ Puerto 5173 (Frontend) inactivo" -ForegroundColor Red }
    
    if ($port8000) { Write-Host "   ✅ Puerto 8000 (Backend) activo" -ForegroundColor Green }
    else { Write-Host "   ❌ Puerto 8000 (Backend) inactivo" -ForegroundColor Red }
} catch {
    Write-Host "   ⚠️  No se pudieron verificar puertos" -ForegroundColor Yellow
}

# 4. Verificar reglas de firewall
Write-Host "`n4️⃣ Reglas de Firewall:" -ForegroundColor Cyan
try {
    $rule5173 = netsh advfirewall firewall show rule name="Packfy PWA HTTPS" 2>$null
    $rule8000 = netsh advfirewall firewall show rule name="Packfy API HTTP" 2>$null
    
    if ($LASTEXITCODE -eq 0) { Write-Host "   ✅ Regla firewall para puerto 5173 existe" -ForegroundColor Green }
    else { Write-Host "   ❌ Regla firewall para puerto 5173 NO existe" -ForegroundColor Red }
} catch {
    Write-Host "   ❌ No se pudieron verificar reglas de firewall" -ForegroundColor Red
}

# 5. Probar conectividad local
Write-Host "`n5️⃣ Pruebas de conectividad:" -ForegroundColor Cyan

# Test localhost
try {
    $localTest = Invoke-WebRequest -Uri "https://localhost:5173" -Method Head -SkipCertificateCheck -TimeoutSec 5
    Write-Host "   ✅ HTTPS localhost funciona" -ForegroundColor Green
} catch {
    Write-Host "   ❌ HTTPS localhost falla: $($_.Exception.Message)" -ForegroundColor Red
}

# Test IP local
try {
    $ipTest = Invoke-WebRequest -Uri "https://$ip`:5173" -Method Head -SkipCertificateCheck -TimeoutSec 5
    Write-Host "   ✅ HTTPS desde IP funciona" -ForegroundColor Green
} catch {
    Write-Host "   ❌ HTTPS desde IP falla: $($_.Exception.Message)" -ForegroundColor Red
}

# 6. Información para el móvil
Write-Host "`n6 URLs para acceso movil:" -ForegroundColor Cyan
Write-Host "   PWA: https://$ip`:5173" -ForegroundColor White
Write-Host "   API: http://$ip`:8000" -ForegroundColor White

# 7. Credenciales de prueba
Write-Host "`n7 Credenciales de prueba:" -ForegroundColor Cyan
Write-Host "   Email: admin@packfy.cu" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White

Write-Host "`n✅ Diagnóstico completado!" -ForegroundColor Green
Write-Host "Si hay errores, ejecuta como administrador: .\configurar-firewall-movil.ps1" -ForegroundColor Yellow
