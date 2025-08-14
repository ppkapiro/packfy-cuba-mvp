# 🇨🇺 PACKFY CUBA - Script de Despliegue Global v4.0

param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("development", "staging", "production")]
    [string]$Environment = "development",

    [Parameter(Mandatory = $false)]
    [ValidateSet("cuba", "mexico", "colombia", "usa", "spain", "all")]
    [string]$Region = "cuba",

    [Parameter(Mandatory = $false)]
    [switch]$SkipTests,

    [Parameter(Mandatory = $false)]
    [switch]$SkipMigrations,

    [Parameter(Mandatory = $false)]
    [switch]$Rollback,

    [Parameter(Mandatory = $false)]
    [string]$Version = "latest"
)

# Configuración
$ErrorActionPreference = "Stop"
$deploymentConfig = @{
    "development" = @{
        "compose_file"   = "docker-compose.yml"
        "env_file"       = ".env.development"
        "replica_count"  = 1
        "health_timeout" = 60
    }
    "staging"     = @{
        "compose_file"   = "docker-compose.staging.yml"
        "env_file"       = ".env.staging"
        "replica_count"  = 2
        "health_timeout" = 120
    }
    "production"  = @{
        "compose_file"   = "docker-compose.scalable.yml"
        "env_file"       = ".env.production"
        "replica_count"  = 3
        "health_timeout" = 180
    }
}

$regionEndpoints = @{
    "cuba"     = "packfy-cuba.com"
    "mexico"   = "packfy-mx.com"
    "colombia" = "packfy-co.com"
    "usa"      = "packfy-us.com"
    "spain"    = "packfy-es.com"
}

function Write-DeploymentLog {
    param([string]$Message, [string]$Level = "INFO")

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "Green" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        default { "White" }
    }

    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color

    # Log a archivo
    "$timestamp [$Level] $Message" | Out-File -FilePath "deployment.log" -Append
}

function Test-Prerequisites {
    Write-DeploymentLog "🔍 Verificando prerrequisitos..."

    # Verificar Docker
    try {
        $dockerVersion = docker --version
        Write-DeploymentLog "✅ Docker encontrado: $dockerVersion"
    }
    catch {
        Write-DeploymentLog "❌ Docker no está instalado o no está en PATH" "ERROR"
        exit 1
    }

    # Verificar Docker Compose
    try {
        $composeVersion = docker-compose --version
        Write-DeploymentLog "✅ Docker Compose encontrado: $composeVersion"
    }
    catch {
        Write-DeploymentLog "❌ Docker Compose no está instalado" "ERROR"
        exit 1
    }

    # Verificar archivos de configuración
    $config = $deploymentConfig[$Environment]
    if (-not (Test-Path $config.compose_file)) {
        Write-DeploymentLog "❌ Archivo de compose no encontrado: $($config.compose_file)" "ERROR"
        exit 1
    }

    if (-not (Test-Path $config.env_file)) {
        Write-DeploymentLog "❌ Archivo de entorno no encontrado: $($config.env_file)" "ERROR"
        exit 1
    }

    Write-DeploymentLog "✅ Prerrequisitos verificados correctamente"
}

function Run-Tests {
    if ($SkipTests) {
        Write-DeploymentLog "⏭️ Saltando pruebas por solicitud del usuario"
        return
    }

    Write-DeploymentLog "🧪 Ejecutando pruebas..."

    # Pruebas del backend
    Write-DeploymentLog "📚 Ejecutando pruebas del backend..."
    docker-compose -f docker-compose.test.yml run --rm backend-test pytest --maxfail=1 --tb=short

    if ($LASTEXITCODE -ne 0) {
        Write-DeploymentLog "❌ Pruebas del backend fallaron" "ERROR"
        exit 1
    }

    # Pruebas del frontend
    Write-DeploymentLog "🎨 Ejecutando pruebas del frontend..."
    docker-compose -f docker-compose.test.yml run --rm frontend-test npm test -- --watchAll=false

    if ($LASTEXITCODE -ne 0) {
        Write-DeploymentLog "❌ Pruebas del frontend fallaron" "ERROR"
        exit 1
    }

    Write-DeploymentLog "✅ Todas las pruebas pasaron exitosamente"
}

