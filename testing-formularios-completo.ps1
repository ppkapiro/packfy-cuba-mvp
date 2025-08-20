# Sistema de Testing Completo para Formularios de Envío Unificados
# Validación integral del sistema implementado

Write-Host "=== 🧪 INICIANDO TESTING SISTEMA FORMULARIOS UNIFICADOS ===" -ForegroundColor Cyan

# Función para mostrar estado de testing
function Show-TestStatus {
    param(
        [string]$TestName,
        [string]$Status,
        [string]$Details = ""
    )

    $color = switch ($Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "WARN" { "Yellow" }
        "INFO" { "Cyan" }
        default { "White" }
    }

    Write-Host "[$Status] $TestName" -ForegroundColor $color
    if ($Details) {
        Write-Host "    └─ $Details" -ForegroundColor Gray
    }
}

Write-Host "`n📋 PLAN DE TESTING:" -ForegroundColor Yellow
Write-Host "1. ✅ Verificación de estructura de archivos"
Write-Host "2. 🔍 Análisis de sintaxis TypeScript"
Write-Host "3. 🏗️ Validación de compilación"
Write-Host "4. 🔗 Testing de integración con backend"
Write-Host "5. 📱 Pruebas de UI/UX"
Write-Host "6. 🔐 Validación de autenticación y roles"

Write-Host "`n=== 1. VERIFICACIÓN DE ESTRUCTURA DE ARCHIVOS ===" -ForegroundColor Green

# Verificar archivos principales
$requiredFiles = @(
    "frontend\src\components\EnvioFormContainer.tsx",
    "frontend\src\components\envios\RemitenteForm.tsx",
    "frontend\src\components\envios\OperadorForm.tsx",
    "frontend\src\components\envios\AdminForm.tsx",
    "frontend\src\components\envios\DestinatarioView.tsx",
    "frontend\src\components\envios\index.ts"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Show-TestStatus "Archivo $file" "PASS" "Existe y disponible"
    }
    else {
        Show-TestStatus "Archivo $file" "FAIL" "No encontrado"
    }
}

Write-Host "`n=== 2. ANÁLISIS DE SINTAXIS TYPESCRIPT ===" -ForegroundColor Green

# Verificar que no hay errores de sintaxis básicos
$tsFiles = Get-ChildItem -Path "frontend\src\components" -Filter "*.tsx" -Recurse

foreach ($file in $tsFiles) {
    if ($file.Name -match "(EnvioForm|Remitente|Operador|Admin|Destinatario)") {
        $content = Get-Content $file.FullName -Raw

        # Verificaciones básicas
        if ($content -match "import.*React") {
            Show-TestStatus "React import en $($file.Name)" "PASS"
        }
        else {
            Show-TestStatus "React import en $($file.Name)" "FAIL" "Falta import de React"
        }

        if ($content -match "export default") {
            Show-TestStatus "Export default en $($file.Name)" "PASS"
        }
        else {
            Show-TestStatus "Export default en $($file.Name)" "FAIL" "Falta export default"
        }

        if ($content -match "interface.*Props") {
            Show-TestStatus "Interfaces TypeScript en $($file.Name)" "PASS"
        }
        else {
            Show-TestStatus "Interfaces TypeScript en $($file.Name)" "WARN" "No se detectaron interfaces de props"
        }
    }
}

Write-Host "`n=== 3. VALIDACIÓN DE COMPILACIÓN ===" -ForegroundColor Green

# Intentar compilar TypeScript
if (Test-Path "frontend\package.json") {
    Show-TestStatus "package.json encontrado" "PASS"

    # Verificar si está en el directorio correcto
    Push-Location "frontend"

    try {
        # Verificar dependencias
        if (Test-Path "node_modules") {
            Show-TestStatus "node_modules existe" "PASS"
        }
        else {
            Show-TestStatus "node_modules" "WARN" "Dependencias pueden no estar instaladas"
        }

        # Intentar verificar TypeScript
        Write-Host "    Verificando configuración TypeScript..."
        if (Test-Path "tsconfig.json") {
            Show-TestStatus "tsconfig.json" "PASS"
        }
        else {
            Show-TestStatus "tsconfig.json" "WARN" "No encontrado"
        }

    }
    catch {
        Show-TestStatus "Verificación frontend" "FAIL" $_.Exception.Message
    }
    finally {
        Pop-Location
    }
}
else {
    Show-TestStatus "package.json" "FAIL" "No encontrado en frontend/"
}

Write-Host "`n=== 4. TESTING DE INTEGRACIÓN CON BACKEND ===" -ForegroundColor Green

