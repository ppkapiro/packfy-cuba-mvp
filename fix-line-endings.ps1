#!/usr/bin/env pwsh
# Script para corregir definitivamente las terminaciones de línea en archivos shell

Write-Host "🔧 Corrigiendo terminaciones de línea en scripts shell..." -ForegroundColor Yellow

$files = @(
    "backend/scripts/entrypoint.sh",
    "backend/scripts/run_migrations.sh"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  📝 Procesando: $file" -ForegroundColor Cyan

        # Leer contenido y convertir a LF únicamente
        $content = Get-Content $file -Raw
        $content = $content -replace "`r`n", "`n"
        $content = $content -replace "`r", "`n"

        # Escribir con codificación UTF-8 sin BOM y terminaciones LF
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText((Resolve-Path $file).Path, $content, $utf8NoBom)

        Write-Host "  ✅ Corregido: $file" -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ No encontrado: $file" -ForegroundColor Red
    }
}

Write-Host "🎉 Corrección de terminaciones de línea completada" -ForegroundColor Green
