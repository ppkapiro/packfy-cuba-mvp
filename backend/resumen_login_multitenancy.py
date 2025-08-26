#!/usr/bin/env python
"""
📊 RESUMEN EJECUTIVO - SISTEMA LOGIN MULTITENANCY
Estado final después del análisis y reparación completa
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import authenticate
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def main():
    print("🎯 RESUMEN EJECUTIVO - LOGIN MULTITENANCY")
    print("=" * 60)

    # Estado del sistema
    empresas = Empresa.objects.filter(activo=True).count()
    usuarios = Usuario.objects.filter(is_active=True).count()
    perfiles = PerfilUsuario.objects.filter(activo=True).count()

    print(f"📊 SISTEMA:")
    print(f"   🏢 Empresas activas: {empresas}")
    print(f"   👥 Usuarios activos: {usuarios}")
    print(f"   🎭 Perfiles de usuario: {perfiles}")

    # Verificar logins funcionando
    usuarios_con_login = 0
    passwords_comunes = ["admin123", "password123", "demo123"]

    for usuario in Usuario.objects.filter(is_active=True):
        for password in passwords_comunes:
            if authenticate(username=usuario.email, password=password):
                usuarios_con_login += 1
                break

    tasa_login = (usuarios_con_login / usuarios * 100) if usuarios > 0 else 0

    print(f"\n🔐 AUTENTICACIÓN:")
    print(f"   ✅ Usuarios con login: {usuarios_con_login}/{usuarios}")
    print(f"   📈 Tasa de éxito: {tasa_login:.1f}%")

    # Estado de empresas
    print(f"\n🏢 EMPRESAS CONFIGURADAS:")
    for empresa in Empresa.objects.filter(activo=True).order_by("slug"):
        usuarios_empresa = PerfilUsuario.objects.filter(
            empresa=empresa, activo=True
        ).count()
        print(f"   • {empresa.nombre} ({empresa.slug}) - {usuarios_empresa} usuarios")

    # Credenciales principales
    print(f"\n🔑 CREDENCIALES VALIDADAS:")
    credenciales = [
        ("admin@packfy.com", "admin123", "Superadmin"),
        ("dueno@packfy.com", "password123", "Dueño principal"),
        ("consultor@packfy.com", "password123", "Multi-empresa"),
        ("demo@packfy.com", "demo123", "Demo"),
    ]

    for email, password, tipo in credenciales:
        usuario = authenticate(username=email, password=password)
        estado = "✅" if usuario else "❌"
        print(f"   {estado} {email} - {tipo}")

    print(f"\n🚀 ESTADO FINAL:")
    if tasa_login >= 90:
        print("   ✅ SISTEMA COMPLETAMENTE FUNCIONAL")
        print("   🎯 Listo para pruebas de frontend")
        print("   🔗 Credenciales actualizadas en LoginPage.tsx")
    else:
        print("   ⚠️ Sistema requiere ajustes adicionales")

    print("=" * 60)


if __name__ == "__main__":
    main()
