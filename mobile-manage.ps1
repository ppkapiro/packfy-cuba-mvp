# 📱 PACKFY CUBA - Script de Gestión Móvil v4.0
# Script para manejar contenedores con optimizaciones móviles

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("start", "stop", "restart", "rebuild", "logs", "status", "mobile-test")]
    [string]$Action
)

# Colores para output
$Green = "`e[32m"
$Red = "`e[31m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$Reset = "`e[0m"

function Write-Status {
    param([string]$Message, [string]$Color = $Blue)
    Write-Host "${Color}🇨🇺 PACKFY CUBA MÓVIL${Reset} - $Message"
}

function Write-Success {
    param([string]$Message)
    Write-Host "${Green}✅ $Message${Reset}"
}

function Write-Error {
    param([string]$Message)
    Write-Host "${Red}❌ $Message${Reset}"
}

function Write-Warning {
    param([string]$Message)
    Write-Host "${Yellow}⚠️ $Message${Reset}"
}

# Verificar si Docker está corriendo
try {
    docker info > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker no está corriendo. Por favor inicia Docker Desktop."
        exit 1
    }
}
catch {
    Write-Error "Docker no está disponible. Instala Docker Desktop."
    exit 1
}

switch ($Action) {
    "start" {
        Write-Status "Iniciando PACKFY CUBA con optimizaciones móviles..."
        docker-compose up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Contenedores iniciados correctamente"
            Write-Status "Frontend móvil optimizado: https://localhost:5173"
            Write-Status "Backend API: https://localhost:8000"
            Write-Status "Verificando salud de servicios..."
            Start-Sleep 10
            docker-compose ps
        }
        else {
            Write-Error "Error al iniciar contenedores"
        }
    }

    "stop" {
        Write-Status "Deteniendo contenedores PACKFY CUBA..."
        docker-compose down
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Contenedores detenidos correctamente"
        }
        else {
            Write-Error "Error al detener contenedores"
        }
    }

    "restart" {
        Write-Status "Reiniciando PACKFY CUBA con optimizaciones móviles..."
        docker-compose down
        docker-compose up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Contenedores reiniciados correctamente"
            Write-Status "Sistema móvil optimizado listo en: https://localhost:5173"
        }
        else {
            Write-Error "Error al reiniciar contenedores"
        }
    }

    "rebuild" {
        Write-Status "Reconstruyendo contenedores con últimas optimizaciones móviles..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Contenedores reconstruidos y reiniciados"
            Write-Status "Nuevas optimizaciones móviles aplicadas"
            Write-Status "Frontend: https://localhost:5173"
            Write-Status "Backend: https://localhost:8000"
        }
        else {
            Write-Error "Error al reconstruir contenedores"
        }
    }

    "logs" {
        Write-Status "Mostrando logs de servicios móviles..."
        docker-compose logs -f --tail=50
    }

    "status" {
        Write-Status "Estado de contenedores PACKFY CUBA móvil:"
        docker-compose ps
        Write-Host ""
        Write-Status "Uso de recursos:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
    }

    "mobile-test" {
        Write-Status "Ejecutando pruebas específicas móviles..."
        Write-Status "Verificando PWA manifest..."

        try {
            $manifest = Invoke-RestMethod -Uri "https://localhost:5173/manifest.json" -SkipCertificateCheck
            Write-Success "Manifest PWA: ✅ Cargado correctamente"
            Write-Host "  - Nombre: $($manifest.name)"
            Write-Host "  - Versión: $($manifest.version)"
            Write-Host "  - Display: $($manifest.display)"
        }
        catch {
            Write-Error "Manifest PWA: ❌ Error al cargar"
        }

        Write-Status "Verificando Service Worker..."
        try {
            $sw = Invoke-WebRequest -Uri "https://localhost:5173/sw.js" -SkipCertificateCheck
            if ($sw.StatusCode -eq 200) {
                Write-Success "Service Worker: ✅ Disponible"
            }
        }
        catch {
            Write-Error "Service Worker: ❌ No disponible"
        }

        Write-Status "Verificando API Backend..."
        try {
            $api = Invoke-WebRequest -Uri "https://localhost:8000/api/health/" -SkipCertificateCheck
            if ($api.StatusCode -eq 200) {
                Write-Success "API Backend: ✅ Respondiendo"
            }
        }
        catch {
            Write-Error "API Backend: ❌ No responde"
        }

        Write-Status "Verificando optimizaciones móviles..."
        try {
            $css = Invoke-WebRequest -Uri "https://localhost:5173" -SkipCertificateCheck
            if ($css.Content -match "mobile-bottom-nav") {
                Write-Success "Navegación móvil: ✅ Implementada"
            }
            else {
                Write-Warning "Navegación móvil: ⚠️ No detectada en HTML"
            }

            if ($css.Content -match "viewport.*width=device-width") {
                Write-Success "Viewport móvil: ✅ Configurado"
            }
            else {
                Write-Warning "Viewport móvil: ⚠️ No optimizado"
            }
        }
        catch {
            Write-Error "No se pudo verificar optimizaciones móviles"
        }
    }
}

Write-Host ""
Write-Status "Comandos disponibles:"
Write-Host "  ${Green}.\mobile-manage.ps1 start${Reset}     - Iniciar contenedores"
Write-Host "  ${Green}.\mobile-manage.ps1 stop${Reset}      - Detener contenedores"
Write-Host "  ${Green}.\mobile-manage.ps1 restart${Reset}   - Reiniciar contenedores"
Write-Host "  ${Green}.\mobile-manage.ps1 rebuild${Reset}   - Reconstruir contenedores"
Write-Host "  ${Green}.\mobile-manage.ps1 logs${Reset}      - Ver logs en tiempo real"
Write-Host "  ${Green}.\mobile-manage.ps1 status${Reset}    - Estado de servicios"
Write-Host "  ${Green}.\mobile-manage.ps1 mobile-test${Reset} - Pruebas específicas móviles"
