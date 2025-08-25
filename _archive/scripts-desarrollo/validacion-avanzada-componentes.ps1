# Validador Avanzado de Componentes - Testing Detallado
# Análisis profundo de cada componente implementado

Write-Host "=== 🔍 VALIDACIÓN AVANZADA DE COMPONENTES ===" -ForegroundColor Cyan

# Función para analizar archivo TypeScript
function Analyze-TSXComponent {
    param(
        [string]$FilePath,
        [string]$ComponentName
    )

    Write-Host "`n=== 📄 ANALIZANDO $ComponentName ===" -ForegroundColor Green

    if (-not (Test-Path $FilePath)) {
        Write-Host "❌ Archivo no encontrado: $FilePath" -ForegroundColor Red
        return
    }

    $content = Get-Content $FilePath -Raw

    # Análisis de imports
    Write-Host "`n📦 IMPORTS:" -ForegroundColor Yellow
    $imports = $content | Select-String "import.*from" -AllMatches
    foreach ($import in $imports.Matches) {
        Write-Host "  ✓ $($import.Value)" -ForegroundColor Gray
    }

    # Análisis de interfaces
    Write-Host "`n🏗️  INTERFACES:" -ForegroundColor Yellow
    $interfaces = $content | Select-String "interface\s+\w+.*\{" -AllMatches
    foreach ($interface in $interfaces.Matches) {
        Write-Host "  ✓ $($interface.Value)" -ForegroundColor Gray
    }

    # Análisis de hooks utilizados
    Write-Host "`n🪝 HOOKS UTILIZADOS:" -ForegroundColor Yellow
    $hooks = @("useState", "useEffect", "useAuth", "useTenant", "useContext")
    foreach ($hook in $hooks) {
        if ($content -match $hook) {
            Write-Host "  ✓ $hook" -ForegroundColor Green
        }
    }

    # Análisis de elementos UI
    Write-Host "`n🎨 ELEMENTOS UI:" -ForegroundColor Yellow
    $uiElements = @("button", "input", "form", "div", "span", "table", "modal")
    $foundElements = 0
    foreach ($element in $uiElements) {
        if ($content -match "<$element") {
            Write-Host "  ✓ $element" -ForegroundColor Green
            $foundElements++
        }
    }
    Write-Host "  Total elementos UI: $foundElements" -ForegroundColor Cyan

    # Análisis de manejo de estados
    Write-Host "`n🔄 MANEJO DE ESTADOS:" -ForegroundColor Yellow
    if ($content -match "setLoading|isLoading") {
        Write-Host "  ✓ Estados de carga" -ForegroundColor Green
    }
    if ($content -match "setError|error") {
        Write-Host "  ✓ Manejo de errores" -ForegroundColor Green
    }
    if ($content -match "setSuccess|success") {
        Write-Host "  ✓ Estados de éxito" -ForegroundColor Green
    }

    # Análisis de API calls
    Write-Host "`n🌐 LLAMADAS API:" -ForegroundColor Yellow
    if ($content -match "api\.(get|post|put|delete)") {
        Write-Host "  ✓ Integración con API" -ForegroundColor Green
    }
    if ($content -match "fetch|axios") {
        Write-Host "  ✓ HTTP requests" -ForegroundColor Green
    }

    # Análisis de validación
    Write-Host "`n✅ VALIDACIÓN:" -ForegroundColor Yellow
    if ($content -match "required|validate") {
        Write-Host "  ✓ Validación de campos" -ForegroundColor Green
    }
    if ($content -match "trim\(\)|length") {
        Write-Host "  ✓ Validación de formato" -ForegroundColor Green
    }

    # Contar líneas
    $lines = ($content -split "`n").Count
    Write-Host "`n📊 MÉTRICAS:"
    Write-Host "  Líneas de código: $lines" -ForegroundColor Cyan

    # Análisis de complejidad
    $functions = $content | Select-String "const\s+\w+\s*=" -AllMatches
    Write-Host "  Funciones/variables: $($functions.Matches.Count)" -ForegroundColor Cyan
}

# Analizar cada componente
$components = @(
    @{
        Name     = "EnvioFormContainer"
        Path     = "frontend\src\components\EnvioFormContainer.tsx"
        Expected = @("Router", "Autenticación", "Roles")
    },
    @{
        Name     = "RemitenteForm"
        Path     = "frontend\src\components\envios\RemitenteForm.tsx"
        Expected = @("Formulario", "Validación", "API")
    },
    @{
        Name     = "OperadorForm"
        Path     = "frontend\src\components\envios\OperadorForm.tsx"
        Expected = @("Dashboard", "Lista", "Búsqueda")
    },
    @{
        Name     = "AdminForm"
        Path     = "frontend\src\components\envios\AdminForm.tsx"
        Expected = @("Estadísticas", "Gestión")
    },
    @{
        Name     = "DestinatarioView"
        Path     = "frontend\src\components\envios\DestinatarioView.tsx"
        Expected = @("Vista", "Detalles")
    }
)

