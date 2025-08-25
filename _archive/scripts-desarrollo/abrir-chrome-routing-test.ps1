# Script para abrir Packfy en Chrome y probar routing de admin
Write-Host "🌐 ABRIENDO PACKFY EN CHROME - TESTING ROUTING ADMIN" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$urls = @(
    "http://localhost:5173",
    "http://localhost:5173/login",
    "http://localhost:5173/admin/dashboard",
    "http://localhost:5173/admin/envios"
)

Write-Host "`n🔧 INSTRUCCIONES DE PRUEBA:" -ForegroundColor Yellow
Write-Host "1. Se abrirá Chrome con las URLs principales" -ForegroundColor White
Write-Host "2. Hacer login con: admin@packfy.com / packfy123" -ForegroundColor White
Write-Host "3. Verificar que la navegación muestra opciones de admin" -ForegroundColor White
Write-Host "4. ¡CLAVE! Hacer clic en 'Envíos' y verificar que va a /admin/envios" -ForegroundColor Yellow
Write-Host "5. Confirmar que se ve la interfaz de admin, no la básica" -ForegroundColor White

Write-Host "`n🎯 CAMBIOS IMPLEMENTADOS:" -ForegroundColor Green
Write-Host "✅ AdminNavigation → rutas /admin/*" -ForegroundColor White
Write-Host "✅ AdminRouter → maneja /admin/envios, /admin/usuarios, etc." -ForegroundColor White
Write-Host "✅ App.tsx → /admin/* → AdminRouter" -ForegroundColor White

# Abrir Chrome con las URLs
foreach ($url in $urls) {
    Write-Host "`n🚀 Abriendo: $url" -ForegroundColor Green
    Start-Process "chrome.exe" $url
    Start-Sleep 1
}

Write-Host "`n📝 DATOS DE LOGIN:" -ForegroundColor Magenta
Write-Host "Email: admin@packfy.com" -ForegroundColor White
Write-Host "Password: packfy123" -ForegroundColor White
Write-Host "Tenant: packfy-express (se selecciona automáticamente)" -ForegroundColor White

Write-Host "`n🔍 QUÉ VERIFICAR:" -ForegroundColor Cyan
Write-Host "• Navegación superior muestra opciones de dueño" -ForegroundColor White
Write-Host "• Clic en 'Envíos' navega a /admin/envios" -ForegroundColor White
Write-Host "• URL en el navegador debe ser /admin/envios" -ForegroundColor White
Write-Host "• Interfaz debe mostrar GestionEnvios con contexto de admin" -ForegroundColor White
Write-Host "• NO debe mostrar la interfaz básica de antes" -ForegroundColor Yellow

Write-Host "`n🎉 ¡Chrome abierto! Prueba el routing actualizado" -ForegroundColor Green
