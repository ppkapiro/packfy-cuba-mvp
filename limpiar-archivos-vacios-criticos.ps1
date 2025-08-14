#!/usr/bin/env pwsh
# Script para limpiar archivos vacíos críticos del proyecto

Write-Host "🧹 INICIANDO LIMPIEZA DE ARCHIVOS VACÍOS CRÍTICOS..." -ForegroundColor Yellow

$archivosVaciosCriticos = @(
    # Backend - Archivos Python críticos
    "backend\ai_system.py",
    "backend\ai_views.py",
    "backend\chatbot.py",
    "backend\push_notifications.py",
    "backend\push_urls.py",
    "backend\push_views.py",
    "backend\config\__init__.py",
    "backend\empresas\__init__.py",
    "backend\envios\__init__.py",
    "backend\envios\ai_urls.py",
    "backend\usuarios\__init__.py",

    # Frontend - Archivos de configuración críticos
    "frontend\playwright.config.ts",
    "frontend\vite.config.docker.ts",
    "frontend\vite.config.mobile.ts",
    "frontend\vite.config.performance.ts",
    "frontend\vite.config.prod.ts",
    "frontend\vite.config.ts",
    "frontend\vitest.config.testing.ts",
    "frontend\vitest.config.ts"
)

$eliminados = 0
$restaurados = 0

foreach ($archivo in $archivosVaciosCriticos) {
    $rutaCompleta = Join-Path $PWD $archivo

    if (Test-Path $rutaCompleta) {
        $tamaño = (Get-Item $rutaCompleta).Length

        if ($tamaño -eq 0) {
            Write-Host "❌ Eliminando archivo vacío: $archivo" -ForegroundColor Red
            Remove-Item $rutaCompleta -Force
            $eliminados++

            # Restaurar archivos críticos con contenido básico
            if ($archivo.EndsWith("__init__.py")) {
                Write-Host "🔄 Restaurando $archivo con contenido básico" -ForegroundColor Green
                Set-Content -Path $rutaCompleta -Value "# Este archivo permite que Python trate el directorio como un paquete"
                $restaurados++
            }
            elseif ($archivo -eq "frontend\vite.config.ts") {
                Write-Host "🔄 Restaurando configuración básica de Vite" -ForegroundColor Green
                $contenidoVite = @"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})
"@
                Set-Content -Path $rutaCompleta -Value $contenidoVite
                $restaurados++
            }
        }
        else {
            Write-Host "✅ $archivo tiene contenido ($tamaño bytes)" -ForegroundColor Green
        }
    }
    else {
        Write-Host "⚠️  $archivo no existe" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📊 RESUMEN DE LIMPIEZA:" -ForegroundColor Cyan
Write-Host "🗑️  Archivos eliminados: $eliminados" -ForegroundColor Red
Write-Host "🔄 Archivos restaurados: $restaurados" -ForegroundColor Green

Write-Host ""
Write-Host "✅ LIMPIEZA COMPLETADA" -ForegroundColor Green
Write-Host "💡 El frontend funciona con HTTPS en: https://localhost:5173/" -ForegroundColor Blue
Write-Host "💡 El backend funciona con HTTP en: http://localhost:8000/" -ForegroundColor Blue
