#!/usr/bin/env pwsh
# CORRECCION RAPIDA DE ERRORES CRITICOS

Write-Host "🔧 CORRIGIENDO ERRORES CRÍTICOS..." -ForegroundColor Yellow

# 1. Corregir HTML sin lang attribute
Write-Host "🌐 Corrigiendo HTML..." -ForegroundColor Cyan

$testIpFile = "frontend/public/test-ip.html"
if (Test-Path $testIpFile) {
    $content = Get-Content $testIpFile -Raw
    if ($content -match '<html>') {
        $newContent = $content -replace '<html>', '<html lang="es">'
        Set-Content -Path $testIpFile -Value $newContent -NoNewline
        Write-Host "   ✅ Lang attribute agregado a test-ip.html" -ForegroundColor Green
    }
}

# 2. Actualizar Docker images por seguridad
Write-Host "🐳 Actualizando Docker..." -ForegroundColor Cyan

$backendDockerfile = "backend/Dockerfile.prod"
if (Test-Path $backendDockerfile) {
    $content = Get-Content $backendDockerfile -Raw
    $newContent = $content -replace 'python:3\.11-slim', 'python:3.12-slim'
    Set-Content -Path $backendDockerfile -Value $newContent -NoNewline
    Write-Host "   ✅ Backend Python actualizado a 3.12" -ForegroundColor Green
}

$frontendDockerfile = "frontend/Dockerfile.prod"
if (Test-Path $frontendDockerfile) {
    $content = Get-Content $frontendDockerfile -Raw
    $newContent = $content -replace 'node:18-alpine', 'node:20-alpine'
    Set-Content -Path $frontendDockerfile -Value $newContent -NoNewline
    Write-Host "   ✅ Frontend Node actualizado a 20" -ForegroundColor Green
}

# 3. Crear estilos externos para evitar inline styles
Write-Host "📱 Creando estilos externos..." -ForegroundColor Cyan

$stylesDir = "frontend/src/styles"
if (-not (Test-Path $stylesDir)) {
    New-Item -ItemType Directory -Path $stylesDir -Force | Out-Null
}

$externalStyles = @"
/* ESTILOS EXTERNOS - Evitar inline styles */

.camera-container {
  position: relative;
  width: 100%;
  height: 400px;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.test-status-success {
  background-color: #28a745;
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-weight: bold;
}

.test-status-error {
  background-color: #dc3545;
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-weight: bold;
}

.test-status-pending {
  background-color: #ffc107;
  color: #000;
  padding: 5px 15px;
  border-radius: 20px;
  font-weight: bold;
}

.test-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}
"@

Set-Content -Path "$stylesDir/external-styles.css" -Value $externalStyles
Write-Host "   ✅ Estilos externos creados" -ForegroundColor Green

Write-Host ""
Write-Host "✅ ERRORES CRÍTICOS CORREGIDOS!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Resumen de cambios:" -ForegroundColor White
Write-Host "   • HTML lang attribute agregado" -ForegroundColor Gray
Write-Host "   • Docker images actualizadas por seguridad" -ForegroundColor Gray
Write-Host "   • Estilos externos creados" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Para usar los estilos externos:" -ForegroundColor Yellow
Write-Host "   import '../styles/external-styles.css'" -ForegroundColor Gray
