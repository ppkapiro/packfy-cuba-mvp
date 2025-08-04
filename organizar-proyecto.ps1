# Scripts para limpieza y organización del proyecto

Write-Host "🧹 LIMPIEZA Y ORGANIZACION DEL PROYECTO PACKFY" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Crear directorio para scripts temporales si no existe
$tempDir = "scripts/temp"
if (!(Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force
    Write-Host "📁 Creado directorio: $tempDir" -ForegroundColor Yellow
}

# Crear directorio para documentación si no existe  
$docsDir = "docs/desarrollo"
if (!(Test-Path $docsDir)) {
    New-Item -ItemType Directory -Path $docsDir -Force
    Write-Host "📁 Creado directorio: $docsDir" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 ARCHIVOS A ORGANIZAR:" -ForegroundColor Cyan

# Scripts de testing temporal - mover a scripts/temp
$testScripts = @(
    "test-*.ps1",
    "modo-movil*.ps1", 
    "build-movil.ps1",
    "resultado-final-movil.ps1",
    "configurar-firewall.ps1"
)

Write-Host ""
Write-Host "🔧 Scripts de testing temporal:" -ForegroundColor Yellow
foreach ($pattern in $testScripts) {
    $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (Test-Path $file) {
            Write-Host "  - $file" -ForegroundColor White
        }
    }
}

# Documentación de desarrollo - mover a docs/desarrollo  
$devDocs = @(
    "*TESTING*.md",
    "*PLAN*.md", 
    "*MODERNIZACION*.md",
    "*PWA-IMPLEMENTACION*.md",
    "*RESUMEN*.md",
    "CREDENCIALES-TESTING.md"
)

Write-Host ""
Write-Host "📖 Documentación de desarrollo:" -ForegroundColor Yellow
foreach ($pattern in $devDocs) {
    $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (Test-Path $file) {
            Write-Host "  - $file" -ForegroundColor White
        }
    }
}

# Scripts principales a mantener en root
Write-Host ""
Write-Host "✅ Scripts principales (mantener en root):" -ForegroundColor Green
$mainScripts = @("dev.ps1", "cleanup.ps1", "deep-clean.ps1", "rebuild-total.ps1")
foreach ($script in $mainScripts) {
    if (Test-Path $script) {
        Write-Host "  - $script" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "❓ ¿Proceder con la organización? (Y/N)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq "Y" -or $response -eq "y") {
    Write-Host ""
    Write-Host "🚀 Iniciando organización..." -ForegroundColor Green
    
    # Mover scripts de testing
    foreach ($pattern in $testScripts) {
        $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            if (Test-Path $file) {
                Move-Item $file "$tempDir\" -Force
                Write-Host "📦 Movido: $file -> $tempDir\" -ForegroundColor Cyan
            }
        }
    }
    
    # Mover documentación de desarrollo
    foreach ($pattern in $devDocs) {
        $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            if (Test-Path $file) {
                Move-Item $file "$docsDir\" -Force
                Write-Host "📖 Movido: $file -> $docsDir\" -ForegroundColor Cyan
            }
        }
    }
    
    Write-Host ""
    Write-Host "✅ Organización completada!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 Estructura actualizada:" -ForegroundColor Yellow
    Write-Host "  scripts/temp/     - Scripts de testing temporal" -ForegroundColor White
    Write-Host "  docs/desarrollo/  - Documentación de desarrollo" -ForegroundColor White
    Write-Host "  root/             - Scripts principales y README" -ForegroundColor White
    
} else {
    Write-Host "❌ Organización cancelada" -ForegroundColor Red
}

Read-Host "`nPresiona Enter para continuar"
