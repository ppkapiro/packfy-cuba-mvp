# 🔍 PRUEBA NAVEGACIÓN DUEÑO - PACKFY CUBA
# Script para probar la navegación de dueño paso a paso

Write-Host "🇨🇺 PACKFY CUBA - PRUEBA NAVEGACIÓN DUEÑO" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

Write-Host ""
Write-Host "🎯 CREDENCIALES DE PRUEBA:" -ForegroundColor Yellow
Write-Host "Email: dueno@packfy.com" -ForegroundColor White
Write-Host "Password: dueno123!" -ForegroundColor White
Write-Host "Rol: Dueño" -ForegroundColor Green

Write-Host ""
Write-Host "📱 ABRIENDO APLICACIÓN..." -ForegroundColor Cyan

# Abrir navegador en la página de login
$frontendUrl = "http://localhost:5174/login"
Start-Process $frontendUrl

Write-Host "✅ Navegador abierto en: $frontendUrl" -ForegroundColor Green

Write-Host ""
Write-Host "📋 PASOS A SEGUIR:" -ForegroundColor Magenta
Write-Host "1. Hacer login con dueno@packfy.com / dueno123!" -ForegroundColor White
Write-Host "2. Verificar que aparezca la navegación de dueño" -ForegroundColor White
Write-Host "3. Buscar enlaces: Dashboard, Gestión de Usuarios, Reportes" -ForegroundColor White
Write-Host "4. Navegar a /admin/dashboard" -ForegroundColor White

Write-Host ""
Write-Host "🔍 QUÉ BUSCAR EN LA NAVEGACIÓN:" -ForegroundColor Yellow
Write-Host "✅ Dashboard Ejecutivo" -ForegroundColor Green
Write-Host "✅ Gestión de Usuarios (con dropdown)" -ForegroundColor Green
Write-Host "✅ Reportes y Analytics (con dropdown)" -ForegroundColor Green
Write-Host "✅ Configuración de Empresa" -ForegroundColor Green
Write-Host "✅ Admin Django (enlace externo)" -ForegroundColor Green

Write-Host ""
Write-Host "🐛 SI NO VES LA NAVEGACIÓN DE DUEÑO:" -ForegroundColor Red
Write-Host "1. Verifica la consola del navegador (F12)" -ForegroundColor White
Write-Host "2. Busca mensajes de debug que empiecen con 'Layout:'" -ForegroundColor White
Write-Host "3. Verifica que el rol del usuario sea 'dueno'" -ForegroundColor White
Write-Host "4. Recarga la página (Ctrl+F5) para limpiar caché" -ForegroundColor White

Write-Host ""
Write-Host "🔧 URLS DIRECTAS PARA PROBAR:" -ForegroundColor Cyan
Write-Host "Login: http://localhost:5174/login" -ForegroundColor Gray
Write-Host "Dashboard Normal: http://localhost:5174/dashboard" -ForegroundColor Gray
Write-Host "Dashboard Dueño: http://localhost:5174/admin/dashboard" -ForegroundColor Gray

Write-Host ""
Write-Host "🚀 ¡LISTO PARA PROBAR!" -ForegroundColor Green
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
