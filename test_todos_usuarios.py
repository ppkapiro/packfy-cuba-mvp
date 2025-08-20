#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 PRUEBA EXHAUSTIVA DE TODOS LOS USUARIOS

Verifica cada usuario individualmente:
1. Login en API
2. Endpoint /me/
3. Permisos y roles
4. Acceso a diferentes endpoints
"""

import json
from datetime import datetime

import requests


def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    icon = icons.get(level, "ℹ️")
    print(f"[{timestamp}] {icon} {message}")


def probar_usuario(email, password, nombre_rol):
    """Prueba exhaustiva de un usuario específico"""
    log(f"PROBANDO: {nombre_rol} ({email})", "INFO")
    print("-" * 60)

    resultado = {
        "email": email,
        "rol": nombre_rol,
        "login_ok": False,
        "me_ok": False,
        "datos": {},
        "perfiles": [],
        "errores": [],
    }

    try:
        # 1. PROBAR LOGIN
        login_response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"email": email, "password": password},
            timeout=10,
        )

        if login_response.status_code == 200:
            resultado["login_ok"] = True
            token_data = login_response.json()
            access_token = token_data.get("access")
            log("Login exitoso", "SUCCESS")

            # 2. PROBAR ENDPOINT /ME/
            headers = {"Authorization": f"Bearer {access_token}"}

            me_response = requests.get(
                "http://localhost:8000/api/usuarios/me/",
                headers=headers,
                timeout=10,
            )

            if me_response.status_code == 200:
                resultado["me_ok"] = True
                user_data = me_response.json()
                resultado["datos"] = user_data

                log(f"Datos obtenidos correctamente", "SUCCESS")
                log(f"  📧 Email: {user_data.get('email')}")
                log(
                    f"  👤 Nombre: {user_data.get('first_name')} {user_data.get('last_name')}"
                )
                log(f"  🔧 Staff: {user_data.get('is_staff')}")
                log(f"  👑 Superuser: {user_data.get('is_superuser')}")
                log(f"  ✅ Activo: {user_data.get('is_active')}")

                # Verificar perfiles de usuario
                perfiles = user_data.get("perfiles_usuario", [])
                resultado["perfiles"] = perfiles

                if perfiles:
                    log(f"📋 Perfiles encontrados: {len(perfiles)}")
                    for perfil in perfiles:
                        empresa = perfil.get("empresa", {})
                        rol = perfil.get("rol")
                        activo = perfil.get("activo")
                        log(
                            f"  🏢 Empresa: {empresa.get('nombre')} | Rol: {rol} | Activo: {activo}"
                        )
                else:
                    log("⚠️ No se encontraron perfiles de empresa", "WARNING")

            else:
                log(
                    f"Error en endpoint /me/: {me_response.status_code}",
                    "ERROR",
                )
                log(f"Respuesta: {me_response.text}", "ERROR")
                resultado["errores"].append(
                    f"/me/ failed: {me_response.status_code}"
                )

            # 3. PROBAR OTROS ENDPOINTS SEGÚN EL ROL
            if resultado["me_ok"]:
                log("🔍 Probando endpoints específicos...")

                # Probar endpoint de empresas
                empresas_response = requests.get(
                    "http://localhost:8000/api/empresas/",
                    headers=headers,
                    timeout=10,
                )

                if empresas_response.status_code == 200:
                    empresas_data = empresas_response.json()
                    log(f"✅ Acceso a empresas: {len(empresas_data)} empresas")
                else:
                    log(
                        f"❌ Error accediendo empresas: {empresas_response.status_code}",
                        "ERROR",
                    )

                # Probar endpoint de envíos (si aplica)
                try:
                    envios_response = requests.get(
                        "http://localhost:8000/api/envios/",
                        headers=headers,
                        timeout=10,
                    )

                    if envios_response.status_code == 200:
                        log("✅ Acceso a envíos permitido")
                    elif envios_response.status_code == 403:
                        log(
                            "⚠️ Acceso a envíos denegado (normal según rol)",
                            "WARNING",
                        )
                    else:
                        log(
                            f"❌ Error en envíos: {envios_response.status_code}",
                            "ERROR",
                        )
                except:
                    log("⚠️ Endpoint envíos no disponible", "WARNING")

        else:
            log(f"Error en login: {login_response.status_code}", "ERROR")
            log(f"Respuesta: {login_response.text}", "ERROR")
            resultado["errores"].append(
                f"Login failed: {login_response.status_code}"
            )

    except Exception as e:
        log(f"Error general: {e}", "ERROR")
        resultado["errores"].append(f"Exception: {e}")

    print("\n" + "=" * 60 + "\n")
    return resultado


def main():
    """Función principal para probar todos los usuarios"""
    log("🚀 INICIANDO PRUEBA EXHAUSTIVA DE USUARIOS", "INFO")
    log("=" * 60, "INFO")

    # Lista de usuarios a probar
    usuarios = [
        ("superadmin@packfy.com", "super123!", "SUPERADMINISTRADOR"),
        ("dueno@packfy.com", "dueno123!", "DUEÑO DE EMPRESA"),
        ("miami@packfy.com", "miami123!", "OPERADOR MIAMI"),
        ("cuba@packfy.com", "cuba123!", "OPERADOR CUBA"),
        ("remitente1@packfy.com", "remitente123!", "REMITENTE 1"),
        ("remitente2@packfy.com", "remitente123!", "REMITENTE 2"),
        ("remitente3@packfy.com", "remitente123!", "REMITENTE 3"),
        ("destinatario1@cuba.cu", "destinatario123!", "DESTINATARIO 1"),
        ("destinatario2@cuba.cu", "destinatario123!", "DESTINATARIO 2"),
        ("destinatario3@cuba.cu", "destinatario123!", "DESTINATARIO 3"),
    ]

    resultados = []

    for email, password, rol in usuarios:
        resultado = probar_usuario(email, password, rol)
        resultados.append(resultado)

    # RESUMEN FINAL
    log("📊 RESUMEN FINAL", "INFO")
    log("=" * 60, "INFO")

    exitosos = [r for r in resultados if r["login_ok"] and r["me_ok"]]
    con_problemas = [
        r for r in resultados if not (r["login_ok"] and r["me_ok"])
    ]

    log(
        f"✅ Usuarios funcionando correctamente: {len(exitosos)}/{len(resultados)}"
    )
    for r in exitosos:
        log(f"  ✅ {r['rol']}: {r['email']}")

    if con_problemas:
        log(f"❌ Usuarios con problemas: {len(con_problemas)}")
        for r in con_problemas:
            log(
                f"  ❌ {r['rol']}: {r['email']} - Errores: {', '.join(r['errores'])}"
            )

    # Información específica sobre perfiles
    log("\n🏢 ANÁLISIS DE PERFILES POR EMPRESA:", "INFO")
    for r in exitosos:
        if r["perfiles"]:
            log(f"📋 {r['rol']} ({r['email']}):")
            for perfil in r["perfiles"]:
                empresa = perfil.get("empresa", {})
                log(
                    f"  🏢 {empresa.get('nombre')} - Rol: {perfil.get('rol')} - Activo: {perfil.get('activo')}"
                )
        else:
            if r["datos"].get("is_superuser"):
                log(
                    f"👑 {r['rol']}: Superusuario (no necesita perfiles de empresa)"
                )
            else:
                log(f"⚠️ {r['rol']}: SIN PERFILES DE EMPRESA", "WARNING")


if __name__ == "__main__":
    main()
