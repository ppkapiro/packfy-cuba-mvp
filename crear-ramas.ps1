# CREAR RAMAS DE DESARROLLO PARA PACKFY
Write-Host "CREANDO ESTRUCTURA DE RAMAS PARA DESARROLLO" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

Write-Host "`nESTRUCTURA DE RAMAS RECOMENDADA:" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow
Write-Host "main - Rama principal (produccion)" -ForegroundColor Green
Write-Host "develop - Rama de desarrollo principal" -ForegroundColor Cyan
Write-Host "feature/pwa-improvements - Mejoras PWA" -ForegroundColor Blue
Write-Host "feature/mobile-optimization - Optimizacion movil" -ForegroundColor Blue
Write-Host "feature/dashboard-enhancement - Mejoras dashboard" -ForegroundColor Blue
Write-Host "feature/notifications - Sistema notificaciones" -ForegroundColor Blue
Write-Host "hotfix/critical-fixes - Correcciones criticas" -ForegroundColor Red
Write-Host "release/v1.0 - Preparacion version 1.0" -ForegroundColor Magenta

Write-Host "`n1. CREAR RAMA DEVELOP (base para desarrollo):" -ForegroundColor Yellow
git checkout -b develop
git push -u origin develop
Write-Host "✅ Rama develop creada" -ForegroundColor Green

Write-Host "`n2. CREAR RAMAS DE FEATURES:" -ForegroundColor Yellow

# Feature: PWA Improvements
git checkout -b feature/pwa-improvements
git push -u origin feature/pwa-improvements
Write-Host "✅ Rama feature/pwa-improvements creada" -ForegroundColor Green

# Feature: Mobile Optimization  
git checkout -b feature/mobile-optimization
git push -u origin feature/mobile-optimization
Write-Host "✅ Rama feature/mobile-optimization creada" -ForegroundColor Green

# Feature: Dashboard Enhancement
git checkout -b feature/dashboard-enhancement
git push -u origin feature/dashboard-enhancement
Write-Host "✅ Rama feature/dashboard-enhancement creada" -ForegroundColor Green

# Feature: Notifications System
git checkout -b feature/notifications
git push -u origin feature/notifications
Write-Host "✅ Rama feature/notifications creada" -ForegroundColor Green

Write-Host "`n3. CREAR RAMAS DE MANTENIMIENTO:" -ForegroundColor Yellow

# Hotfix branch
git checkout main
git checkout -b hotfix/critical-fixes
git push -u origin hotfix/critical-fixes
Write-Host "✅ Rama hotfix/critical-fixes creada" -ForegroundColor Green

# Release branch
git checkout develop
git checkout -b release/v1.0
git push -u origin release/v1.0
Write-Host "✅ Rama release/v1.0 creada" -ForegroundColor Green

Write-Host "`n4. VOLVER A RAMA DEVELOP PARA TRABAJAR:" -ForegroundColor Yellow
git checkout develop
Write-Host "✅ Cambiado a rama develop" -ForegroundColor Green

Write-Host "`n5. VERIFICAR RAMAS CREADAS:" -ForegroundColor Yellow
git branch -a
Write-Host "✅ Ramas verificadas" -ForegroundColor Green

Write-Host "`nFLUJO DE TRABAJO RECOMENDADO:" -ForegroundColor Yellow
Write-Host "==============================" -ForegroundColor Yellow
Write-Host "1. Desarrollo diario: feature/nombre-feature" -ForegroundColor White
Write-Host "2. Integration: develop" -ForegroundColor White
Write-Host "3. Testing: release/vX.X" -ForegroundColor White
Write-Host "4. Production: main" -ForegroundColor White
Write-Host "5. Hotfixes: hotfix/descripcion" -ForegroundColor White

Write-Host "`nCOMANDOS UTILES:" -ForegroundColor Yellow
Write-Host "================" -ForegroundColor Yellow
Write-Host "Ver ramas: git branch -a" -ForegroundColor Cyan
Write-Host "Cambiar rama: git checkout nombre-rama" -ForegroundColor Cyan
Write-Host "Crear nueva feature: git checkout -b feature/nueva-funcionalidad" -ForegroundColor Cyan
Write-Host "Merge a develop: git checkout develop && git merge feature/nombre" -ForegroundColor Cyan
Write-Host "Push rama: git push -u origin nombre-rama" -ForegroundColor Cyan

Write-Host "`n✅ ESTRUCTURA DE RAMAS COMPLETADA!" -ForegroundColor Green
Write-Host "Ahora puedes trabajar de forma organizada en cada feature." -ForegroundColor Yellow
