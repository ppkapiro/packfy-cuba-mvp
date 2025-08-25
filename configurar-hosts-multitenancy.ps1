# 🔐 CONFIGURAR HOSTS PARA MULTITENANCY - AUTOMATIZADO
# Packfy Cuba - Configuración automática de subdominios

Write-Host "🔐 CONFIGURANDO ARCHIVO HOSTS PARA MULTITENANCY" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Verificar permisos de administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ ERROR: Este script requiere permisos de administrador" -ForegroundColor Red
    Write-Host "💡 Solución: Haz clic derecho en PowerShell → 'Ejecutar como administrador'" -ForegroundColor Yellow
    Write-Host "   Luego ejecuta nuevamente: .\configurar-hosts-multitenancy.ps1" -ForegroundColor Yellow
    Read-Host "Presiona Enter para cerrar..."
    exit 1
}

Write-Host "✅ Ejecutando con permisos de administrador" -ForegroundColor Green

# Ruta del archivo hosts
$hostsPath = "C:\Windows\System32\drivers\etc\hosts"

# Backup del archivo hosts original
$backupPath = "$hostsPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"

Write-Host ""
Write-Host "📋 CONFIGURACIÓN MULTITENANCY:" -ForegroundColor Magenta
Write-Host "🔄 Creando backup: $backupPath" -ForegroundColor Blue

try {
    Copy-Item $hostsPath $backupPath
    Write-Host "✅ Backup creado exitosamente" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error creando backup: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Leer contenido actual del archivo hosts
$currentHosts = Get-Content $hostsPath

# Definir entradas para multitenancy
$multitenancyEntries = @(
    "",
    "# === PACKFY CUBA MULTITENANCY ===",
    "# Configurado automáticamente el $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "127.0.0.1       packfy-express.localhost",
    "127.0.0.1       cuba-fast-delivery.localhost",
    "127.0.0.1       habana-cargo.localhost",
    "127.0.0.1       app.localhost",
    "127.0.0.1       admin.localhost",
    "# === FIN PACKFY MULTITENANCY ==="
)

# Verificar si ya existen entradas de Packfy
$packfyExists = $currentHosts | Where-Object { $_ -match "packfy|PACKFY" }

if ($packfyExists) {
    Write-Host ""
    Write-Host "⚠️  ENTRADAS EXISTENTES DETECTADAS:" -ForegroundColor Yellow
    Write-Host "Se encontraron entradas relacionadas con Packfy en el archivo hosts:" -ForegroundColor Yellow

    foreach ($entry in $packfyExists) {
        Write-Host "   $entry" -ForegroundColor Gray
    }

    Write-Host ""
    $response = Read-Host "¿Deseas continuar y agregar/actualizar las entradas? (s/n)"

    if ($response -ne 's' -and $response -ne 'S' -and $response -ne 'y' -and $response -ne 'Y') {
        Write-Host "❌ Operación cancelada por el usuario" -ForegroundColor Red
        exit 0
    }

    # Remover entradas existentes de Packfy
    Write-Host "🔄 Removiendo entradas existentes de Packfy..." -ForegroundColor Blue
    $filteredHosts = $currentHosts | Where-Object {
        $_ -notmatch "packfy|PACKFY" -and
        $_ -notmatch "app\.localhost" -and
        $_ -notmatch "admin\.localhost"
    }
    $currentHosts = $filteredHosts
}

Write-Host ""
Write-Host "➕ AGREGANDO ENTRADAS MULTITENANCY:" -ForegroundColor Green

foreach ($entry in $multitenancyEntries) {
    if ($entry -notmatch "^#" -and $entry.Trim() -ne "") {
        Write-Host "   $entry" -ForegroundColor White
    }
}

# Combinar contenido original con nuevas entradas
$newHostsContent = $currentHosts + $multitenancyEntries

# Escribir al archivo hosts
try {
    $newHostsContent | Out-File -FilePath $hostsPath -Encoding ASCII -Force
    Write-Host ""
    Write-Host "✅ ARCHIVO HOSTS ACTUALIZADO EXITOSAMENTE" -ForegroundColor Green
}
catch {
    Write-Host ""
    Write-Host "❌ Error escribiendo archivo hosts: $($_.Exception.Message)" -ForegroundColor Red

    # Restaurar backup
    Write-Host "🔄 Restaurando backup..." -ForegroundColor Yellow
    try {
        Copy-Item $backupPath $hostsPath -Force
        Write-Host "✅ Backup restaurado" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Error restaurando backup!" -ForegroundColor Red
    }
    exit 1
}

Write-Host ""
Write-Host "🧪 VERIFICANDO CONFIGURACIÓN:" -ForegroundColor Magenta

# Verificar que las entradas están en el archivo
$verificationEntries = @(
    "packfy-express.localhost",
    "cuba-fast-delivery.localhost",
    "habana-cargo.localhost"
)

foreach ($domain in $verificationEntries) {
    $exists = Get-Content $hostsPath | Where-Object { $_ -match $domain }
    if ($exists) {
        Write-Host "✅ $domain configurado" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $domain NO encontrado" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🚀 CONFIGURACIÓN COMPLETADA" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host ""
Write-Host "📋 SIGUIENTES PASOS:" -ForegroundColor Magenta
Write-Host "1. ✅ Archivo hosts configurado" -ForegroundColor Green
Write-Host "2. 🔄 Reinicia tu navegador (Chrome/Edge/Firefox)" -ForegroundColor Yellow
Write-Host "3. 🌐 Ejecuta: .\probar-dominios-multitenancy.ps1" -ForegroundColor Yellow
Write-Host "4. 🧪 Prueba los dominios configurados" -ForegroundColor Yellow

Write-Host ""
Write-Host "🌐 DOMINIOS DISPONIBLES:" -ForegroundColor Magenta
Write-Host "• http://localhost:5173 (Admin general)" -ForegroundColor White
Write-Host "• http://packfy-express.localhost:5173 (PackFy Express)" -ForegroundColor White
Write-Host "• http://cuba-fast-delivery.localhost:5173 (Cuba Fast Delivery)" -ForegroundColor White
Write-Host "• http://habana-cargo.localhost:5173 (Habana Cargo)" -ForegroundColor White

Write-Host ""
Write-Host "💾 BACKUP CREADO EN: $backupPath" -ForegroundColor Blue

Write-Host ""
Read-Host "Presiona Enter para continuar con las pruebas..."

# Ejecutar automáticamente el script de pruebas
Write-Host "🚀 Ejecutando pruebas de dominios..." -ForegroundColor Green
try {
    & ".\probar-dominios-multitenancy.ps1"
}
catch {
    Write-Host "❌ Error ejecutando pruebas. Ejecuta manualmente: .\probar-dominios-multitenancy.ps1" -ForegroundColor Red
}
