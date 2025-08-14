# 🇨🇺 PACKFY CUBA - Script de Instalación PWA
Write-Host "📱 PACKFY CUBA - Instalando Funciones PWA" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan

# Función para mostrar el progreso
function Show-Progress {
    param([string]$Activity, [string]$Status, [int]$PercentComplete)
    Write-Progress -Activity $Activity -Status $Status -PercentComplete $PercentComplete
}

try {
    # 1. Instalar dependencias del frontend
    Write-Host "`n🔧 Instalando dependencias de PWA en el frontend..." -ForegroundColor Yellow
    Show-Progress "Instalación PWA" "Instalando dependencias frontend" 10

    Set-Location "frontend"
    npm install vite-plugin-pwa@^0.20.5 --save-dev
    npm install workbox-window --save

    if ($LASTEXITCODE -ne 0) {
        throw "Error instalando dependencias del frontend"
    }

    # 2. Instalar dependencias del backend
    Write-Host "`n🔧 Instalando dependencias de Push Notifications en backend..." -ForegroundColor Yellow
    Show-Progress "Instalación PWA" "Instalando dependencias backend" 30

    Set-Location "../backend"

    # Activar entorno virtual si existe
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & "venv\Scripts\Activate.ps1"
    }

    pip install pywebpush==1.14.0
    pip install cryptography==41.0.0
    pip install ecdsa==0.18.0

    if ($LASTEXITCODE -ne 0) {
        throw "Error instalando dependencias del backend"
    }

    # 3. Generar claves VAPID
    Write-Host "`n🔑 Generando claves VAPID para notificaciones push..." -ForegroundColor Yellow
    Show-Progress "Instalación PWA" "Generando claves VAPID" 50

    $vapidScript = @"
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import base64

# Generar clave privada
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

# Obtener clave pública
public_key = private_key.public_key()

# Serializar clave privada en formato PEM
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Serializar clave pública en formato DER
public_der = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

# Convertir a base64 para uso en web
private_key_b64 = base64.urlsafe_b64encode(private_pem).decode('utf-8').rstrip('=')
public_key_b64 = base64.urlsafe_b64encode(public_der).decode('utf-8').rstrip('=')

# Guardar en archivo de configuración
vapid_config = {
    'private_key': private_key_b64,
    'public_key': public_key_b64,
    'subject': 'mailto:admin@packfycuba.com'
}

with open('vapid_keys.json', 'w') as f:
    json.dump(vapid_config, f, indent=2)

