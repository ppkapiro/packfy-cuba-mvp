# 🇨🇺 PACKFY CUBA - RECONSTRUCCIÓN COMPLETA Y LIMPIA

Write-Host "🇨🇺 PACKFY CUBA - RECONSTRUCCIÓN LIMPIA DEL SISTEMA" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Cambiar al directorio del proyecto
Set-Location "C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp"

Write-Host "`n🧹 PASO 1: LIMPIEZA COMPLETA" -ForegroundColor Yellow
.\clean_all.ps1

Write-Host "`n🔧 PASO 2: VERIFICANDO ARCHIVOS LIMPIOS" -ForegroundColor Yellow
Write-Host "Verificando que los archivos limpios están en su lugar..."
if (Test-Path "backend\usuarios\serializers_clean.py") {
    Write-Host "✅ Serializers limpios - OK" -ForegroundColor Green
}
else {
    Write-Host "❌ Serializers limpios - FALTA" -ForegroundColor Red
}

if (Test-Path "backend\usuarios\auth_views_clean.py") {
    Write-Host "✅ Views limpias - OK" -ForegroundColor Green
}
else {
    Write-Host "❌ Views limpias - FALTA" -ForegroundColor Red
}

Write-Host "`n🏗️ PASO 3: RECONSTRUYENDO CONTENEDORES" -ForegroundColor Yellow
Write-Host "Construyendo con cache limpio..."
docker compose build --no-cache

Write-Host "`n🚀 PASO 4: INICIANDO SISTEMA LIMPIO" -ForegroundColor Yellow
docker compose up -d

Write-Host "`n⏳ PASO 5: ESPERANDO INICIALIZACIÓN" -ForegroundColor Yellow
Write-Host "Esperando que los servicios estén listos..."
Start-Sleep -Seconds 20

Write-Host "`n🗄️ PASO 6: CONFIGURANDO BASE DE DATOS LIMPIA" -ForegroundColor Yellow
Write-Host "Aplicando migraciones..."
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

Write-Host "`n👤 PASO 7: CREANDO USUARIO ADMIN LIMPIO" -ForegroundColor Yellow
$createAdminCommand = @"
from usuarios.models import Usuario;
admin = Usuario.objects.create_user(
    email='admin@packfy.cu',
    password='admin123',
    username='admin@packfy.cu',
    first_name='Admin',
    last_name='Packfy',
    is_staff=True,
    is_superuser=True,
    is_active=True
);
print(f'Admin creado: {admin.email}')
"@

docker compose exec -T backend python manage.py shell -c $createAdminCommand

Write-Host "`n📊 PASO 8: VERIFICACIÓN FINAL" -ForegroundColor Yellow
Write-Host "Estado de contenedores:"
docker compose ps

Write-Host "`nUsuarios en la base de datos:"
docker compose exec -T backend python manage.py shell -c "from usuarios.models import Usuario; users = Usuario.objects.all(); [print(f'  {u.email} - Active: {u.is_active}') for u in users]"

Write-Host "`n🎉 RECONSTRUCCIÓN COMPLETA TERMINADA" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "Sistema limpio y funcional."
Write-Host "URL: https://localhost:5173"
Write-Host "Credenciales: admin@packfy.cu / admin123"
