# 🇨🇺 PACKFY CUBA - Inicializador de Monitoring v4.0

param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "setup")]
    [string]$Action = "start",

    [Parameter(Mandatory = $false)]
    [ValidateSet("all", "prometheus", "grafana", "elk", "exporters", "alerting")]
    [string]$Service = "all",

    [Parameter(Mandatory = $false)]
    [switch]$Build,

    [Parameter(Mandatory = $false)]
    [switch]$Verbose,

    [Parameter(Mandatory = $false)]
    [switch]$DetachedMode = $true
)

# Configuración de colores y estilos
$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "PACKFY CUBA - Monitoring Manager v4.0"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    switch ($Color) {
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Blue" { Write-Host $Message -ForegroundColor Blue }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        "Magenta" { Write-Host $Message -ForegroundColor Magenta }
        default { Write-Host $Message }
    }
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-ColorOutput "============================================" "Cyan"
    Write-ColorOutput "  $Title" "Cyan"
    Write-ColorOutput "============================================" "Cyan"
    Write-Host ""
}

function Test-Prerequisites {
    Write-Header "🔍 VERIFICANDO PRERREQUISITOS"

    $missingTools = @()

    # Verificar Docker
    try {
        $dockerVersion = docker --version 2>&1
        Write-ColorOutput "✅ Docker: $dockerVersion" "Green"
    }
    catch {
        $missingTools += "Docker"
        Write-ColorOutput "❌ Docker no encontrado" "Red"
    }

    # Verificar Docker Compose
    try {
        $composeVersion = docker-compose --version 2>&1
        Write-ColorOutput "✅ Docker Compose: $composeVersion" "Green"
    }
    catch {
        $missingTools += "Docker Compose"
        Write-ColorOutput "❌ Docker Compose no encontrado" "Red"
    }

    if ($missingTools.Count -gt 0) {
        Write-ColorOutput "❌ Faltan herramientas: $($missingTools -join ', ')" "Red"
        Write-ColorOutput "Instale las herramientas faltantes antes de continuar." "Red"
        exit 1
    }

    Write-ColorOutput "✅ Todos los prerrequisitos están disponibles" "Green"
}

function Initialize-Directories {
    Write-Header "📁 INICIALIZANDO DIRECTORIOS"

    $directories = @(
        "data/prometheus",
        "data/grafana",
        "data/elasticsearch",
        "data/alertmanager",
        "data/uptime-kuma",
        "data/portainer",
        "monitoring/prometheus",
        "monitoring/grafana/provisioning/datasources",
        "monitoring/grafana/provisioning/dashboards",
        "monitoring/alertmanager",
        "monitoring/elk/logstash/config",
        "monitoring/elk/logstash/pipeline",
        "monitoring/blackbox"
    )

    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-ColorOutput "📁 Creado: $dir" "Blue"
        }
        else {
            Write-ColorOutput "✅ Existe: $dir" "Green"
        }
    }

    Write-ColorOutput "✅ Directorios inicializados" "Green"
}

function Set-Permissions {
    Write-Header "🔐 CONFIGURANDO PERMISOS"

    # Configurar permisos para volúmenes de datos
    $dataDirectories = @(
        "data/prometheus",
        "data/grafana",
        "data/elasticsearch",
        "data/alertmanager"
    )

    foreach ($dir in $dataDirectories) {
        if (Test-Path $dir) {
            try {
                # En Windows, asegurar que el directorio es escribible
                $acl = Get-Acl $dir
                $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone", "FullControl", "Allow")
                $acl.SetAccessRule($accessRule)
                Set-Acl $dir $acl
                Write-ColorOutput "🔐 Permisos configurados para: $dir" "Green"
            }
            catch {
                Write-ColorOutput "⚠️  No se pudieron configurar permisos para: $dir" "Yellow"
            }
        }
    }
}

