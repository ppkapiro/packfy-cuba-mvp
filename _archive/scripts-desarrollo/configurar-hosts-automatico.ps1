# 🔐 CONFIGURAR HOSTS AUTOMÁTICO - SIN INTERACCIÓN
# Packfy Cuba - Configuración automática y silenciosa

# Verificar permisos de administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "🔐 Ejecutando con permisos elevados..." -ForegroundColor Cyan
    Start-Process PowerShell -ArgumentList "-File", $PSCommandPath -Verb RunAs
    exit
}

Write-Host "🇨🇺 CONFIGURACIÓN AUTOMÁTICA HOSTS - PACKFY MULTITENANCY" -ForegroundColor Cyan

# Ruta del archivo hosts
$hostsPath = "C:\Windows\System32\drivers\etc\hosts"

# Leer contenido actual
$currentHosts = Get-Content $hostsPath

# Definir entradas para multitenancy
$multitenancyEntries = @(
    "",
    "# === PACKFY CUBA MULTITENANCY ===",
    "127.0.0.1       packfy-express.localhost",
    "127.0.0.1       cuba-fast-delivery.localhost",
    "127.0.0.1       habana-cargo.localhost",
    "127.0.0.1       app.localhost",
    "127.0.0.1       admin.localhost",
    "# === FIN PACKFY MULTITENANCY ==="
)

# Remover entradas existentes de Packfy si las hay
$filteredHosts = $currentHosts | Where-Object {
    $_ -notmatch "packfy|PACKFY" -and
    $_ -notmatch "app\.localhost" -and
    $_ -notmatch "admin\.localhost"
}

# Combinar contenido
$newHostsContent = $filteredHosts + $multitenancyEntries

# Escribir archivo
try {
    $newHostsContent | Out-File -FilePath $hostsPath -Encoding ASCII -Force
    Write-Host "✅ Archivo hosts configurado automáticamente" -ForegroundColor Green

    # Verificar configuración
    $verificationEntries = @("packfy-express.localhost", "cuba-fast-delivery.localhost", "habana-cargo.localhost")
    foreach ($domain in $verificationEntries) {
        $exists = Get-Content $hostsPath | Where-Object { $_ -match $domain }
        if ($exists) {
            Write-Host "✅ $domain configurado" -ForegroundColor Green
        }
    }

    Write-Host ""
    Write-Host "🌐 DOMINIOS CONFIGURADOS:" -ForegroundColor Magenta
    Write-Host "• http://packfy-express.localhost:5173" -ForegroundColor White
    Write-Host "• http://cuba-fast-delivery.localhost:5173" -ForegroundColor White
    Write-Host "• http://habana-cargo.localhost:5173" -ForegroundColor White

    # Esperar 3 segundos antes de continuar
    Start-Sleep -Seconds 3
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
