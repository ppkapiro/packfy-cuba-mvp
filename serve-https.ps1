# Solucion HTTPS simple con serveit
Write-Host "SOLUCION HTTPS ALTERNATIVA" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

# 1. Verificar si Node.js esta instalado
Write-Host "1. Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js no encontrado, instalando..." -ForegroundColor Red
    # Descargar e instalar Node.js portable
    $nodeUrl = "https://nodejs.org/dist/v20.10.0/node-v20.10.0-win-x64.zip"
    Write-Host "Descargando Node.js..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $nodeUrl -OutFile "node.zip"
    Expand-Archive -Path "node.zip" -DestinationPath "." -Force
    Remove-Item "node.zip"
    $env:PATH += ";$(Get-Location)\node-v20.10.0-win-x64"
}

Write-Host "`n2. Instalando serve con HTTPS..." -ForegroundColor Yellow
npm install -g serve

Write-Host "`n3. Creando certificado autofirmado..." -ForegroundColor Yellow
# Crear certificado simple con OpenSSL (si está disponible) o usar serve con --ssl-cert

Write-Host "`n4. Iniciando servidor HTTPS en puerto 3000..." -ForegroundColor Yellow
Write-Host "IMPORTANTE: Mantén esta ventana abierta" -ForegroundColor Red

# Cambiar al directorio frontend/dist o public
$buildDir = "frontend/dist"
if (!(Test-Path $buildDir)) {
    $buildDir = "frontend/public"
}

if (Test-Path $buildDir) {
    cd $buildDir
    Write-Host "Sirviendo desde: $buildDir" -ForegroundColor Cyan
} else {
    Write-Host "Directorio de build no encontrado, usando directorio actual" -ForegroundColor Yellow
}

# Servir con HTTPS (serve crea certificados automaticamente)
serve -s . -l 3000 --ssl

Write-Host "`nServidor HTTPS iniciado en:" -ForegroundColor Green
$ip = (Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null}).IPv4Address.IPAddress | Select-Object -First 1
Write-Host "PC: https://localhost:3000" -ForegroundColor Cyan
Write-Host "Movil: https://$ip:3000" -ForegroundColor Cyan