function Build-Images {
    Write-DeploymentLog "🔨 Construyendo imágenes Docker..."

    $config = $deploymentConfig[$Environment]

    # Construir con etiquetas de versión
    $imageTag = if ($Version -eq "latest") { "latest" } else { $Version }

    Write-DeploymentLog "📦 Construyendo imagen del backend..."
    docker build -t "packfy/backend:$imageTag" -f backend/Dockerfile.prod backend/

    if ($LASTEXITCODE -ne 0) {
        Write-DeploymentLog "❌ Error construyendo imagen del backend" "ERROR"
        exit 1
    }

    Write-DeploymentLog "🎨 Construyendo imagen del frontend..."
    docker build -t "packfy/frontend:$imageTag" -f frontend/Dockerfile.prod frontend/

    if ($LASTEXITCODE -ne 0) {
        Write-DeploymentLog "❌ Error construyendo imagen del frontend" "ERROR"
        exit 1
    }

    Write-DeploymentLog "✅ Imágenes construidas exitosamente"
}

function Deploy-Database-Migrations {
    if ($SkipMigrations) {
        Write-DeploymentLog "⏭️ Saltando migraciones por solicitud del usuario"
        return
    }

    Write-DeploymentLog "🗄️ Ejecutando migraciones de base de datos..."

    $config = $deploymentConfig[$Environment]

    # Crear contenedor temporal para migraciones
    docker-compose -f $config.compose_file --env-file $config.env_file run --rm backend python manage.py migrate

    if ($LASTEXITCODE -ne 0) {
        Write-DeploymentLog "❌ Error ejecutando migraciones" "ERROR"
        exit 1
    }

    # Recopilar archivos estáticos
    docker-compose -f $config.compose_file --env-file $config.env_file run --rm backend python manage.py collectstatic --noinput

    if ($LASTEXITCODE -ne 0) {
        Write-DeploymentLog "❌ Error recopilando archivos estáticos" "ERROR"
        exit 1
    }

    Write-DeploymentLog "✅ Migraciones ejecutadas exitosamente"
}

function Deploy-Services {
    Write-DeploymentLog "🚀 Desplegando servicios..."

    $config = $deploymentConfig[$Environment]

    # Crear backup del estado actual si es producción
    if ($Environment -eq "production") {
        Backup-Current-State
    }

    # Detener servicios actuales gradualmente
    Write-DeploymentLog "🔄 Realizando despliegue rolling..."

    # Escalar réplicas para zero-downtime deployment
    if ($Environment -eq "production") {
        # Escalar temporalmente
        docker-compose -f $config.compose_file --env-file $config.env_file up -d --scale backend=$($config.replica_count * 2)
        Start-Sleep -Seconds 30

        # Verificar salud de nuevas instancias
        Test-Service-Health

        # Remover instancias antigas
        docker-compose -f $config.compose_file --env-file $config.env_file up -d --scale backend=$config.replica_count
    }
    else {
        # Despliegue simple para desarrollo/staging
        docker-compose -f $config.compose_file --env-file $config.env_file up -d
    }

    if ($LASTEXITCODE -ne 0) {
        Write-DeploymentLog "❌ Error desplegando servicios" "ERROR"
        if ($Environment -eq "production") {
            Rollback-Deployment
        }
        exit 1
    }

    Write-DeploymentLog "✅ Servicios desplegados exitosamente"
}

function Test-Service-Health {
    Write-DeploymentLog "🏥 Verificando salud de servicios..."

    $config = $deploymentConfig[$Environment]
    $endpoint = if ($Region -ne "all") { $regionEndpoints[$Region] } else { "localhost" }
    $timeout = $config.health_timeout

    # Verificar backend
    $backendHealthy = $false
    $attempts = 0
    $maxAttempts = $timeout / 5

    while (-not $backendHealthy -and $attempts -lt $maxAttempts) {
        try {
            $response = Invoke-RestMethod -Uri "http://$endpoint/api/health/" -TimeoutSec 5
            if ($response.status -eq "healthy") {
                $backendHealthy = $true
                Write-DeploymentLog "✅ Backend saludable"
            }
        }
        catch {
            $attempts++
            Write-DeploymentLog "🔄 Esperando que el backend esté listo... (intento $attempts/$maxAttempts)"
            Start-Sleep -Seconds 5
        }
    }

    if (-not $backendHealthy) {
        Write-DeploymentLog "❌ Backend no respondió en el tiempo esperado" "ERROR"
        return $false
    }

    # Verificar frontend
    try {
        $response = Invoke-WebRequest -Uri "http://$endpoint/" -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-DeploymentLog "✅ Frontend saludable"
        }
    }
    catch {
        Write-DeploymentLog "❌ Frontend no está respondiendo" "ERROR"
        return $false
    }

    # Verificar base de datos
    try {
        $dbCheck = docker-compose -f $config.compose_file --env-file $config.env_file exec -T backend python manage.py check --database default
        Write-DeploymentLog "✅ Base de datos saludable"
    }
    catch {
        Write-DeploymentLog "❌ Problemas con la base de datos" "ERROR"
        return $false
    }

    Write-DeploymentLog "✅ Todos los servicios están saludables"
    return $true
}

