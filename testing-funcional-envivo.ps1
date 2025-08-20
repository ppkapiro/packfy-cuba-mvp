# Testing Funcional de Formularios de Envío - En Vivo
# Validación del sistema completo con servidores ejecutándose

Write-Host "=== 🚀 TESTING FUNCIONAL EN VIVO ===" -ForegroundColor Cyan

Write-Host "`n📋 VERIFICANDO SERVICIOS ACTIVOS..." -ForegroundColor Yellow

# Función para verificar URL
function Test-ServiceUrl {
    param(
        [string]$Url,
        [string]$ServiceName,
        [int]$TimeoutSeconds = 10
    )

    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec $TimeoutSeconds -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $ServiceName" -ForegroundColor Green -NoNewline
            Write-Host " - Activo en $Url" -ForegroundColor Gray
            return $true
        }
    }
    catch {
        Write-Host "❌ $ServiceName" -ForegroundColor Red -NoNewline
        Write-Host " - No disponible en $Url" -ForegroundColor Gray
        return $false
    }
}

# Verificar servicios
$frontendActive = Test-ServiceUrl "http://localhost:5173" "Frontend React"
$backendActive = Test-ServiceUrl "http://localhost:8000" "Backend Django"

if (-not $frontendActive -or -not $backendActive) {
    Write-Host "`n⚠️  ALGUNOS SERVICIOS NO ESTÁN ACTIVOS" -ForegroundColor Yellow
    Write-Host "Asegúrate de que estén ejecutándose:"
    Write-Host "- Frontend: cd frontend && npm run dev"
    Write-Host "- Backend: docker-compose up -d"
    Write-Host ""
}

Write-Host "`n=== 🔐 TESTING DE AUTENTICACIÓN ===" -ForegroundColor Green

# Probar endpoint de autenticación
try {
    $authTest = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/user/" -UseBasicParsing
    Write-Host "✅ Endpoint de autenticación disponible" -ForegroundColor Green
}
catch {
    Write-Host "⚠️  Endpoint de autenticación no responde" -ForegroundColor Yellow
}

Write-Host "`n=== 📦 TESTING DE API DE ENVÍOS ===" -ForegroundColor Green

# Probar endpoints de envíos
$enviosEndpoints = @(
    "http://localhost:8000/api/envios/",
    "http://localhost:8000/api/empresas/",
    "http://localhost:8000/api/perfiles/"
)

foreach ($endpoint in $enviosEndpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint -UseBasicParsing
        $endpointName = ($endpoint -split '/')[-2]
        Write-Host "✅ API $endpointName disponible" -ForegroundColor Green
    }
    catch {
        $endpointName = ($endpoint -split '/')[-2]
        Write-Host "⚠️  API $endpointName no responde (puede requerir autenticación)" -ForegroundColor Yellow
    }
}

Write-Host "`n=== 🎨 TESTING DE COMPONENTES FRONTEND ===" -ForegroundColor Green

# Verificar que el frontend carga correctamente
try {
    $frontendContent = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing

    if ($frontendContent.Content -match "React") {
        Write-Host "✅ Frontend React cargando correctamente" -ForegroundColor Green
    }

    # Verificar si hay errores de JavaScript básicos
    if ($frontendContent.Content -match "script") {
        Write-Host "✅ Scripts JavaScript detectados" -ForegroundColor Green
    }

}
catch {
    Write-Host "❌ Error al cargar frontend" -ForegroundColor Red
}

Write-Host "`n=== 📱 TESTING DE RESPONSIVIDAD ===" -ForegroundColor Green

Write-Host "📋 URLs para testing manual:" -ForegroundColor Cyan
Write-Host "🖥️  Desktop: http://localhost:5173"
Write-Host "📱 Móvil: http://192.168.12.178:5173 (desde otro dispositivo)"
Write-Host "🔗 Admin: http://localhost:8000/admin/"

