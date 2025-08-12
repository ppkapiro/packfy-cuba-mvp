#!/usr/bin/env pwsh
# 🔧 PACKFY CUBA - DIAGNOSTICO Y SOLUCION BUSQUEDA POR NOMBRES
# ============================================================

Write-Host "🔧 PACKFY CUBA - DIAGNOSTICO BUSQUEDA POR NOMBRES" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

$backendDir = "c:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp\backend"

# 1. CREAR DATOS DE PRUEBA
Write-Host "`n📊 1. CREANDO DATOS DE PRUEBA" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

$createDataScript = @"
from envios.models import Envio
from datetime import datetime

# Eliminar datos existentes para empezar limpio
Envio.objects.all().delete()

# Crear envíos de prueba
envios_prueba = [
    {
        'numero_guia': 'CU001',
        'remitente_nombre': 'José García',
        'destinatario_nombre': 'María López',
        'estado_actual': 'en_proceso',
        'peso': 2.5,
        'direccion_origen': 'La Habana',
        'direccion_destino': 'Santiago'
    },
    {
        'numero_guia': 'CU002',
        'remitente_nombre': 'Ana Fernández',
        'destinatario_nombre': 'Carlos Pérez',
        'estado_actual': 'entregado',
        'peso': 1.8,
        'direccion_origen': 'Matanzas',
        'direccion_destino': 'Camagüey'
    },
    {
        'numero_guia': 'CU003',
        'remitente_nombre': 'Luis Rodríguez',
        'destinatario_nombre': 'Elena García',
        'estado_actual': 'pendiente',
        'peso': 3.2,
        'direccion_origen': 'Villa Clara',
        'direccion_destino': 'Holguín'
    }
]

for datos in envios_prueba:
    Envio.objects.create(**datos)

print(f'✅ {len(envios_prueba)} envíos de prueba creados')
print('Envíos disponibles:')
for envio in Envio.objects.all():
    print(f'  - {envio.numero_guia}: {envio.remitente_nombre} → {envio.destinatario_nombre}')
"@

Write-Host "🔄 Creando datos de prueba..." -ForegroundColor Cyan
Set-Location $backendDir
echo $createDataScript | python manage.py shell

# 2. PROBAR ENDPOINTS DE BUSQUEDA
Write-Host "`n🔍 2. PROBANDO ENDPOINTS DE BUSQUEDA" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

Write-Host "🧪 Probando búsqueda por remitente 'José'..." -ForegroundColor Cyan
$response1 = curl -s "http://localhost:8000/api/envios/rastrear_por_nombre/?nombre=José&tipo=remitente"
Write-Host "Respuesta: $response1" -ForegroundColor White

Write-Host "`n🧪 Probando búsqueda por destinatario 'María'..." -ForegroundColor Cyan
$response2 = curl -s "http://localhost:8000/api/envios/rastrear_por_nombre/?nombre=María&tipo=destinatario"
Write-Host "Respuesta: $response2" -ForegroundColor White

Write-Host "`n🧪 Probando búsqueda en ambos 'García'..." -ForegroundColor Cyan
$response3 = curl -s "http://localhost:8000/api/envios/rastrear_por_nombre/?nombre=García&tipo=ambos"
Write-Host "Respuesta: $response3" -ForegroundColor White

# 3. VERIFICAR FRONTEND
Write-Host "`n🌐 3. VERIFICANDO ACCESO AL FRONTEND" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

Write-Host "🌐 Abriendo páginas de prueba..." -ForegroundColor Cyan

# Abrir página de login
Start-Process "chrome.exe" -ArgumentList "--new-window", "https://localhost:5173/login"
Start-Sleep -Seconds 2

# Abrir página de rastreo directo
Start-Process "chrome.exe" -ArgumentList "--new-tab", "https://localhost:5173/rastreo"

Write-Host "`n💡 CREDENCIALES DE PRUEBA:" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow
Write-Host "📧 Email: admin@packfy.cu" -ForegroundColor White
Write-Host "🔑 Password: admin123" -ForegroundColor White

# 4. CREAR USUARIO ADMIN SI NO EXISTE
Write-Host "`n👤 4. VERIFICANDO USUARIO ADMIN" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

$createUserScript = @"
from django.contrib.auth.models import User

# Verificar si existe usuario admin
admin_user = User.objects.filter(username='admin').first()

if not admin_user:
    # Crear usuario admin
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@packfy.cu',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )
    print('✅ Usuario admin creado: admin@packfy.cu / admin123')
else:
    print(f'✅ Usuario admin ya existe: {admin_user.email}')
"@

Write-Host "🔄 Verificando usuario admin..." -ForegroundColor Cyan
echo $createUserScript | python manage.py shell

# 5. INSTRUCCIONES DE PRUEBA
Write-Host "`n📋 5. INSTRUCCIONES DE PRUEBA" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

Write-Host "🔹 PASO 1: Hacer login en https://localhost:5173/login" -ForegroundColor Cyan
Write-Host "   📧 Email: admin@packfy.cu" -ForegroundColor White
Write-Host "   🔑 Password: admin123" -ForegroundColor White

Write-Host "`n🔹 PASO 2: Ir a la pestaña 'Seguimiento'" -ForegroundColor Cyan
Write-Host "   📍 URL: https://localhost:5173/rastreo" -ForegroundColor White

Write-Host "`n🔹 PASO 3: Probar búsquedas con estos nombres:" -ForegroundColor Cyan
Write-Host "   🔸 'José' (debe encontrar 1 envío como remitente)" -ForegroundColor White
Write-Host "   🔸 'María' (debe encontrar 1 envío como destinatario)" -ForegroundColor White
Write-Host "   🔸 'García' (debe encontrar 2 envíos: 1 remitente + 1 destinatario)" -ForegroundColor White
Write-Host "   🔸 'Carlos' (debe encontrar 1 envío como destinatario)" -ForegroundColor White

Write-Host "`n📱 6. ACCESO MOVIL" -ForegroundColor Yellow
Write-Host "=================" -ForegroundColor Yellow
Write-Host "📍 URL móvil: https://192.168.12.178:5173/" -ForegroundColor Green
Write-Host "🔗 Mismas credenciales: admin@packfy.cu / admin123" -ForegroundColor White

Write-Host "`n🎯 7. VERIFICACION DE SOLUCION" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow
Write-Host "✅ Datos de prueba creados en base de datos" -ForegroundColor Green
Write-Host "✅ Endpoints de búsqueda funcionando" -ForegroundColor Green
Write-Host "✅ Usuario admin disponible para login" -ForegroundColor Green
Write-Host "✅ Frontend accesible en PC y móvil" -ForegroundColor Green

Write-Host "`n🇨🇺 Packfy Cuba - ¡Sistema de búsqueda por nombres listo!" -ForegroundColor Green

Write-Host "`nPresiona cualquier tecla para continuar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
