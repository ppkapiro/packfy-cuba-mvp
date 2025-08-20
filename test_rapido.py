import requests

usuarios = [
    ("superadmin@packfy.com", "super123!", "SUPERADMIN"),
    ("dueno@packfy.com", "dueno123!", "DUEÑO"),
    ("miami@packfy.com", "miami123!", "MIAMI"),
    ("cuba@packfy.com", "cuba123!", "CUBA"),
    ("remitente1@packfy.com", "remitente123!", "REMITENTE1"),
]

print("🧪 PRUEBA RÁPIDA DE USUARIOS")
print("=" * 40)

for email, password, nombre in usuarios:
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"email": email, "password": password},
            timeout=5,
        )

        if response.status_code == 200:
            token_data = response.json()

            me_response = requests.get(
                "http://localhost:8000/api/usuarios/me/",
                headers={"Authorization": f'Bearer {token_data["access"]}'},
                timeout=5,
            )

            if me_response.status_code == 200:
                user_data = me_response.json()
                perfiles = len(user_data.get("perfiles_usuario", []))
                is_staff = user_data.get("is_staff", False)
                is_super = user_data.get("is_superuser", False)

                status = (
                    "🎉 COMPLETO"
                    if (perfiles > 0 or is_super)
                    else "⚠️ SIN PERFILES"
                )

                print(
                    f"{status} {nombre}: Perfiles={perfiles}, Staff={is_staff}, Super={is_super}"
                )

                # Mostrar perfiles si los tiene
                for perfil in user_data.get("perfiles_usuario", [])[
                    :1
                ]:  # Solo el primero
                    empresa = perfil.get("empresa", {}).get("nombre", "")
                    rol = perfil.get("rol", "")
                    print(f"         -> {empresa} ({rol})")
            else:
                print(
                    f"❌ {nombre}: Error en /me/ - {me_response.status_code}"
                )
        else:
            print(f"❌ {nombre}: Error login - {response.status_code}")

    except Exception as e:
        print(f"❌ {nombre}: Error - {str(e)[:30]}...")

print(f"\n🎯 VERIFICA:")
print(f"✅ SUPERADMIN debe tener Staff=True, Super=True")
print(f"✅ DUEÑO debe tener Perfiles=1 con Packfy Express")
print(f"✅ Otros deben tener Perfiles=1 con sus roles correspondientes")
