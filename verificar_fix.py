import requests

print("🧪 VERIFICANDO REPARACIÓN...")

# Probar superadmin
response = requests.post(
    "http://localhost:8000/api/auth/login/",
    json={"email": "superadmin@packfy.com", "password": "super123!"},
    timeout=10,
)

if response.status_code == 200:
    token_data = response.json()

    # Probar endpoint me
    me_response = requests.get(
        "http://localhost:8000/api/usuarios/me/",
        headers={"Authorization": f'Bearer {token_data["access"]}'},
        timeout=10,
    )

    if me_response.status_code == 200:
        user_data = me_response.json()
        print(f'✅ Superadmin: {user_data.get("email")}')
        print(f'   Staff: {user_data.get("is_staff")}')
        print(f'   Superuser: {user_data.get("is_superuser")}')
        print(f'   Perfiles: {len(user_data.get("perfiles_usuario", []))}')

# Probar dueño
print("\n🧪 Probando dueño...")
response = requests.post(
    "http://localhost:8000/api/auth/login/",
    json={"email": "dueno@packfy.com", "password": "dueno123!"},
    timeout=10,
)

if response.status_code == 200:
    token_data = response.json()

    me_response = requests.get(
        "http://localhost:8000/api/usuarios/me/",
        headers={"Authorization": f'Bearer {token_data["access"]}'},
        timeout=10,
    )

    if me_response.status_code == 200:
        user_data = me_response.json()
        print(f'✅ Dueño: {user_data.get("email")}')
        print(f'   Perfiles: {len(user_data.get("perfiles_usuario", []))}')
        for perfil in user_data.get("perfiles_usuario", []):
            empresa_nombre = perfil.get("empresa", {}).get(
                "nombre", "Sin nombre"
            )
            rol = perfil.get("rol", "Sin rol")
            print(f"   - {empresa_nombre} ({rol})")

print("\n🎯 RESULTADO:")
print("Si ves Staff=True y Superuser=True para superadmin, ¡FUNCIONÓ!")
print("Si ves al menos 1 perfil para dueño, ¡TAMBIÉN FUNCIONÓ!")
