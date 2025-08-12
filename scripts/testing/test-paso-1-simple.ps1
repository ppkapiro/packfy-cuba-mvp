#!/usr/bin/env pwsh

Write-Host "🚀 TESTING RÁPIDO - PACKFY CUBA v2.0" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ VERIFICACIÓN INMEDIATA" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔗 URLs para probar:" -ForegroundColor Blue
Write-Host "   Desarrollo: http://localhost:5173/" -ForegroundColor White
Write-Host "   Red local: http://192.168.12.179:5173/" -ForegroundColor White
Write-Host ""

Write-Host "🎯 QUÉ BUSCAR AL ABRIR:" -ForegroundColor Blue
Write-Host ""

Write-Host "1️⃣ ANIMACIÓN DE ENTRADA (primeros 2 segundos)" -ForegroundColor Magenta
Write-Host "   [ ] La página aparece con efecto fadeIn suave" -ForegroundColor White
Write-Host "   [ ] Header con slideUp desde abajo" -ForegroundColor White
Write-Host "   [ ] Bandera 🇨🇺 debe flotar arriba/abajo" -ForegroundColor White
Write-Host ""

Write-Host "2️⃣ EFECTOS HOVER (pasar mouse)" -ForegroundColor Magenta
Write-Host "   [ ] Bandera 🇨🇺: Debe crecer y rotar al hover" -ForegroundColor White
Write-Host "   [ ] Tarjetas: Deben elevarse con efecto 3D" -ForegroundColor White
Write-Host "   [ ] Botones: Deben tener efecto de brillo" -ForegroundColor White
Write-Host ""

Write-Host "3️⃣ GRADIENTES ANIMADOS" -ForegroundColor Magenta
Write-Host "   [ ] Título 'Packfy Cuba': Colores que se mueven" -ForegroundColor White
Write-Host "   [ ] Badges: Verde con efecto glow" -ForegroundColor White
Write-Host "   [ ] Botón Premium: Gradiente dorado/rojo" -ForegroundColor White
Write-Host ""

Write-Host "4️⃣ RESPONSIVE MÓVIL" -ForegroundColor Magenta
Write-Host "   [ ] F12 → Cambiar a móvil" -ForegroundColor White
Write-Host "   [ ] Animaciones más suaves" -ForegroundColor White
Write-Host "   [ ] Todo se ve bien en pantalla pequeña" -ForegroundColor White
Write-Host ""

Write-Host "🚨 SI NO VES LAS ANIMACIONES:" -ForegroundColor Red
Write-Host ""
Write-Host "Opción 1: Forzar recarga → Ctrl + F5" -ForegroundColor Yellow
Write-Host "Opción 2: Limpiar cache → F12 → Application → Storage → Clear site data" -ForegroundColor Yellow
Write-Host "Opción 3: Modo incógnito → Ctrl + Shift + N" -ForegroundColor Yellow
Write-Host ""

Write-Host "🎨 CARACTERÍSTICAS IMPLEMENTADAS:" -ForegroundColor Green
Write-Host ""
Write-Host "✨ Animaciones CSS:" -ForegroundColor Cyan
Write-Host "   - fadeInSlow (entrada de página)" -ForegroundColor White
Write-Host "   - floatCuba (bandera flotante)" -ForegroundColor White
Write-Host "   - shimmerCuba (título con gradiente)" -ForegroundColor White
Write-Host "   - glowCuba (badges con resplandor)" -ForegroundColor White
Write-Host ""

Write-Host "💎 Efectos Hover:" -ForegroundColor Cyan
Write-Host "   - Bandera: scale(1.1) + rotate(5deg)" -ForegroundColor White
Write-Host "   - Tarjetas: translateY(-20px) + scale(1.03)" -ForegroundColor White
Write-Host "   - Botones: translateY(-3px) + box-shadow" -ForegroundColor White
Write-Host ""

Write-Host "🇨🇺 Identidad Cubana:" -ForegroundColor Cyan
Write-Host "   - Gradiente patriótico: azul → morado → rojo" -ForegroundColor White
Write-Host "   - Bandera con animación float" -ForegroundColor White
Write-Host "   - Badges verdes con glow" -ForegroundColor White
Write-Host "   - Partículas de fondo" -ForegroundColor White
Write-Host ""

Write-Host "🎉 ¡SI VES ESTAS ANIMACIONES = ÉXITO TOTAL!" -ForegroundColor Green
Write-Host "Packfy Cuba v2.0 estará funcionando perfectamente con todos los efectos visuales premium implementados. 🚀🇨🇺✨" -ForegroundColor Yellow
Write-Host ""

