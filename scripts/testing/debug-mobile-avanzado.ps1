#!/usr/bin/env pwsh

Write-Host "🔧 DEBUGGING FUNCIONALIDADES MÓVILES AVANZADAS" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Verificar que los archivos existen
Write-Host "📂 1. Verificando archivos de servicios..." -ForegroundColor Green

$servicios = @(
    "frontend/src/services/currency.ts",
    "frontend/src/services/camera.ts", 
    "frontend/src/services/qr.ts"
)

$componentes = @(
    "frontend/src/components/PriceCalculator.tsx",
    "frontend/src/components/PackageCamera.tsx",
    "frontend/src/components/AdvancedPackageForm.tsx"
)

$paginas = @(
    "frontend/src/pages/AdvancedPackagePage.tsx"
)

foreach ($archivo in $servicios) {
    if (Test-Path $archivo) {
        Write-Host "  ✅ $archivo" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $archivo (FALTANTE)" -ForegroundColor Red
    }
}

foreach ($archivo in $componentes) {
    if (Test-Path $archivo) {
        Write-Host "  ✅ $archivo" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $archivo (FALTANTE)" -ForegroundColor Red
    }
}

foreach ($archivo in $paginas) {
    if (Test-Path $archivo) {
        Write-Host "  ✅ $archivo" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $archivo (FALTANTE)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📦 2. Verificando dependencias..." -ForegroundColor Green
Write-Host "Verificando lucide-react..."

$packageJson = Get-Content "frontend/package.json" | ConvertFrom-Json
$lucideVersion = $packageJson.dependencies.'lucide-react'

if ($lucideVersion) {
    Write-Host "  ✅ lucide-react: $lucideVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ lucide-react no encontrado" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔨 3. Compilando frontend..." -ForegroundColor Green

Set-Location frontend
$buildResult = npm run build 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Compilación exitosa" -ForegroundColor Green
} else {
    Write-Host "  ❌ Errores de compilación:" -ForegroundColor Red
    Write-Host $buildResult -ForegroundColor Red
}

Set-Location ..

Write-Host ""
Write-Host "🌐 4. Verificando rutas en App.tsx..." -ForegroundColor Green

$appContent = Get-Content "frontend/src/App.tsx" -Raw
if ($appContent -match "envios/avanzado.*AdvancedPackagePage") {
    Write-Host "  ✅ Ruta /envios/avanzado configurada correctamente" -ForegroundColor Green
} else {
    Write-Host "  ❌ Ruta /envios/avanzado NO configurada" -ForegroundColor Red
}

Write-Host ""
Write-Host "🧪 5. Verificando estructura de servicios..." -ForegroundColor Green

# Verificar exportaciones de servicios
$currencyExports = Select-String -Path "frontend/src/services/currency.ts" -Pattern "export.*default|export.*interface"
$cameraExports = Select-String -Path "frontend/src/services/camera.ts" -Pattern "export.*default|export.*interface" 
$qrExports = Select-String -Path "frontend/src/services/qr.ts" -Pattern "export.*default|export.*interface"

Write-Host "Currency exports: $($currencyExports.Count)" -ForegroundColor White
Write-Host "Camera exports: $($cameraExports.Count)" -ForegroundColor White  
Write-Host "QR exports: $($qrExports.Count)" -ForegroundColor White

Write-Host ""
Write-Host "💡 6. URLs de testing:" -ForegroundColor Yellow
Write-Host "  • Página principal: http://localhost:5173/" -ForegroundColor White
Write-Host "  • Formulario avanzado: http://localhost:5173/envios/avanzado" -ForegroundColor White
Write-Host "  • Test de funcionalidades: http://localhost:5173/test-mobile.html" -ForegroundColor White
Write-Host "  • Móvil (IP local): http://192.168.12.179:5173/envios/avanzado" -ForegroundColor White

Write-Host ""
Write-Host "🐛 7. Pasos de debugging:" -ForegroundColor Yellow
Write-Host "   1. Abre la consola del navegador (F12)" -ForegroundColor White
Write-Host "   2. Ve a http://localhost:5173/envios/avanzado" -ForegroundColor White
Write-Host "   3. Verifica si hay errores de importación" -ForegroundColor White
Write-Host "   4. Prueba capturar foto en móvil" -ForegroundColor White
Write-Host "   5. Verifica cálculo de precios con datos de prueba" -ForegroundColor White

Write-Host ""
Write-Host "📋 8. Datos de prueba sugeridos:" -ForegroundColor Yellow
Write-Host "   • Peso: 2.5 kg" -ForegroundColor White
Write-Host "   • Dimensiones: 30x20x15 cm" -ForegroundColor White
Write-Host "   • Nombre: Juan Pérez" -ForegroundColor White
Write-Host "   • Dirección: Calle 23 #456, Vedado, La Habana" -ForegroundColor White
Write-Host "   • Teléfono: +53 5555-1234" -ForegroundColor White

Write-Host ""
if (Test-Path "docker-compose.yml") {
    Write-Host "🐳 Verificando contenedores..." -ForegroundColor Green
    docker-compose ps
    
    Write-Host ""
    Write-Host "🔄 Si hay problemas, intenta:" -ForegroundColor Yellow
    Write-Host "   docker-compose restart frontend" -ForegroundColor Gray
    Write-Host "   docker-compose logs frontend" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ DEBUGGING COMPLETADO" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Cyan

Read-Host "Presiona Enter para continuar"
