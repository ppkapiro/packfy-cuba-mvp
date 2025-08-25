# Script para configurar HTTPS local para PWA
Write-Host "🔒 CONFIGURANDO HTTPS LOCAL PARA PWA" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# 1. Verificar si tenemos Chocolatey
Write-Host "📦 1. Verificando Chocolatey..." -ForegroundColor Yellow
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Chocolatey no está instalado" -ForegroundColor Red
    Write-Host "🔧 Instalando Chocolatey..." -ForegroundColor Yellow
    
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    Write-Host "✅ Chocolatey instalado" -ForegroundColor Green
} else {
    Write-Host "✅ Chocolatey ya está instalado" -ForegroundColor Green
}

# 2. Instalar mkcert
Write-Host "`n🔑 2. Instalando mkcert..." -ForegroundColor Yellow
try {
    choco install mkcert -y
    Write-Host "✅ mkcert instalado" -ForegroundColor Green
} catch {
    Write-Host "❌ Error instalando mkcert: $_" -ForegroundColor Red
    exit 1
}

# 3. Crear certificados
Write-Host "`n📜 3. Creando certificados locales..." -ForegroundColor Yellow
cd frontend

# Instalar CA root
mkcert -install

# Crear certificados para localhost y la IP local
$ip = (Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -ne "Disconnected"}).IPv4Address.IPAddress
Write-Host "📍 IP detectada: $ip" -ForegroundColor Cyan

mkcert localhost 127.0.0.1 ::1 $ip

Write-Host "✅ Certificados creados" -ForegroundColor Green

# 4. Reiniciar frontend
Write-Host "`n🔄 4. Reiniciando frontend con HTTPS..." -ForegroundColor Yellow
cd ..
docker compose restart frontend

Write-Host "`n🎉 CONFIGURACIÓN COMPLETADA!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "🌐 URLs HTTPS:" -ForegroundColor Yellow
Write-Host "PC: https://localhost:5173" -ForegroundColor Cyan
Write-Host "Móvil: https://$ip:5173" -ForegroundColor Cyan
Write-Host "Test PWA: https://$ip:5173/test-pwa.html" -ForegroundColor Cyan
Write-Host "`n⚠️  IMPORTANTE: Acepta el certificado de seguridad en el navegador" -ForegroundColor Yellow
