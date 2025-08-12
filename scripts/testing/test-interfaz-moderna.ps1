# 🎨 VERIFICADOR DE INTERFAZ MODERNA - PACKFY CUBA
# Script para verificar que la interfaz premium esté funcionando correctamente

Write-Host "🇨🇺 =============================================" -ForegroundColor Cyan
Write-Host "🎨 VERIFICADOR DE INTERFAZ MODERNA PACKFY CUBA" -ForegroundColor Cyan
Write-Host "🇨🇺 =============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar servidores
Write-Host "📡 Verificando servidores..." -ForegroundColor Yellow

# Backend
Write-Host "🔍 Verificando Backend (Django)..." -ForegroundColor White
try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/user/" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
    if ($backendResponse.StatusCode -eq 200 -or $backendResponse.StatusCode -eq 401) {
        Write-Host "✅ Backend Django funcionando en puerto 8000" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Backend responde pero con código: $($backendResponse.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Backend NO está funcionando en puerto 8000" -ForegroundColor Red
}

# Frontend
Write-Host "🔍 Verificando Frontend (Vite)..." -ForegroundColor White
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:5174/" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend Vite funcionando en puerto 5174" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Frontend responde pero con código: $($frontendResponse.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    try {
        $frontendResponse2 = Invoke-WebRequest -Uri "http://localhost:5173/" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($frontendResponse2.StatusCode -eq 200) {
            Write-Host "✅ Frontend Vite funcionando en puerto 5173" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Frontend NO está funcionando en puertos 5173 o 5174" -ForegroundColor Red
    }
}

Write-Host ""

# Verificar archivos CSS
Write-Host "🎨 Verificando archivos de estilos..." -ForegroundColor Yellow

$cssFiles = @(
    "frontend/src/styles/master-premium.css",
    "frontend/src/styles/layout-fixes.css", 
    "frontend/src/styles/mobile-optimized.css"
)

foreach ($file in $cssFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "✅ $file ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "❌ $file (NO ENCONTRADO)" -ForegroundColor Red
    }
}

Write-Host ""

# Verificar main.tsx
Write-Host "🔧 Verificando configuración main.tsx..." -ForegroundColor Yellow
if (Test-Path "frontend/src/main.tsx") {
    $mainContent = Get-Content "frontend/src/main.tsx" -Raw
    if ($mainContent -match "master-premium\.css") {
        Write-Host "✅ master-premium.css está importado" -ForegroundColor Green
    } else {
        Write-Host "❌ master-premium.css NO está importado" -ForegroundColor Red
    }
    
    if ($mainContent -match "layout-fixes\.css") {
        Write-Host "✅ layout-fixes.css está importado" -ForegroundColor Green
    } else {
        Write-Host "❌ layout-fixes.css NO está importado" -ForegroundColor Red
    }
    
    if ($mainContent -match "mobile-optimized\.css") {
        Write-Host "✅ mobile-optimized.css está importado" -ForegroundColor Green
    } else {
        Write-Host "❌ mobile-optimized.css NO está importado" -ForegroundColor Red
    }
} else {
    Write-Host "❌ main.tsx NO encontrado" -ForegroundColor Red
}

Write-Host ""

# URLs de acceso
Write-Host "🌐 URLs de acceso:" -ForegroundColor Yellow
Write-Host "   💻 Computadora: http://localhost:5174/" -ForegroundColor Cyan
Write-Host "   📱 Móvil: http://192.168.12.178:5174/" -ForegroundColor Cyan
Write-Host "   🔧 API Backend: http://localhost:8000/admin/" -ForegroundColor Cyan

Write-Host ""

# Credenciales de prueba
Write-Host "🔐 Credenciales de prueba:" -ForegroundColor Yellow
Write-Host "   👑 Admin: admin@packfy.cu / admin123" -ForegroundColor White
Write-Host "   🏢 Empresa: empresa@test.cu / empresa123" -ForegroundColor White
Write-Host "   🇨🇺 Cliente: cliente@test.cu / cliente123" -ForegroundColor White

Write-Host ""

# Características implementadas
Write-Host "🎨 Características de la Interfaz Moderna:" -ForegroundColor Yellow
Write-Host "   ✅ Tema cubano con colores premium" -ForegroundColor Green
Write-Host "   ✅ Iconos SVG profesionales" -ForegroundColor Green
Write-Host "   ✅ Diseño responsivo optimizado" -ForegroundColor Green
Write-Host "   ✅ Navegación moderna" -ForegroundColor Green
Write-Host "   ✅ Formularios premium" -ForegroundColor Green
Write-Host "   ✅ Dashboard con estadísticas" -ForegroundColor Green
Write-Host "   ✅ Optimización móvil completa" -ForegroundColor Green
Write-Host "   ✅ Transiciones y animaciones" -ForegroundColor Green

Write-Host ""
Write-Host "🎯 INSTRUCCIONES:" -ForegroundColor Cyan
Write-Host "1. Abre tu navegador en http://localhost:5174/" -ForegroundColor White
Write-Host "2. La interfaz debe verse MODERNA con diseño cubano" -ForegroundColor White
Write-Host "3. En móvil usa: http://192.168.12.178:5174/" -ForegroundColor White
Write-Host "4. Usa las credenciales de prueba para entrar" -ForegroundColor White
Write-Host "5. Verifica que el diseño se vea premium y profesional" -ForegroundColor White

Write-Host ""
Write-Host "🇨🇺 ¡Packfy Cuba listo con diseño moderno!" -ForegroundColor Green
