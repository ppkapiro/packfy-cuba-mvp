#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 LIMPIEZA DEFINITIVA Y ARREGLO FINAL

1. Eliminar usuarios viejos/innecesarios
2. Arreglar permisos correctamente
3. Verificar que solo queden los usuarios necesarios
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario

print("🧹 LIMPIEZA DEFINITIVA Y ARREGLO FINAL")
print("=" * 60)

# 1. ELIMINAR USUARIOS VIEJOS QUE NO NECESITAMOS
usuarios_a_eliminar = [
    "admin@packfy.cu",  # Admin viejo
    "cliente@test.cu",  # Demo data
    "empresa@test.cu",  # Demo data
]

print("🗑️ ELIMINANDO USUARIOS INNECESARIOS...")
for email in usuarios_a_eliminar:
    try:
        usuario = Usuario.objects.get(email=email)
        print(
            f"❌ Eliminando: {email} ({usuario.first_name} {usuario.last_name})"
        )
        usuario.delete()
    except Usuario.DoesNotExist:
        print(f"ℹ️ No encontrado (ya eliminado): {email}")

# 2. VERIFICAR USUARIOS QUE DEBEN QUEDAR
usuarios_correctos = [
    "superadmin@packfy.com",
    "dueno@packfy.com",
    "miami@packfy.com",
    "cuba@packfy.com",
    "remitente1@packfy.com",
    "remitente2@packfy.com",
    "remitente3@packfy.com",
    "destinatario1@cuba.cu",
    "destinatario2@cuba.cu",
    "destinatario3@cuba.cu",
]

print(f"\n✅ VERIFICANDO USUARIOS CORRECTOS...")
usuarios_existentes = []

for email in usuarios_correctos:
    try:
        usuario = Usuario.objects.get(email=email)
        usuarios_existentes.append(usuario)
        print(
            f"✅ Encontrado: {email} ({usuario.first_name} {usuario.last_name})"
        )
    except Usuario.DoesNotExist:
        print(f"❌ FALTA: {email}")

# 3. ARREGLAR PERMISOS ESPECÍFICOS
print(f"\n🔧 ARREGLANDO PERMISOS...")

# Superadmin - debe tener TODOS los permisos
try:
    superadmin = Usuario.objects.get(email="superadmin@packfy.com")
    superadmin.is_staff = True
    superadmin.is_superuser = True
    superadmin.es_administrador_empresa = True  # ¡IMPORTANTE!
    superadmin.save()
    print(
        f"👑 Superadmin configurado: staff={superadmin.is_staff}, super={superadmin.is_superuser}, admin_empresa={superadmin.es_administrador_empresa}"
    )
except Usuario.DoesNotExist:
    print("❌ Superadmin no encontrado")

# Dueño - debe ser administrador de empresa
try:
    dueno = Usuario.objects.get(email="dueno@packfy.com")
    dueno.es_administrador_empresa = True
    dueno.save()
    print(
        f"👔 Dueño configurado: admin_empresa={dueno.es_administrador_empresa}"
    )
except Usuario.DoesNotExist:
    print("❌ Dueño no encontrado")

# Operadores Miami y Cuba - pueden ser administradores
try:
    miami = Usuario.objects.get(email="miami@packfy.com")
    miami.es_administrador_empresa = True
    miami.save()
    print(
        f"🌴 Miami configurado: admin_empresa={miami.es_administrador_empresa}"
    )
except Usuario.DoesNotExist:
    print("❌ Miami no encontrado")

try:
    cuba = Usuario.objects.get(email="cuba@packfy.com")
    cuba.es_administrador_empresa = True
    cuba.save()
    print(f"🏝️ Cuba configurado: admin_empresa={cuba.es_administrador_empresa}")
except Usuario.DoesNotExist:
    print("❌ Cuba no encontrado")

# 4. VERIFICAR QUE NO HAYA USUARIOS EXTRAS
print(f"\n🔍 VERIFICANDO QUE NO HAYA USUARIOS EXTRAS...")
todos_los_usuarios = Usuario.objects.all()

for usuario in todos_los_usuarios:
    if usuario.email not in usuarios_correctos:
        print(
            f"⚠️ USUARIO EXTRA ENCONTRADO: {usuario.email} ({usuario.first_name} {usuario.last_name})"
        )
        print(f"   ¿Eliminar este usuario? (Revisa manualmente)")

# 5. RESUMEN FINAL
print(f"\n📊 ESTADO FINAL:")
print(f"   Total usuarios: {Usuario.objects.count()}")
print(f"   Total empresas: {Empresa.objects.count()}")
print(f"   Total perfiles: {PerfilUsuario.objects.count()}")

print(f"\n👥 USUARIOS FINALES:")
for usuario in Usuario.objects.all().order_by("email"):
    perfiles = PerfilUsuario.objects.filter(usuario=usuario).count()
    print(f"   📧 {usuario.email}")
    print(f"      👤 {usuario.first_name} {usuario.last_name}")
    print(
        f"      🔧 Staff: {usuario.is_staff} | Super: {usuario.is_superuser} | Admin Empresa: {usuario.es_administrador_empresa}"
    )
    print(f"      📋 Perfiles: {perfiles}")
    print()

print("🎉 ¡LIMPIEZA COMPLETADA!")
print("Ahora verifica en el panel de administración que todo esté correcto.")
