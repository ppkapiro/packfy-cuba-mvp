# 🛡️ COMANDOS RÁPIDOS DE BLINDAJE

# Crear respaldo de la estructura actual
function Crear-Respaldo {
    Write-Host "🛡️ Creando respaldo de estructura..." -ForegroundColor Green
    python blindar_estructura.py
}

# Verificar estado de la estructura
function Verificar-Estructura {
    Write-Host "🔍 Verificando estructura..." -ForegroundColor Blue
    Set-Location backend
    python verificar_blindaje.py
    Set-Location ..
}

# Restaurar estructura completa
function Restaurar-Estructura {
    Write-Host "🔄 Restaurando estructura..." -ForegroundColor Yellow
    Set-Location backend
    $latestRestore = Get-ChildItem "restaurar_estructura_*.py" | Sort-Object Name -Descending | Select-Object -First 1
    if ($latestRestore) {
        python $latestRestore.Name
        Write-Host "✅ Estructura restaurada usando: $($latestRestore.Name)" -ForegroundColor Green
    }
    else {
        Write-Host "❌ No se encontró script de restauración" -ForegroundColor Red
    }
    Set-Location ..
}

# Test rápido de autenticación
function Test-Auth {
    Write-Host "🔐 Probando autenticación..." -ForegroundColor Cyan

    # Test superadmin
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -ContentType "application/json" -Body '{"email":"superadmin@packfy.com","password":"super123!"}'
        Write-Host "✅ Superadmin: Login exitoso" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Superadmin: Login falló" -ForegroundColor Red
    }

    # Test dueño
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -ContentType "application/json" -Body '{"email":"dueno@packfy.com","password":"dueno123!"}'
        Write-Host "✅ Dueño: Login exitoso" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Dueño: Login falló" -ForegroundColor Red
    }
}

# Mostrar credenciales
function Mostrar-Credenciales {
    Write-Host "`n🔑 CREDENCIALES BLINDADAS:" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "👑 Superadmin: superadmin@packfy.com / super123!" -ForegroundColor Red
    Write-Host "👔 Dueño:      dueno@packfy.com / dueno123!" -ForegroundColor Blue
    Write-Host "🌴 Miami:      miami@packfy.com / miami123!" -ForegroundColor Green
    Write-Host "🏝️  Cuba:       cuba@packfy.com / cuba123!" -ForegroundColor Green
    Write-Host "📦 Remitentes: remitente[1-3]@packfy.com / remitente123!" -ForegroundColor Cyan
    Write-Host "🎯 Destinatarios: destinatario[1-3]@cuba.cu / destinatario123!" -ForegroundColor Magenta
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray
}

# Mostrar ayuda
function Ayuda-Blindaje {
    Write-Host "`n🛡️ SISTEMA DE BLINDAJE PACKFY" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "Comandos disponibles:" -ForegroundColor White
    Write-Host "  Crear-Respaldo        - Crear respaldo completo" -ForegroundColor Green
    Write-Host "  Verificar-Estructura  - Verificar estado actual" -ForegroundColor Blue
    Write-Host "  Restaurar-Estructura  - Restaurar estructura completa" -ForegroundColor Yellow
    Write-Host "  Test-Auth             - Probar autenticación API" -ForegroundColor Cyan
    Write-Host "  Mostrar-Credenciales  - Ver todas las credenciales" -ForegroundColor Magenta
    Write-Host "  Ayuda-Blindaje        - Mostrar esta ayuda" -ForegroundColor White
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray
}

# Mostrar ayuda al cargar
Write-Host "🛡️ Sistema de Blindaje cargado. Usa 'Ayuda-Blindaje' para ver comandos." -ForegroundColor Green
