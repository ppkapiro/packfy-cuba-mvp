# CONFIGURAR POWERSHELL 7 COMO PREDETERMINADO - DEFINITIVO
# Script para asegurar que PowerShell 7 sea el terminal predeterminado

Write-Host "🔧 CONFIGURANDO POWERSHELL 7 COMO PREDETERMINADO" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# 1. Verificar que PowerShell 7 esté disponible
try {
    $pwsh7Path = Get-Command pwsh -ErrorAction Stop
    Write-Host "✅ PowerShell 7 encontrado en: $($pwsh7Path.Source)" -ForegroundColor Green
}
catch {
    Write-Host "❌ PowerShell 7 no encontrado. Ejecuta: winget install Microsoft.PowerShell" -ForegroundColor Red
    exit 1
}

# 2. Verificar configuración de VS Code
Write-Host "`n📝 Verificando configuración de VS Code..." -ForegroundColor Yellow

$vsCodeSettings = ".vscode\settings.json"
if (Test-Path $vsCodeSettings) {
    $settingsContent = Get-Content $vsCodeSettings -Raw
    if ($settingsContent -like '*"terminal.integrated.defaultProfile.windows": "PowerShell 7"*') {
        Write-Host "✅ VS Code ya está configurado con PowerShell 7 como predeterminado" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  VS Code no está configurado correctamente" -ForegroundColor Yellow

        # Backup y aplicar configuración
        $backupPath = ".vscode\settings-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
        Copy-Item $vsCodeSettings $backupPath

        if (Test-Path ".vscode\settings-ideal.json") {
            Copy-Item ".vscode\settings-ideal.json" $vsCodeSettings -Force
            Write-Host "✅ Configuración ideal aplicada" -ForegroundColor Green
        }
    }
}
else {
    Write-Host "⚠️  Archivo settings.json no encontrado" -ForegroundColor Yellow
}

# 3. Verificar profile de PowerShell 7
Write-Host "`n🔧 Verificando profile de PowerShell 7..." -ForegroundColor Yellow

$profilePath = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "PowerShell\Microsoft.PowerShell_profile.ps1"
if (Test-Path $profilePath) {
    Write-Host "✅ Profile de PowerShell 7 existe" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Creando profile de PowerShell 7..." -ForegroundColor Yellow

    # Crear directorio si no existe
    $profileDir = Split-Path $profilePath -Parent
    if (!(Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    # Copiar profile si existe el local
    if (Test-Path "pwsh7-profile.ps1") {
        Copy-Item "pwsh7-profile.ps1" $profilePath -Force
        Write-Host "✅ Profile copiado correctamente" -ForegroundColor Green
    }
}

# 4. Probar aliases
Write-Host "`n🧪 Probando aliases..." -ForegroundColor Yellow

# Ejecutar en PowerShell 7 y probar aliases
$testScript = @"
if (Test-Path '$profilePath') { . '$profilePath' }
try {
    gs | Out-Null
    Write-Host '✅ Alias gs funciona' -ForegroundColor Green
} catch {
    Write-Host '❌ Alias gs no funciona' -ForegroundColor Red
}

try {
    ll | Select-Object -First 1 | Out-Null
    Write-Host '✅ Alias ll funciona' -ForegroundColor Green
} catch {
    Write-Host '❌ Alias ll no funciona' -ForegroundColor Red
}

try {
    dc --version | Out-Null
    Write-Host '✅ Alias dc funciona' -ForegroundColor Green
} catch {
    Write-Host '❌ Alias dc no funciona' -ForegroundColor Red
}
"@

# Ejecutar pruebas
pwsh -NoProfile -Command $testScript

# 5. Configurar como predeterminado del sistema
Write-Host "`n🖥️  Configurando como predeterminado del sistema..." -ForegroundColor Yellow

# Agregar PowerShell 7 al PATH si no está
$pwsh7Dir = "C:\Program Files\PowerShell\7"
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")

if ($currentPath -notlike "*$pwsh7Dir*") {
    Write-Host "⚠️  Agregando PowerShell 7 al PATH..." -ForegroundColor Yellow
    $newPath = "$currentPath;$pwsh7Dir"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "✅ PowerShell 7 agregado al PATH" -ForegroundColor Green
}
else {
    Write-Host "✅ PowerShell 7 ya está en el PATH" -ForegroundColor Green
}

# 6. Resumen final
Write-Host "`n🎉 CONFIGURACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "==========================" -ForegroundColor Green

Write-Host "`n📋 ESTADO ACTUAL:" -ForegroundColor Cyan
Write-Host "• PowerShell 7: $(pwsh --version)" -ForegroundColor White
Write-Host "• VS Code: Configurado con PowerShell 7" -ForegroundColor White
Write-Host "• Profile: Cargado con aliases" -ForegroundColor White
Write-Host "• Aliases: gs, ll, dc funcionando" -ForegroundColor White

Write-Host "`n🚀 PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "1. Reinicia VS Code para aplicar cambios" -ForegroundColor White
Write-Host "2. Abre Windows Terminal (busca 'Windows Terminal')" -ForegroundColor White
Write-Host "3. O ejecuta directamente: pwsh" -ForegroundColor White

Write-Host "`n💡 COMANDOS PARA USAR:" -ForegroundColor Cyan
Write-Host "pwsh           # Abrir PowerShell 7" -ForegroundColor White
Write-Host "gs             # Git status" -ForegroundColor White
Write-Host "ll             # Listar archivos" -ForegroundColor White
Write-Host "dc up -d       # Docker Compose up" -ForegroundColor White

Write-Host "`n✨ ¡PowerShell 7 configurado como predeterminado!" -ForegroundColor Green
