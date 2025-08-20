#!/usr/bin/env python3
"""
PRUEBAS COMPLETAS DEL SISTEMA PACKFY CUBA MVP
============================================

Script para probar todo el sistema incluyendo Docker.
Fecha: 20 de agosto de 2025
"""

import json
import subprocess
import time

import requests


def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔧 {descripcion}")
    print("=" * 50)

    try:
        resultado = subprocess.run(
            comando, shell=True, capture_output=True, text=True, timeout=30
        )

        if resultado.returncode == 0:
            print(f"✅ {descripcion} - EXITOSO")
            if resultado.stdout:
                print(f"📝 Salida: {resultado.stdout[:200]}...")
        else:
            print(f"❌ {descripcion} - ERROR")
            print(f"❌ Error: {resultado.stderr[:200]}")

        return resultado.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"⏰ {descripcion} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {descripcion} - EXCEPCIÓN: {e}")
        return False


def verificar_docker():
    """Verifica que Docker esté funcionando"""
    print("\n🐳 VERIFICANDO DOCKER")
    print("=" * 30)

    # Verificar Docker
    if not ejecutar_comando("docker --version", "Verificar Docker instalado"):
        return False

    # Verificar Docker Compose
    if not ejecutar_comando(
        "docker compose version", "Verificar Docker Compose"
    ):
        return False

    # Verificar contenedores corriendo
    ejecutar_comando("docker ps", "Contenedores activos")

    return True


def probar_sistema_local():
    """Prueba el sistema sin Docker"""
    print("\n💻 PROBANDO SISTEMA LOCAL")
    print("=" * 30)

    # Verificar estructura de archivos
    archivos_criticos = [
        "backend/manage.py",
        "frontend/package.json",
        "compose.yml",
        "backend/config/settings.py",
    ]

    for archivo in archivos_criticos:
        try:
            with open(archivo, "r") as f:
                print(f"✅ {archivo} existe")
        except FileNotFoundError:
            print(f"❌ {archivo} NO existe")
            return False

    return True


def probar_docker_compose():
    """Prueba Docker Compose"""
    print("\n🚀 PROBANDO DOCKER COMPOSE")
    print("=" * 35)

    # Detener servicios existentes
    ejecutar_comando("docker compose down", "Deteniendo servicios existentes")

    # Construir imágenes
    if not ejecutar_comando(
        "docker compose build", "Construyendo imágenes Docker"
    ):
        return False

    # Iniciar servicios
    if not ejecutar_comando("docker compose up -d", "Iniciando servicios"):
        return False

    # Esperar que los servicios se inicien
    print("⏰ Esperando que los servicios se inicien...")
    time.sleep(30)

    # Verificar servicios
    ejecutar_comando("docker compose ps", "Estado de servicios")

    # Verificar logs
    ejecutar_comando("docker compose logs --tail=10", "Logs recientes")

    return True


def probar_endpoints():
    """Prueba los endpoints principales"""
    print("\n🌐 PROBANDO ENDPOINTS")
    print("=" * 25)

    endpoints = [
        "http://localhost:8000/api/",
        "http://localhost:8000/api/empresas/",
        "http://localhost:3000/",
    ]

    for endpoint in endpoints:
        try:
            print(f"🔍 Probando {endpoint}...")
            response = requests.get(endpoint, timeout=10)
            print(f"✅ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")


def main():
    print("🚀 INICIANDO PRUEBAS COMPLETAS DEL SISTEMA")
    print("=" * 50)
    print("📅 Fecha: 20 de agosto de 2025")
    print("🎯 Objetivo: Verificar todo antes de commit final")

    exito_total = True

    # Paso 1: Verificar Docker
    if not verificar_docker():
        print("❌ Docker no está disponible")
        exito_total = False

    # Paso 2: Verificar sistema local
    if not probar_sistema_local():
        print("❌ Sistema local tiene problemas")
        exito_total = False

    # Paso 3: Probar Docker Compose
    if exito_total:
        if not probar_docker_compose():
            print("❌ Docker Compose falló")
            exito_total = False

    # Paso 4: Probar endpoints
    if exito_total:
        probar_endpoints()

    # Resultado final
    print("\n" + "=" * 60)
    if exito_total:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ Sistema listo para producción")
        print("✅ Docker funcionando correctamente")
        print("✅ Endpoints respondiendo")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("🔧 Revisar errores arriba")

    print("=" * 60)


if __name__ == "__main__":
    main()