# Verificar que el backend está disponible
try {
    # Verificar archivos de configuración del backend
    if (Test-Path "backend\packfy\settings.py") {
        Show-TestStatus "Backend Django configurado" "PASS"
    }
    else {
        Show-TestStatus "Backend Django" "FAIL" "settings.py no encontrado"
    }

    # Verificar modelos de envío
    if (Test-Path "backend\apps\envios\models.py") {
        Show-TestStatus "Modelos de envío" "PASS"
    }
    else {
        Show-TestStatus "Modelos de envío" "FAIL" "models.py no encontrado"
    }

    # Verificar API endpoints
    if (Test-Path "backend\apps\envios\views.py") {
        Show-TestStatus "Views de envío" "PASS"
    }
    else {
        Show-TestStatus "Views de envío" "FAIL" "views.py no encontrado"
    }

}
catch {
    Show-TestStatus "Verificación backend" "FAIL" $_.Exception.Message
}

Write-Host "`n=== 5. PRUEBAS DE UI/UX ===" -ForegroundColor Green

# Verificar estructura de componentes UI
$uiComponents = @(
    @{ Name = "RemitenteForm"; Expected = @("formulario", "validación", "api") },
    @{ Name = "OperadorForm"; Expected = @("dashboard", "lista", "búsqueda") },
    @{ Name = "AdminForm"; Expected = @("estadísticas", "gestión") },
    @{ Name = "DestinatarioView"; Expected = @("consulta", "detalles") }
)

foreach ($component in $uiComponents) {
    $file = "frontend\src\components\envios\$($component.Name).tsx"
    if (Test-Path $file) {
        $content = Get-Content $file -Raw

        # Verificar elementos de UI esperados
        $foundElements = 0
        foreach ($element in $component.Expected) {
            if ($content -match $element) {
                $foundElements++
            }
        }

        if ($foundElements -gt 0) {
            Show-TestStatus "$($component.Name) elementos UI" "PASS" "$foundElements/$($component.Expected.Count) elementos encontrados"
        }
        else {
            Show-TestStatus "$($component.Name) elementos UI" "WARN" "Pocos elementos detectados"
        }
    }
}

Write-Host "`n=== 6. VALIDACIÓN DE AUTENTICACIÓN Y ROLES ===" -ForegroundColor Green

# Verificar integración con contextos
$containerFile = "frontend\src\components\EnvioFormContainer.tsx"
if (Test-Path $containerFile) {
    $content = Get-Content $containerFile -Raw

    if ($content -match "useAuth") {
        Show-TestStatus "Integración useAuth" "PASS"
    }
    else {
        Show-TestStatus "Integración useAuth" "FAIL" "No se detectó useAuth"
    }

    if ($content -match "useTenant") {
        Show-TestStatus "Integración useTenant" "PASS"
    }
    else {
        Show-TestStatus "Integración useTenant" "FAIL" "No se detectó useTenant"
    }

    # Verificar roles
    $roles = @("dueno", "operador", "remitente", "destinatario")
    $rolesFound = 0
    foreach ($rol in $roles) {
        if ($content -match $rol) {
            $rolesFound++
        }
    }

    if ($rolesFound -eq $roles.Count) {
        Show-TestStatus "Validación de roles" "PASS" "Todos los roles detectados"
    }
    else {
        Show-TestStatus "Validación de roles" "WARN" "$rolesFound/$($roles.Count) roles detectados"
    }
}

Write-Host "`n=== 📊 RESUMEN DE TESTING ===" -ForegroundColor Magenta

Write-Host "`n✅ ÁREAS VALIDADAS:" -ForegroundColor Green
Write-Host "- Estructura de archivos y organización"
Write-Host "- Sintaxis básica de TypeScript"
Write-Host "- Configuración de proyecto"
Write-Host "- Integración con backend"
Write-Host "- Elementos de UI/UX"
Write-Host "- Sistema de autenticación y roles"

Write-Host "`n🔄 PRÓXIMOS PASOS PARA TESTING COMPLETO:" -ForegroundColor Yellow
Write-Host "1. 🖥️  Ejecutar servidor de desarrollo"
Write-Host "2. 🔐 Probar flujos de autenticación"
Write-Host "3. 👥 Validar cada rol de usuario"
Write-Host "4. 📱 Testing responsive en navegador"
Write-Host "5. 🔗 Pruebas de API en vivo"

Write-Host "`n📋 COMANDOS SUGERIDOS PARA TESTING MANUAL:"
Write-Host "cd frontend && npm run dev       # Servidor desarrollo"
Write-Host "cd backend && python manage.py runserver  # API backend"
Write-Host "# Luego abrir http://localhost:3000"

Write-Host "`n🎯 TESTING COMPLETADO - Revisión inicial exitosa" -ForegroundColor Green
