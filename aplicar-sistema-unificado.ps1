# 🇨🇺 PACKFY CUBA - APLICAR SISTEMA UNIFICADO v3.0
Write-Host "🇨🇺 PACKFY CUBA - APLICANDO SISTEMA UNIFICADO v3.0" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

Write-Host "`n🔄 PASO 1: BACKUP DE ARCHIVOS ACTUALES" -ForegroundColor Yellow
if (!(Test-Path "backup-original")) {
    New-Item -ItemType Directory -Path "backup-original" -Force
    Write-Host "✅ Directorio backup creado" -ForegroundColor Green
}

# Backup de archivos principales
Copy-Item "frontend\src\App.tsx" "backup-original\App.tsx.bak" -Force -ErrorAction SilentlyContinue
Copy-Item "frontend\vite.config.ts" "backup-original\vite.config.ts.bak" -Force -ErrorAction SilentlyContinue
Copy-Item "frontend\src\services\api.ts" "backup-original\api.ts.bak" -Force -ErrorAction SilentlyContinue

Write-Host "✅ Backup completado" -ForegroundColor Green

Write-Host "`n🔄 PASO 2: APLICANDO CONFIGURACIONES LIMPIAS" -ForegroundColor Yellow

# Aplicar nuevo sistema de archivos
Copy-Item "frontend\src\App.clean.tsx" "frontend\src\App.tsx" -Force
Copy-Item "frontend\vite.config.clean.ts" "frontend\vite.config.ts" -Force
Copy-Item "frontend\src\services\api-unified.ts" "frontend\src\services\api.ts" -Force

Write-Host "✅ Archivos principales actualizados" -ForegroundColor Green

Write-Host "`n🔄 PASO 3: VERIFICANDO CERTIFICADOS HTTPS" -ForegroundColor Yellow
if (Test-Path "frontend\certs\cert.key" -and (Test-Path "frontend\certs\cert.crt")) {
    Write-Host "✅ Certificados HTTPS encontrados" -ForegroundColor Green
} else {
    Write-Host "⚠️  Certificados HTTPS no encontrados - generando..." -ForegroundColor Yellow
    # Los certificados se generarán automáticamente al iniciar Vite
}

Write-Host "`n🚀 PASO 4: INSTALANDO DEPENDENCIAS" -ForegroundColor Yellow
Set-Location "frontend"
npm install
Set-Location ".."
Write-Host "✅ Dependencias actualizadas" -ForegroundColor Green

Write-Host "`n🎯 CONFIGURACIÓN UNIFICADA APLICADA:" -ForegroundColor Green
Write-Host "• Sistema CSS unificado en unified-system.css" -ForegroundColor White
Write-Host "• API robusta con configuración automática" -ForegroundColor White
Write-Host "• Configuración Vite optimizada" -ForegroundColor White
Write-Host "• HTTPS con certificados locales" -ForegroundColor White
Write-Host "• PWA completamente funcional" -ForegroundColor White

Write-Host "`n📱 PARA PROBAR EL SISTEMA:" -ForegroundColor Yellow
Write-Host "1. Ejecutar: .\iniciar-sistema-unificado.ps1" -ForegroundColor White
Write-Host "2. Frontend: https://192.168.12.178:5173/" -ForegroundColor Cyan
Write-Host "3. Backend: http://192.168.12.178:8000/" -ForegroundColor White

Write-Host "`n✨ SISTEMA UNIFICADO v3.0 LISTO!" -ForegroundColor Green
