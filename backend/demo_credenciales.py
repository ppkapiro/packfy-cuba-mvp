#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DEMO DE CREDENCIALES - SISTEMA MULTITENANCY
Demostración de todas las credenciales disponibles
"""
import json
import urllib.request


def demo_credenciales():
    print("🔐 DEMO DE CREDENCIALES - SISTEMA MULTITENANCY")
    print("=" * 55)

    credenciales = [
        ("Cuba Express Cargo", "admin@cubaexpress.com", "admin123", "cuba-express"),
        (
            "Habana Premium Logistics",
            "admin@habanapremium.com",
            "admin123",
            "habana-premium",
        ),
        (
            "Miami Shipping Express",
            "admin@miamishipping.com",
            "admin123",
            "miami-shipping",
        ),
        ("Packfy Express", "admin@packfy.com", "admin123", "packfy-express"),
    ]

    print("\n📋 CREDENCIALES PARA LOGIN:")
    print("-" * 40)

    exitosos = 0
    total = len(credenciales)

    for empresa, email, password, tenant in credenciales:
        print(f"\n🏢 {empresa}")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Password: {password}")
        print(f"   🏷️  Tenant: {tenant}")
        print(f"   🌐 Endpoint: http://localhost:8000/api/auth/login/")

        try:
            url = "http://localhost:8000/api/auth/login/"
            data = json.dumps({"email": email, "password": password}).encode("utf-8")
            headers = {"Content-Type": "application/json", "X-Tenant-Slug": tenant}
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")

            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode("utf-8"))
                print(f"   ✅ LOGIN EXITOSO")
                print(f"   👤 Usuario ID: {response_data['user']['id']}")
                print(f"   🔑 Rol: {response_data['user']['rol']}")
                exitosos += 1
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}...")

    print(f"\n🎯 RESUMEN:")
    print(f"✅ Exitosos: {exitosos}/{total}")
    print(f"📊 Tasa éxito: {(exitosos/total)*100:.0f}%")

    print(f"\n👑 SUPERADMIN:")
    print(f"📧 Email: superadmin@packfy.com")
    print(f"🔑 Password: [usar password existente del superusuario]")
    print(f"🏷️  Tenant: packfy-express (o cualquier otro)")
    print(f"🌐 Acceso: TODAS las empresas")

    print(f"\n🎯 CÓMO USAR ESTAS CREDENCIALES:")
    print(f"1. 🖥️  Backend: Usar con script Python o curl")
    print(f"2. 🌐 Frontend: Usar en http://localhost:8080/test_login_frontend.html")
    print(f"3. 📱 React App: Usar en frontend-multitenant")
    print(f"4. 🧪 Testing: Usar con login_rapido.py (interactivo)")


if __name__ == "__main__":
    demo_credenciales()
