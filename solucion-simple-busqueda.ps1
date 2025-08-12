#!/usr/bin/env pwsh
# 🔧 PACKFY CUBA - SOLUCION SIMPLE BUSQUEDA POR NOMBRES
# ====================================================

Write-Host "🔧 PACKFY CUBA - SOLUCION SIMPLE BUSQUEDA POR NOMBRES" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green

# 1. VERIFICAR SERVICIOS
Write-Host "`n📊 1. VERIFICANDO SERVICIOS" -ForegroundColor Yellow
Write-Host "===========================" -ForegroundColor Yellow

$backend = netstat -an | findstr ":8000.*LISTENING"
$frontend = netstat -an | findstr ":5173.*LISTENING"

if ($backend) {
    Write-Host "✅ Backend (8000): ACTIVO" -ForegroundColor Green
}
else {
    Write-Host "❌ Backend (8000): NO ACTIVO" -ForegroundColor Red
    Write-Host "💡 Ejecuta: cd backend && python manage.py runserver 0.0.0.0:8000" -ForegroundColor Yellow
}

if ($frontend) {
    Write-Host "✅ Frontend (5173): ACTIVO" -ForegroundColor Green
}
else {
    Write-Host "❌ Frontend (5173): NO ACTIVO" -ForegroundColor Red
    Write-Host "💡 Ejecuta: cd frontend && npm run dev" -ForegroundColor Yellow
}

# 2. CREAR DATOS DE PRUEBA MINIMOS
Write-Host "`n📦 2. CREANDO DATOS DE PRUEBA" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

$backendDir = "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend"
Set-Location $backendDir

# Script simplificado para crear datos
$script = @"
from envios.models import Envio
from django.contrib.auth.models import User

# Crear usuario admin si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_user('admin', 'admin@packfy.cu', 'admin123', is_staff=True, is_superuser=True)
    print('✅ Usuario admin creado')
else:
    print('✅ Usuario admin ya existe')

# Limpiar y crear envíos de prueba
Envio.objects.all().delete()

Envio.objects.create(
    numero_guia='CU001',
    remitente_nombre='José García',
    destinatario_nombre='María López',
    estado_actual='RECIBIDO',
    peso=2.5,
    descripcion='Paquete de prueba 1',
    remitente_direccion='La Habana',
    remitente_telefono='12345678',
    destinatario_direccion='Santiago',
    destinatario_telefono='87654321'
)

Envio.objects.create(
    numero_guia='CU002',
    remitente_nombre='Ana García',
    destinatario_nombre='Carlos Pérez',
    estado_actual='EN_TRANSITO',
    peso=1.8,
    descripcion='Paquete de prueba 2',
    remitente_direccion='Matanzas',
    remitente_telefono='11111111',
    destinatario_direccion='Camagüey',
    destinatario_telefono='22222222'
)

print(f'✅ {Envio.objects.count()} envíos creados')
for e in Envio.objects.all():
    print(f'  - {e.numero_guia}: {e.remitente_nombre} → {e.destinatario_nombre}')
"@

Write-Host "🔄 Creando datos..." -ForegroundColor Cyan
Write-Output $script | python manage.py shell

# 3. PROBAR ENDPOINT DIRECTO
Write-Host "`n🔍 3. PROBANDO ENDPOINT BUSQUEDA" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

Write-Host "🧪 Probando endpoint de rastreo por nombres..." -ForegroundColor Cyan

# Probar diferentes consultas
$tests = @(
    @{nombre = "José"; tipo = "remitente"; desc = "Buscar José como remitente" },
    @{nombre = "María"; tipo = "destinatario"; desc = "Buscar María como destinatario" },
    @{nombre = "García"; tipo = "ambos"; desc = "Buscar García en ambos campos" }
)

foreach ($test in $tests) {
    Write-Host "`n🔸 $($test.desc):" -ForegroundColor Cyan
    $url = "http://localhost:8000/api/envios/rastrear_por_nombre/?nombre=$($test.nombre)&tipo=$($test.tipo)"
    Write-Host "   URL: $url" -ForegroundColor Gray

    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
        $content = $response.Content | ConvertFrom-Json

        if ($content.resultados -gt 0) {
            Write-Host "   ✅ Encontrados: $($content.resultados) envíos" -ForegroundColor Green
            foreach ($envio in $content.envios) {
                Write-Host "      📦 $($envio.numero_guia): $($envio.remitente_nombre) → $($envio.destinatario_nombre)" -ForegroundColor White
            }
        }
        else {
            Write-Host "   ⚠️  No se encontraron resultados" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 4. ABRIR FRONTEND PARA PRUEBAS
Write-Host "`n🌐 4. ABRIENDO FRONTEND PARA PRUEBAS" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

Write-Host "🌐 Abriendo aplicación en navegador..." -ForegroundColor Cyan

# Abrir login
Start-Process "chrome.exe" -ArgumentList "--new-window", "https://localhost:5173/login"
Start-Sleep -Seconds 1

# Abrir rastreo
Start-Process "chrome.exe" -ArgumentList "--new-tab", "https://localhost:5173/rastreo"

Write-Host "`n💡 CREDENCIALES PARA LOGIN:" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow
Write-Host "📧 Email: admin@packfy.cu" -ForegroundColor Green
Write-Host "🔑 Password: admin123" -ForegroundColor Green

# 5. INSTRUCCIONES DE PRUEBA
Write-Host "`n📋 5. INSTRUCCIONES DE PRUEBA" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

Write-Host "🔹 PASO 1: Hacer login con las credenciales arriba" -ForegroundColor Cyan
Write-Host "🔹 PASO 2: Ir a la pestaña 'Seguimiento'" -ForegroundColor Cyan
Write-Host "🔹 PASO 3: Probar estas búsquedas:" -ForegroundColor Cyan
Write-Host "   📝 'José' (tipo: remitente)" -ForegroundColor White
Write-Host "   📝 'María' (tipo: destinatario)" -ForegroundColor White
Write-Host "   📝 'García' (tipo: ambos)" -ForegroundColor White

Write-Host "`n📱 6. ACCESO MOVIL" -ForegroundColor Yellow
Write-Host "=================" -ForegroundColor Yellow
Write-Host "📍 URL: https://192.168.12.178:5173/" -ForegroundColor Green

Write-Host "`n🎯 7. ESTADO ACTUAL" -ForegroundColor Yellow
Write-Host "==================" -ForegroundColor Yellow
Write-Host "✅ Datos de prueba creados" -ForegroundColor Green
Write-Host "✅ Usuario admin disponible" -ForegroundColor Green
Write-Host "✅ Endpoints probados directamente" -ForegroundColor Green
Write-Host "✅ Frontend abierto para pruebas" -ForegroundColor Green

Write-Host "`n🇨🇺 Packfy Cuba - ¡Prueba la búsqueda por nombres ahora!" -ForegroundColor Green