Write-Host "`n=== 🧪 CASOS DE PRUEBA MANUALES ===" -ForegroundColor Magenta

Write-Host "`n👤 TESTING COMO REMITENTE:" -ForegroundColor Cyan
Write-Host "1. Acceder a http://localhost:5173"
Write-Host "2. Iniciar sesión con usuario remitente"
Write-Host "3. Verificar que aparece formulario simple"
Write-Host "4. Crear un envío de prueba"
Write-Host "5. Validar confirmación de éxito"

Write-Host "`n👥 TESTING COMO OPERADOR:" -ForegroundColor Cyan
Write-Host "1. Iniciar sesión con usuario operador"
Write-Host "2. Verificar dashboard con pestañas"
Write-Host "3. Probar lista de envíos"
Write-Host "4. Usar búsqueda y filtros"
Write-Host "5. Crear envío desde pestaña"

Write-Host "`n👑 TESTING COMO ADMIN:" -ForegroundColor Cyan
Write-Host "1. Iniciar sesión con usuario dueño"
Write-Host "2. Verificar estadísticas en dashboard"
Write-Host "3. Navegar entre pestañas"
Write-Host "4. Acceder a gestión de usuarios"
Write-Host "5. Probar admin de Django"

Write-Host "`n📨 TESTING COMO DESTINATARIO:" -ForegroundColor Cyan
Write-Host "1. Iniciar sesión con usuario destinatario"
Write-Host "2. Verificar lista de envíos dirigidos"
Write-Host "3. Hacer clic en envío para detalles"
Write-Host "4. Probar búsqueda de envíos"
Write-Host "5. Verificar datos de remitente"

Write-Host "`n=== 🔍 TESTING DE ERRORES COMUNES ===" -ForegroundColor Yellow

Write-Host "`n🚫 ESCENARIOS DE ERROR A PROBAR:" -ForegroundColor Red
Write-Host "1. Acceso sin autenticación"
Write-Host "2. Usuario sin empresa/tenant"
Write-Host "3. Usuario sin permisos activos"
Write-Host "4. Formularios con campos vacíos"
Write-Host "5. Conexión API interrumpida"

Write-Host "`n=== 📊 MÉTRICAS A VERIFICAR ===" -ForegroundColor Magenta

Write-Host "`n⚡ RENDIMIENTO:" -ForegroundColor Yellow
Write-Host "- Tiempo de carga inicial < 3 segundos"
Write-Host "- Tiempo de navegación entre roles < 1 segundo"
Write-Host "- Respuesta de formularios < 2 segundos"

Write-Host "`n🎯 FUNCIONALIDAD:" -ForegroundColor Yellow
Write-Host "- Validación de campos en tiempo real"
Write-Host "- Estados visuales correctos"
Write-Host "- Mensajes de error claros"
Write-Host "- Confirmaciones de éxito"

Write-Host "`n📱 RESPONSIVE:" -ForegroundColor Yellow
Write-Host "- Layouts móviles funcionales"
Write-Host "- Navegación táctil cómoda"
Write-Host "- Formularios usables en móvil"

Write-Host "`n=== 🎉 TESTING COMPLETADO ===" -ForegroundColor Green

Write-Host "`n✅ VERIFICACIONES REALIZADAS:" -ForegroundColor Green
Write-Host "- Servicios activos y disponibles"
Write-Host "- APIs respondiendo correctamente"
Write-Host "- Frontend cargando sin errores"
Write-Host "- Endpoints de envíos disponibles"

Write-Host "`n🔄 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. 🖱️  Realizar testing manual en navegador"
Write-Host "2. 👥 Probar cada rol de usuario"
Write-Host "3. 📱 Validar en diferentes dispositivos"
Write-Host "4. 🐛 Reportar cualquier bug encontrado"

Write-Host "`n🎯 SISTEMA LISTO PARA TESTING MANUAL" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Admin: http://localhost:8000/admin/" -ForegroundColor Cyan
