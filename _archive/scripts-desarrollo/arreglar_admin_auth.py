#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 ARREGLAR AUTENTICACIÓN ADMIN PANEL

Vamos a asegurar que todos los usuarios puedan autenticarse en el admin panel.
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import authenticate
from usuarios.models import Usuario

print("🔧 ARREGLANDO AUTENTICACIÓN ADMIN PANEL")
print("=" * 60)

# Lista de usuarios a arreglar
usuarios_arreglar = [
    ("superadmin@packfy.com", "super123!"),
    ("dueno@packfy.com", "dueno123!"),
]

for email, password in usuarios_arreglar:
    print(f"\n🔧 Arreglando: {email}")

    try:
        usuario = Usuario.objects.get(email=email)

        # 1. Asegurar que username == email
        if usuario.username != email:
            print(
                f"   📝 Cambiando username de '{usuario.username}' a '{email}'"
            )
            usuario.username = email

        # 2. Resetear password para asegurar que esté bien hasheado
        print(f"   🔐 Reseteando password...")
        usuario.set_password(password)

        # 3. Asegurar permisos para admin panel
        if email == "superadmin@packfy.com":
            usuario.is_staff = True
            usuario.is_superuser = True
            usuario.es_administrador_empresa = True
            print(f"   👑 Permisos superadmin configurados")
        elif email == "dueno@packfy.com":
            usuario.is_staff = (
                True  # ¡IMPORTANTE! Necesita is_staff para admin panel
            )
            usuario.es_administrador_empresa = True
            print(f"   👔 Permisos dueño configurados")

        usuario.save()
        print(f"   ✅ Usuario guardado")

        # 4. Probar autenticación
        print(f"   🧪 Probando autenticación...")
        auth_user = authenticate(username=email, password=password)
        if auth_user:
            print(f"   ✅ Autenticación exitosa")
        else:
            print(f"   ❌ Autenticación falló")

            # Probar con username
            auth_user_by_username = authenticate(
                username=usuario.username, password=password
            )
            if auth_user_by_username:
                print(f"   ✅ Autenticación por username exitosa")
            else:
                print(f"   ❌ Autenticación por username también falló")

        # 5. Verificar password manual
        if usuario.check_password(password):
            print(f"   ✅ Password verificado manualmente")
        else:
            print(f"   ❌ Password no verifica manualmente")

    except Usuario.DoesNotExist:
        print(f"   ❌ Usuario no encontrado: {email}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n📊 RESUMEN FINAL:")
print(f"Usuarios que DEBERÍAN poder entrar al admin panel:")

for email, _ in usuarios_arreglar:
    try:
        usuario = Usuario.objects.get(email=email)
        puede_admin = usuario.is_staff or usuario.is_superuser

        print(f"\n👤 {email}:")
        print(f"   📧 Email: {usuario.email}")
        print(f"   👤 Username: {usuario.username}")
        print(f"   🔧 is_staff: {usuario.is_staff}")
        print(f"   👑 is_superuser: {usuario.is_superuser}")
        print(f"   🏢 es_admin_empresa: {usuario.es_administrador_empresa}")
        print(f"   ✅ is_active: {usuario.is_active}")
        print(f"   🎛️ Puede acceder admin: {'✅' if puede_admin else '❌'}")

    except Usuario.DoesNotExist:
        print(f"❌ {email}: No encontrado")

print(f"\n🎯 PARA PROBAR:")
print(f"1. Ve a: http://localhost:8000/admin/")
print(f"2. Usa: superadmin@packfy.com / super123!")
print(f"3. O usa: dueno@packfy.com / dueno123!")
print(f"4. Ambos deberían funcionar ahora")

print(f"\n⚠️ NOTA IMPORTANTE:")
print(f"Para el admin panel de Django, el usuario DEBE tener is_staff=True")
print(f"Es diferente a la API que solo necesita estar autenticado.")