function Create-ConfigFiles {
    Write-Header "📄 CREANDO ARCHIVOS DE CONFIGURACIÓN"

    # Crear archivo de configuración de Grafana datasources
    $grafanaDatasourcesConfig = @"
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true

  - name: Elasticsearch
    type: elasticsearch
    access: proxy
    url: http://elasticsearch:9200
    database: "[packfy-logs-]YYYY.MM.DD"
    interval: Daily
    timeField: "@timestamp"
    editable: true
"@

    $datasourcesPath = "monitoring/grafana/provisioning/datasources/datasources.yml"
    if (!(Test-Path $datasourcesPath)) {
        $grafanaDatasourcesConfig | Out-File -FilePath $datasourcesPath -Encoding UTF8
        Write-ColorOutput "📄 Creado: $datasourcesPath" "Blue"
    }

    # Crear archivo de configuración de dashboards
    $grafanaDashboardsConfig = @"
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    editable: true
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
"@

    $dashboardsPath = "monitoring/grafana/provisioning/dashboards/dashboards.yml"
    if (!(Test-Path $dashboardsPath)) {
        $grafanaDashboardsConfig | Out-File -FilePath $dashboardsPath -Encoding UTF8
        Write-ColorOutput "📄 Creado: $dashboardsPath" "Blue"
    }

    # Crear configuración de Blackbox Exporter
    $blackboxConfig = @"
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      valid_http_versions: ["HTTP/1.1", "HTTP/2.0"]
      valid_status_codes: []
      method: GET
      follow_redirects: true
      preferred_ip_protocol: "ip4"

  http_post_2xx:
    prober: http
    timeout: 5s
    http:
      method: POST
      headers:
        Content-Type: application/json
      body: '{}'

  tcp_connect:
    prober: tcp
    timeout: 5s

  pop3s_banner:
    prober: tcp
    tcp:
      query_response:
        - expect: "^+OK"
      tls: true
      tls_config:
        insecure_skip_verify: false

  ssh_banner:
    prober: tcp
    timeout: 10s
    tcp:
      query_response:
        - expect: "^SSH-2.0-"

  irc_banner:
    prober: tcp
    timeout: 5s
    tcp:
      query_response:
        - send: "NICK prober"
        - send: "USER prober prober prober :prober"
        - expect: "PING :([^ ]+)"
          send: "PONG :$1"
        - expect: "^:[^ ]+ 001"
"@

    $blackboxPath = "monitoring/blackbox/blackbox.yml"
    if (!(Test-Path $blackboxPath)) {
        $blackboxConfig | Out-File -FilePath $blackboxPath -Encoding UTF8
        Write-ColorOutput "📄 Creado: $blackboxPath" "Blue"
    }

    Write-ColorOutput "✅ Archivos de configuración creados" "Green"
}

function Get-ServiceGroups {
    $serviceGroups = @{
        "prometheus" = @("prometheus")
        "grafana"    = @("grafana")
        "elk"        = @("elasticsearch", "kibana", "logstash")
        "exporters"  = @("node_exporter", "postgres_exporter", "redis_exporter", "nginx_exporter", "blackbox_exporter", "cadvisor")
        "alerting"   = @("alertmanager")
        "all"        = @("prometheus", "grafana", "elasticsearch", "kibana", "logstash", "alertmanager", "node_exporter", "postgres_exporter", "redis_exporter", "nginx_exporter", "blackbox_exporter", "cadvisor", "uptime-kuma", "jaeger", "portainer")
    }

    return $serviceGroups
}

function Start-MonitoringServices {
    Write-Header "🚀 INICIANDO SERVICIOS DE MONITORING"

    $serviceGroups = Get-ServiceGroups
    $services = $serviceGroups[$Service]

    if (!$services) {
        Write-ColorOutput "❌ Grupo de servicios '$Service' no válido" "Red"
        return
    }

    $dockerComposeArgs = @("-f", "docker-compose.monitoring.yml", "up")

    if ($DetachedMode) {
        $dockerComposeArgs += "-d"
    }

    if ($Build) {
        $dockerComposeArgs += "--build"
    }

    if ($Service -ne "all") {
        $dockerComposeArgs += $services
    }

    Write-ColorOutput "🚀 Iniciando servicios: $($services -join ', ')" "Blue"

    if ($Verbose) {
        Write-ColorOutput "Comando: docker-compose $($dockerComposeArgs -join ' ')" "Cyan"
    }

    try {
        & docker-compose @dockerComposeArgs

        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Servicios iniciados exitosamente" "Green"

            Start-Sleep -Seconds 5
            Show-ServiceUrls
        }
        else {
            Write-ColorOutput "❌ Error al iniciar servicios" "Red"
        }
    }
    catch {
        Write-ColorOutput "❌ Error ejecutando docker-compose: $($_.Exception.Message)" "Red"
    }
}

function Stop-MonitoringServices {
    Write-Header "🛑 DETENIENDO SERVICIOS DE MONITORING"

    $serviceGroups = Get-ServiceGroups
    $services = $serviceGroups[$Service]

    if (!$services) {
        Write-ColorOutput "❌ Grupo de servicios '$Service' no válido" "Red"
        return
    }

    $dockerComposeArgs = @("-f", "docker-compose.monitoring.yml", "down")

    if ($Service -ne "all") {
        # Para parar servicios específicos, usar stop en lugar de down
        $dockerComposeArgs = @("-f", "docker-compose.monitoring.yml", "stop") + $services
    }

    Write-ColorOutput "🛑 Deteniendo servicios: $($services -join ', ')" "Blue"

    try {
        & docker-compose @dockerComposeArgs

        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Servicios detenidos exitosamente" "Green"
        }
        else {
            Write-ColorOutput "❌ Error al detener servicios" "Red"
        }
    }
    catch {
        Write-ColorOutput "❌ Error ejecutando docker-compose: $($_.Exception.Message)" "Red"
    }
}

