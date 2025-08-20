#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 RESETEAR CREDENCIALES ADMIN

Script para resetear las credenciales del administrador y mostrarlas claramente.
"""

import subprocess
from datetime import datetime

import requests


def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")


def reset_admin_credentials():
    """Resetear credenciales del administrador"""
    log("🔐 Reseteando credenciales del administrador...")

    try:
        # Script Django para resetear usuario admin
        django_script = """
from usuarios.models import Usuario
from empresas.models import Empresa, PerfilUsuario

# 1. Buscar o crear empresa
empresa, created = Empresa.objects.get_or_create(
    slug="miami-shipping",
    defaults={
        "nombre": "Miami Shipping Co",
        "activo": True
    }
)
print(f"Empresa: {empresa.nombre}")

# 2. Eliminar usuario admin existente si existe
try:
    old_user = Usuario.objects.get(email="admin@packfy.com")
    old_user.delete()
    print("Usuario anterior eliminado")
except Usuario.DoesNotExist:
    print("No había usuario anterior")

# 3. Crear nuevo usuario admin
admin_user = Usuario.objects.create_user(
    email="admin@packfy.com",
    password="admin123!",
    username="admin@packfy.com",
    first_name="Administrador",
    last_name="Sistema",
    is_active=True,
    is_staff=True,
    is_superuser=True
)
print(f"Usuario creado: {admin_user.email}")

# 4. Crear perfil
perfil, created = PerfilUsuario.objects.get_or_create(
    usuario=admin_user,
    empresa=empresa,
    defaults={
        "rol": "dueno",
        "activo": True
    }
)
print(f"Perfil creado: {perfil.rol} en {perfil.empresa.nombre}")

# 5. Verificar que el password funciona
if admin_user.check_password("admin123!"):
    print("✅ Password verificado correctamente")
else:
    print("❌ Error en password")

print("\\n=== CREDENCIALES FINALES ===")
print("Email: admin@packfy.com")
print("Password: admin123!")
print("Empresa: Miami Shipping Co")
"""

        # Ejecutar en Django
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-backend",
                "python",
                "manage.py",
                "shell",
            ],
            input=django_script,
            text=True,
            capture_output=True,
            timeout=30,
        )

        if result.returncode == 0:
            log("✅ Usuario admin reseteado exitosamente:")
            print(result.stdout)
            return True
        else:
            log(f"❌ Error reseteando usuario: {result.stderr}")
            return False

    except Exception as e:
        log(f"❌ Error ejecutando script: {e}")
        return False


def test_credentials():
    """Probar las credenciales en la API"""
    log("🧪 Probando credenciales en la API...")

    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"email": "admin@packfy.com", "password": "admin123!"},
            timeout=10,
        )

        if response.status_code == 200:
            log("✅ ¡Credenciales funcionan correctamente!")
            token_data = response.json()

            # Probar /usuarios/me/
            me_response = requests.get(
                "http://localhost:8000/api/usuarios/me/",
                headers={"Authorization": f"Bearer {token_data['access']}"},
                timeout=10,
            )

            if me_response.status_code == 200:
                user_data = me_response.json()
                log(f"✅ Usuario logueado: {user_data.get('email')}")
                log(
                    f"✅ Empresas disponibles: {len(user_data.get('empresas', []))}"
                )
                return True
            else:
                log(f"❌ Error en /usuarios/me/: {me_response.status_code}")
        else:
            log(f"❌ Error en login: {response.status_code}")
            log(f"Respuesta: {response.text}")

    except Exception as e:
        log(f"❌ Error probando API: {e}")

    return False


def main():
    """Función principal"""
    log("🚀 Iniciando reseteo de credenciales...")

    if reset_admin_credentials():
        if test_credentials():
            log("\n🎉 ¡CREDENCIALES CONFIRMADAS!")
            log("=" * 40)
            log("📧 Email: admin@packfy.com")
            log("🔐 Password: admin123!")
            log("🏢 Empresa: Miami Shipping Co")
            log("🌐 URL: http://localhost:5173")
            log("=" * 40)
        else:
            log("⚠️ Credenciales creadas pero no funcionan en API")
    else:
        log("❌ No se pudieron resetear las credenciales")


if __name__ == "__main__":
    main()