print("✅ Claves VAPID generadas exitosamente")
print(f"🔑 Clave pública: {public_key_b64[:50]}...")
print(f"🔒 Clave privada guardada en vapid_keys.json")
"@

    $vapidScript | Out-File -FilePath "generate_vapid.py" -Encoding UTF8
    python generate_vapid.py
    Remove-Item "generate_vapid.py"

    # 4. Crear directorio de iconos
    Write-Host "`n🎨 Configurando iconos PWA..." -ForegroundColor Yellow
    Show-Progress "Instalación PWA" "Configurando iconos" 70

    Set-Location "../frontend/public"
    if (-not (Test-Path "icons")) {
        New-Item -ItemType Directory -Path "icons"
    }

    # Crear iconos SVG básicos si no existen
    if (-not (Test-Path "icons/icon-192.svg")) {
        $iconSvg = @"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192" width="192" height="192">
  <defs>
    <linearGradient id="cubaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="192" height="192" rx="20" fill="url(#cubaGrad)"/>
  <text x="96" y="120" font-family="Arial,sans-serif" font-size="40" font-weight="bold" text-anchor="middle" fill="white">📦</text>
  <text x="96" y="150" font-family="Arial,sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="white">PACKFY</text>
  <text x="96" y="170" font-family="Arial,sans-serif" font-size="12" text-anchor="middle" fill="#e8f4fd">CUBA 🇨🇺</text>
</svg>
"@
        $iconSvg | Out-File -FilePath "icons/icon-192.svg" -Encoding UTF8
        $iconSvg | Out-File -FilePath "icons/icon-512.svg" -Encoding UTF8
    }

    # 5. Actualizar configuración de Django
    Write-Host "`n⚙️ Configurando Django para PWA..." -ForegroundColor Yellow
    Show-Progress "Instalación PWA" "Configurando Django" 85

    Set-Location "../../backend"

    # Verificar si las configuraciones ya existen en settings
    $settingsFile = "config/settings.py"
    if (Test-Path $settingsFile) {
        $content = Get-Content $settingsFile -Raw
        if ($content -notmatch "VAPID_PRIVATE_KEY") {
            $pwaSettings = @"

# 📱 PWA Y NOTIFICACIONES PUSH
VAPID_PRIVATE_KEY = os.getenv('VAPID_PRIVATE_KEY', '')
VAPID_PUBLIC_KEY = os.getenv('VAPID_PUBLIC_KEY', '')
VAPID_ADMIN_EMAIL = os.getenv('VAPID_ADMIN_EMAIL', 'admin@packfycuba.com')

# Configuración de notificaciones push
PUSH_NOTIFICATIONS_SETTINGS = {
    'GCM_API_KEY': '',
    'APNS_CERTIFICATE': '',
    'APNS_TOPIC': 'com.packfy.cuba',
    'WNS_PACKAGE_SECURITY_ID': '',
    'WNS_SECRET_KEY': '',
}
"@
            Add-Content -Path $settingsFile -Value $pwaSettings
        }
    }

    # 6. Crear template de notificaciones
    Write-Host "`n📧 Configurando plantillas de notificaciones..." -ForegroundColor Yellow
    Show-Progress "Instalación PWA" "Creando plantillas" 95

    $notificationTemplate = @"
# 🇨🇺 PACKFY CUBA - Script de inicialización de plantillas de notificaciones
from backend.push_notifications import NotificationTemplate

def create_default_templates():
    templates = [
        {
            'type': 'welcome',
            'title_template': '¡Bienvenido a PACKFY CUBA! 🇨🇺',
            'body_template': 'Hola {username}, gracias por unirte a nuestro sistema de paquetería moderno.',
            'icon_url': '/icons/welcome-notification.png',
            'action_url': '/dashboard',
            'require_interaction': False
        },
        {
            'type': 'shipment_created',
            'title_template': '📦 Nuevo Envío Creado',
            'body_template': 'Tu envío {numero_guia} ha sido creado exitosamente.',
            'icon_url': '/icons/shipment-notification.png',
            'action_url': '/envios/{id}',
            'require_interaction': False
        },
        {
            'type': 'shipment_status_update',
            'title_template': '📦 Estado de Envío Actualizado',
            'body_template': 'Tu envío {numero_guia} está ahora: {new_status}',
            'icon_url': '/icons/status-notification.png',
            'action_url': '/envios/{id}',
            'require_interaction': True
        },
        {
            'type': 'delivery_reminder',
            'title_template': '🚚 Recordatorio de Entrega',
            'body_template': 'Tu envío {numero_guia} será entregado hoy a {destinatario}',
            'icon_url': '/icons/delivery-notification.png',
            'action_url': '/envios/{id}',
            'require_interaction': True
        }
    ]

    for template_data in templates:
        template, created = NotificationTemplate.objects.get_or_create(
            type=template_data['type'],
            defaults=template_data
        )
        if created:
            print(f"✅ Plantilla creada: {template.get_type_display()}")
        else:
            print(f"ℹ️ Plantilla ya existe: {template.get_type_display()}")

if __name__ == '__main__':
    create_default_templates()
    print("🎉 Plantillas de notificaciones configuradas")
"@

    $notificationTemplate | Out-File -FilePath "init_notification_templates.py" -Encoding UTF8

    # 7. Finalizar
    Show-Progress "Instalación PWA" "Completando instalación" 100
    Write-Host "`n✅ ¡Instalación PWA completada exitosamente!" -ForegroundColor Green

    Write-Host "`n📋 PRÓXIMOS PASOS:" -ForegroundColor Cyan
    Write-Host "1. Configura las variables VAPID en tu archivo .env" -ForegroundColor White
    Write-Host "2. Ejecuta las migraciones: python manage.py migrate" -ForegroundColor White
    Write-Host "3. Inicializa las plantillas: python init_notification_templates.py" -ForegroundColor White
    Write-Host "4. Instala dependencias frontend: npm install" -ForegroundColor White
    Write-Host "5. Construye el proyecto: npm run build" -ForegroundColor White

    Write-Host "`n🔧 CONFIGURACIÓN REQUERIDA:" -ForegroundColor Yellow
    Write-Host "• Agrega las URLs de push_notifications a tu urls.py principal" -ForegroundColor White
    Write-Host "• Configura HTTPS para producción (requerido para PWA)" -ForegroundColor White
    Write-Host "• Verifica que los iconos PWA estén en /public/icons/" -ForegroundColor White

    if (Test-Path "vapid_keys.json") {
        $vapidKeys = Get-Content "vapid_keys.json" | ConvertFrom-Json
        Write-Host "`n🔑 CLAVES VAPID GENERADAS:" -ForegroundColor Magenta
        Write-Host "VAPID_PUBLIC_KEY=$($vapidKeys.public_key)" -ForegroundColor Gray
        Write-Host "VAPID_PRIVATE_KEY=$($vapidKeys.private_key)" -ForegroundColor Gray
        Write-Host "VAPID_ADMIN_EMAIL=$($vapidKeys.subject)" -ForegroundColor Gray
    }

}
catch {
    Write-Host "`n❌ Error durante la instalación: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔧 Verifica que tienes Node.js, Python y pip instalados correctamente" -ForegroundColor Yellow
    exit 1
}
finally {
    # Limpiar progreso
    Write-Progress -Activity "Instalación PWA" -Completed
    Set-Location $PSScriptRoot
}

Write-Host "`n🇨🇺 ¡PACKFY CUBA PWA está listo para usar!" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