function Restart-MonitoringServices {
    Write-Header "🔄 REINICIANDO SERVICIOS DE MONITORING"

    Stop-MonitoringServices
    Start-Sleep -Seconds 3
    Start-MonitoringServices
}

function Show-ServiceStatus {
    Write-Header "📊 ESTADO DE SERVICIOS DE MONITORING"

    try {
        $status = docker-compose -f docker-compose.monitoring.yml ps
        Write-Host $status

        Write-Host ""
        Write-ColorOutput "💡 Uso de recursos:" "Blue"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" $(docker-compose -f docker-compose.monitoring.yml ps -q)

    }
    catch {
        Write-ColorOutput "❌ Error obteniendo estado: $($_.Exception.Message)" "Red"
    }
}

function Show-ServiceLogs {
    Write-Header "📋 LOGS DE SERVICIOS DE MONITORING"

    $serviceGroups = Get-ServiceGroups
    $services = $serviceGroups[$Service]

    if (!$services) {
        Write-ColorOutput "❌ Grupo de servicios '$Service' no válido" "Red"
        return
    }

    $dockerComposeArgs = @("-f", "docker-compose.monitoring.yml", "logs", "-f", "--tail=100")

    if ($Service -ne "all") {
        $dockerComposeArgs += $services
    }

    Write-ColorOutput "📋 Mostrando logs para: $($services -join ', ')" "Blue"
    Write-ColorOutput "Presione Ctrl+C para salir" "Yellow"

    try {
        & docker-compose @dockerComposeArgs
    }
    catch {
        Write-ColorOutput "❌ Error mostrando logs: $($_.Exception.Message)" "Red"
    }
}

function Show-ServiceUrls {
    Write-Header "🌐 URLS DE SERVICIOS DE MONITORING"

    $services = @{
        "Prometheus"    = "http://localhost:9090"
        "Grafana"       = "http://localhost:3001 (admin/packfy2024!)"
        "Kibana"        = "http://localhost:5601"
        "Elasticsearch" = "http://localhost:9200"
        "Alertmanager"  = "http://localhost:9093"
        "Uptime Kuma"   = "http://localhost:3002"
        "Jaeger"        = "http://localhost:16686"
        "Portainer"     = "http://localhost:9000"
    }

    foreach ($service in $services.GetEnumerator()) {
        Write-ColorOutput "🔗 $($service.Key): $($service.Value)" "Cyan"
    }

    Write-Host ""
    Write-ColorOutput "💡 Exporters disponibles:" "Blue"
    Write-ColorOutput "  - Node Exporter: http://localhost:9100" "Cyan"
    Write-ColorOutput "  - Postgres Exporter: http://localhost:9187" "Cyan"
    Write-ColorOutput "  - Redis Exporter: http://localhost:9121" "Cyan"
    Write-ColorOutput "  - Nginx Exporter: http://localhost:9113" "Cyan"
    Write-ColorOutput "  - Blackbox Exporter: http://localhost:9115" "Cyan"
    Write-ColorOutput "  - cAdvisor: http://localhost:8080" "Cyan"
}

function Setup-Monitoring {
    Write-Header "⚙️ CONFIGURACIÓN INICIAL DE MONITORING"

    Test-Prerequisites
    Initialize-Directories
    Set-Permissions
    Create-ConfigFiles

    Write-ColorOutput "✅ Setup completado. Ahora puede ejecutar: .\start-monitoring.ps1 -Action start" "Green"
}

# FUNCIÓN PRINCIPAL
function Main {
    Write-Header "🇨🇺 PACKFY CUBA - MONITORING MANAGER v4.0"

    Write-ColorOutput "Configuración:" "Blue"
    Write-ColorOutput "  - Acción: $Action" "Cyan"
    Write-ColorOutput "  - Servicio: $Service" "Cyan"
    Write-ColorOutput "  - Modo detached: $DetachedMode" "Cyan"
    if ($Build) { Write-ColorOutput "  - Rebuild: Sí" "Cyan" }

    switch ($Action) {
        "setup" {
            Setup-Monitoring
        }
        "start" {
            Start-MonitoringServices
        }
        "stop" {
            Stop-MonitoringServices
        }
        "restart" {
            Restart-MonitoringServices
        }
        "status" {
            Show-ServiceStatus
        }
        "logs" {
            Show-ServiceLogs
        }
        default {
            Write-ColorOutput "❌ Acción '$Action' no válida" "Red"
            Write-ColorOutput "Acciones válidas: setup, start, stop, restart, status, logs" "Yellow"
        }
    }
}

# Ejecutar función principal
Main
