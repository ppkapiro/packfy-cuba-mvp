# 🇨🇺 PACKFY CUBA - Configuración SSL Móvil v4.0
# Script para generar certificados SSL compatibles con móviles

Write-Host "🔐 Generando certificados SSL para acceso móvil..." -ForegroundColor Cyan

# Crear directorios si no existen
if (!(Test-Path "backend/certs")) {
    New-Item -ItemType Directory -Path "backend/certs" -Force
    Write-Host "✅ Creado directorio backend/certs" -ForegroundColor Green
}

if (!(Test-Path "frontend/certs")) {
    New-Item -ItemType Directory -Path "frontend/certs" -Force
    Write-Host "✅ Creado directorio frontend/certs" -ForegroundColor Green
}

# Configuración del certificado con SAN para móvil
$certConfig = @"
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
CN = PACKFY CUBA MVP
O = Packfy Cuba
C = CU
ST = Havana
L = Havana

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
DNS.3 = backend
DNS.4 = frontend
IP.1 = 127.0.0.1
IP.2 = 192.168.12.178
IP.3 = 172.20.0.5
IP.4 = 0.0.0.0
"@

# Escribir configuración
$certConfig | Out-File -FilePath "ssl-mobile.conf" -Encoding UTF8

Write-Host "📝 Configuración SSL creada con IPs móviles" -ForegroundColor Yellow

# Generar certificado con OpenSSL (si está disponible)
try {
    # Generar clave privada
    openssl genrsa -out mobile-key.pem 2048

    # Generar certificado
    openssl req -new -x509 -key mobile-key.pem -out mobile-cert.pem -days 365 -config ssl-mobile.conf -extensions v3_req

    Write-Host "✅ Certificados SSL generados exitosamente" -ForegroundColor Green

    # Copiar a los directorios necesarios
    Copy-Item "mobile-cert.pem" "frontend/certs/localhost.crt"
    Copy-Item "mobile-key.pem" "frontend/certs/localhost.key"
    Copy-Item "mobile-cert.pem" "backend/certs/localhost.crt"
    Copy-Item "mobile-key.pem" "backend/certs/localhost.key"

    Write-Host "✅ Certificados copiados a frontend y backend" -ForegroundColor Green

}
catch {
    Write-Host "❌ OpenSSL no disponible. Usando método alternativo..." -ForegroundColor Yellow

    # Método alternativo para Windows sin OpenSSL
    Write-Host "🔧 Configurando certificados existentes..." -ForegroundColor Cyan

    # Usar certificados existentes del frontend
    if (Test-Path "frontend/certs/server.crt") {
        Copy-Item "frontend/certs/server.crt" "backend/certs/localhost.crt"
        Copy-Item "frontend/certs/server.key" "backend/certs/localhost.key"
        Write-Host "✅ Certificados copiados desde frontend" -ForegroundColor Green
    }
}

# Limpiar archivos temporales
if (Test-Path "ssl-mobile.conf") { Remove-Item "ssl-mobile.conf" -Force }
if (Test-Path "mobile-cert.pem") { Remove-Item "mobile-cert.pem" -Force }
if (Test-Path "mobile-key.pem") { Remove-Item "mobile-key.pem" -Force }

Write-Host ""
Write-Host "🎉 Configuración SSL móvil completada" -ForegroundColor Green
