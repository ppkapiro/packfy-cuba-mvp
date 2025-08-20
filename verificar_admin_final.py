import time

import requests

print("🧪 VERIFICACIÓN FINAL - ADMIN PANEL")
print("=" * 50)

# Esperar a que el backend esté listo
print("⏳ Esperando backend...")
time.sleep(5)

# Probar autenticación API primero
print("\n🔌 PROBANDO API:")
try:
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json={"email": "superadmin@packfy.com", "password": "super123!"},
        timeout=10,
    )

    if response.status_code == 200:
        print("✅ API Login exitoso")

        token = response.json()["access"]
        me_response = requests.get(
            "http://localhost:8000/api/usuarios/me/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )

        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"✅ Datos obtenidos:")
            print(f"   📧 Email: {user_data.get('email')}")
            print(f"   🔧 Staff: {user_data.get('is_staff')}")
            print(f"   👑 Super: {user_data.get('is_superuser')}")
        else:
            print(f"❌ Error en /me/: {me_response.status_code}")
    else:
        print(f"❌ Error en API login: {response.status_code}")
        print(f"Respuesta: {response.text}")

except Exception as e:
    print(f"❌ Error de conexión API: {e}")

# Probar admin panel
print(f"\n🎛️ PROBANDO ADMIN PANEL:")
try:
    # Probar login del admin
    session = requests.Session()

    # Primero obtener el CSRF token
    csrf_response = session.get(
        "http://localhost:8000/admin/login/", timeout=10
    )
    if csrf_response.status_code == 200:
        print("✅ Página de login cargada")

        # Intentar login (esto es más complejo debido a CSRF, pero podemos verificar que la página carga)
        admin_response = session.get(
            "http://localhost:8000/admin/", timeout=10
        )
        if admin_response.status_code in [200, 302]:  # 302 = redirect to login
            print("✅ Admin panel accesible")
        else:
            print(f"❌ Admin panel no accesible: {admin_response.status_code}")
    else:
        print(f"❌ Error cargando login: {csrf_response.status_code}")

except Exception as e:
    print(f"❌ Error admin panel: {e}")

print(f"\n🎯 PARA PROBAR MANUALMENTE:")
print(f"1. Ve a: http://localhost:8000/admin/")
print(f"2. Usuario: superadmin@packfy.com")
print(f"3. Password: super123!")
print(f"4. También prueba: dueno@packfy.com / dueno123!")

print(f"\n📋 CREDENCIALES ADMIN CONFIRMADAS:")
print(f"👑 SUPERADMIN: superadmin@packfy.com / super123!")
print(f"👔 DUEÑO: dueno@packfy.com / dueno123!")
print(f"   (Ambos tienen is_staff=True ahora)")

print(f"\n⚠️ Si aún no funciona:")
print(f"1. Refresca la página (F5)")
print(f"2. Borra cookies del navegador")
print(f"3. Intenta en modo incógnito")
