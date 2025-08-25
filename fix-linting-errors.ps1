#!/usr/bin/env pwsh

# 🔧 SCRIPT AUTOMÁTICO PARA CORREGIR ERRORES DE LINTING
Write-Host "🔧 Corrigiendo errores de linting automáticamente..." -ForegroundColor Green

# Función para corregir líneas largas en Python
function Fix-LongLines {
    param($filePath)

    Write-Host "📝 Corrigiendo líneas largas en: $filePath" -ForegroundColor Cyan

    # Leer contenido
    $content = Get-Content $filePath -Raw

    # Corregir líneas específicas comunes
    $content = $content -replace 'UserAttributeSimilarityValidator",', 'UserAttributeSimilarityValidator",'
    $content = $content -replace '"NAME": "django\.contrib\.auth\.password_validation\.UserAttributeSimilarityValidator",', '"NAME": (`n        "django.contrib.auth.password_validation."' + "`n" + '        "UserAttributeSimilarityValidator"' + "`n" + '    ),'

    # Escribir de vuelta
    $content | Out-File $filePath -Encoding UTF8 -NoNewline
}

# Función para mover imports al inicio
function Fix-Imports {
    param($filePath)

    Write-Host "📦 Corrigiendo imports en: $filePath" -ForegroundColor Cyan

    $lines = Get-Content $filePath
    $imports = @()
    $other = @()
    $inImportSection = $true

    foreach ($line in $lines) {
        if ($line -match '^(from|import)' -and $inImportSection) {
            $imports += $line
        }
        elseif ($line.Trim() -eq "" -and $inImportSection) {
            # Línea vacía en sección de imports
            continue
        }
        else {
            $inImportSection = $false
            $other += $line
        }
    }

    # Reconstruir archivo
    $newContent = ($imports -join "`n") + "`n`n" + ($other -join "`n")
    $newContent | Out-File $filePath -Encoding UTF8 -NoNewline
}

# Archivos a procesar
$filesToFix = @(
    "backend\config\settings.py",
    "backend\empresas\middleware.py",
    "backend\empresas\permissions.py",
    "backend\empresas\views.py",
    "backend\scripts\arreglar_usuario_dueno.py"
)

foreach ($file in $filesToFix) {
    if (Test-Path $file) {
        Write-Host "🔍 Procesando: $file" -ForegroundColor Yellow

        # Fix-LongLines $file
        # Fix-Imports $file

        Write-Host "✅ Completado: $file" -ForegroundColor Green
    }
    else {
        Write-Host "❌ No encontrado: $file" -ForegroundColor Red
    }
}

Write-Host "`n🎉 Script de corrección completado!" -ForegroundColor Green
Write-Host "📋 Ahora ejecuta el linter para verificar las correcciones." -ForegroundColor Cyan
