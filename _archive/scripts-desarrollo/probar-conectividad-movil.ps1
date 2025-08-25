# PACKFY CUBA - PRUEBA DE CONECTIVIDAD MOVIL
# Script para verificar acceso desde movil

Write-Host "PACKFY - DIAGNOSTICO CONECTIVIDAD MOVIL" -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Yellow

# 1. Verificar IP
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress
Write-Host "`n1. IP del servidor: $ip" -ForegroundColor Cyan

# 2. Verificar servicios
Write-Host "`n2. Estado de servicios:" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Select-Object -First 4

# 3. Verificar puertos
Write-Host "`n3. Puertos activos:" -ForegroundColor Cyan
$port5173 = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
$port8000 = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue

if ($port5173) { Write-Host "   ✓ Puerto 5173 (Frontend) - ACTIVO" -ForegroundColor Green }
else { Write-Host "   ✗ Puerto 5173 (Frontend) - INACTIVO" -ForegroundColor Red }

if ($port8000) { Write-Host "   ✓ Puerto 8000 (Backend) - ACTIVO" -ForegroundColor Green }
else { Write-Host "   ✗ Puerto 8000 (Backend) - INACTIVO" -ForegroundColor Red }

# 4. Verificar firewall
Write-Host "`n4. Reglas de firewall:" -ForegroundColor Cyan
try {
    $result5173 = netsh advfirewall firewall show rule name="Packfy PWA HTTPS" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Regla para puerto 5173 - EXISTE" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Regla para puerto 5173 - NO EXISTE" -ForegroundColor Red
    }
} catch {
    Write-Host "   ✗ No se pudo verificar firewall" -ForegroundColor Red
}

try {
    $result8000 = netsh advfirewall firewall show rule name="Packfy API HTTP" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Regla para puerto 8000 - EXISTE" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Regla para puerto 8000 - NO EXISTE" -ForegroundColor Red
    }
} catch {
    Write-Host "   ✗ No se pudo verificar firewall" -ForegroundColor Red
}

# 5. Probar conectividad local
Write-Host "`n5. Pruebas de conectividad:" -ForegroundColor Cyan

# Test frontend desde IP
try {
    $test = Invoke-WebRequest -Uri "https://$ip`:5173" -Method Head -SkipCertificateCheck -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   ✓ Frontend desde IP - FUNCIONA" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Frontend desde IP - FALLA" -ForegroundColor Red
    Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test API desde IP
try {
    $test = Invoke-WebRequest -Uri "http://$ip`:8000/api/" -Method Head -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   ✓ API desde IP - FUNCIONA" -ForegroundColor Green
} catch {
    Write-Host "   ✗ API desde IP - FALLA" -ForegroundColor Red
    Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

# 6. URLs para el movil
Write-Host "`n6. URLs para acceso movil:" -ForegroundColor Green
Write-Host "   📱 PWA: https://$ip`:5173" -ForegroundColor White
Write-Host "   🔌 API: http://$ip`:8000" -ForegroundColor White

# 7. Credenciales
Write-Host "`n7. Credenciales de login:" -ForegroundColor Green
Write-Host "   📧 Email: admin@packfy.cu" -ForegroundColor White
Write-Host "   🔑 Password: admin123" -ForegroundColor White

# 8. Instrucciones
Write-Host "`n8. Instrucciones para el movil:" -ForegroundColor Cyan
Write-Host "   1. Abre Chrome en tu movil" -ForegroundColor White
Write-Host "   2. Navega a: https://$ip`:5173" -ForegroundColor Yellow
Write-Host "   3. Si aparece 'No es seguro', acepta el certificado" -ForegroundColor White
Write-Host "   4. Usa las credenciales de arriba para login" -ForegroundColor White

# 9. Solucion de problemas
Write-Host "`n9. Si no funciona:" -ForegroundColor Red
Write-Host "   - Configura firewall como ADMINISTRADOR:" -ForegroundColor Yellow
Write-Host "     .\configurar-firewall-movil.ps1" -ForegroundColor White
Write-Host "   - Verifica que PC y movil esten en la misma red WiFi" -ForegroundColor Yellow
Write-Host "   - Reinicia el router si es necesario" -ForegroundColor Yellow

Write-Host "`n✅ Diagnostico completado!" -ForegroundColor Green