function Backup-Current-State {
    Write-DeploymentLog "💾 Creando backup del estado actual..."

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backupDir = "backups/$timestamp"

    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

    # Backup de base de datos
    docker-compose exec -T postgres pg_dump -U packfy packfy_cuba > "$backupDir/database.sql"

    # Backup de configuración
    Copy-Item -Path "docker-compose.scalable.yml" -Destination "$backupDir/"
    Copy-Item -Path ".env.production" -Destination "$backupDir/"

    # Backup de volúmenes críticos
    docker run --rm -v packfy_backend-media:/data -v ${PWD}/${backupDir}:/backup busybox tar czf /backup/media.tar.gz -C /data .

    Write-DeploymentLog "✅ Backup creado en $backupDir"

    # Guardar referencia para rollback
    $backupDir | Out-File -FilePath "latest-backup.txt"
}

function Rollback-Deployment {
    Write-DeploymentLog "🔄 Iniciando rollback..." "WARN"

    if (-not (Test-Path "latest-backup.txt")) {
        Write-DeploymentLog "❌ No se encontró backup para rollback" "ERROR"
        return
    }

    $backupDir = Get-Content "latest-backup.txt"

    if (-not (Test-Path $backupDir)) {
        Write-DeploymentLog "❌ Directorio de backup no encontrado: $backupDir" "ERROR"
        return
    }

    Write-DeploymentLog "📥 Restaurando desde backup: $backupDir"

    # Detener servicios actuales
    docker-compose -f $deploymentConfig[$Environment].compose_file down

    # Restaurar configuración
    Copy-Item -Path "$backupDir/docker-compose.scalable.yml" -Destination "." -Force
    Copy-Item -Path "$backupDir/.env.production" -Destination "." -Force

    # Restaurar base de datos
    docker-compose up -d postgres
    Start-Sleep -Seconds 10
    Get-Content "$backupDir/database.sql" | docker-compose exec -T postgres psql -U packfy packfy_cuba

    # Restaurar medios
    docker run --rm -v packfy_backend-media:/data -v ${PWD}/${backupDir}:/backup busybox tar xzf /backup/media.tar.gz -C /data

    # Levantar servicios
    docker-compose -f $deploymentConfig[$Environment].compose_file up -d

    Write-DeploymentLog "✅ Rollback completado"
}

function Deploy-To-Multiple-Regions {
    if ($Region -eq "all") {
        Write-DeploymentLog "🌍 Desplegando a todas las regiones..."

        $regions = @("cuba", "mexico", "colombia", "usa", "spain")
        $failedRegions = @()

        foreach ($targetRegion in $regions) {
            Write-DeploymentLog "📍 Desplegando a región: $targetRegion"

            try {
                # Ejecutar despliegue recursivo para cada región
                & $PSCommandPath -Environment $Environment -Region $targetRegion -SkipTests

                if ($LASTEXITCODE -ne 0) {
                    $failedRegions += $targetRegion
                    Write-DeploymentLog "❌ Fallo en región: $targetRegion" "ERROR"
                }
                else {
                    Write-DeploymentLog "✅ Éxito en región: $targetRegion"
                }
            }
            catch {
                $failedRegions += $targetRegion
                Write-DeploymentLog "❌ Error en región $targetRegion : $($_.Exception.Message)" "ERROR"
            }
        }

        if ($failedRegions.Count -gt 0) {
            Write-DeploymentLog "❌ Regiones que fallaron: $($failedRegions -join ', ')" "ERROR"
            exit 1
        }
        else {
            Write-DeploymentLog "✅ Despliegue exitoso en todas las regiones"
        }

        return
    }
}

