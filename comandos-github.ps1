# COMANDOS PARA CONECTAR CON GITHUB
# Reemplaza TU_USUARIO con tu usuario real de GitHub

Write-Host "COMANDOS PARA SUBIR A GITHUB:" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

Write-Host "`n1. CONECTAR CON REPOSITORIO REMOTO:" -ForegroundColor Yellow
Write-Host "git remote add origin https://github.com/TU_USUARIO/packfy-cuba-mvp.git" -ForegroundColor Cyan

Write-Host "`n2. CAMBIAR A RAMA MAIN:" -ForegroundColor Yellow  
Write-Host "git branch -M main" -ForegroundColor Cyan

Write-Host "`n3. SUBIR CODIGO:" -ForegroundColor Yellow
Write-Host "git push -u origin main" -ForegroundColor Cyan

Write-Host "`nREEMPLAZA 'TU_USUARIO' CON TU USUARIO DE GITHUB" -ForegroundColor Red
Write-Host "Ejemplo: si tu usuario es 'pepecoder', seria:" -ForegroundColor Yellow
Write-Host "git remote add origin https://github.com/pepecoder/packfy-cuba-mvp.git" -ForegroundColor Green

Write-Host "`nTIPS:" -ForegroundColor Yellow
Write-Host "- Si te pide credenciales, usa tu token de GitHub (no password)" -ForegroundColor White
Write-Host "- Puedes generar un token en: GitHub > Settings > Developer settings > Personal access tokens" -ForegroundColor White
