# Script para crear build para móvil - SIN HMR
Write-Host "Creando build optimizado para móvil..." -ForegroundColor Green

# Configurar variables para build móvil
$envContent = @"
VITE_API_BASE_URL=http://192.168.12.179:8000
"@

Write-Host "Configurando variables de entorno..." -ForegroundColor Cyan
$envContent | Out-File -FilePath "frontend\.env" -Encoding UTF8

# Crear build de producción
Write-Host "Creando build de producción..." -ForegroundColor Yellow
docker-compose exec frontend npm run build

# Crear archivo serve.json para configurar el servidor estático
$serveConfig = @"
{
  "public": "dist",
  "rewrites": [
    { "source": "/api/*", "destination": "http://192.168.12.179:8000/api/*" },
    { "source": "*", "destination": "/index.html" }
  ]
}
"@

Write-Host "Configurando servidor estático..." -ForegroundColor Cyan
$serveConfig | Out-File -FilePath "frontend\serve.json" -Encoding UTF8

# Instalar serve si no está disponible
Write-Host "Verificando serve..." -ForegroundColor Blue
docker-compose exec frontend npm list serve 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Instalando serve..." -ForegroundColor Yellow
    docker-compose exec frontend npm install -g serve
}

# Servir la aplicación sin HMR
Write-Host "Iniciando servidor estático (SIN HMR)..." -ForegroundColor Green
docker-compose exec -d frontend serve -s dist -l 5174 -p 192.168.12.179:8000/api

Write-Host ""
Write-Host "BUILD MÓVIL COMPLETADO!" -ForegroundColor Green
Write-Host "URLs para acceder desde móvil (SIN HMR):" -ForegroundColor Yellow
Write-Host "   http://192.168.12.179:5174" -ForegroundColor White

Write-Host ""
Write-Host "Credenciales:" -ForegroundColor Yellow
Write-Host "   test@test.com / 123456" -ForegroundColor White

Write-Host ""
Write-Host "Ventajas del build móvil:" -ForegroundColor Cyan
Write-Host "   NO HAY actualizaciones automáticas" -ForegroundColor Green
Write-Host "   Aplicación estática optimizada" -ForegroundColor Green
Write-Host "   Mejor rendimiento en móvil" -ForegroundColor Green

Read-Host "`nPresiona Enter para continuar"
