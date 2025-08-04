#!/usr/bin/env powershell
# Script completo de verificación PWA para Packfy
# Versión 2.0 - Verificación avanzada

Write-Host "🔍 VERIFICACION AVANZADA PWA PACKFY v2.0" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# 1. Verificar servicios Docker
Write-Host "`n1. 🐳 Estado de servicios Docker:" -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" | Where-Object { $_ -match "packfy" }

# 2. Verificar archivos PWA críticos
Write-Host "`n2. 📱 Archivos PWA:" -ForegroundColor Yellow

$manifest = "frontend/public/manifest.json"
$sw = "frontend/public/sw.js"
$testPage = "frontend/public/test-pwa.html"

if (Test-Path $manifest) {
    $manifestSize = (Get-Item $manifest).Length
    Write-Host "   ✅ Manifest: $manifestSize bytes" -ForegroundColor Green
} else {
    Write-Host "   ❌ Manifest no encontrado" -ForegroundColor Red
}

if (Test-Path $sw) {
    $swSize = (Get-Item $sw).Length
    Write-Host "   ✅ Service Worker: $swSize bytes" -ForegroundColor Green
    
    # Verificar versión del SW
    $swContent = Get-Content $sw -Raw
    if ($swContent -match "VERSION = '[^']*'") {
        $version = $matches[0]
        Write-Host "   📄 $version" -ForegroundColor Cyan
    }
    
    # Verificar cachés definidos
    if ($swContent -match "CACHE_NAME") {
        Write-Host "   📦 Estrategia de caché: Multi-caché implementada" -ForegroundColor Cyan
    }
} else {
    Write-Host "   ❌ Service Worker no encontrado" -ForegroundColor Red
}

if (Test-Path $testPage) {
    $testSize = (Get-Item $testPage).Length
    Write-Host "   ✅ Página de prueba: $testSize bytes" -ForegroundColor Green
} else {
    Write-Host "   ❌ Página de prueba no encontrada" -ForegroundColor Red
}

# 3. Verificar componentes React PWA
Write-Host "`n3. ⚛️ Componentes React PWA:" -ForegroundColor Yellow

$pwaComponent = "frontend/src/components/PWAInstallPrompt.tsx"
$networkHook = "frontend/src/hooks/useNetworkStatus.ts"
$networkComponent = "frontend/src/components/NetworkStatusBanner.tsx"

if (Test-Path $pwaComponent) {
    Write-Host "   ✅ PWAInstallPrompt component" -ForegroundColor Green
} else {
    Write-Host "   ❌ PWAInstallPrompt component faltante" -ForegroundColor Red
}

if (Test-Path $networkHook) {
    Write-Host "   ✅ useNetworkStatus hook" -ForegroundColor Green
} else {
    Write-Host "   ❌ useNetworkStatus hook faltante" -ForegroundColor Red
}

if (Test-Path $networkComponent) {
    Write-Host "   ✅ NetworkStatusBanner component" -ForegroundColor Green
} else {
    Write-Host "   ❌ NetworkStatusBanner component faltante" -ForegroundColor Red
}

# 4. Verificar integración en App.tsx
Write-Host "`n4. 🔗 Integración en App:" -ForegroundColor Yellow

$appFile = "frontend/src/App.tsx"
if (Test-Path $appFile) {
    $appContent = Get-Content $appFile -Raw
    
    if ($appContent -match "PWAInstallPrompt") {
        Write-Host "   ✅ PWAInstallPrompt integrado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ PWAInstallPrompt no integrado" -ForegroundColor Yellow
    }
    
    if ($appContent -match "NetworkStatusBanner") {
        Write-Host "   ✅ NetworkStatusBanner integrado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ NetworkStatusBanner no integrado" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ App.tsx no encontrado" -ForegroundColor Red
}

# 5. Verificar estilos PWA
Write-Host "`n5. 🎨 Estilos PWA:" -ForegroundColor Yellow

$appCss = "frontend/src/App.css"
if (Test-Path $appCss) {
    $cssContent = Get-Content $appCss -Raw
    
    if ($cssContent -match "ESTILOS PWA") {
        Write-Host "   ✅ Estilos PWA implementados" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Estilos PWA básicos" -ForegroundColor Yellow
    }
    
    if ($cssContent -match "display-mode: standalone") {
        Write-Host "   ✅ Detección modo standalone" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Sin detección standalone" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ App.css no encontrado" -ForegroundColor Red
}

# 6. Obtener IP local para pruebas móviles
Write-Host "`n6. 🌐 Configuración de red:" -ForegroundColor Yellow

$ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*" | Where-Object { $_.IPAddress -notmatch "169.254" } | Select-Object -First 1).IPAddress

if ($ip) {
    Write-Host "   📱 IP Local: $ip" -ForegroundColor Cyan
    Write-Host "   🖥️ PC: http://localhost:5173" -ForegroundColor Cyan
    Write-Host "   📲 Móvil: http://$ip:5173" -ForegroundColor Cyan
} else {
    Write-Host "   ⚠️ No se pudo obtener IP local" -ForegroundColor Yellow
}

# 7. Instrucciones de prueba
Write-Host "`n7. 📋 Instrucciones de prueba:" -ForegroundColor Yellow
Write-Host "   Android Chrome:" -ForegroundColor Cyan
Write-Host "     1. Ir a http://$ip:5173" -ForegroundColor White
Write-Host "     2. Menú (⋮) > 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "     3. Confirmar instalación" -ForegroundColor White

Write-Host "`n   iOS Safari:" -ForegroundColor Cyan
Write-Host "     1. Ir a http://$ip:5173" -ForegroundColor White
Write-Host "     2. Compartir (⬆️) > 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "     3. Confirmar 'Agregar'" -ForegroundColor White

Write-Host "`n   Desktop Chrome:" -ForegroundColor Cyan
Write-Host "     1. Ir a http://localhost:5173" -ForegroundColor White
Write-Host "     2. Buscar botón 'Instalar App' (flotante)" -ForegroundColor White
Write-Host "     3. O icono de instalación en barra de direcciones" -ForegroundColor White

# 8. Funcionalidades PWA a probar
Write-Host "`n8. ✅ Funcionalidades a verificar:" -ForegroundColor Yellow
Write-Host "   □ Instalación desde navegador" -ForegroundColor White
Write-Host "   □ Apertura en modo standalone" -ForegroundColor White
Write-Host "   □ Funcionamiento offline" -ForegroundColor White
Write-Host "   □ Banner de estado de conexión" -ForegroundColor White
Write-Host "   □ Prompt de instalación automático" -ForegroundColor White
Write-Host "   □ Cache de recursos estáticos" -ForegroundColor White
Write-Host "   □ Cache de respuestas API" -ForegroundColor White
Write-Host "   □ Página offline personalizada" -ForegroundColor White

Write-Host "`n🎉 Verificación PWA completada!" -ForegroundColor Green
Write-Host "💡 Tip: Abre DevTools > Application > Service Workers para debug" -ForegroundColor Cyan
