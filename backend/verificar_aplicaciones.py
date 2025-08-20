#!/usr/bin/env python3
"""
VERIFICACIÓN COMPLETA DEL ESTADO DE APLICACIONES
===============================================

Verifica que todas las aplicaciones estén corriendo correctamente.
Fecha: 20 de agosto de 2025
"""

import json
import os
import subprocess

import requests


def verificar_servidor_django():
    """Verifica el estado del servidor Django"""
    print("🐍 SERVIDOR DJANGO (Backend)")
    print("-" * 30)

    try:
        # Verificar endpoints principales
        endpoints = {
            "/api/": "API raíz",
            "/api/envios/": "Envíos",
            "/api/usuarios/": "Usuarios",
            "/api/empresas/": "Empresas",
            "/api/auth/login/": "Autenticación",
        }

        servidor_ok = True
        for endpoint, descripcion in endpoints.items():
            try:
                response = requests.get(
                    f"http://localhost:8000{endpoint}", timeout=3
                )
                if response.status_code in [200, 401, 403]:
                    print(
                        f"   ✅ {descripcion}: Respondiendo ({response.status_code})"
                    )
                else:
                    print(f"   ⚠️ {descripcion}: Estado {response.status_code}")
                    servidor_ok = False
            except:
                print(f"   ❌ {descripcion}: No responde")
                servidor_ok = False

        if servidor_ok:
            print("   🎉 Django Backend: FUNCIONANDO CORRECTAMENTE")
        else:
            print("   ⚠️ Django Backend: ALGUNOS PROBLEMAS DETECTADOS")

        return servidor_ok

    except Exception as e:
        print(f"   ❌ Error verificando Django: {e}")
        return False


def verificar_frontend():
    """Verifica el estado del frontend"""
    print("\n⚛️ FRONTEND (React/Vite)")
    print("-" * 30)

    puertos_frontend = [3000, 5173, 4173]
    frontend_ok = False

    for puerto in puertos_frontend:
        try:
            response = requests.get(f"http://localhost:{puerto}/", timeout=3)
            if response.status_code == 200:
                print(f"   ✅ Frontend corriendo en puerto {puerto}")
                frontend_ok = True
                break
        except:
            continue

    if not frontend_ok:
        print("   ❌ Frontend no está corriendo en ningún puerto estándar")
        print("   💡 Ejecuta: npm run dev (desde directorio frontend)")

    return frontend_ok


def verificar_base_datos():
    """Verifica conexión a base de datos"""
    print("\n🗄️ BASE DE DATOS")
    print("-" * 30)

    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
        import django

        django.setup()

        from django.db import connection
        from empresas.models import Empresa
        from envios.models import Envio

        # Probar conexión
        connection.ensure_connection()
        print("   ✅ Conexión a base de datos: OK")

        # Verificar datos
        empresas = Empresa.objects.count()
        envios = Envio.objects.count()

        print(f"   📊 Empresas: {empresas}")
        print(f"   📦 Envíos: {envios}")

        if empresas > 0 and envios > 0:
            print("   🎉 Base de datos: POBLADA Y FUNCIONANDO")
            return True
        else:
            print("   ⚠️ Base de datos: SIN DATOS SUFICIENTES")
            return False

    except Exception as e:
        print(f"   ❌ Error en base de datos: {e}")
        return False


def verificar_docker():
    """Verifica si Docker está disponible"""
    print("\n🐳 DOCKER")
    print("-" * 30)

    try:
        result = subprocess.run(
            ["docker", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ {version}")

            # Verificar contenedores corriendo
            result = subprocess.run(
                ["docker", "ps"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                containers = len(lines) - 1 if len(lines) > 1 else 0
                print(f"   📊 Contenedores activos: {containers}")

            return True
        else:
            print("   ❌ Docker no está funcionando")
            return False

    except Exception as e:
        print(f"   ❌ Docker no disponible: {e}")
        return False


def mostrar_resumen(django_ok, frontend_ok, db_ok, docker_ok):
    """Muestra resumen final"""
    print("\n" + "=" * 50)
    print("📊 RESUMEN DEL ESTADO DEL SISTEMA")
    print("=" * 50)

    servicios = [
        ("Django Backend", django_ok),
        ("Frontend React/Vite", frontend_ok),
        ("Base de Datos", db_ok),
        ("Docker", docker_ok),
    ]

    for servicio, estado in servicios:
        status = "✅ FUNCIONANDO" if estado else "❌ PROBLEMA"
        print(f"   {servicio}: {status}")

    total_ok = sum([django_ok, db_ok])  # Docker y frontend son opcionales

    if total_ok >= 2:
        print(f"\n🎉 SISTEMA OPERATIVO AL {(total_ok/2)*100:.0f}%")
        print("   ✅ Listo para desarrollo y pruebas")
    else:
        print(f"\n⚠️ SISTEMA REQUIERE ATENCIÓN")
        print("   🔧 Algunos servicios necesitan reiniciarse")

    print(f"\n💡 PRÓXIMOS PASOS:")
    if not frontend_ok:
        print("   • Iniciar frontend: cd frontend && npm run dev")
    if not django_ok:
        print("   • Reiniciar Django: python manage.py runserver")
    if not db_ok:
        print("   • Verificar base de datos y migraciones")


def main():
    print("🔍 VERIFICACIÓN COMPLETA DEL ESTADO DE APLICACIONES")
    print("=" * 60)

    # Verificar cada componente
    django_ok = verificar_servidor_django()
    frontend_ok = verificar_frontend()
    db_ok = verificar_base_datos()
    docker_ok = verificar_docker()

    # Mostrar resumen
    mostrar_resumen(django_ok, frontend_ok, db_ok, docker_ok)


if __name__ == "__main__":
    main()
