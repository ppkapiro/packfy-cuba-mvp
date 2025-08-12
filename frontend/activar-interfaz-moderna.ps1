#!/usr/bin/env pwsh
# ACTIVACION COMPLETA INTERFAZ MODERNA MOVIL

Write-Host "🎨 ACTIVANDO INTERFAZ MODERNA Y MÓVIL" -ForegroundColor Green
Write-Host ""

# 1. Hacer backup de configuración actual
Write-Host "💾 Creando backup de configuración..." -ForegroundColor Cyan
Copy-Item "vite.config.ts" "vite.config.backup.ts" -Force
Write-Host "   ✅ Backup creado: vite.config.backup.ts" -ForegroundColor Green

# 2. Activar configuración móvil
Write-Host "📱 Activando configuración móvil..." -ForegroundColor Cyan
Copy-Item "vite.config.mobile.ts" "vite.config.ts" -Force
Write-Host "   ✅ Configuración móvil activada" -ForegroundColor Green

# 3. Verificar que package.json tenga script móvil
Write-Host "📦 Verificando scripts npm..." -ForegroundColor Cyan
$packageJson = Get-Content "package.json" | ConvertFrom-Json

if (-not $packageJson.scripts."dev:mobile") {
    Write-Host "   📝 Agregando script dev:mobile" -ForegroundColor Yellow
    $packageJson.scripts | Add-Member -Name "dev:mobile" -Value "vite --config vite.config.mobile.ts --host 0.0.0.0 --port 5173" -MemberType NoteProperty
    $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json"
}
Write-Host "   ✅ Scripts verificados" -ForegroundColor Green

# 4. Limpiar caché
Write-Host "🧹 Limpiando caché..." -ForegroundColor Cyan
if (Test-Path "node_modules/.vite") {
    Remove-Item "node_modules/.vite" -Recurse -Force
    Write-Host "   ✅ Caché Vite limpiado" -ForegroundColor Green
}

# 5. Verificar archivos CSS modernos
Write-Host "🎨 Verificando estilos modernos..." -ForegroundColor Cyan
$cssFiles = @(
    "src/styles/design-system.css",
    "src/styles/mobile-pwa.css", 
    "src/styles/mobile-optimized.css",
    "src/styles/master-premium.css"
)

foreach ($cssFile in $cssFiles) {
    if (Test-Path $cssFile) {
        Write-Host "   ✅ $cssFile" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $cssFile FALTANTE" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🚀 INTERFAZ MODERNA ACTIVADA" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Para usar en móvil:" -ForegroundColor White
Write-Host "   • Configuración móvil activada" -ForegroundColor Gray
Write-Host "   • Estilos premium importados" -ForegroundColor Gray  
Write-Host "   • PWA optimizada" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 URLs de acceso:" -ForegroundColor White
Write-Host "   • PC: http://localhost:5173" -ForegroundColor Cyan
Write-Host "   • Móvil: http://192.168.12.178:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚡ REINICIA LOS SERVIDORES AHORA" -ForegroundColor Yellow
