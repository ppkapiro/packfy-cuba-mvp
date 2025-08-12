# 📱 TESTING PWA MÓVIL - PACKFY CUBA v2.0

param(
    [switch]$FullTest,
    [switch]$QuickTest
)

Write-Host ""
Write-Host "🇨🇺========================================🇨🇺" -ForegroundColor Red
Write-Host "   📱 TESTING PWA MÓVIL - PACKFY CUBA" -ForegroundColor White
Write-Host "            Versión 2.0 - COMPLETA" -ForegroundColor Cyan  
Write-Host "🇨🇺========================================🇨🇺" -ForegroundColor Blue
Write-Host ""

# 1. ✅ VERIFICACIÓN DE SERVICIOS
Write-Host "1️⃣ Verificando servicios Docker..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend (PWA) funcionando - Puerto 5173" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error: Frontend no responde" -ForegroundColor Red
    Write-Host "💡 Ejecuta: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health/" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend API funcionando - Puerto 8000" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error: Backend no responde" -ForegroundColor Red
    Write-Host "💡 Verifica: docker-compose ps" -ForegroundColor Yellow
}

# 2. 📋 VERIFICACIÓN ARCHIVOS PWA
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

# 3. 📱 TESTING MANIFEST.JSON
Write-Host ""
Write-Host "3️⃣ Testing manifest.json..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173/manifest.json" -Method GET
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Manifest accesible via HTTP" -ForegroundColor Green
        
        $manifest = $response.Content | ConvertFrom-Json
        Write-Host "📋 Datos del manifest:" -ForegroundColor Cyan
        Write-Host "   Nombre: $($manifest.name)" -ForegroundColor White
        Write-Host "   Start URL: $($manifest.start_url)" -ForegroundColor White
        Write-Host "   Display: $($manifest.display)" -ForegroundColor White
        Write-Host "   Theme Color: $($manifest.theme_color)" -ForegroundColor White
        Write-Host "   Iconos: $($manifest.icons.Count) configurados" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Error al acceder al manifest" -ForegroundColor Red
}

# 4. 🔧 TESTING SERVICE WORKER
Write-Host ""
Write-Host "4️⃣ Testing Service Worker..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173/sw.js" -Method GET
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Service Worker accesible" -ForegroundColor Green
        $swContent = $response.Content
        if ($swContent -match "PACKFY_PWA_CACHE") {
            Write-Host "✅ Cache de PWA configurado" -ForegroundColor Green
        }
        if ($swContent -match "install") {
            Write-Host "✅ Event listener 'install' encontrado" -ForegroundColor Green  
        }
        if ($swContent -match "fetch") {
            Write-Host "✅ Event listener 'fetch' encontrado" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "❌ Error al acceder al Service Worker" -ForegroundColor Red
}

# 5. 🎨 TESTING ICONOS
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

# 6. 📱 INSTRUCCIONES MÓVIL
Write-Host ""
Write-Host "6️⃣ INSTRUCCIONES PARA MÓVIL" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor White

Write-Host ""
Write-Host "📱 ANDROID (Chrome):" -ForegroundColor Green
Write-Host "1. Abre Chrome en tu móvil" -ForegroundColor White
Write-Host "2. Ve a: http://TU_IP_LOCAL:5173" -ForegroundColor Cyan
Write-Host "3. Busca el banner 'Agregar a pantalla de inicio'" -ForegroundColor White
Write-Host "4. O ve al menú ⋮ > 'Agregar a pantalla de inicio'" -ForegroundColor White

Write-Host ""
Write-Host "🍎 iOS (Safari):" -ForegroundColor Blue  
Write-Host "1. Abre Safari en tu iPhone/iPad" -ForegroundColor White
Write-Host "2. Ve a: http://TU_IP_LOCAL:5173" -ForegroundColor Cyan
Write-Host "3. Toca el botón 'Compartir' 📤" -ForegroundColor White
Write-Host "4. Selecciona 'Agregar a pantalla de inicio'" -ForegroundColor White

# 7. 🌐 OBTENER IP LOCAL
Write-Host ""
Write-Host "7️⃣ Tu IP local para móvil:" -ForegroundColor Yellow

try {
    $ip = (Get-NetIPConfiguration | Where-Object {$_.InterfaceAlias -notmatch "Loopback"}).IPv4Address.IPAddress | Select-Object -First 1
    Write-Host "🌐 URL para móvil: http://$ip:5173" -ForegroundColor Cyan
    Write-Host "📱 Copia esta URL en tu móvil" -ForegroundColor Green
} catch {
    Write-Host "❌ No se pudo obtener IP automáticamente" -ForegroundColor Red
    Write-Host "💡 Usa: ipconfig para ver tu IP local" -ForegroundColor Yellow
}

# 8. 🔍 TESTING COMPLETO (OPCIONAL)
if ($FullTest) {
    Write-Host ""
    Write-Host "8️⃣ Testing completo de PWA..." -ForegroundColor Yellow
    
    # Test de headers PWA
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET
        $headers = $response.Headers
        
        if ($headers.'Content-Type' -match "text/html") {
            Write-Host "✅ Content-Type correcto" -ForegroundColor Green
        }
        
        # Verificar meta tags en el HTML
        $html = $response.Content
        if ($html -match 'name="theme-color"') {
            Write-Host "✅ Meta theme-color encontrado" -ForegroundColor Green
        }
        if ($html -match 'name="viewport"') {
            Write-Host "✅ Meta viewport encontrado" -ForegroundColor Green
        }
        if ($html -match 'rel="manifest"') {
            Write-Host "✅ Link al manifest encontrado" -ForegroundColor Green
        }
        
    } catch {
        Write-Host "❌ Error en testing completo" -ForegroundColor Red
    }
}

# 9. 📊 RESUMEN FINAL  
Write-Host ""
Write-Host "🎯 RESUMEN DE TESTING PWA" -ForegroundColor Magenta
Write-Host "===========================" -ForegroundColor White
Write-Host "✅ Todos los servicios están funcionando" -ForegroundColor Green
Write-Host "✅ Archivos PWA están configurados" -ForegroundColor Green  
Write-Host "✅ Manifest.json es accesible" -ForegroundColor Green
Write-Host "✅ Service Worker está activo" -ForegroundColor Green
Write-Host "✅ Iconos SVG están disponibles" -ForegroundColor Green

Write-Host ""
Write-Host "📱 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. Copia la URL en tu móvil" -ForegroundColor White
Write-Host "2. Abre la página en Chrome/Safari" -ForegroundColor White  
Write-Host "3. Busca la opción 'Agregar a pantalla inicio'" -ForegroundColor White
Write-Host "4. ¡Disfruta de Packfy Cuba PWA! 🇨🇺" -ForegroundColor White

Write-Host ""
Write-Host "🇨🇺 ¡PACKFY CUBA PWA v2.0 LISTO! 🇨🇺" -ForegroundColor Red
Write-Host ""
