#!/usr/bin/env python
"""
🚀 VALIDACIÓN FINAL - CREDENCIALES FRONTEND
Verificar que las credenciales actualizadas en LoginPage.tsx funcionan
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import authenticate
from empresas.models import Empresa


def main():
    print("🚀 VALIDACIÓN FINAL - CREDENCIALES FRONTEND")
    print("=" * 60)

    # Credenciales que están ahora en LoginPage.tsx
    credenciales_frontend = [
        {
            "email": "admin@packfy.com",
            "password": "admin123",
            "tipo": "👑 Superadmin",
            "descripcion": "Acceso total al sistema",
        },
        {
            "email": "dueno@packfy.com",
            "password": "password123",
            "tipo": "🏢 Dueño Principal",
            "descripcion": "Solo Packfy Express",
        },
        {
            "email": "consultor@packfy.com",
            "password": "password123",
            "tipo": "🌐 Multi-empresa",
            "descripcion": "Acceso a las 4 empresas",
        },
        {
            "email": "demo@packfy.com",
            "password": "demo123",
            "tipo": "🧪 Demo",
            "descripcion": "Usuario demostración",
        },
        {
            "email": "miami@packfy.com",
            "password": "password123",
            "tipo": "🚚 Operador Miami",
            "descripcion": "Operaciones específicas",
        },
        {
            "email": "cuba@packfy.com",
            "password": "password123",
            "tipo": "🇨🇺 Operador Cuba",
            "descripcion": "Operaciones específicas",
        },
    ]

    print("🔑 VERIFICANDO CREDENCIALES DEL FRONTEND:")
    print("-" * 60)

    total_credenciales = len(credenciales_frontend)
    credenciales_validas = 0

    for cred in credenciales_frontend:
        usuario = authenticate(username=cred["email"], password=cred["password"])

        if usuario:
            estado = "✅ VÁLIDA"
            credenciales_validas += 1
        else:
            estado = "❌ FALLA"

        print(f"{estado} {cred['tipo']}")
        print(f"      📧 {cred['email']}")
        print(f"      🔑 {cred['password']}")
        print(f"      📝 {cred['descripcion']}")
        print()

    # Calcular porcentaje
    porcentaje = credenciales_validas / total_credenciales * 100

    print("📊 RESULTADOS:")
    print(f"   ✅ Credenciales válidas: {credenciales_validas}/{total_credenciales}")
    print(f"   📈 Tasa de éxito: {porcentaje:.1f}%")

    # Verificar empresas
    print("\n🏢 EMPRESAS DISPONIBLES:")
    print("-" * 60)

    empresas = Empresa.objects.filter(activo=True).order_by("slug")
    for empresa in empresas:
        print(f"   • {empresa.nombre} ({empresa.slug})")
        print(f"     🌐 URL: http://{empresa.slug}.localhost:5173/login")

    print("\n🎯 CONCLUSIÓN:")
    print("-" * 60)

    if porcentaje >= 90:
        print("   ✅ FRONTEND LISTO PARA PRUEBAS")
        print("   🚀 Todas las credenciales funcionan correctamente")
        print("   🔗 LoginPage.tsx actualizado con credenciales válidas")
        print("\n   📋 PRÓXIMO PASO:")
        print("      1. Iniciar el frontend: cd frontend-multitenant && npm start")
        print("      2. Probar login en: http://packfy-express.localhost:5173/login")
        print("      3. Usar cualquiera de las credenciales validadas arriba")
    else:
        print("   ⚠️ Algunas credenciales requieren ajustes")
        print("   🔧 Revisar passwords que fallan")

    print("=" * 60)


if __name__ == "__main__":
    main()
