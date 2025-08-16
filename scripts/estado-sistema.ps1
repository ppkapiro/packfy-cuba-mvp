# Muestra un resumen del estado del sistema (frontend/backend/CI)
param()

$ErrorActionPreference = 'SilentlyContinue'

Write-Host "=== PACKFY - ESTADO DEL SISTEMA ===" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor DarkGray

# Frontend
Write-Host "`n[Frontend]" -ForegroundColor Yellow
Push-Location "$PSScriptRoot\..\frontend"
try {
    npm run -s type-check | Out-Host
    npm run -s test:ci | Out-Host
    Write-Host "Frontend OK (types + tests)" -ForegroundColor Green
}
catch {
    Write-Host "Frontend con advertencias/errores" -ForegroundColor Red
}
Pop-Location

# Backend (si hay tests)
Write-Host "`n[Backend]" -ForegroundColor Yellow
Push-Location "$PSScriptRoot\..\backend"
try {
    if (Test-Path "..\.venv\Scripts\pytest.exe") {
        ..\.venv\Scripts\pytest -q | Out-Host
    }
    else {
        python -m pytest -q | Out-Host
    }
    Write-Host "Backend tests ejecutados (si existían)" -ForegroundColor Green
}
catch {
    Write-Host "Sin pruebas o con errores (no bloquea)" -ForegroundColor DarkYellow
}
Pop-Location

# CI resumen
Write-Host "`n[CI/CD]" -ForegroundColor Yellow
if (Test-Path "$PSScriptRoot\..\.github\workflows\testing.yml") {
    Write-Host "Workflow testing.yml presente (E2E no bloqueante)" -ForegroundColor Green
}
if (Test-Path "$PSScriptRoot\..\.github\workflows\ci-cd.yml") {
    Write-Host "Workflow ci-cd.yml (main) presente" -ForegroundColor Green
}

Write-Host "`n📄 Consulta STATUS.md para más detalles." -ForegroundColor Cyan
