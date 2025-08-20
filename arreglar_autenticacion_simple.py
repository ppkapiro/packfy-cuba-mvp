#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 ARREGLAR AUTENTICACIÓN - VERSIÓN SIMPLE

Este script arregla directamente los usuarios usando comandos Django simples.
"""

import subprocess
from datetime import datetime

import requests


def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")


def run_django_command(commands):
    """Ejecutar comando Django en el container"""
    log(f"Ejecutando: {commands[:50]}...")

    try:
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-backend",
                "python",
                "manage.py",
                "shell",
            ],
            input=commands,
            text=True,
            capture_output=True,
            check=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def main():
    """Función principal simplificada"""
    log("🚀 Arreglando autenticación de forma simple...")

    # Comandos Django para crear usuario administrador
    django_commands = """
# Importar modelos necesarios
from usuarios.models import Usuario
from empresas.models import Empresa, PerfilUsuario

# 1. Crear empresa por defecto
print("1. Creando empresa...")
empresa, created = Empresa.objects.get_or_create(
    slug='miami-shipping',
    defaults={
        'nombre': 'Miami Shipping Co',
        'activo': True
    }
)
print(f"Empresa: {empresa.nombre} {'(creada)' if created else '(existente)'}")

# 2. Crear o actualizar usuario administrador
print("2. Creando usuario admin...")
try:
    usuario = Usuario.objects.get(email='admin@packfy.com')
    print("Usuario existente encontrado, actualizando...")
except Usuario.DoesNotExist:
    usuario = Usuario(email='admin@packfy.com')
    print("Creando nuevo usuario...")

# Configurar datos del usuario
usuario.username = 'admin@packfy.com'
usuario.first_name = 'Administrador'
usuario.last_name = 'Sistema'
usuario.telefono = '+1234567890'
usuario.is_active = True
usuario.is_staff = True
usuario.is_superuser = True
usuario.set_password('admin123!')
usuario.save()
print(f"Usuario guardado: {usuario.email}")

# 3. Crear perfil de usuario
print("3. Creando perfil...")
perfil, created = PerfilUsuario.objects.get_or_create(
    usuario=usuario,
    empresa=empresa,
    defaults={
        'rol': 'dueno',
        'activo': True
    }
)
print(f"Perfil: {perfil.usuario.email} - {perfil.get_rol_display()} en {perfil.empresa.nombre}")

# 4. Verificar autenticación
print("4. Verificando autenticación...")
from django.contrib.auth import authenticate
auth_user = authenticate(username='admin@packfy.com', password='admin123!')
if not auth_user:
    # Intentar con email
    auth_user = authenticate(email='admin@packfy.com', password='admin123!')

print(f"Autenticación: {'✅ Exitosa' if auth_user else '❌ Falló'}")

print("\\n✅ Configuración completada!")
print("📋 Credenciales:")
print("  Email: admin@packfy.com")
print("  Password: admin123!")
print("  Empresa: Miami Shipping Co")
"""

    success, output = run_django_command(django_commands)
    if success:
        log("✅ Configuración de usuario completada:")
        print(output)

        # Probar autenticación API
        log("🔍 Probando autenticación API...")
        try:
            response = requests.post(
                "http://localhost:8000/api/auth/login/",
                json={"email": "admin@packfy.com", "password": "admin123!"},
                timeout=10,
            )

            if response.status_code == 200:
                token_data = response.json()
                log("🎉 ¡AUTENTICACIÓN API FUNCIONANDO!")

                # Probar endpoint /usuarios/me/
                me_response = requests.get(
                    "http://localhost:8000/api/usuarios/me/",
                    headers={
                        "Authorization": f"Bearer {token_data['access']}"
                    },
                    timeout=10,
                )

                if me_response.status_code == 200:
                    user_data = me_response.json()
                    log(
                        f"✅ /usuarios/me/ funcionando - Usuario: {user_data.get('email')}"
                    )

                    if "empresas" in user_data:
                        log(
                            f"✅ Campo empresas presente: {len(user_data['empresas'])} empresas"
                        )
                        log("🎉 ¡SISTEMA MULTITENANCY FUNCIONANDO!")
                        return True
                    else:
                        log("⚠️ Campo empresas ausente pero usuario funciona")

                else:
                    log(
                        f"❌ /usuarios/me/ falló - Status: {me_response.status_code}"
                    )
            else:
                log(f"❌ Login API falló - Status: {response.status_code}")
                log(f"Response: {response.text}")

        except Exception as e:
            log(f"❌ Error probando API: {e}")
    else:
        log(f"❌ Error en configuración: {output}")
        return False


if __name__ == "__main__":
    main()
