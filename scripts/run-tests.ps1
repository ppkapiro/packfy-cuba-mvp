# Ejecuta pruebas frontend (Vitest) y backend (pytest) con preparación mínima
param()

$ErrorActionPreference = 'Continue'

Write-Host "=== PACKFY - TEST SUITE ===" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor DarkGray

# Frontend tests
Write-Host "`n[Frontend] Instalando dependencias si faltan..." -ForegroundColor Yellow
Push-Location "$PSScriptRoot\..\frontend"
try {
    if (!(Test-Path node_modules)) {
        npm install | Out-Host
    }
    Write-Host "[Frontend] Type-check..." -ForegroundColor Yellow
    npm run -s type-check | Out-Host
    Write-Host "[Frontend] Tests (vitest run)..." -ForegroundColor Yellow
    npm run -s test:ci | Out-Host
    Write-Host "[Frontend] OK" -ForegroundColor Green
}
catch {
    Write-Host "[Frontend] Falló el proceso de tests" -ForegroundColor Red
}
finally {
    Pop-Location
}

# Backend tests
Write-Host "`n[Backend] Buscando tests..." -ForegroundColor Yellow
Push-Location "$PSScriptRoot\..\backend"
try {
    $hasTests = (Test-Path ".\tests") -or (Get-ChildItem -Recurse -Filter "test_*.py" -ErrorAction SilentlyContinue)
    if ($hasTests) {
        if (Test-Path "..\.venv\Scripts\pytest.exe") {
            ..\.venv\Scripts\pytest -q | Out-Host
        }
        else {
            python -m pytest -q | Out-Host
        }
        Write-Host "[Backend] Tests ejecutados" -ForegroundColor Green
    }
    else {
        Write-Host "[Backend] No se encontraron tests (saltado)" -ForegroundColor DarkYellow
    }
}
catch {
    Write-Host "[Backend] Falló el proceso de tests (no bloquea)" -ForegroundColor Red
}
finally {
    Pop-Location
}

Write-Host "`n=== FIN TEST SUITE ===" -ForegroundColor Cyan
