#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de análisis profundo del sistema multitenancy
"""

import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.apps import apps
from django.contrib.auth.models import User
from django.db import connection


def main():
    print("=== ANÁLISIS PROFUNDO DEL SISTEMA ===")
    print()

    # 1. Verificar modelos registrados
    print("📊 MODELOS REGISTRADOS:")
    for app_config in apps.get_app_configs():
        if app_config.name in ["usuarios", "empresas", "envios"]:
            print(f"  📁 {app_config.name}:")
            for model in app_config.get_models():
                print(f"    📄 {model.__name__}")
    print()

    # 2. Verificar tablas en BD
    print("🗄️ TABLAS EN BASE DE DATOS:")
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        )
        tables = cursor.fetchall()
        for table in tables:
            print(f"  📋 {table[0]}")
    print()

    # 3. Verificar usuarios
    print(f"👥 USUARIOS REGISTRADOS: {User.objects.count()}")
    for user in User.objects.all()[:5]:
        print(f"  👤 {user.username} - {user.email} (admin: {user.is_superuser})")
    print()

    # 4. Verificar empresas
    try:
        from empresas.models import Empresa, PerfilUsuario

        print(f"🏢 EMPRESAS REGISTRADAS: {Empresa.objects.count()}")
        for empresa in Empresa.objects.all()[:5]:
            print(f"  🏢 {empresa.nombre} (slug: {empresa.slug})")

        print(f"👔 PERFILES DE USUARIO: {PerfilUsuario.objects.count()}")
        for perfil in PerfilUsuario.objects.all()[:5]:
            print(
                f"  👔 {perfil.usuario.username} - {perfil.rol} en {perfil.empresa.nombre}"
            )
    except Exception as e:
        print(f"❌ Error con empresas: {e}")
    print()

    # 5. Verificar envíos
    try:
        from envios.models import Envio

        print(f"📦 ENVÍOS REGISTRADOS: {Envio.objects.count()}")
        for envio in Envio.objects.all()[:3]:
            print(f"  📦 {envio.numero_tracking} - {envio.estado}")
    except Exception as e:
        print(f"❌ Error con envíos: {e}")
    print()

    # 6. Verificar middleware
    from django.conf import settings

    print("⚙️ MIDDLEWARE CONFIGURADO:")
    for middleware in settings.MIDDLEWARE:
        if "tenant" in middleware.lower() or "empresa" in middleware.lower():
            print(f"  🎯 {middleware}")
        else:
            print(f"  ⚪ {middleware}")
    print()

    # 7. Verificar aplicaciones instaladas
    print("🔧 APLICACIONES INSTALADAS:")
    for app in settings.INSTALLED_APPS:
        if app in ["usuarios", "empresas", "envios"]:
            print(f"  🎯 {app}")
        elif app.startswith("django."):
            print(f"  🔵 {app}")
        else:
            print(f"  🟢 {app}")
    print()

    # 8. Verificar URLs
    try:
        from django.urls import get_resolver

        urlconf = get_resolver()
        print("🌐 CONFIGURACIÓN DE URLS:")
        print(f"  📍 URL root: {urlconf.url_patterns}")
    except Exception as e:
        print(f"❌ Error con URLs: {e}")
    print()

    print("✅ Análisis completado")


if __name__ == "__main__":
    main()
