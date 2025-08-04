#!/usr/bin/env powershell
# Script de limpieza total y rebuild para Packfy PWA
# VersiWrite-Host "URLS DE ACCESO:" -ForegroundColor Greenn 1.0 - 4 de agosto de 2025

Write-Host "LIMPIEZA TOTAL PACKFY + REBUILD COMPLETO" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow

# Función para esperar con puntos
function Wait-WithDots {
    param([int]$seconds, [string]$message)
    Write-Host "$message" -NoNewline
    for ($i = 0; $i -lt $seconds; $i++) {
        Start-Sleep 1
        Write-Host "." -NoNewline
    }
    Write-Host " ✅" -ForegroundColor Green
}

# Paso 1: Detener todo
Write-Host "`n1. 🛑 Deteniendo servicios..." -ForegroundColor Cyan
docker compose down --remove-orphans 2>$null
docker stop $(docker ps -aq) 2>$null

# Paso 2: Limpiar contenedores
Write-Host "`n2. 📦 Eliminando contenedores..." -ForegroundColor Cyan
docker rm $(docker ps -aq) 2>$null

# Paso 3: Limpiar imágenes
Write-Host "`n3. 🖼️ Eliminando imágenes..." -ForegroundColor Cyan
docker rmi $(docker images -q) --force 2>$null

# Paso 4: Limpiar volúmenes específicos
Write-Host "`n4. 💾 Eliminando volúmenes de datos..." -ForegroundColor Cyan
docker volume rm packfy_postgres_data packfy_static_files packfy_media_files 2>$null
docker volume rm paqueteria-cuba-mvp_postgres_data paqueteria-cuba-mvp_static_files paqueteria-cuba-mvp_media_files 2>$null

# Paso 5: Limpieza general
Write-Host "`n5. 🗑️ Limpieza general Docker..." -ForegroundColor Cyan
docker system prune -af --volumes 2>$null

# Paso 6: Verificar limpieza
Write-Host "`n6. 🔍 Verificando limpieza..." -ForegroundColor Cyan
$containers = docker ps -aq
$images = docker images -q
$volumes = docker volume ls -q | Where-Object { $_ -match "packfy|paqueteria" }

if ($containers) {
    Write-Host "   ⚠️ Contenedores restantes: $($containers.Count)" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Sin contenedores" -ForegroundColor Green
}

if ($images) {
    Write-Host "   ⚠️ Imágenes restantes: $($images.Count)" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Sin imágenes del proyecto" -ForegroundColor Green
}

if ($volumes) {
    Write-Host "   ⚠️ Volúmenes restantes: $($volumes.Count)" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Sin volúmenes del proyecto" -ForegroundColor Green
}

# Paso 7: Rebuild desde cero
Write-Host "`n7. 🏗️ Reconstruyendo desde cero..." -ForegroundColor Cyan
Write-Host "   📋 Esto puede tomar varios minutos..." -ForegroundColor White

docker compose build --no-cache --progress=plain

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Build completado exitosamente" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error en el build" -ForegroundColor Red
    exit 1
}

# Paso 8: Iniciar servicios
Write-Host "`n8. 🚀 Iniciando servicios..." -ForegroundColor Cyan
docker compose up -d

Wait-WithDots 10 "   ⏳ Esperando que los servicios estén listos"

# Paso 9: Verificar estado
Write-Host "`n9. 📊 Estado final..." -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Paso 10: URLs de acceso
Write-Host "`n🎯 URLS DE ACCESO:" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "🖥️ PC: http://localhost:5173" -ForegroundColor White
Write-Host "📱 Móvil: http://192.168.12.179:5173" -ForegroundColor White
Write-Host ""
Write-Host "CREDENCIALES:" -ForegroundColor Green
Write-Host "- admin@packfy.com / admin123" -ForegroundColor White
Write-Host "- demo@packfy.com / demo123" -ForegroundColor White  
Write-Host "- test@test.com / 123456" -ForegroundColor White
Write-Host ""
Write-Host "PWA FEATURES:" -ForegroundColor Green
Write-Host "- Service Worker v1.2 activo" -ForegroundColor White
Write-Host "- Instalacion automatica" -ForegroundColor White
Write-Host "- Modo offline completo" -ForegroundColor White
Write-Host "- Banner de conectividad" -ForegroundColor White

Write-Host ""
Write-Host "REBUILD COMPLETADO!" -ForegroundColor Green
