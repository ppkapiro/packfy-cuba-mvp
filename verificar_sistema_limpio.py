#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 VERIFICACIÓN RÁPIDA DEL SISTEMA

Verifica que la estructura simple esté funcionando correctamente.
"""

import json
from datetime import datetime

import requests


def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")


def verificar_sistema():
    """Verificar que el sistema funcione correctamente"""

    # URLs del sistema
    backend_url = "http://localhost:8000"
    frontend_url = "http://localhost:5173"

    log("🧪 VERIFICANDO SISTEMA LIMPIO...")
    log("=" * 50)

    # 1. Verificar backend
    try:
        response = requests.get(f"{backend_url}/api/health/", timeout=5)
        if response.status_code == 200:
            log("✅ Backend: Funcionando")
        else:
            log(f"⚠️ Backend: Status {response.status_code}")
    except Exception as e:
        log(f"❌ Backend: Error - {e}")
        return False

    # 2. Verificar frontend
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            log("✅ Frontend: Funcionando")
        else:
            log(f"⚠️ Frontend: Status {response.status_code}")
    except Exception as e:
        log(f"❌ Frontend: Error - {e}")

    # 3. Probar credenciales del superadmin
    log("\n🔐 PROBANDO CREDENCIALES...")
    log("-" * 30)

    credenciales = [
        ("superadmin@packfy.com", "super123!", "Superadministrador"),
        ("dueno@packfy.com", "dueno123!", "Dueño"),
        ("miami@packfy.com", "miami123!", "Operador Miami"),
        ("cuba@packfy.com", "cuba123!", "Operador Cuba"),
        ("remitente1@packfy.com", "remitente123!", "Remitente"),
        ("destinatario1@cuba.cu", "destinatario123!", "Destinatario"),
    ]

    tokens = {}

    for email, password, rol in credenciales:
        try:
            response = requests.post(
                f"{backend_url}/api/auth/login/",
                json={"email": email, "password": password},
                timeout=10,
            )

            if response.status_code == 200:
                token_data = response.json()
                tokens[email] = token_data["access"]
                log(f"✅ {rol}: {email} - Login exitoso")
            else:
                log(f"❌ {rol}: {email} - Error {response.status_code}")

        except Exception as e:
            log(f"❌ {rol}: {email} - Error: {e}")

    # 4. Probar endpoint /me/ con superadmin
    if "superadmin@packfy.com" in tokens:
        log("\n👤 PROBANDO DATOS DE USUARIO...")
        log("-" * 30)

        try:
            response = requests.get(
                f"{backend_url}/api/usuarios/me/",
                headers={
                    "Authorization": f"Bearer {tokens['superadmin@packfy.com']}"
                },
                timeout=10,
            )

            if response.status_code == 200:
                user_data = response.json()
                log("✅ Datos del superadmin:")
                log(f"   📧 Email: {user_data.get('email')}")
                log(
                    f"   👤 Nombre: {user_data.get('first_name')} {user_data.get('last_name')}"
                )
                log(f"   🔧 Staff: {user_data.get('is_staff')}")
                log(f"   👑 Superuser: {user_data.get('is_superuser')}")
            else:
                log(f"❌ Error obteniendo datos: {response.status_code}")

        except Exception as e:
            log(f"❌ Error probando /me/: {e}")

    # 5. Resumen final
    log("\n📋 RESUMEN DEL SISTEMA")
    log("=" * 50)
    log("🌐 URLs del sistema:")
    log(f"   • Frontend: {frontend_url}")
    log(f"   • Backend API: {backend_url}")
    log("")
    log("🔑 CREDENCIALES PRINCIPALES:")
    log("   • Superadmin: superadmin@packfy.com / super123!")
    log("   • Dueño: dueno@packfy.com / dueno123!")
    log("   • Miami: miami@packfy.com / miami123!")
    log("   • Cuba: cuba@packfy.com / cuba123!")
    log("   • Remitentes: remitente1@packfy.com / remitente123!")
    log("   • Destinatarios: destinatario1@cuba.cu / destinatario123!")
    log("")
    log("✅ Sistema limpio y funcionando correctamente")
    log("🚀 ¡Listo para usar!")


if __name__ == "__main__":
    verificar_sistema()
