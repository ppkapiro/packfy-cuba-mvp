#!/usr/bin/env python3
"""
Script completo para verificar y solucionar problemas de autenticación
"""

import json
import os
import subprocess
import time

import requests


def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔧 {description}")
    print("-" * 50)
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=r"C:\Users\pepec\Projects\Packfy\paqueteria-cuba-mvp",
        )
        if result.returncode == 0:
            print(f"✅ {description} - EXITOSO")
            if result.stdout.strip():
                print(result.stdout)
        else:
            print(f"❌ {description} - FALLÓ")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False


def check_containers():
    """Verificar estado de contenedores"""
    print("\n📦 VERIFICANDO CONTENEDORES")
    print("=" * 50)

    # Verificar si están corriendo
    success = run_command(
        "docker compose ps", "Verificando estado de contenedores"
    )

    if not success:
        print("\n🚀 Iniciando contenedores...")
        run_command("docker compose up -d", "Iniciando contenedores")
        time.sleep(10)  # Esperar que se inicien

    return True


def test_database_connection():
    """Probar conexión a la base de datos"""
    print("\n🗄️ VERIFICANDO BASE DE DATOS")
    print("=" * 50)

    # Verificar usuarios en la base de datos
    success = run_command(
        "docker compose exec -T backend python manage.py shell -c \"from usuarios.models import Usuario; print(f'Usuarios: {Usuario.objects.count()}')\"",
        "Verificando usuarios en BD",
    )

    return success


def test_authentication():
    """Probar autenticación directamente"""
    print("\n🔐 PROBANDO AUTENTICACIÓN")
    print("=" * 50)

    # Crear usuario admin si no existe
    run_command(
        "docker compose exec -T backend python manage.py shell -c \"from usuarios.models import Usuario; admin, created = Usuario.objects.get_or_create(email='admin@packfy.cu', defaults={'username': 'admin@packfy.cu', 'first_name': 'Admin', 'last_name': 'Packfy', 'is_staff': True, 'is_superuser': True, 'is_active': True}); admin.set_password('admin123'); admin.save(); print(f'Admin {\"creado\" if created else \"actualizado\"}: {admin.email}')\"",
        "Creando/actualizando usuario admin",
    )

    # Probar autenticación Django
    run_command(
        "docker compose exec -T backend python manage.py shell -c \"from django.contrib.auth import authenticate; user = authenticate(username='admin@packfy.cu', password='admin123'); print(f'Autenticación: {\"EXITOSA\" if user else \"FALLÓ\"}')\"",
        "Probando autenticación Django",
    )


def test_api_endpoints():
    """Probar endpoints de API"""
    print("\n🌐 PROBANDO ENDPOINTS DE API")
    print("=" * 50)

    # Esperar que el backend esté listo
    time.sleep(5)

    # Probar endpoint simple
    try:
        data = {"username": "admin@packfy.cu", "password": "admin123"}

        print("🧪 Probando endpoint simple de login...")
        response = requests.post(
            "https://localhost:8443/api/auth/test-login/",
            json=data,
            verify=False,
            timeout=10,
        )

        if response.status_code == 200:
            print("✅ Login simple - EXITOSO")
            result = response.json()
            print(f"Usuario: {result.get('user', {}).get('email', 'N/A')}")
        else:
            print(f"❌ Login simple - FALLÓ (Status: {response.status_code})")
            print(response.text)

    except Exception as e:
        print(f"❌ Error probando endpoint simple: {e}")

    # Probar endpoint principal
    try:
        print("\n🔐 Probando endpoint principal de login...")
        response = requests.post(
            "https://localhost:8443/api/auth/login/",
            json=data,
            verify=False,
            timeout=10,
        )

        if response.status_code == 200:
            print("✅ Login principal - EXITOSO")
            result = response.json()
            print(f"Usuario: {result.get('user', {}).get('email', 'N/A')}")
        else:
            print(
                f"❌ Login principal - FALLÓ (Status: {response.status_code})"
            )
            print(response.text)

    except Exception as e:
        print(f"❌ Error probando endpoint principal: {e}")


def clear_cache():
    """Limpiar cache de Redis"""
    print("\n🧹 LIMPIANDO CACHE")
    print("=" * 50)

    run_command(
        "docker compose exec -T redis redis-cli FLUSHALL",
        "Limpiando cache de Redis",
    )


def main():
    """Función principal"""
    print("🇨🇺 PACKFY CUBA - VERIFICACIÓN Y SOLUCIÓN DE AUTENTICACIÓN")
    print("=" * 60)

    # 1. Verificar y reiniciar contenedores
    check_containers()

    # 2. Limpiar cache
    clear_cache()

    # 3. Reiniciar backend para cargar cambios
    print("\n🔄 REINICIANDO BACKEND")
    print("=" * 50)
    run_command("docker compose restart backend", "Reiniciando backend")
    time.sleep(10)  # Esperar que se reinicie

    # 4. Verificar base de datos
    test_database_connection()

    # 5. Probar autenticación
    test_authentication()

    # 6. Probar endpoints de API
    test_api_endpoints()

    print("\n🎉 VERIFICACIÓN COMPLETADA")
    print("=" * 60)
    print("Si todos los tests pasaron, el sistema debería estar funcionando.")
    print("Puedes probar el login en: https://localhost:5173")
    print("Credenciales: admin@packfy.cu / admin123")


if __name__ == "__main__":
    main()