# Test básico de conectividad
Write-Host "🔍 Verificando servidor..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173/" -UseBasicParsing -TimeoutSec 5
    
    $checks = @(
        @{ Text = "Registro de Paquete Simplificado"; Description = "Título principal" },
        @{ Text = "Remitente"; Description = "Campo remitente" },
        @{ Text = "Destinatario"; Description = "Campo destinatario" },
        @{ Text = "Peso"; Description = "Campo peso" },
        @{ Text = "Calcular Precio"; Description = "Botón calcular" }
    )
    
    foreach ($check in $checks) {
        if ($content.Content -like "*$($check.Text)*") {
            Write-Host "   ✅ $($check.Description) presente" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $($check.Description) faltante" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "   ❌ Error verificando contenido: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Verificar que no hay errores de JavaScript
Write-Host "3. 🧪 Instrucciones para testing manual:" -ForegroundColor Blue
Write-Host ""
Write-Host "   📱 PASOS A SEGUIR:" -ForegroundColor Yellow
Write-Host "   =================" -ForegroundColor White
Write-Host ""
Write-Host "   a) Abre http://localhost:5173/envios/simple en tu navegador" -ForegroundColor Gray
Write-Host "   b) Abre la consola del navegador (F12 → Console)" -ForegroundColor Gray
Write-Host "   c) Verifica que NO hay errores en rojo" -ForegroundColor Gray
Write-Host "   d) Llena el formulario con estos datos de prueba:" -ForegroundColor Gray
Write-Host ""
Write-Host "      • Remitente: Juan Pérez" -ForegroundColor Cyan
Write-Host "      • Destinatario: María González" -ForegroundColor Cyan
Write-Host "      • Dirección: Calle 23 #456, Vedado, La Habana" -ForegroundColor Cyan
Write-Host "      • Peso: 2.5" -ForegroundColor Cyan
Write-Host "      • Descripción: Ropa y zapatos" -ForegroundColor Cyan
Write-Host ""
Write-Host "   e) Haz clic en 'Calcular Precio'" -ForegroundColor Gray
Write-Host "   f) Deberías ver el precio en CUP (~$61,600 CUP)" -ForegroundColor Gray
Write-Host ""

Write-Host "💰 RESULTADO ESPERADO:" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor White
Write-Host ""
Write-Host "   • Precio base para 2.5kg: ~$28 USD" -ForegroundColor Yellow
Write-Host "   • Con tarifas (15% manejo): ~$32.20 USD" -ForegroundColor Yellow
Write-Host "   • Conversión a CUP (320 tasa): ~$10,304 CUP" -ForegroundColor Yellow
Write-Host ""
Write-Host "   ⚠️ NOTA: Si el cálculo no coincide, hay error en el servicio" -ForegroundColor Red
Write-Host ""

Write-Host "📷 TESTING DE CÁMARA:" -ForegroundColor Blue
Write-Host "=====================" -ForegroundColor White
Write-Host ""
Write-Host "   1. Después de calcular precio, haz clic en 'Continuar a Foto'" -ForegroundColor Gray
Write-Host "   2. Haz clic en 'Capturar Foto'" -ForegroundColor Gray
Write-Host "   3. En móvil: Debe abrir la cámara" -ForegroundColor Gray
Write-Host "   4. En desktop: Debe abrir selector de archivos" -ForegroundColor Gray
Write-Host "   5. Selecciona/toma una foto" -ForegroundColor Gray
Write-Host "   6. Debe mostrar '✅ Foto capturada: nombre.jpg'" -ForegroundColor Gray
Write-Host ""

Write-Host "🔖 TESTING DE QR:" -ForegroundColor Blue
Write-Host "=================" -ForegroundColor White
Write-Host ""
Write-Host "   1. Después de capturar foto, haz clic en 'Continuar a QR'" -ForegroundColor Gray
Write-Host "   2. Haz clic en 'Generar QR y Finalizar'" -ForegroundColor Gray
Write-Host "   3. Debe mostrar alert con tracking número tipo 'PCK12345678'" -ForegroundColor Gray
Write-Host "   4. Debe mostrar el precio final en CUP" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ CRITERIOS DE ÉXITO:" -ForegroundColor Green
Write-Host "======================" -ForegroundColor White
Write-Host ""
Write-Host "   ✓ Página carga sin errores en consola" -ForegroundColor Green
Write-Host "   ✓ Conversión USD → CUP funciona correctamente" -ForegroundColor Green
Write-Host "   ✓ Captura de foto abre cámara/selector" -ForegroundColor Green
Write-Host "   ✓ Generación de QR muestra tracking number" -ForegroundColor Green
Write-Host "   ✓ Workflow completo: Info → Precio → Foto → QR" -ForegroundColor Green
Write-Host ""

Write-Host "❌ SI ALGO FALLA:" -ForegroundColor Red
Write-Host "==================" -ForegroundColor White
Write-Host ""
Write-Host "   • Anota el error EXACTO de la consola" -ForegroundColor Yellow
Write-Host "   • Indica en qué paso falló" -ForegroundColor Yellow
Write-Host "   • Menciona si es en móvil o desktop" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔄 TESTING MÓVIL ADICIONAL:" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor White
Write-Host ""
Write-Host "   📱 URL móvil: http://192.168.12.179:5173/envios/simple" -ForegroundColor Yellow
Write-Host "   • Acceder desde teléfono/tablet" -ForegroundColor Gray
Write-Host "   • Repetir el mismo workflow" -ForegroundColor Gray
Write-Host "   • Verificar que la cámara funciona nativamente" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 ¿TODO FUNCIONÓ EN VERSIÓN SIMPLE?" -ForegroundColor Magenta
Write-Host "====================================" -ForegroundColor White
Write-Host ""
Write-Host "   ✅ SÍ → Procedemos al PASO 2 (Versión Avanzada)" -ForegroundColor Green
Write-Host "   ❌ NO → Necesitamos debuggear la versión simple primero" -ForegroundColor Red
Write-Host ""

Read-Host "Presiona Enter cuando hayas completado las pruebas del PASO 1"
