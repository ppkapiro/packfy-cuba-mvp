#!/usr/bin/env pwsh
# 🔧 PACKFY CUBA - DIAGNOSTICO PASO A PASO
# =========================================

Write-Host "🔧 PACKFY CUBA - DIAGNOSTICO PASO A PASO" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

Write-Host "`n📊 1. VERIFICANDO ESTADO ACTUAL" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

# Verificar servicios
$backend = netstat -an | findstr ":8000.*LISTENING"
$frontend = netstat -an | findstr ":5173.*LISTENING"

Write-Host "Backend:" $(if ($backend) { "✅ FUNCIONANDO" } else { "❌ NO FUNCIONA" }) -ForegroundColor $(if ($backend) { "Green" } else { "Red" })
Write-Host "Frontend:" $(if ($frontend) { "✅ FUNCIONANDO" } else { "❌ NO FUNCIONA" }) -ForegroundColor $(if ($frontend) { "Green" } else { "Red" })

# 2. PROBAR URLS DIRECTAMENTE
Write-Host "`n🌐 2. PROBANDO URLS DIRECTAMENTE" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

$urls = @(
    "https://localhost:5173/",
    "https://localhost:5173/login",
    "https://localhost:5173/rastreo",
    "https://localhost:5173/seguimiento",
    "http://localhost:8000/admin/"
)

foreach ($url in $urls) {
    Write-Host "🔗 Probando: $url" -ForegroundColor Cyan
    try {
        if ($url.StartsWith("https://localhost:5173/")) {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -SkipCertificateCheck -TimeoutSec 3
        }
        else {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
        }
        Write-Host "   ✅ Respuesta: $($response.StatusCode)" -ForegroundColor Green
    }
    catch {
        Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 3. REINICIAR SERVICIOS PARA FORZAR RECARGA
Write-Host "`n🔄 3. FORZANDO RECARGA DE SERVICIOS" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

Write-Host "⚠️  Los cambios pueden no estar aplicándose por caché." -ForegroundColor Yellow
Write-Host "Voy a intentar reiniciar los servicios..." -ForegroundColor Cyan

# Matar procesos Node.js (frontend)
Write-Host "`n🔹 Reiniciando Frontend..." -ForegroundColor Cyan
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Matar procesos Python (backend)
Write-Host "🔹 Reiniciando Backend..." -ForegroundColor Cyan
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

Write-Host "✅ Servicios detenidos. Ahora necesitas reiniciarlos manualmente:" -ForegroundColor Green

# 4. INSTRUCCIONES DE REINICIO
Write-Host "`n📋 4. INSTRUCCIONES DE REINICIO" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

Write-Host "🔹 TERMINAL 1 - Backend:" -ForegroundColor Cyan
Write-Host "   cd c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend" -ForegroundColor White
Write-Host "   python manage.py runserver 0.0.0.0:8000" -ForegroundColor Gray

Write-Host "`n🔹 TERMINAL 2 - Frontend:" -ForegroundColor Cyan
Write-Host "   cd c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Gray

Write-Host "`n🔹 TERMINAL 3 - Testing:" -ForegroundColor Cyan
Write-Host "   Después de reiniciar, ejecuta este script de nuevo" -ForegroundColor White

# 5. CREAR DATOS DE PRUEBA SIMPLES
Write-Host "`n📦 5. CREANDO DATOS DE PRUEBA SIMPLES" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

$simpleDataScript = @"
from envios.models import Envio
from django.contrib.auth.models import User

# Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print('✅ Superusuario creado')

# Limpiar envíos existentes
Envio.objects.all().delete()

# Crear envío simple
envio = Envio.objects.create(
    numero_guia='TEST001',
    remitente_nombre='José García',
    destinatario_nombre='María López',
    estado_actual='RECIBIDO',
    peso=2.5,
    descripcion='Paquete de prueba',
    remitente_direccion='La Habana, Cuba',
    remitente_telefono='12345678',
    destinatario_direccion='Santiago, Cuba',
    destinatario_telefono='87654321'
)

print(f'✅ Envío creado: {envio.numero_guia} - {envio.remitente_nombre} → {envio.destinatario_nombre}')
"@

$dataFile = "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\crear_datos_simple.py"
$simpleDataScript | Out-File -FilePath $dataFile -Encoding UTF8

Write-Host "✅ Script de datos creado: crear_datos_simple.py" -ForegroundColor Green
Write-Host "💡 Después de reiniciar backend, ejecuta:" -ForegroundColor Yellow
Write-Host "   cd backend && python manage.py shell < ../crear_datos_simple.py" -ForegroundColor Gray

# 6. ABRIR TERMINAL NUEVAS
Write-Host "`n💻 6. ABRIENDO TERMINALES NUEVAS" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

# Abrir PowerShell para backend
Start-Process "powershell" -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend' ; Write-Host '🔥 BACKEND - Ejecuta: python manage.py runserver 0.0.0.0:8000' -ForegroundColor Red"

# Abrir PowerShell para frontend
Start-Process "powershell" -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\frontend' ; Write-Host '🌐 FRONTEND - Ejecuta: npm run dev' -ForegroundColor Blue"

Write-Host "✅ Terminales abiertas. Ejecuta los comandos mostrados en cada terminal." -ForegroundColor Green

# 7. PRUEBAS A REALIZAR
Write-Host "`n🧪 7. PRUEBAS A REALIZAR DESPUÉS DE REINICIAR" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Yellow

Write-Host "🔹 Paso 1: Reiniciar servicios en las terminales nuevas" -ForegroundColor Cyan
Write-Host "🔹 Paso 2: Crear datos con: python manage.py shell < ../crear_datos_simple.py" -ForegroundColor Cyan
Write-Host "🔹 Paso 3: Abrir navegador en modo incógnito" -ForegroundColor Cyan
Write-Host "🔹 Paso 4: Ir a https://localhost:5173/login" -ForegroundColor Cyan
Write-Host "🔹 Paso 5: Login con admin / admin123" -ForegroundColor Cyan
Write-Host "🔹 Paso 6: Probar /rastreo y /seguimiento" -ForegroundColor Cyan

Write-Host "`n🎯 OBJETIVO:" -ForegroundColor Yellow
Write-Host "============" -ForegroundColor Yellow
Write-Host "✅ /seguimiento debe redirigir a /rastreo" -ForegroundColor Green
Write-Host "✅ /rastreo debe mostrar búsqueda por NOMBRES" -ForegroundColor Green
Write-Host "✅ Búsqueda debe encontrar 'José' y 'María'" -ForegroundColor Green

Write-Host "`n🇨🇺 Packfy Cuba - Reinicio completo en progreso..." -ForegroundColor Green
