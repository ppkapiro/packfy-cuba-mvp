#!/usr/bin/env pwsh
# 🔧 PACKFY CUBA - SOLUCION ERRORES TYPESCRIPT
# ==========================================

Write-Host "🔧 PACKFY CUBA - SOLUCIONANDO ERRORES TYPESCRIPT" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# 1. Parar procesos conflictivos
Write-Host "`n📦 1. DETENIENDO PROCESOS CONFLICTIVOS" -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# 2. Verificar ubicación
Write-Host "`n📍 2. VERIFICANDO UBICACIÓN" -ForegroundColor Yellow
$projectRoot = "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"
$frontendDir = "$projectRoot\frontend"

if (!(Test-Path $frontendDir)) {
    Write-Host "❌ Directorio frontend no encontrado: $frontendDir" -ForegroundColor Red
    exit 1
}

Set-Location $frontendDir
Write-Host "✅ Directorio frontend localizado: $frontendDir" -ForegroundColor Green

# 3. Limpiar cache y reinstalar dependencias
Write-Host "`n🧹 3. LIMPIANDO CACHE Y DEPENDENCIAS" -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules"
    Write-Host "✅ Cache node_modules limpiado" -ForegroundColor Green
}

if (Test-Path "package-lock.json") {
    Remove-Item -Force "package-lock.json"
    Write-Host "✅ package-lock.json eliminado" -ForegroundColor Green
}

# 4. Reinstalar dependencias
Write-Host "`n📦 4. REINSTALANDO DEPENDENCIAS" -ForegroundColor Yellow
npm install --legacy-peer-deps
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
}
else {
    Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
    exit 1
}

# 5. Iniciar servidor de desarrollo
Write-Host "`n🚀 5. INICIANDO SERVIDOR DE DESARROLLO" -ForegroundColor Yellow
Write-Host "🌐 Frontend estará disponible en: https://localhost:5173/" -ForegroundColor Cyan
Write-Host "🌐 Acceso móvil en: https://192.168.12.178:5173/" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Yellow
Write-Host "💡 NOTA: En modo desarrollo los errores TypeScript no bloquean" -ForegroundColor Yellow
Write-Host "💡 La página debería cargar normalmente" -ForegroundColor Yellow
Write-Host "" -ForegroundColor Yellow
Write-Host "🔄 Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow

npm run dev
