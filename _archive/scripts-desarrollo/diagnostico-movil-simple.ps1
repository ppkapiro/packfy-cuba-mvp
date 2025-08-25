# PACKFY CUBA - DIAGNOSTICO COMPLETO MOVIL
# Verifica todos los aspectos de conectividad movil

Write-Host "DIAGNOSTICO COMPLETO PACKFY MOVIL" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

# 1. Verificar IP actual
Write-Host "`n1. IP de la maquina:" -ForegroundColor Cyan
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress
Write-Host "   IP actual: $ip" -ForegroundColor White

# 2. Verificar servicios Docker
Write-Host "`n2. Estado de servicios Docker:" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 3. Verificar puertos abiertos
Write-Host "`n3. Puertos en uso:" -ForegroundColor Cyan
try {
    $port5173 = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
    $port8000 = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    
    if ($port5173) { Write-Host "   OK Puerto 5173 (Frontend) activo" -ForegroundColor Green }
    else { Write-Host "   ERROR Puerto 5173 (Frontend) inactivo" -ForegroundColor Red }
    
    if ($port8000) { Write-Host "   OK Puerto 8000 (Backend) activo" -ForegroundColor Green }
    else { Write-Host "   ERROR Puerto 8000 (Backend) inactivo" -ForegroundColor Red }
} catch {
    Write-Host "   WARNING No se pudieron verificar puertos" -ForegroundColor Yellow
}

# 4. Verificar reglas de firewall
Write-Host "`n4. Reglas de Firewall:" -ForegroundColor Cyan
try {
    netsh advfirewall firewall show rule name="Packfy PWA HTTPS" >$null 2>&1
    if ($LASTEXITCODE -eq 0) { 
        Write-Host "   OK Regla firewall para puerto 5173 existe" -ForegroundColor Green 
    } else { 
        Write-Host "   ERROR Regla firewall para puerto 5173 NO existe" -ForegroundColor Red 
    }
} catch {
    Write-Host "   ERROR No se pudieron verificar reglas de firewall" -ForegroundColor Red
}

# 5. Probar conectividad local
Write-Host "`n5. Pruebas de conectividad:" -ForegroundColor Cyan

# Test localhost
try {
    Invoke-WebRequest -Uri "https://localhost:5173" -Method Head -SkipCertificateCheck -TimeoutSec 5 >$null
    Write-Host "   OK HTTPS localhost funciona" -ForegroundColor Green
} catch {
    Write-Host "   ERROR HTTPS localhost falla" -ForegroundColor Red
}

# Test IP local
try {
    Invoke-WebRequest -Uri "https://$ip`:5173" -Method Head -SkipCertificateCheck -TimeoutSec 5 >$null
    Write-Host "   OK HTTPS desde IP funciona" -ForegroundColor Green
} catch {
    Write-Host "   ERROR HTTPS desde IP falla" -ForegroundColor Red
}

# 6. Informacion para el movil
Write-Host "`n6. URLs para acceso movil:" -ForegroundColor Cyan
Write-Host "   PWA: https://$ip`:5173" -ForegroundColor White
Write-Host "   API: http://$ip`:8000" -ForegroundColor White

# 7. Credenciales de prueba
Write-Host "`n7. Credenciales de prueba:" -ForegroundColor Cyan
Write-Host "   Email: admin@packfy.cu" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White

Write-Host "`nDiagnostico completado!" -ForegroundColor Green
Write-Host "Si hay errores de firewall, ejecuta como administrador:" -ForegroundColor Yellow
Write-Host ".\configurar-firewall-movil.ps1" -ForegroundColor Yellow
