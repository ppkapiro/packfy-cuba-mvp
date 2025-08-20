#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 ARREGLAR USUARIOS Y AUTENTICACIÓN

Este script repara los problemas de autenticación y usuarios en el sistema.
"""

import json
import os
import subprocess
from datetime import datetime

import django


def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")


def execute_django_command(command):
    """Ejecutar comando Django en el container"""
    try:
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-backend",
                "python",
                "manage.py",
                "shell",
                "-c",
                command,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def check_users():
    """Verificar usuarios existentes"""
    log("🔍 Verificando usuarios existentes...")

    command = """
from django.contrib.auth.models import User
from usuarios.models import Usuario
from empresas.models import Empresa, PerfilUsuario

# Verificar usuarios Django
django_users = User.objects.all()
print(f"Usuarios Django: {django_users.count()}")
for u in django_users:
    print(f"  - {u.username} ({u.email}) - Activo: {u.is_active}")

# Verificar usuarios custom
custom_users = Usuario.objects.all()
print(f"Usuarios Custom: {custom_users.count()}")
for u in custom_users:
    print(f"  - {u.email} - Activo: {u.is_active}")

# Verificar perfiles
perfiles = PerfilUsuario.objects.all()
print(f"Perfiles de Usuario: {perfiles.count()}")
for p in perfiles:
    print(f"  - {p.usuario.email if hasattr(p, 'usuario') else 'No usuario'} - Empresa: {p.empresa.nombre if p.empresa else 'Sin empresa'}")

# Verificar empresas
empresas = Empresa.objects.all()
print(f"Empresas: {empresas.count()}")
for e in empresas:
    print(f"  - {e.nombre} ({e.slug}) - Activa: {e.activo}")
"""

    success, output = execute_django_command(command)
    if success:
        log("✅ Verificación de usuarios completada:")
        print(output)
    else:
        log(f"❌ Error verificando usuarios: {output}")

    return success


def create_admin_user():
    """Crear usuario administrador"""
    log("🔧 Creando usuario administrador...")

    command = """
from django.contrib.auth.models import User
from usuarios.models import Usuario
from empresas.models import Empresa, PerfilUsuario
from django.contrib.auth.hashers import make_password

# Crear o obtener empresa por defecto
empresa, created = Empresa.objects.get_or_create(
    slug='miami-shipping',
    defaults={
        'nombre': 'Miami Shipping Co',
        'activo': True
    }
)
print(f"Empresa: {empresa.nombre} {'(creada)' if created else '(existente)'}")

# Crear usuario custom
usuario, created = Usuario.objects.get_or_create(
    email='admin@packfy.com',
    defaults={
        'first_name': 'Administrador',
        'last_name': 'Sistema',
        'telefono': '+1234567890',
        'is_active': True,
        'is_staff': True,
        'is_superuser': True,
        'username': 'admin@packfy.com'
    }
)

if created or not usuario.check_password('admin123!'):
    usuario.set_password('admin123!')
    usuario.save()
    print(f"Usuario: {usuario.email} {'(creado)' if created else '(actualizado)'}")

# Crear perfil de usuario
perfil, created = PerfilUsuario.objects.get_or_create(
    usuario=usuario,
    empresa=empresa,
    defaults={
        'rol': 'dueno',
        'activo': True
    }
)

print(f"Perfil: {perfil.usuario.email} en {perfil.empresa.nombre} {'(creado)' if created else '(actualizado)'}")

# Verificar que el usuario puede autenticarse
from django.contrib.auth import authenticate
auth_user = authenticate(email='admin@packfy.com', password='admin123!')
print(f"Autenticación: {'✅ Exitosa' if auth_user else '❌ Falló'}")
"""

    success, output = execute_django_command(command)
    if success:
        log("✅ Usuario administrador configurado:")
        print(output)
    else:
        log(f"❌ Error creando usuario administrador: {output}")

    return success


def test_authentication():
    """Probar autenticación API"""
    log("🔍 Probando autenticación API...")

    import requests

    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"email": "admin@packfy.com", "password": "admin123!"},
            timeout=10,
        )

        if response.status_code == 200:
            token_data = response.json()
            log("✅ Login API funcionando correctamente")

            # Probar endpoint /usuarios/me/
            me_response = requests.get(
                "http://localhost:8000/api/usuarios/me/",
                headers={"Authorization": f"Bearer {token_data['access']}"},
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
                else:
                    log("❌ Campo empresas ausente en respuesta")

                return True
            else:
                log(
                    f"❌ /usuarios/me/ falló - Status: {me_response.status_code}"
                )
                log(f"Response: {me_response.text}")
        else:
            log(f"❌ Login API falló - Status: {response.status_code}")
            log(f"Response: {response.text}")

    except Exception as e:
        log(f"❌ Error probando autenticación: {e}")

    return False


def run_migrations():
    """Ejecutar migraciones pendientes"""
    log("🔄 Ejecutando migraciones...")

    try:
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-backend",
                "python",
                "manage.py",
                "migrate",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        log("✅ Migraciones ejecutadas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        log(f"❌ Error ejecutando migraciones: {e.stderr}")
        return False


def main():
    """Función principal de reparación"""
    log("🚀 Iniciando reparación de usuarios y autenticación...")

    # Paso 1: Ejecutar migraciones
    if not run_migrations():
        log("❌ No se pudieron ejecutar las migraciones")
        return False

    # Paso 2: Verificar estado actual
    check_users()

    # Paso 3: Crear/reparar usuario admin
    if not create_admin_user():
        log("❌ No se pudo crear el usuario administrador")
        return False

    # Paso 4: Probar autenticación
    if test_authentication():
        log("🎉 ¡Autenticación reparada exitosamente!")
        log("📋 Credenciales de acceso:")
        log("  Email: admin@packfy.com")
        log("  Password: admin123!")
        log("  Empresa: Miami Shipping Co")
        return True
    else:
        log("❌ La autenticación sigue fallando")
        return False


if __name__ == "__main__":
    main()
