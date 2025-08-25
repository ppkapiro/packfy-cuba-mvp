# 🧪 PRUEBA DIRECTA - GESTIÓN GRATUITA Y PREMIUM
# Script para verificar que las nuevas funcionalidades estén funcionando

Write-Host "🧪 INICIANDO PRUEBAS DE GESTIÓN GRATUITA Y PREMIUM" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan

# Verificar que los servicios estén funcionando
Write-Host "`n🔍 Verificando servicios..." -ForegroundColor Yellow
$servicios = docker-compose ps --format "table {{.Name}}`t{{.Status}}"
Write-Host $servicios

# URLs a probar
$urls = @(
    "https://localhost:5173",
    "https://localhost:5173/login",
    "https://localhost:5173/dashboard",
    "https://localhost:5173/envios",
    "https://localhost:5173/gestion/gratuita",
    "https://localhost:5173/gestion/premium"
)

Write-Host "`n🌐 URLs configuradas:" -ForegroundColor Yellow
foreach ($url in $urls) {
    Write-Host "  - $url" -ForegroundColor White
}

# Prueba de navegación
Write-Host "`n🎯 FLUJO DE PRUEBA MANUAL:" -ForegroundColor Green
Write-Host "1. Ir a: https://localhost:5173" -ForegroundColor Cyan
Write-Host "2. Hacer login con: admin@packfy.cu / admin123" -ForegroundColor Cyan
Write-Host "3. Ir al Dashboard" -ForegroundColor Cyan
Write-Host "4. Hacer clic en 'Gestión' (debe mostrar selector de modos)" -ForegroundColor Cyan
Write-Host "5. Probar 'Gestión Gratuita' - debe mostrar lista de envíos" -ForegroundColor Cyan
Write-Host "6. Regresar y probar 'Gestión Premium' - debe mostrar funciones avanzadas" -ForegroundColor Cyan

Write-Host "`n📊 VERIFICACIONES ESPERADAS:" -ForegroundColor Yellow
Write-Host "✅ Enlace 'Gestión' muestra selector con dos modos" -ForegroundColor Green
Write-Host "✅ Modo Gratuito: Lista básica de envíos" -ForegroundColor Green
Write-Host "✅ Modo Premium: Botones 'Exportar' y 'Análisis'" -ForegroundColor Green
Write-Host "✅ Títulos diferentes: 'Gestión Gratuita' vs 'Gestión Premium'" -ForegroundColor Green
Write-Host "✅ Iconos diferentes: Package vs Star" -ForegroundColor Green

# Abrir Chrome en la página principal
Write-Host "`n🚀 Abriendo Chrome..." -ForegroundColor Cyan
Start-Process "chrome.exe" -ArgumentList "https://localhost:5173"

Write-Host "`n✨ INSTRUCCIONES:" -ForegroundColor Yellow
Write-Host "1. Acepta el certificado SSL en Chrome" -ForegroundColor White
Write-Host "2. Sigue el flujo de prueba manual arriba" -ForegroundColor White
Write-Host "3. Reporta si las funcionalidades están funcionando" -ForegroundColor White

Write-Host "`n🎯 PRUEBA COMPLETADA - Revisa Chrome y reporta resultados" -ForegroundColor Green
