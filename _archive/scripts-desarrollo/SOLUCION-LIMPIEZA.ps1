# 🧹 LIMPIEZA DE ARCHIVOS VACÍOS - PACKFY CUBA MVP
# Script para limpiar archivos de documentación vacíos y reorganizar

Write-Host "🇨🇺 PACKFY CUBA - Limpieza de archivos vacíos..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Lista de archivos vacíos identificados
$archivosVacios = @(
    "ANALISIS-CODIGO-PROFUNDO-v4.0.md",
    "ANALISIS-ESTADO-PROYECTO-COMPLETO.md",
    "DIAGNOSTICO-SISTEMATICO-COMPLETADO.md",
    "EJECUCION-COMPLETADA-REPORTE-FINAL.md",
    "GUIA-VALIDACION-RAPIDA.md",
    "IMPLEMENTACION-CSS-DOCKER-COMPLETADA.md",
    "LIMPIEZA-RADICAL-COMPLETADA.md",
    "MEJORAS-CRITICAS-COMPLETADAS-v4.1.md",
    "MEJORAS-CRITICAS-HOY.md",
    "OPTIMIZACION-CSS-COMPLETA-v6.0.md",
    "PLAN-ACCION-ESTRATEGICO-COMPLETO.md",
    "REVISION-COMPLETA-WARNINGS-SOLUCIONADOS.md",
    "SISTEMA-CSS-UNIFICADO-COMPLETADO-v6.md"
)

# 1. Crear carpeta de archivo para documentos obsoletos
Write-Host "📁 1. Creando carpeta de archivo..." -ForegroundColor Yellow
$archivoDir = "archive/docs-vacios-$(Get-Date -Format 'yyyy-MM-dd')"
if (!(Test-Path $archivoDir)) {
    New-Item -ItemType Directory -Path $archivoDir -Force | Out-Null
    Write-Host "✅ Carpeta creada: $archivoDir" -ForegroundColor Green
}

# 2. Mover archivos vacíos al archivo
Write-Host "`n🗂️ 2. Moviendo archivos vacíos..." -ForegroundColor Yellow
$archivosMVCount = 0

foreach ($archivo in $archivosVacios) {
    if (Test-Path $archivo) {
        $tamaño = (Get-Item $archivo).Length
        if ($tamaño -eq 0) {
            Move-Item $archivo $archivoDir -Force
            Write-Host "✅ Movido: $archivo (0 bytes)" -ForegroundColor Green
            $archivosMVCount++
        }
        else {
            Write-Host "⚠️ Saltado: $archivo ($tamaño bytes - no vacío)" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "ℹ️ No encontrado: $archivo" -ForegroundColor Gray
    }
}

# 3. Crear archivo README en el archivo
Write-Host "`n📝 3. Creando documentación del archivo..." -ForegroundColor Yellow
$readmeContent = @"
# 📚 Archivos de Documentación Vacíos - $(Get-Date -Format 'yyyy-MM-dd')

## 🗑️ Archivos Movidos

Estos archivos estaban vacíos (0 bytes) y fueron movidos aquí durante la limpieza del proyecto:

"@

foreach ($archivo in $archivosVacios) {
    if (Test-Path "$archivoDir\$archivo") {
        $readmeContent += "`n- ✅ $archivo"
    }
}

$readmeContent += @"

## 📋 Razón del Archivo

Estos archivos fueron creados durante el desarrollo pero nunca fueron completados con contenido.
Para mantener la organización del proyecto, fueron movidos a esta carpeta de archivo.

## 🔄 Restauración

Si necesitas restaurar algún archivo:
``````powershell
Move-Item "archive/docs-vacios-$(Get-Date -Format 'yyyy-MM-dd')/NOMBRE_ARCHIVO.md" ./
``````

---
*Limpieza automática realizada por: SOLUCION-LIMPIEZA.ps1*
*Fecha: $(Get-Date)*
"@

$readmeContent | Out-File "$archivoDir\README.md" -Encoding UTF8

# 4. Verificar archivos restantes
Write-Host "`n📊 4. Verificando archivos restantes..." -ForegroundColor Yellow
$archivosRestantes = Get-ChildItem -Name "*.md" | Where-Object { (Get-Item $_).Length -eq 0 }

if ($archivosRestantes.Count -eq 0) {
    Write-Host "✅ No quedan archivos .md vacíos en el directorio raíz" -ForegroundColor Green
}
else {
    Write-Host "⚠️ Archivos vacíos restantes:" -ForegroundColor Yellow
    $archivosRestantes | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
}

# 5. Mostrar resumen de archivos de documentación útiles
Write-Host "`n📋 5. Documentación útil disponible:" -ForegroundColor Yellow
$archivosUtiles = Get-ChildItem -Name "*.md" | Where-Object { (Get-Item $_).Length -gt 0 } | Sort-Object

foreach ($archivo in $archivosUtiles) {
    $tamaño = [math]::Round((Get-Item $archivo).Length / 1KB, 1)
    Write-Host "✅ $archivo ($tamaño KB)" -ForegroundColor Green
}

# 6. Verificar estructura del proyecto
Write-Host "`n🏗️ 6. Estructura de documentación recomendada:" -ForegroundColor Yellow
$estructuraRecomendada = @(
    "README.md",
    "CHANGELOG.md",
    "STATUS.md",
    "TROUBLESHOOTING.md",
    "ANALISIS-PROFUNDO-ESTADO-ACTUAL-COMPLETO.md"
)

foreach ($doc in $estructuraRecomendada) {
    if (Test-Path $doc) {
        $tamaño = [math]::Round((Get-Item $doc).Length / 1KB, 1)
        Write-Host "✅ $doc ($tamaño KB)" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $doc - FALTANTE" -ForegroundColor Red
    }
}

Write-Host "`n🎉 Limpieza completada!" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "📊 Resumen:" -ForegroundColor White
Write-Host "  - Archivos movidos: $archivosMVCount" -ForegroundColor Green
Write-Host "  - Carpeta de archivo: $archivoDir" -ForegroundColor Blue
Write-Host "  - Documentación útil: $($archivosUtiles.Count) archivos" -ForegroundColor Green
