#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO ADMIN PANEL DJANGO

Vamos a verificar exactamente qué está pasando con la autenticación del admin panel.
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import authenticate
from usuarios.models import Usuario

print("🔍 DIAGNÓSTICO ADMIN PANEL DJANGO")
print("=" * 60)

# Lista de usuarios a probar
usuarios_test = [
    ("superadmin@packfy.com", "super123!", "SUPERADMIN"),
    ("dueno@packfy.com", "dueno123!", "DUEÑO"),
]

print("🧪 PROBANDO AUTENTICACIÓN DJANGO...")

for email, password, nombre in usuarios_test:
    print(f"\n👤 Probando {nombre} ({email}):")

    try:
        # 1. Verificar que el usuario existe
        usuario = Usuario.objects.get(email=email)
        print(f"   ✅ Usuario encontrado: {usuario.email}")
        print(f"   📧 Email: {usuario.email}")
        print(f"   👤 Username: {usuario.username}")
        print(f"   🔧 is_staff: {usuario.is_staff}")
        print(f"   👑 is_superuser: {usuario.is_superuser}")
        print(
            f"   🏢 es_administrador_empresa: {usuario.es_administrador_empresa}"
        )
        print(f"   ✅ is_active: {usuario.is_active}")

        # 2. Probar autenticación Django
        print(f"   🔐 Probando authenticate()...")
        auth_user = authenticate(username=email, password=password)
        if auth_user:
            print(f"   ✅ authenticate() exitoso")
            print(f"   👤 Usuario autenticado: {auth_user.email}")
        else:
            print(f"   ❌ authenticate() falló")

            # Intentar con username en lugar de email
            auth_user_username = authenticate(
                username=usuario.username, password=password
            )
            if auth_user_username:
                print(f"   ✅ authenticate() con username exitoso")
            else:
                print(f"   ❌ authenticate() con username también falló")

        # 3. Verificar password manually
        print(f"   🔐 Verificando password manual...")
        if usuario.check_password(password):
            print(f"   ✅ Password correcto")
        else:
            print(f"   ❌ Password incorrecto")
            # Intentar resetear password
            print(f"   🔧 Reseteando password...")
            usuario.set_password(password)
            usuario.save()
            print(f"   ✅ Password reseteado")

            # Verificar de nuevo
            if usuario.check_password(password):
                print(f"   ✅ Password ahora funciona")
            else:
                print(f"   ❌ Password aún no funciona")

    except Usuario.DoesNotExist:
        print(f"   ❌ Usuario no encontrado: {email}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# 4. Verificar configuración de autenticación
print(f"\n⚙️ VERIFICANDO CONFIGURACIÓN DE AUTENTICACIÓN:")

try:
    from django.conf import settings

    # Verificar AUTHENTICATION_BACKENDS
    auth_backends = getattr(settings, "AUTHENTICATION_BACKENDS", [])
    print(f"   📋 AUTHENTICATION_BACKENDS:")
    for backend in auth_backends:
        print(f"      - {backend}")

    # Verificar AUTH_USER_MODEL
    auth_user_model = getattr(settings, "AUTH_USER_MODEL", None)
    print(f"   👤 AUTH_USER_MODEL: {auth_user_model}")

    # Verificar LOGIN_URL
    login_url = getattr(settings, "LOGIN_URL", None)
    print(f"   🔗 LOGIN_URL: {login_url}")

except Exception as e:
    print(f"   ❌ Error verificando configuración: {e}")

print(f"\n🔧 RESUMEN:")
print(f"Si authenticate() falla pero check_password() funciona,")
print(f"entonces hay un problema con los AUTHENTICATION_BACKENDS.")
print(f"Si ambos fallan, entonces hay un problema con las passwords.")
