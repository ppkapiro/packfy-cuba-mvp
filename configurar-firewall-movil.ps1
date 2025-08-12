# 🔥 PACKFY CUBA - CONFIGURAR FIREWALL PARA ACCESO MÓVIL
# Ejecutar como Administrador

Write-Host "🔥 Configurando Firewall para Packfy PWA..." -ForegroundColor Yellow

# Eliminar reglas existentes si existen
try {
    netsh advfirewall firewall delete rule name="Packfy PWA HTTPS" 2>$null
    netsh advfirewall firewall delete rule name="Packfy API HTTP" 2>$null
} catch {}

# Crear reglas para HTTPS frontend (puerto 5173)
netsh advfirewall firewall add rule name="Packfy PWA HTTPS" dir=in action=allow protocol=TCP localport=5173
Write-Host "✅ Regla HTTPS creada para puerto 5173" -ForegroundColor Green

# Crear reglas para HTTP API backend (puerto 8000)
netsh advfirewall firewall add rule name="Packfy API HTTP" dir=in action=allow protocol=TCP localport=8000
Write-Host "✅ Regla HTTP creada para puerto 8000" -ForegroundColor Green

# Verificar las reglas
Write-Host "`n🔍 Verificando reglas creadas:" -ForegroundColor Cyan
netsh advfirewall firewall show rule name="Packfy PWA HTTPS"
netsh advfirewall firewall show rule name="Packfy API HTTP"

Write-Host "`n✅ Configuración completada!" -ForegroundColor Green
Write-Host "📱 Ahora puedes acceder desde el móvil a:" -ForegroundColor White
Write-Host "   https://192.168.12.178:5173" -ForegroundColor Yellow
