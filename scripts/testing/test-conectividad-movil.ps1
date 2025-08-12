# 🔧 Verificación y Reinicio Completo de Servidores - Packfy Cuba
# Script para asegurar que ambos servidores estén funcionando correctamente

Write-Host "🚀 VERIFICACIÓN COMPLETA DE SERVIDORES PACKFY CUBA" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# Función para obtener IP local
function Get-LocalIP {
    $adapters = @("Wi-Fi", "Ethernet", "WiFi", "LAN")
    foreach ($adapter in $adapters) {
        try {
            $ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias $adapter -ErrorAction SilentlyContinue).IPAddress
            if ($ip -and $ip -ne "127.0.0.1") {
                return $ip
            }
        } catch {
            continue
        }
    }
    
    # Backup: obtener cualquier IP privada
    $privateIPs = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
        $_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*" 
    }
    if ($privateIPs) {
        return $privateIPs[0].IPAddress
    }
    
    return "192.168.1.100" # IP de ejemplo
}

$localIP = Get-LocalIP
Write-Host "📡 IP Local detectada: $localIP" -ForegroundColor Cyan

# 1. DETENER PROCESOS ANTERIORES
Write-Host "`n🛑 PASO 1: Deteniendo procesos anteriores..." -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Gray

try {
    # Detener Node.js
    $nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
    if ($nodeProcesses) {
        Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
        Write-Host "✅ Procesos Node.js detenidos" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "ℹ️ No había procesos Node.js ejecutándose" -ForegroundColor Gray
    }
    
    # Liberar puertos específicos
    $ports = @(5173, 5174, 5175)
    foreach ($port in $ports) {
        try {
            $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
            if ($connection) {
                $processId = $connection.OwningProcess
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                Write-Host "✅ Puerto $port liberado" -ForegroundColor Green
            }
        } catch {
            # Puerto ya libre
        }
    }
} catch {
    Write-Host "ℹ️ Limpieza de procesos completada" -ForegroundColor Gray
}

# 2. VERIFICAR BACKEND
Write-Host "`n🔍 PASO 2: Verificando Backend Django..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Gray

try {
    $backendResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/swagger/" -UseBasicParsing -TimeoutSec 5
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend funcionando correctamente en puerto 8000" -ForegroundColor Green
        Write-Host "   📊 API Swagger: http://127.0.0.1:8000/api/swagger/" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Backend no responde. Iniciando..." -ForegroundColor Red
    
    # Iniciar backend
    Write-Host "🔄 Iniciando servidor Django..." -ForegroundColor Yellow
    Start-Process PowerShell -ArgumentList "-Command", "cd 'C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend'; python manage.py runserver" -WindowStyle Minimized
    
    Write-Host "⏳ Esperando que el backend se inicie..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Verificar nuevamente
    try {
        $backendCheck = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/swagger/" -UseBasicParsing -TimeoutSec 10
        if ($backendCheck.StatusCode -eq 200) {
            Write-Host "✅ Backend iniciado exitosamente" -ForegroundColor Green
        }
    } catch {
        Write-Host "⚠️ Backend tardando en iniciar. Continúa con frontend..." -ForegroundColor Yellow
    }
}

# 3. NAVEGAR AL DIRECTORIO FRONTEND
Write-Host "`n📁 PASO 3: Configurando Frontend..." -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Gray

Set-Location "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend"
Write-Host "📂 Directorio actual: $(Get-Location)" -ForegroundColor Cyan

# 4. VERIFICAR DEPENDENCIAS
Write-Host "`n📦 PASO 4: Verificando dependencias..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "📥 Instalando dependencias..." -ForegroundColor Yellow
    npm install
}
Write-Host "✅ Dependencias verificadas" -ForegroundColor Green

# 5. INICIAR FRONTEND
Write-Host "`n🚀 PASO 5: Iniciando Frontend Optimizado..." -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Gray

Write-Host "⚙️ Configuración aplicada:" -ForegroundColor Cyan
Write-Host "  • HMR estabilizado para móvil" -ForegroundColor White
Write-Host "  • Polling desactivado" -ForegroundColor White
Write-Host "  • Timeouts extendidos" -ForegroundColor White
Write-Host "  • Sin overlay de errores" -ForegroundColor White

Write-Host "`n🌐 INFORMACIÓN DE CONEXIÓN:" -ForegroundColor Magenta
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "🖥️  Escritorio: http://localhost:5173" -ForegroundColor White
Write-Host "📱 Móvil: http://${localIP}:5173" -ForegroundColor Yellow
Write-Host "🔗 PWA: Chrome → Menú → Instalar aplicación" -ForegroundColor Cyan

Write-Host "`n🧪 CREDENCIALES DE PRUEBA:" -ForegroundColor Magenta
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "👑 Administrador: admin@packfy.cu / admin123" -ForegroundColor White
Write-Host "🏢 Empresa: empresa@test.cu / empresa123" -ForegroundColor White
Write-Host "🇨🇺 Cliente: cliente@test.cu / cliente123" -ForegroundColor White

Write-Host "`n📱 INSTRUCCIONES PARA MÓVIL:" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "1. 📶 Conecta tu móvil al mismo WiFi que tu PC" -ForegroundColor White
Write-Host "2. 🌐 Abre Chrome en el móvil" -ForegroundColor White
Write-Host "3. 🎯 Ve a: http://${localIP}:5173" -ForegroundColor Yellow
Write-Host "4. ⏳ Espera carga completa (puede tardar)" -ForegroundColor White
Write-Host "5. 🔑 Login: admin@packfy.cu / admin123" -ForegroundColor White

Write-Host "`n🔧 SOLUCIÓN PROBLEMAS COMUNES:" -ForegroundColor Red
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "• Si no conecta: Verifica firewall de Windows" -ForegroundColor White
Write-Host "• Si se actualiza mucho: Instala como PWA" -ForegroundColor White
Write-Host "• Si es lento: Usa WiFi estable" -ForegroundColor White
Write-Host "• Si no carga: Limpia caché de Chrome" -ForegroundColor White

Write-Host "`n⚡ Iniciando servidor en 3 segundos..." -ForegroundColor Green
Start-Sleep -Seconds 3

# Ejecutar servidor
npm run dev
