#!/usr/bin/env pwsh

Write-Host "🐛 DEBUGGING ESPECÍFICO DE FUNCIONALIDADES" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Pasos de verificación manual:" -ForegroundColor Green
Write-Host ""

Write-Host "1. 🌐 Verificar versión SIMPLE (funciona):" -ForegroundColor Yellow
Write-Host "   URL: http://localhost:5173/envios/simple" -ForegroundColor White
Write-Host "   • Debe cargar sin errores" -ForegroundColor Gray
Write-Host "   • Probar conversión USD → CUP" -ForegroundColor Gray
Write-Host "   • Probar captura de foto" -ForegroundColor Gray
Write-Host "   • Probar generación de QR" -ForegroundColor Gray
Write-Host ""

Write-Host "2. 🧪 Verificar versión AVANZADA (con problemas):" -ForegroundColor Yellow
Write-Host "   URL: http://localhost:5173/envios/avanzado" -ForegroundColor White
Write-Host "   • Abrir consola del navegador (F12)" -ForegroundColor Gray
Write-Host "   • Buscar errores de importación" -ForegroundColor Gray
Write-Host "   • Verificar si los servicios se cargan" -ForegroundColor Gray
Write-Host ""

Write-Host "3. 📱 Testing móvil:" -ForegroundColor Yellow
Write-Host "   • Acceder desde móvil: http://192.168.12.179:5173/envios/simple" -ForegroundColor White
Write-Host "   • Probar captura de foto (debe abrir cámara)" -ForegroundColor Gray
Write-Host "   • Verificar que la conversión funciona" -ForegroundColor Gray
Write-Host ""

Write-Host "4. 🔍 Errores comunes a verificar:" -ForegroundColor Yellow
Write-Host "   ❌ Error: Cannot read property 'X' of undefined" -ForegroundColor Red
Write-Host "      → Verificar importaciones de servicios" -ForegroundColor Gray
Write-Host ""
Write-Host "   ❌ Error: getUserMedia is not a function" -ForegroundColor Red
Write-Host "      → Problema de permisos de cámara" -ForegroundColor Gray
Write-Host ""
Write-Host "   ❌ Error: Module not found" -ForegroundColor Red
Write-Host "      → Problema de rutas de importación" -ForegroundColor Gray
Write-Host ""

Write-Host "5. 🧪 Test manual de servicios en consola:" -ForegroundColor Yellow
Write-Host "   Abrir consola y ejecutar:" -ForegroundColor White
Write-Host ""
Write-Host "   // Test 1: Verificar importación" -ForegroundColor Gray
Write-Host "   window.testCurrency = () => {" -ForegroundColor Gray
Write-Host "     const rate = 320;" -ForegroundColor Gray
Write-Host "     const price = 25.50 * rate;" -ForegroundColor Gray
Write-Host "     console.log('Conversión:', price, 'CUP');" -ForegroundColor Gray
Write-Host "   };" -ForegroundColor Gray
Write-Host ""
Write-Host "   // Test 2: Verificar cámara" -ForegroundColor Gray
Write-Host "   window.testCamera = () => {" -ForegroundColor Gray
Write-Host "     const input = document.createElement('input');" -ForegroundColor Gray
Write-Host "     input.type = 'file';" -ForegroundColor Gray
Write-Host "     input.accept = 'image/*';" -ForegroundColor Gray
Write-Host "     input.capture = 'environment';" -ForegroundColor Gray
Write-Host "     input.click();" -ForegroundColor Gray
Write-Host "   };" -ForegroundColor Gray
Write-Host ""

Write-Host "6. 📊 Resultados esperados:" -ForegroundColor Green
Write-Host ""
Write-Host "   ✅ Versión SIMPLE debe funcionar al 100%" -ForegroundColor Green
Write-Host "   • Conversión: 2.5kg → ~$61,600 CUP" -ForegroundColor White
Write-Host "   • Cámara: Debe abrir selector de archivos/cámara" -ForegroundColor White
Write-Host "   • QR: Debe generar tracking tipo PCK12345678" -ForegroundColor White
Write-Host ""
Write-Host "   🔧 Versión AVANZADA debe debuggearse:" -ForegroundColor Yellow
Write-Host "   • Si hay errores de importación → revisar TypeScript" -ForegroundColor White
Write-Host "   • Si no funciona la cámara → problema de permisos" -ForegroundColor White
Write-Host "   • Si no calcula precios → error en servicios" -ForegroundColor White
Write-Host ""

Write-Host "7. 🚀 URLs de acceso directo:" -ForegroundColor Cyan
Write-Host "   • Simple:   http://localhost:5173/envios/simple" -ForegroundColor White
Write-Host "   • Avanzado: http://localhost:5173/envios/avanzado" -ForegroundColor White
Write-Host "   • Test:     http://localhost:5173/test-mobile.html" -ForegroundColor White
Write-Host ""

# Verificar estado actual
Write-Host "📊 Estado actual del sistema:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "💡 RECOMENDACIÓN:" -ForegroundColor Green
Write-Host "==================" -ForegroundColor White
Write-Host "1. Usar la versión SIMPLE primero para confirmar que funciona" -ForegroundColor Yellow
Write-Host "2. Abrir consola del navegador en versión AVANZADA" -ForegroundColor Yellow
Write-Host "3. Identificar errores específicos" -ForegroundColor Yellow
Write-Host "4. Corregir problemas uno por uno" -ForegroundColor Yellow

Write-Host ""
Read-Host "Presiona Enter para continuar"
