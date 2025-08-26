import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from empresas.models import Empresa

print("🔍 VERIFICACIÓN COMPLETA DE BASE DE DATOS")
print("=" * 50)

# Verificar usuarios
Usuario = get_user_model()
print(f"\n👥 USUARIOS TOTALES: {Usuario.objects.count()}")

if Usuario.objects.count() == 0:
    print("❌ NO HAY USUARIOS EN LA BASE DE DATOS")
else:
    print("\nDetalles de usuarios:")
    for usuario in Usuario.objects.all():
        grupos = ", ".join([g.name for g in usuario.groups.all()])
        estado = "✅ ACTIVO" if usuario.is_active else "❌ INACTIVO"
        tipo = ""
        if usuario.is_superuser:
            tipo = " (SUPERUSUARIO)"
        elif usuario.is_staff:
            tipo = " (STAFF)"

        print(f"  • {usuario.email} - {estado}{tipo}")
        if grupos:
            print(f"    Grupos: {grupos}")

# Verificar empresas
print(f"\n🏢 EMPRESAS TOTALES: {Empresa.objects.count()}")
if Empresa.objects.count() == 0:
    print("❌ NO HAY EMPRESAS EN LA BASE DE DATOS")
else:
    for empresa in Empresa.objects.all():
        print(f"  • {empresa.nombre} ({empresa.slug})")

# Verificar grupos
print(f"\n📋 GRUPOS TOTALES: {Group.objects.count()}")
for grupo in Group.objects.all():
    usuarios_count = grupo.user_set.count()
    print(f"  • {grupo.name} ({usuarios_count} usuarios)")

# Verificar usuario específico que está fallando
print(f"\n🔍 VERIFICACIÓN ESPECÍFICA: admin@primeexpress.com")
usuario_prime = Usuario.objects.filter(email="admin@primeexpress.com").first()
if usuario_prime:
    print(f"  ✅ Usuario encontrado:")
    print(f"    - Email: {usuario_prime.email}")
    print(f"    - Activo: {usuario_prime.is_active}")
    print(f"    - Nombre: {usuario_prime.first_name} {usuario_prime.last_name}")
    print(f"    - Grupos: {[g.name for g in usuario_prime.groups.all()]}")
    print(f"    - Último login: {usuario_prime.last_login}")
    print(f"    - Fecha creación: {usuario_prime.date_joined}")
else:
    print("  ❌ Usuario admin@primeexpress.com NO ENCONTRADO")

print(f"\n🔍 VERIFICACIÓN PASSWORD ESPECÍFICA:")
if usuario_prime:
    # Verificar si la contraseña está correctamente hasheada
    print(f"  - Password hash: {usuario_prime.password[:50]}...")
    # Probar contraseña
    from django.contrib.auth import authenticate

    auth_result = authenticate(username="admin@primeexpress.com", password="admin123")
    if auth_result:
        print("  ✅ Autenticación exitosa con admin123")
    else:
        print("  ❌ Autenticación falló con admin123")
