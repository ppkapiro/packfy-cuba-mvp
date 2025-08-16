# 🔍 DIAGNÓSTICO RÁPIDO HTTPS MÓVIL - PACKFY CUBA

param(
    [switch]$Full
)

$Green = "`e[32m"
$Red = "`e[31m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$Reset = "`e[0m"

function Test-HttpsEndpoint {
    param([string]$Url, [string]$Description)

    try {
        $response = Invoke-WebRequest -Uri $Url -SkipCertificateCheck -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "${Green}✅ $Description${Reset} - Status: $($response.StatusCode)"
            return $true
        }
        else {
            Write-Host "${Yellow}⚠️ $Description${Reset} - Status: $($response.StatusCode)"
            return $false
        }
    }
    catch {
        Write-Host "${Red}❌ $Description${Reset} - Error: $($_.Exception.Message)"
        return $false
    }
}

function Get-LocalIPs {
    $ips = @()
    $ips += (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notmatch "^127\." -and $_.IPAddress -notmatch "^169\.254\." } | Select-Object -ExpandProperty IPAddress)
    return $ips
}

Write-Host "${Blue}🔍 DIAGNÓSTICO HTTPS MÓVIL - PACKFY CUBA v4.0${Reset}"
Write-Host "=================================================="

# 1. Verificar IPs disponibles
Write-Host "`n${Blue}📡 DIRECCIONES IP DISPONIBLES:${Reset}"
$localIPs = Get-LocalIPs
foreach ($ip in $localIPs) {
    Write-Host "  - $ip"
}

# 2. Verificar estado de contenedores
Write-Host "`n${Blue}🐳 ESTADO DE CONTENEDORES:${Reset}"
try {
    $containers = docker-compose ps --format json | ConvertFrom-Json
    foreach ($container in $containers) {
        $status = if ($container.State -eq "running") { "${Green}✅" } else { "${Red}❌" }
        Write-Host "  $status $($container.Name) - $($container.State)${Reset}"
    }
}
catch {
    Write-Host "${Red}❌ Error al verificar contenedores${Reset}"
}

# 3. Verificar endpoints HTTPS principales
Write-Host "`n${Blue}🔒 VERIFICACIÓN ENDPOINTS HTTPS:${Reset}"

# Frontend localhost
Test-HttpsEndpoint "https://localhost:5173" "Frontend Localhost"

# Frontend IP de red
foreach ($ip in $localIPs) {
    Test-HttpsEndpoint "https://${ip}:5173" "Frontend IP $ip"
}

# Backend localhost
Test-HttpsEndpoint "https://localhost:8443/api/health/" "Backend API Localhost"

# Backend IP de red
foreach ($ip in $localIPs) {
    Test-HttpsEndpoint "https://${ip}:8443/api/health/" "Backend API IP $ip"
}

# 4. Verificar PWA assets
Write-Host "`n${Blue}📱 VERIFICACIÓN PWA ASSETS:${Reset}"
foreach ($ip in $localIPs) {
    Test-HttpsEndpoint "https://${ip}:5173/manifest.json" "PWA Manifest IP $ip"
    Test-HttpsEndpoint "https://${ip}:5173/sw.js" "Service Worker IP $ip"
}

# 5. Verificar certificados SSL
Write-Host "`n${Blue}🔑 VERIFICACIÓN CERTIFICADOS SSL:${Reset}"
try {
    if (Test-Path ".\frontend\certs\cert.crt") {
        Write-Host "${Green}✅ Certificado SSL encontrado${Reset}"

        # Verificar validez del certificado
        $certInfo = openssl x509 -in ".\frontend\certs\cert.crt" -text -noout 2>$null
        if ($certInfo) {
            Write-Host "${Green}✅ Certificado SSL válido${Reset}"
        }
        else {
            Write-Host "${Red}❌ Certificado SSL inválido${Reset}"
        }
    }
    else {
        Write-Host "${Red}❌ Certificado SSL no encontrado${Reset}"
    }
}
catch {
    Write-Host "${Yellow}⚠️ No se pudo verificar certificado SSL${Reset}"
}

if ($Full) {
    # 6. Verificar configuración de red Docker
    Write-Host "`n${Blue}🌐 CONFIGURACIÓN RED DOCKER:${Reset}"
    try {
        $networks = docker network ls --format "{{.Name}}" | Where-Object { $_ -like "*packfy*" }
        foreach ($network in $networks) {
            Write-Host "  - Red: $network"
            docker network inspect $network --format "{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{end}}" | ForEach-Object {
                Write-Host "    $($_)"
            }
        }
    }
    catch {
        Write-Host "${Red}❌ Error al verificar redes Docker${Reset}"
    }

    # 7. Verificar logs recientes
    Write-Host "`n${Blue}📋 LOGS RECIENTES (Últimas 5 líneas):${Reset}"
    try {
        Write-Host "${Yellow}Frontend:${Reset}"
        docker-compose logs frontend --tail=5 2>$null | ForEach-Object { Write-Host "  $_" }

        Write-Host "${Yellow}Backend:${Reset}"
        docker-compose logs backend --tail=5 2>$null | ForEach-Object { Write-Host "  $_" }
    }
    catch {
        Write-Host "${Red}❌ Error al obtener logs${Reset}"
    }
}

# 8. Generar URLs para testing móvil
Write-Host "`n${Blue}📱 URLS PARA TESTING MÓVIL:${Reset}"
Write-Host "${Green}Conecta tu móvil a la misma red WiFi y usa estas URLs:${Reset}"
foreach ($ip in $localIPs) {
    Write-Host "  🔗 https://${ip}:5173"
}

Write-Host "`n${Blue}💡 CONSEJOS PARA MÓVIL:${Reset}"
Write-Host "  1. Acepta el certificado SSL autofirmado en el navegador móvil"
Write-Host "  2. Verifica que el móvil esté en la misma red WiFi"
Write-Host "  3. Desactiva temporalmente el antivirus/firewall si es necesario"
Write-Host "  4. Usa navegador móvil actualizado (Chrome/Safari)"

Write-Host "`n${Blue}🔧 COMANDOS ÚTILES:${Reset}"
Write-Host "  ${Green}.\https-diagnostico.ps1 -Full${Reset}     - Diagnóstico completo"
Write-Host "  ${Green}.\mobile-manage.ps1 mobile-test${Reset}   - Test específico móvil"
Write-Host "  ${Green}docker-compose logs frontend${Reset}      - Ver logs frontend"
Write-Host "  ${Green}docker-compose logs backend${Reset}       - Ver logs backend"