function Send-Deployment-Notification {
    param([bool]$Success, [string]$Details = "")

    $status = if ($Success) { "✅ ÉXITO" } else { "❌ FALLO" }
    $color = if ($Success) { "good" } else { "danger" }

    $message = @"
🚀 **Despliegue PACKFY CUBA**

**Estado:** $status
**Entorno:** $Environment
**Región:** $Region
**Versión:** $Version
**Hora:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

$Details
"@

    Write-DeploymentLog $message

    # En producción, enviar a Slack/Teams/etc.
    # Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload
}

function Show-Deployment-Summary {
    $config = $deploymentConfig[$Environment]
    $endpoint = if ($Region -ne "all") { $regionEndpoints[$Region] } else { "localhost" }

    Write-Host "`n" -NoNewline
    Write-Host "🎉 " -ForegroundColor Green -NoNewline
    Write-Host "DESPLIEGUE COMPLETADO EXITOSAMENTE" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green

    Write-Host "📊 RESUMEN DEL DESPLIEGUE:" -ForegroundColor Cyan
    Write-Host "  • Entorno: " -NoNewline; Write-Host $Environment -ForegroundColor Yellow
    Write-Host "  • Región: " -NoNewline; Write-Host $Region -ForegroundColor Yellow
    Write-Host "  • Versión: " -NoNewline; Write-Host $Version -ForegroundColor Yellow
    Write-Host "  • Réplicas: " -NoNewline; Write-Host $config.replica_count -ForegroundColor Yellow

    Write-Host "`n🔗 ENDPOINTS DISPONIBLES:" -ForegroundColor Cyan
    Write-Host "  • Frontend: " -NoNewline; Write-Host "http://$endpoint/" -ForegroundColor Blue
    Write-Host "  • API: " -NoNewline; Write-Host "http://$endpoint/api/" -ForegroundColor Blue
    Write-Host "  • Admin: " -NoNewline; Write-Host "http://$endpoint/admin/" -ForegroundColor Blue
    Write-Host "  • Docs: " -NoNewline; Write-Host "http://$endpoint/api/swagger/" -ForegroundColor Blue

    if ($Environment -eq "production") {
        Write-Host "  • Monitoreo: " -NoNewline; Write-Host "http://$endpoint:3001/" -ForegroundColor Blue
        Write-Host "  • Métricas: " -NoNewline; Write-Host "http://$endpoint:9090/" -ForegroundColor Blue
    }

    Write-Host "`n⚡ COMANDOS ÚTILES:" -ForegroundColor Cyan
    Write-Host "  • Ver logs: " -NoNewline; Write-Host "docker-compose -f $($config.compose_file) logs -f" -ForegroundColor Magenta
    Write-Host "  • Estado: " -NoNewline; Write-Host "docker-compose -f $($config.compose_file) ps" -ForegroundColor Magenta
    Write-Host "  • Escalar: " -NoNewline; Write-Host "docker-compose -f $($config.compose_file) up -d --scale backend=5" -ForegroundColor Magenta

    Write-Host "`n🚀 ¡PACKFY CUBA está listo para conquistar el mundo! 🇨🇺" -ForegroundColor Green
}

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

try {
    Write-DeploymentLog "🚀 Iniciando despliegue de PACKFY CUBA"
    Write-DeploymentLog "📋 Configuración: Entorno=$Environment, Región=$Region, Versión=$Version"

    # Manejar rollback
    if ($Rollback) {
        Rollback-Deployment
        exit 0
    }

    # Despliegue multi-región
    if ($Region -eq "all") {
        Deploy-To-Multiple-Regions
        exit 0
    }

    # Flujo de despliegue normal
    Test-Prerequisites
    Run-Tests
    Build-Images
    Deploy-Database-Migrations
    Deploy-Services

    # Verificar salud del despliegue
    if (Test-Service-Health) {
        Send-Deployment-Notification -Success $true -Details "Despliegue completado sin problemas"
        Show-Deployment-Summary
    }
    else {
        throw "Verificaciones de salud fallaron"
    }
}
catch {
    $errorMsg = "Error durante el despliegue: $($_.Exception.Message)"
    Write-DeploymentLog $errorMsg "ERROR"
    Send-Deployment-Notification -Success $false -Details $errorMsg

    if ($Environment -eq "production") {
        Write-DeploymentLog "🔄 Iniciando rollback automático..." "WARN"
        Rollback-Deployment
    }

    exit 1
}

Write-DeploymentLog "🎉 Despliegue completado exitosamente en $(Get-Date -Format 'HH:mm:ss')"
