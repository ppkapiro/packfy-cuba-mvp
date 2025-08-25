#!/usr/bin/env pwsh

# 🧹 LIMPIEZA AGRESIVA FINAL
# Remover archivos duplicados que ya están en _archive/

Write-Host "🔥 INICIANDO LIMPIEZA AGRESIVA FINAL..." -ForegroundColor Red

# Lista de archivos a eliminar (ya están en _archive/)
$archivosAEliminar = @(
    "ANALISIS-FORMULARIOS-ENVIO.md",
    "ANALISIS-INTERFACES-ROLES.md",
    "COMIC-MODERNIZACION-ENVIOS.txt",
    "IMPLEMENTACION-NAVEGACION-INTEGRADA.md",
    "MODERNIZACION-ENVIOS-COMPLETADA.md",
    "PLAN-LIMPIEZA-DETALLADO.md",
    "RESUMEN-MULTITENANCY-ADMIN-v2.0.md",
    "RESUMEN-TRABAJO-COMPLETADO.md",
    "SISTEMA-MULTITENANCY-COMPLETADO.md",
    "abrir-chrome-routing-test.ps1",
    "auditoria_completa_bd.py",
    "commit-formularios-unificados.ps1",
    "commit-testing-completo.ps1",
    "configurar-hosts-automatico.ps1",
    "configurar-hosts-multitenancy.ps1",
    "configurar_empresas_dominios.py",
    "contenedores-actualizados.ps1",
    "corregir_roles.py",
    "corregir_roles_command.py",
    "crear-datos-demo-completa.ps1",
    "crear-envio-exitoso.ps1",
    "crear_datos_minimos.py",
    "debug-envio-error.ps1",
    "demo-multitenancy-completo.ps1",
    "diagnostico-acceso-envios.ps1",
    "diagnostico-sistema-completo.ps1",
    "ejecutar-limpieza-multitenancy.ps1",
    "guia-prueba-interfaz-dueno.ps1",
    "hosts-multitenancy.txt",
    "investigar_usuarios.py",
    "probar-apis-completas.ps1",
    "probar-apis-con-tenant.ps1",
    "probar-creacion-datos.ps1",
    "probar-dominios-multitenancy.ps1",
    "probar-multitenancy-sin-hosts.ps1",
    "prueba-navegacion-dueno.ps1",
    "prueba-usuarios.ps1",
    "shell_crear_datos.py",
    "testing-formularios-completo.ps1",
    "testing-funcional-envivo.ps1",
    "testing-manual-dashboard.ps1",
    "validacion-avanzada-componentes.ps1",
    "validacion-navegacion-dueno.ps1",
    "verificacion-navegacion-vivo.ps1",
    "verificar-admin-perfecto.ps1",
    "verificar-dashboard-completo.ps1",
    "verificar-endpoints-reales.ps1",
    "verificar-envios-modernizada.ps1",
    "verificar-navegacion-admin-completa.ps1",
    "verificar-navegacion-docker.ps1",
    "verificar-post-limpieza.ps1",
    "verificar-routing-admin.ps1",
    "verificar-todos-flujos.ps1",
    "verificar-urls-exactas.ps1",
    "verificar_estado_sistema.py"
)

$eliminados = 0
$noEncontrados = 0

foreach ($archivo in $archivosAEliminar) {
    if (Test-Path $archivo) {
        Write-Host "🗑️ Eliminando: $archivo" -ForegroundColor Yellow
        Remove-Item $archivo -Force
        $eliminados++
    }
    else {
        $noEncontrados++
    }
}

Write-Host "`n✅ LIMPIEZA COMPLETADA:" -ForegroundColor Green
Write-Host "   📁 Archivos eliminados: $eliminados" -ForegroundColor Cyan
Write-Host "   ❓ No encontrados: $noEncontrados" -ForegroundColor Gray

# Verificar archivos restantes
$psFiles = (Get-ChildItem *.ps1 -ErrorAction SilentlyContinue).Count
$mdFiles = (Get-ChildItem *.md -ErrorAction SilentlyContinue).Count
$pyFiles = (Get-ChildItem *.py -ErrorAction SilentlyContinue).Count

Write-Host "`n📊 ARCHIVOS RESTANTES EN ROOT:" -ForegroundColor Magenta
Write-Host "   📜 Scripts PS1: $psFiles" -ForegroundColor Cyan
Write-Host "   📋 Docs MD: $mdFiles" -ForegroundColor Cyan
Write-Host "   🐍 Scripts PY: $pyFiles" -ForegroundColor Cyan

if ($psFiles -le 7 -and $mdFiles -le 3 -and $pyFiles -le 2) {
    Write-Host "`n🎉 PROYECTO LIMPIO - Estructura optimizada!" -ForegroundColor Green
}
else {
    Write-Host "`n⚠️ Revisar archivos restantes manualmente" -ForegroundColor Yellow
}
