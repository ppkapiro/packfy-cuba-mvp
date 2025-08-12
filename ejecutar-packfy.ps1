# Script de PowerShell para ejecutar Packfy Cuba v2.0
# Con todas las mejoras avanzadas implementadas

Write-Host "🚀 INICIANDO PACKFY CUBA v2.0 - EXPERIENCIA PREMIUM" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Yellow

# Navegar al directorio del frontend
Set-Location "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend"

Write-Host "📂 Directorio actual: $(Get-Location)" -ForegroundColor Green

# Verificar que existe package.json
if (Test-Path "package.json") {
    Write-Host "✅ package.json encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ package.json no encontrado" -ForegroundColor Red
    exit 1
}

# Mostrar información del proyecto
Write-Host "`n🎨 CARACTERÍSTICAS IMPLEMENTADAS:" -ForegroundColor Magenta
Write-Host "• ✨ 12+ animaciones CSS cinematográficas" -ForegroundColor White
Write-Host "• 🇨🇺 Partículas cubanas patrióticas" -ForegroundColor White
Write-Host "• 💎 Efectos hover 3D premium" -ForegroundColor White
Write-Host "• 🎭 Modal de pago con cristal blur" -ForegroundColor White
Write-Host "• 📱 Responsividad perfecta móvil" -ForegroundColor White
Write-Host "• 🚀 Performance optimizada GPU" -ForegroundColor White

Write-Host "`n🎯 MODO FREEMIUM ACTIVO:" -ForegroundColor Yellow
Write-Host "• 🆓 Modo Simple: 100% Gratis" -ForegroundColor Green
Write-Host "• 👑 Modo Premium: $5 USD - Experiencia cinematográfica" -ForegroundColor Yellow

Write-Host "`n🔧 Iniciando servidor de desarrollo..." -ForegroundColor Cyan
Write-Host "📱 La aplicación se abrirá en: http://localhost:5173" -ForegroundColor Green
Write-Host "`n⚡ PRESIONA CTRL+C PARA DETENER" -ForegroundColor Red

# Ejecutar el servidor de desarrollo
try {
    npm run dev
} catch {
    Write-Host "❌ Error al iniciar el servidor" -ForegroundColor Red
    Write-Host "💡 Intentando instalar dependencias..." -ForegroundColor Yellow
    npm install
    Write-Host "🔄 Reintentando iniciar servidor..." -ForegroundColor Cyan
    npm run dev
}

Write-Host "`n🎉 ¡DISFRUTA LA EXPERIENCIA PACKFY CUBA v2.0!" -ForegroundColor Green
