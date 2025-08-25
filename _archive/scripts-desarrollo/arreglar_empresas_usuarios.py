#!/usr/bin/env python3
"""
🔧 ARREGLAR ASIGNACIÓN DE EMPRESAS A USUARIOS
=============================================
Script para asignar la empresa 'Packfy Demo' al usuario admin.
"""

import json
import os
import subprocess
import sys


def ejecutar_comando_docker(comando):
    """Ejecutar comando en el contenedor Docker del backend"""
    try:
        # Comando completo para ejecutar en Docker
        cmd_completo = f'docker exec -it packfy-backend python manage.py shell -c "{comando}"'

        print(f"🔧 Ejecutando: {comando}")

        # Ejecutar comando
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-backend",
                "python",
                "manage.py",
                "shell",
                "-c",
                comando,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print(f"✅ Éxito: {result.stdout.strip()}")
            return result.stdout.strip()
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return None

    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return None


def verificar_estado_actual():
    """Verificar el estado actual de usuarios y empresas"""
    print("🔍 VERIFICANDO ESTADO ACTUAL")
    print("=" * 35)
    print()

    # Verificar empresas existentes
    comando_empresas = """
from empresas.models import Empresa
empresas = Empresa.objects.all()
print(f'Empresas disponibles: {len(empresas)}')
for emp in empresas:
    print(f'  - {emp.nombre} (slug: {emp.slug})')
"""
    ejecutar_comando_docker(comando_empresas)
    print()

    # Verificar usuarios
    comando_usuarios = """
from usuarios.models import Usuario
from empresas.models import Empresa
usuarios = Usuario.objects.all()
print(f'Usuarios existentes: {len(usuarios)}')
for user in usuarios:
    empresas_count = user.empresas.count()
    print(f'  - {user.email} (empresas: {empresas_count})')
    for emp in user.empresas.all():
        print(f'    * {emp.nombre}')
"""
    ejecutar_comando_docker(comando_usuarios)


def arreglar_asignaciones():
    """Asignar la empresa Packfy Demo a todos los usuarios"""
    print("\n🔧 ARREGLANDO ASIGNACIONES")
    print("=" * 30)
    print()

    # Asignar empresa a usuarios
    comando_asignar = """
from usuarios.models import Usuario
from empresas.models import Empresa

try:
    # Obtener la empresa demo
    empresa_demo = Empresa.objects.get(slug='packfy-demo')
    print(f'✅ Empresa encontrada: {empresa_demo.nombre}')

    # Obtener todos los usuarios
    usuarios = Usuario.objects.all()
    print(f'📋 Usuarios a procesar: {len(usuarios)}')

    for usuario in usuarios:
        # Asignar empresa si no la tiene
        if not usuario.empresas.filter(slug='packfy-demo').exists():
            usuario.empresas.add(empresa_demo)
            print(f'✅ Asignado {empresa_demo.nombre} a {usuario.email}')
        else:
            print(f'ℹ️ {usuario.email} ya tiene asignada {empresa_demo.nombre}')

    print('🎉 Asignaciones completadas')

except Empresa.DoesNotExist:
    print('❌ Empresa packfy-demo no encontrada')
except Exception as e:
    print(f'❌ Error: {e}')
"""
    ejecutar_comando_docker(comando_asignar)


def verificar_resultado():
    """Verificar que las asignaciones funcionaron"""
    print("\n✅ VERIFICANDO RESULTADO")
    print("=" * 25)
    print()

    comando_verificar = """
from usuarios.models import Usuario
print('Estado final de usuarios:')
for user in Usuario.objects.all():
    empresas_list = [emp.nombre for emp in user.empresas.all()]
    print(f'  {user.email}: {empresas_list}')
"""
    ejecutar_comando_docker(comando_verificar)


def main():
    print("🔧 ARREGLAR ASIGNACIÓN DE EMPRESAS A USUARIOS")
    print("=" * 50)
    print()

    # Verificar estado actual
    verificar_estado_actual()

    # Arreglar asignaciones
    arreglar_asignaciones()

    # Verificar resultado
    verificar_resultado()

    print("\n🎉 PROCESO COMPLETADO")
    print("Ahora los usuarios deberían tener acceso a la empresa Packfy Demo")


if __name__ == "__main__":
    main()
