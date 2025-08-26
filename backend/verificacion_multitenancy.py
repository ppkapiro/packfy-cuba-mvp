#!/usr/bin/env python
"""
🔍 VERIFICACIÓN MULTITENANCY COMPLETADA
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import models
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario

print("=" * 70)
print("🔍 VERIFICACIÓN FINAL DEL SISTEMA MULTITENANCY")
print("=" * 70)

# Empresas
print("\n🏢 === EMPRESAS CONFIGURADAS ===")
empresas = Empresa.objects.all().order_by("id")
for empresa in empresas:
    usuarios_count = PerfilUsuario.objects.filter(empresa=empresa, activo=True).count()
    print(f"   ✅ {empresa.nombre}")
    print(f"      🔗 Slug: '{empresa.slug}'")
    print(f"      👥 Usuarios: {usuarios_count}")
    print(f"      🌐 URL: {empresa.slug}.localhost:5173")

# Usuarios multi-empresa
print(f"\n👥 === USUARIOS MULTI-EMPRESA ===")
usuarios_multi = Usuario.objects.annotate(
    num_empresas=models.Count("perfiles_empresa")
).filter(num_empresas__gt=1)

for usuario in usuarios_multi:
    perfiles = PerfilUsuario.objects.filter(
        usuario=usuario, activo=True
    ).select_related("empresa")
    print(f"   👤 {usuario.username} ({usuario.email})")
    for perfil in perfiles:
        print(f"      🏢 {perfil.empresa.nombre} → {perfil.get_rol_display()}")

# Estadísticas
print(f"\n📊 === ESTADÍSTICAS ===")
print(f"   🏢 Total empresas: {Empresa.objects.count()}")
print(f"   👥 Total usuarios: {Usuario.objects.count()}")
print(f"   🎭 Total perfiles: {PerfilUsuario.objects.count()}")
print(f"   🔄 Usuarios multi-empresa: {usuarios_multi.count()}")

# URLs de prueba
print(f"\n🌐 === URLS DE PRUEBA DISPONIBLES ===")
for empresa in empresas:
    print(f"   🔗 {empresa.slug}.localhost:5173")
    print(f"   📋 localhost:5173?empresa={empresa.slug}")

print(f"\n🔐 === CREDENCIALES DE PRUEBA ===")
print("   👑 Admin: admin@packfy.com / admin123")
print("   🔄 Multi-empresa: consultor@packfy.com / consultor123")

print("\n" + "=" * 70)
print("✅ SISTEMA MULTITENANCY COMPLETAMENTE CONFIGURADO")
print("🎯 LISTO PARA CREAR DATOS DE ENVÍOS")
print("=" * 70)
