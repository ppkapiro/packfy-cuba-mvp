import requests

print("🧪 PRUEBA DE LOGIN DESPUÉS DE LIMPIEZA")
print("=" * 50)

usuarios_test = [
    ("superadmin@packfy.com", "super123!", "SUPERADMIN"),
    ("dueno@packfy.com", "dueno123!", "DUEÑO"),
    ("miami@packfy.com", "miami123!", "MIAMI"),
    ("cuba@packfy.com", "cuba123!", "CUBA"),
    ("remitente1@packfy.com", "remitente123!", "REMITENTE"),
    ("destinatario1@cuba.cu", "destinatario123!", "DESTINATARIO"),
]

resultados = []

for email, password, nombre in usuarios_test:
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"email": email, "password": password},
            timeout=10,
        )

        if response.status_code == 200:
            token_data = response.json()

            # Probar endpoint /me/
            me_response = requests.get(
                "http://localhost:8000/api/usuarios/me/",
                headers={"Authorization": f'Bearer {token_data["access"]}'},
                timeout=10,
            )

            if me_response.status_code == 200:
                user_data = me_response.json()

                login_ok = True
                staff = user_data.get("is_staff", False)
                superuser = user_data.get("is_superuser", False)
                perfiles = len(user_data.get("perfiles_usuario", []))

                # Para el panel de administración
                admin_access = staff or superuser

                print(f"✅ {nombre}: Login OK")
                print(f"   🔧 Staff: {staff} | Super: {superuser}")
                print(f"   📋 Perfiles: {perfiles}")
                print(
                    f"   🎛️ Acceso Admin Panel: {'✅' if admin_access else '❌'}"
                )

                if perfiles > 0:
                    perfil = user_data.get("perfiles_usuario", [])[0]
                    empresa = perfil.get("empresa", {}).get("nombre", "")
                    rol = perfil.get("rol", "")
                    print(f"   🏢 {empresa} ({rol})")

                resultados.append(
                    {
                        "email": email,
                        "nombre": nombre,
                        "login_ok": True,
                        "admin_access": admin_access,
                        "perfiles": perfiles,
                    }
                )

            else:
                print(
                    f"❌ {nombre}: Error en /me/ ({me_response.status_code})"
                )
                resultados.append(
                    {"email": email, "nombre": nombre, "login_ok": False}
                )
        else:
            print(f"❌ {nombre}: Error login ({response.status_code})")
            print(f"   Respuesta: {response.text}")
            resultados.append(
                {"email": email, "nombre": nombre, "login_ok": False}
            )

    except Exception as e:
        print(f"❌ {nombre}: Error de conexión - {e}")
        resultados.append(
            {"email": email, "nombre": nombre, "login_ok": False}
        )

    print()

# Resumen
print("📊 RESUMEN:")
login_exitosos = [r for r in resultados if r.get("login_ok")]
con_admin = [r for r in resultados if r.get("admin_access")]

print(f"✅ Login exitoso: {len(login_exitosos)}/{len(usuarios_test)}")
print(f"🎛️ Con acceso admin: {len(con_admin)}")

if len(login_exitosos) == len(usuarios_test):
    print("🎉 ¡TODOS LOS USUARIOS FUNCIONAN!")
else:
    print("⚠️ Algunos usuarios tienen problemas")

print(f"\n🔑 CREDENCIALES CONFIRMADAS:")
for resultado in login_exitosos:
    admin_text = " (+ Admin Panel)" if resultado.get("admin_access") else ""
    print(f"   📧 {resultado['email']} / contraseña{admin_text}")
