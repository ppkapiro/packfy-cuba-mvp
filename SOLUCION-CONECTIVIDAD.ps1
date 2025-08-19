# 🔧 SOLUCIÓN DE CONECTIVIDAD DOCKER - PACKFY CUBA MVP
# Script para solucionar problemas de conectividad entre contenedores

Write-Host "🇨🇺 PACKFY CUBA - Solucionando problemas de conectividad..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# 1. Verificar estado de los contenedores
Write-Host "🔍 1. Verificando estado de contenedores..." -ForegroundColor Yellow
docker compose ps

# 2. Verificar red Docker
Write-Host "`n🌐 2. Verificando configuración de red..." -ForegroundColor Yellow
$networkInfo = docker network inspect packfy_network_v4 2>$null
if ($networkInfo) {
    Write-Host "✅ Red packfy_network_v4 encontrada" -ForegroundColor Green
}
else {
    Write-Host "❌ Red no encontrada, recreando..." -ForegroundColor Red
    docker compose down
    docker compose up -d
}

# 3. Probar conectividad interna
Write-Host "`n🔗 3. Probando conectividad interna..." -ForegroundColor Yellow

# Frontend -> Backend
Write-Host "Testing Frontend -> Backend..."
$frontendToBackend = docker compose exec -T frontend curl -s -m 3 http://backend:8000/api/health/ 2>$null
if ($frontendToBackend) {
    Write-Host "✅ Frontend -> Backend: OK" -ForegroundColor Green
}
else {
    Write-Host "❌ Frontend -> Backend: FALLO" -ForegroundColor Red
}

# Backend -> Database
Write-Host "Testing Backend -> Database..."
$backendToDb = docker compose exec -T backend python -c "
import psycopg2
import os
try:
    conn = psycopg2.connect(
        host='database',
        port='5432',
        database='packfy',
        user='postgres',
        password='postgres'
    )
    print('✅ Backend -> Database: OK')
    conn.close()
except Exception as e:
    print(f'❌ Backend -> Database: {e}')
" 2>$null

if ($backendToDb) {
    Write-Host $backendToDb
}
else {
    Write-Host "❌ Backend -> Database: FALLO" -ForegroundColor Red
}

# 4. Verificar configuración de proxy Vite
Write-Host "`n⚙️ 4. Verificando configuración de proxy..." -ForegroundColor Yellow
$viteConfig = Get-Content "frontend/vite.config.ts" | Select-String "target.*backend"
if ($viteConfig) {
    Write-Host "✅ Proxy configurado para backend:8000" -ForegroundColor Green
}
else {
    Write-Host "❌ Configuración de proxy incorrecta" -ForegroundColor Red
}

# 5. Limpiar cache y reiniciar servicios problemáticos
Write-Host "`n🧹 5. Limpiando cache y reiniciando..." -ForegroundColor Yellow
docker compose restart frontend
Start-Sleep 5

# 6. Verificación final
Write-Host "`n✅ 6. Verificación final..." -ForegroundColor Yellow
Start-Sleep 10

# Probar endpoint desde el exterior
Write-Host "Probando acceso externo..."
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/health/" -TimeoutSec 5
    if ($response.status -eq "ok") {
        Write-Host "✅ Backend accesible externamente" -ForegroundColor Green
    }
}
catch {
    Write-Host "❌ Backend no accesible externamente" -ForegroundColor Red
}

try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 5 -UseBasicParsing
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend accesible externamente" -ForegroundColor Green
    }
}
catch {
    Write-Host "❌ Frontend no accesible externamente" -ForegroundColor Red
}

Write-Host "`n🎉 Proceso completado!" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "📝 Si persisten problemas, ejecuta: docker compose down && docker compose up -d" -ForegroundColor Yellow
