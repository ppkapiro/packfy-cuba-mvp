import json

import requests

print("🧪 PROBANDO SISTEMA LIMPIO...")
print("=" * 40)

try:
    # Probar login del superadmin
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json={"email": "superadmin@packfy.com", "password": "super123!"},
        timeout=10,
    )

    if response.status_code == 200:
        print("✅ Login del superadmin: EXITOSO")
        token_data = response.json()

        # Probar endpoint me
        me_response = requests.get(
            "http://localhost:8000/api/usuarios/me/",
            headers={"Authorization": f'Bearer {token_data["access"]}'},
            timeout=10,
        )

        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f'👤 Usuario: {user_data.get("email")}')
            print(
                f'📛 Nombre: {user_data.get("first_name")} {user_data.get("last_name")}'
            )
            print(f'👑 Superuser: {user_data.get("is_superuser")}')
            print(f'🔧 Staff: {user_data.get("is_staff")}')
            print("\n🎉 ¡SISTEMA FUNCIONANDO CORRECTAMENTE!")
            print("\n📋 CREDENCIALES CONFIRMADAS:")
            print("   📧 Email: superadmin@packfy.com")
            print("   🔐 Password: super123!")
            print("\n🌐 URLs:")
            print("   • Frontend: http://localhost:5173")
            print("   • Backend: http://localhost:8000")
        else:
            print(f"❌ Error en /me/: {me_response.status_code}")
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(f"Respuesta: {response.text}")

except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("🔍 Verificar que los contenedores estén corriendo")
