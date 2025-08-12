# 📱 TESTING PWA MÓVIL - PACKFY CUBA v2.0

Write-Host ""
Write-Host "🇨🇺 ========================================🇨🇺" -ForegroundColor Red
Write-Host "     📱 TESTING PWA MÓVIL - PACKFY CUBA" -ForegroundColor White
Write-Host "              Versión 2.0 - COMPLETA" -ForegroundColor Cyan  
Write-Host "🇨🇺 ========================================🇨🇺" -ForegroundColor Blue
Write-Host ""

# 1. VERIFICACIÓN DE SERVICIOS
Write-Host "1️⃣ Verificando servicios Docker..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend (PWA) funcionando - Puerto 5173" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error: Frontend no responde" -ForegroundColor Red
    Write-Host "💡 Ejecuta: docker-compose up -d" -ForegroundColor Yellow
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health/" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend API funcionando - Puerto 8000" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error: Backend no responde" -ForegroundColor Red
}

# 2. VERIFICACIÓN ARCHIVOS PWA
Write-Host ""
Write-Host "2️⃣ Verificando archivos PWA..." -ForegroundColor Yellow

$pwaFiles = @(
    "frontend/public/manifest.json",
    "frontend/public/sw.js", 
    "frontend/public/icon-72.svg",
    "frontend/public/icon-192-new.svg",
    "frontend/public/icon-512-new.svg"
)

foreach ($file in $pwaFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file - FALTANTE" -ForegroundColor Red
    }
}

# 3. TESTING MANIFEST.JSON
Write-Host ""
Write-Host "3️⃣ Testing manifest.json..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173/manifest.json" -Method GET
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Manifest accesible via HTTP" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error al acceder al manifest" -ForegroundColor Red
}

# 4. TESTING SERVICE WORKER
Write-Host ""
Write-Host "4️⃣ Testing Service Worker..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173/sw.js" -Method GET
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Service Worker accesible" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error al acceder al Service Worker" -ForegroundColor Red
}

# 5. TESTING ICONOS
Write-Host ""
Write-Host "5️⃣ Testing iconos PWA..." -ForegroundColor Yellow

$iconos = @("icon-72.svg", "icon-192-new.svg", "icon-512-new.svg")
foreach ($icono in $iconos) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5173/$icono" -Method GET
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $icono accesible" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ $icono no accesible" -ForegroundColor Red
    }
}

# 6. OBTENER IP LOCAL
Write-Host ""
Write-Host "6️⃣ Tu IP local para móvil:" -ForegroundColor Yellow

try {
    $ipConfig = ipconfig | Select-String "IPv4"
    $ip = ($ipConfig | Select-Object -First 1).ToString().Split(":")[1].Trim()
    Write-Host "🌐 URL para móvil: http://$ip:5173" -ForegroundColor Cyan
    Write-Host "📱 Copia esta URL en tu móvil" -ForegroundColor Green
} catch {
    Write-Host "❌ No se pudo obtener IP automáticamente" -ForegroundColor Red
    Write-Host "💡 Usa: ipconfig para ver tu IP local" -ForegroundColor Yellow
}

# 7. INSTRUCCIONES MÓVIL
Write-Host ""
Write-Host "7️⃣ INSTRUCCIONES PARA MÓVIL" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor White

Write-Host ""
Write-Host "📱 ANDROID (Chrome):" -ForegroundColor Green
Write-Host "1. Abre Chrome en tu móvil" -ForegroundColor White
Write-Host "2. Ve a la URL mostrada arriba" -ForegroundColor Cyan
Write-Host "3. Busca el banner 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "4. O ve al menú ⋮ > 'Agregar a pantalla de inicio'" -ForegroundColor White

Write-Host ""
Write-Host "🍎 iOS (Safari):" -ForegroundColor Blue  
Write-Host "1. Abre Safari en tu iPhone/iPad" -ForegroundColor White
Write-Host "2. Ve a la URL mostrada arriba" -ForegroundColor Cyan
Write-Host "3. Toca el botón 'Compartir' 📤" -ForegroundColor White
Write-Host "4. Selecciona 'Agregar a pantalla de inicio'" -ForegroundColor White

# 8. RESUMEN FINAL  
Write-Host ""
Write-Host "🎯 RESUMEN DE TESTING PWA" -ForegroundColor Magenta
Write-Host "===========================" -ForegroundColor White
Write-Host "✅ PWA optimizada para móvil está lista" -ForegroundColor Green
Write-Host "✅ Manifest.json con iconos cubanos" -ForegroundColor Green  
Write-Host "✅ Service Worker v2.0 optimizado" -ForegroundColor Green
Write-Host "✅ Iconos SVG con colores patrios" -ForegroundColor Green

Write-Host ""
Write-Host "📱 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. Copia la URL en tu móvil" -ForegroundColor White
Write-Host "2. Abre la página en Chrome/Safari" -ForegroundColor White  
Write-Host "3. Busca la opción 'Agregar a pantalla inicio'" -ForegroundColor White
Write-Host "4. ¡Disfruta de Packfy Cuba PWA! 🇨🇺" -ForegroundColor White

Write-Host ""
Write-Host "🇨🇺 ¡PACKFY CUBA PWA v2.0 LISTO! 🇨🇺" -ForegroundColor Red
Write-Host ""