foreach ($component in $components) {
    Analyze-TSXComponent -FilePath $component.Path -ComponentName $component.Name
}

Write-Host "`n=== 📋 CHECKLIST DE TESTING MANUAL ===" -ForegroundColor Magenta

Write-Host "`n🔐 AUTENTICACIÓN Y NAVEGACIÓN:" -ForegroundColor Yellow
Write-Host "□ Login funciona correctamente"
Write-Host "□ Redirección según rol es correcta"
Write-Host "□ Logout funciona y limpia sesión"
Write-Host "□ Manejo de sesiones expiradas"

Write-Host "`n👤 REMITENTE FORM:" -ForegroundColor Yellow
Write-Host "□ Formulario se carga correctamente"
Write-Host "□ Validación de campos obligatorios"
Write-Host "□ Envío de datos funciona"
Write-Host "□ Mensaje de confirmación aparece"
Write-Host "□ Formulario se resetea tras envío"

Write-Host "`n👥 OPERADOR FORM:" -ForegroundColor Yellow
Write-Host "□ Dashboard carga con pestañas"
Write-Host "□ Lista de envíos se muestra"
Write-Host "□ Búsqueda funciona correctamente"
Write-Host "□ Filtros operan bien"
Write-Host "□ Creación de envío desde pestaña"

Write-Host "`n👑 ADMIN FORM:" -ForegroundColor Yellow
Write-Host "□ Estadísticas se calculan y muestran"
Write-Host "□ Navegación entre pestañas fluida"
Write-Host "□ Acceso a gestión de envíos"
Write-Host "□ Enlaces a admin Django funcionan"
Write-Host "□ Actualización de datos opera"

Write-Host "`n📨 DESTINATARIO VIEW:" -ForegroundColor Yellow
Write-Host "□ Lista de envíos se filtra correctamente"
Write-Host "□ Vista detalle funciona"
Write-Host "□ Búsqueda opera en tiempo real"
Write-Host "□ Información completa se muestra"
Write-Host "□ Navegación entre vistas fluida"

Write-Host "`n📱 RESPONSIVE TESTING:" -ForegroundColor Yellow
Write-Host "□ Móvil: Layouts se adaptan bien"
Write-Host "□ Tablet: Navegación es cómoda"
Write-Host "□ Desktop: Aprovecha espacio disponible"
Write-Host "□ Formularios usables en todos los tamaños"

Write-Host "`n🚫 TESTING DE ERRORES:" -ForegroundColor Yellow
Write-Host "□ Sin conexión: Manejo graceful"
Write-Host "□ API errors: Mensajes claros"
Write-Host "□ Campos vacíos: Validación correcta"
Write-Host "□ Permisos: Restricciones respetadas"

Write-Host "`n=== 🎯 CRITERIOS DE APROBACIÓN ===" -ForegroundColor Green

Write-Host "`n✅ FUNCIONALIDAD:" -ForegroundColor Cyan
Write-Host "- Cada rol accede a su vista correcta"
Write-Host "- Formularios envían y validan datos"
Write-Host "- Navegación es intuitiva y fluida"
Write-Host "- Estados de carga/error/éxito son claros"

Write-Host "`n✅ RENDIMIENTO:" -ForegroundColor Cyan
Write-Host "- Carga inicial < 3 segundos"
Write-Host "- Navegación entre vistas < 1 segundo"
Write-Host "- Sin memory leaks visibles"
Write-Host "- Respuesta de formularios ágil"

Write-Host "`n✅ UX/UI:" -ForegroundColor Cyan
Write-Host "- Diseño consistente en todas las vistas"
Write-Host "- Iconografía clara y comprensible"
Write-Host "- Feedback visual apropiado"
Write-Host "- Responsive design funcional"

Write-Host "`n✅ INTEGRACIÓN:" -ForegroundColor Cyan
Write-Host "- Contextos de auth/tenant operan"
Write-Host "- API calls funcionan correctamente"
Write-Host "- Manejo de errores es robusto"
Write-Host "- Datos se persisten apropiadamente"

Write-Host "`n🎉 VALIDACIÓN AVANZADA COMPLETADA" -ForegroundColor Green
Write-Host "📋 Usar checklist para testing manual sistemático" -ForegroundColor Cyan
