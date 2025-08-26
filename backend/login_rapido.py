#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT DE LOGIN RÁPIDO - SISTEMA MULTITENANCY
Herramienta para probar cualquier credencial fácilmente
"""
import json
import urllib.error
import urllib.request


def test_single_login(email, password, tenant_slug):
    """Probar un login específico y mostrar resultado detallado"""
    print(f"\n🔐 PROBANDO LOGIN")
    print(f"=" * 30)
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")
    print(f"🏷️  Tenant: {tenant_slug}")
    print(f"🌐 URL: http://localhost:8000/api/auth/login/")

    try:
        # Preparar request
        url = "http://localhost:8000/api/auth/login/"
        data = json.dumps({"email": email, "password": password}).encode("utf-8")
        headers = {"Content-Type": "application/json", "X-Tenant-Slug": tenant_slug}

        print(f"\n📤 Enviando request...")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode("utf-8"))

            print(f"\n✅ LOGIN EXITOSO!")
            print(f"📊 Status Code: {response.getcode()}")
            print(f"👤 Usuario ID: {response_data['user']['id']}")
            print(f"📧 Email confirmado: {response_data['user']['email']}")
            print(f"🏢 Empresa: {response_data['user']['empresa_actual']['nombre']}")
            print(f"🔑 Rol: {response_data['user']['rol']}")
            print(f"👑 Superuser: {response_data['user']['is_superuser']}")
            print(
                f"🎫 Access Token: {'✅ Generado' if response_data.get('access') else '❌ No generado'}"
            )
            print(
                f"🔄 Refresh Token: {'✅ Generado' if response_data.get('refresh') else '❌ No generado'}"
            )

            return True, response_data

    except urllib.error.HTTPError as e:
        error_data = e.read().decode("utf-8")
        print(f"\n❌ LOGIN FALLÓ!")
        print(f"📊 Status Code: {e.code}")
        print(f"📝 Error: {e.reason}")
        print(f"📄 Detalles: {error_data[:200]}...")
        return False, None

    except Exception as e:
        print(f"\n❌ ERROR DE CONEXIÓN!")
        print(f"📝 Error: {e}")
        print(f"💡 Verificar que el servidor esté corriendo")
        return False, None


def show_credentials_menu():
    """Mostrar menú de credenciales disponibles"""
    print(f"\n📋 CREDENCIALES DISPONIBLES:")
    print(f"=" * 40)

    credenciales = [
        (
            "1",
            "admin@cubaexpress.com",
            "admin123",
            "cuba-express",
            "Cuba Express Cargo",
        ),
        (
            "2",
            "admin@habanapremium.com",
            "admin123",
            "habana-premium",
            "Habana Premium Logistics",
        ),
        (
            "3",
            "admin@miamishipping.com",
            "admin123",
            "miami-shipping",
            "Miami Shipping Express",
        ),
        ("4", "admin@packfy.com", "admin123", "packfy-express", "Packfy Express"),
        (
            "5",
            "superadmin@packfy.com",
            "[password existente]",
            "packfy-express",
            "Superadmin Global",
        ),
    ]

    for num, email, password, tenant, empresa in credenciales:
        print(f"{num}. {empresa}")
        print(f"   📧 {email}")
        print(f"   🔑 {password}")
        print(f"   🏷️  {tenant}")
        print()

    return credenciales


def main():
    print(f"🔐 SCRIPT DE LOGIN RÁPIDO - SISTEMA MULTITENANCY")
    print(f"=" * 55)

    # Verificar conectividad
    try:
        urllib.request.urlopen("http://localhost:8000/", timeout=5)
        print(f"✅ Servidor Django conectado")
    except:
        print(f"❌ Error: Servidor Django no responde")
        print(f"💡 Ejecutar: python manage.py runserver")
        return

    # Mostrar menú
    credenciales = show_credentials_menu()

    print(f"🎯 OPCIONES:")
    print(f"1-5: Probar credencial específica")
    print(f"all: Probar todas las credenciales")
    print(f"custom: Ingresar credenciales personalizadas")
    print(f"exit: Salir")

    while True:
        opcion = input(f"\n🎮 Selecciona opción: ").strip().lower()

        if opcion == "exit":
            print(f"👋 ¡Hasta luego!")
            break

        elif opcion == "all":
            print(f"\n🚀 PROBANDO TODAS LAS CREDENCIALES")
            exitosos = 0
            for _, email, password, tenant, empresa in credenciales[
                :-1
            ]:  # Excluir superadmin
                if password != "[password existente]":
                    success, _ = test_single_login(email, password, tenant)
                    if success:
                        exitosos += 1
            print(f"\n📊 Resultado: {exitosos}/4 logins exitosos")

        elif opcion == "custom":
            print(f"\n📝 CREDENCIALES PERSONALIZADAS:")
            email = input(f"📧 Email: ")
            password = input(f"🔑 Password: ")
            tenant = input(f"🏷️  Tenant Slug: ")
            test_single_login(email, password, tenant)

        elif opcion in ["1", "2", "3", "4"]:
            idx = int(opcion) - 1
            _, email, password, tenant, empresa = credenciales[idx]
            if password == "[password existente]":
                print(f"⚠️  Este usuario requiere password existente")
                password = input(f"🔑 Ingresa password para {email}: ")
            test_single_login(email, password, tenant)

        elif opcion == "5":
            print(f"⚠️  Superadmin requiere password existente")
            password = input(f"🔑 Ingresa password para superadmin@packfy.com: ")
            test_single_login("superadmin@packfy.com", password, "packfy-express")

        else:
            print(f"❌ Opción no válida")


if __name__ == "__main__":
    main()
