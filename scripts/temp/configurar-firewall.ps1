# Script para configurar Firewall de Windows para Packfy
# Ejecutar como Administrador

Write-Host "🔥 Configurando Firewall para Packfy..." -ForegroundColor Yellow

# Eliminar reglas existentes si existen
try {
    netsh advfirewall firewall delete rule name="Packfy Frontend" 2>$null
    netsh advfirewall firewall delete rule name="Packfy Backend" 2>$null
    Write-Host "✅ Reglas anteriores eliminadas" -ForegroundColor Green
} catch {
    Write-Host "ℹ️ No había reglas anteriores" -ForegroundColor Blue
}

# Crear reglas para entrada (inbound)
Write-Host "📡 Creando regla para Frontend (puerto 5173)..." -ForegroundColor Cyan
netsh advfirewall firewall add rule name="Packfy Frontend" dir=in action=allow protocol=TCP localport=5173

Write-Host "🔧 Creando regla para Backend (puerto 8000)..." -ForegroundColor Cyan
netsh advfirewall firewall add rule name="Packfy Backend" dir=in action=allow protocol=TCP localport=8000

# Verificar reglas creadas
Write-Host "`n🔍 Verificando reglas creadas:" -ForegroundColor Green
netsh advfirewall firewall show rule name="Packfy Frontend"
netsh advfirewall firewall show rule name="Packfy Backend"

Write-Host "`n✅ Configuración completada!" -ForegroundColor Green
Write-Host "📱 Ahora deberías poder acceder desde móvil usando:" -ForegroundColor Yellow
Write-Host "   Frontend: http://192.168.12.179:5173" -ForegroundColor White
Write-Host "   Backend:  http://192.168.12.179:8000" -ForegroundColor White

Read-Host "`nPresiona Enter para cerrar"
