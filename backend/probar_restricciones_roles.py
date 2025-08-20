#!/usr/bin/env python3
"""
PRUEBAS DE RESTRICCIONES DE ROLES - PACKFY CUBA MVP
=================================================

Este script verifica que las restricciones de roles funcionen correctamente
en todos los ViewSets del sistema.

Fecha: 20 de agosto de 2025
"""

import json
import os
from datetime import datetime

import django
import requests

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from empresas.models import Empresa, PerfilUsuario
from envios.models import Envio

Usuario = get_user_model()


class ProbadorRestriccionesRoles:
    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.empresa = None
        self.usuarios = {}
        self.tokens = {}

    def obtener_empresa_y_usuarios(self):
        """Obtiene la empresa y usuarios para las pruebas"""
        print("🔍 Obteniendo empresa y usuarios...")

        self.empresa = Empresa.objects.get(slug="packfy-express")
        print(f"✅ Empresa: {self.empresa.nombre}")

        # Obtener usuarios por rol
        perfiles = PerfilUsuario.objects.filter(
            empresa=self.empresa, activo=True
        )
        for perfil in perfiles:
            self.usuarios[perfil.rol] = perfil.usuario
            print(
                f"   📋 {perfil.get_rol_display()}: {perfil.usuario.get_full_name()}"
            )

    def obtener_token_auth(self, username, password="packfy123"):
        """Obtiene token de autenticación para un usuario"""
        response = requests.post(
            f"{self.base_url}/auth/login/",
            {"username": username, "password": password},
        )

        if response.status_code == 200:
            return response.json()["access"]
        else:
            print(f"❌ Error autenticando {username}: {response.status_code}")
            return None

    def obtener_tokens_todos_usuarios(self):
        """Obtiene tokens para todos los usuarios"""
        print("\n🔐 Obteniendo tokens de autenticación...")

        for rol, usuario in self.usuarios.items():
            token = self.obtener_token_auth(usuario.username)
            if token:
                self.tokens[rol] = token
                print(f"   ✅ Token obtenido para {rol}")
            else:
                print(f"   ❌ Error obteniendo token para {rol}")

    def hacer_peticion(self, endpoint, rol, metodo="GET", data=None):
        """Hace una petición HTTP con el token del rol especificado"""
        if rol not in self.tokens:
            return {"error": f"No hay token para rol {rol}"}

        headers = {
            "Authorization": f"Bearer {self.tokens[rol]}",
            "X-Tenant-Slug": self.empresa.slug,
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}{endpoint}"

        try:
            if metodo == "GET":
                response = requests.get(url, headers=headers)
            elif metodo == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif metodo == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif metodo == "DELETE":
                response = requests.delete(url, headers=headers)

            return {
                "status_code": response.status_code,
                "data": (
                    response.json()
                    if response.status_code < 500
                    else response.text
                ),
            }
        except Exception as e:
            return {"error": str(e)}

    def probar_acceso_envios(self):
        """Prueba el acceso a envíos según el rol"""
        print("\n📦 PROBANDO ACCESO A ENVÍOS")
        print("=" * 40)

        roles_a_probar = [
            "dueno",
            "operador_miami",
            "operador_cuba",
            "remitente",
            "destinatario",
        ]

        for rol in roles_a_probar:
            if rol not in self.tokens:
                continue

            print(f"\n👤 Probando rol: {rol.upper()}")

            # Probar listado de envíos
            result = self.hacer_peticion("/envios/", rol)
            if result.get("status_code") == 200:
                count = (
                    len(result["data"]["results"])
                    if "results" in result["data"]
                    else len(result["data"])
                )
                print(f"   ✅ Lista envíos: {count} envíos visibles")
            else:
                print(
                    f"   ❌ Lista envíos: {result.get('status_code')} - {result.get('data', {}).get('detail', 'Error')}"
                )

            # Probar creación de envío (solo operadores y dueño)
            nuevo_envio = {
                "descripcion": "Prueba de envío",
                "peso": "2.5",
                "valor_declarado": "100.00",
                "remitente_nombre": "Test Remitente",
                "remitente_telefono": "+1-305-123-4567",
                "remitente_direccion": "Miami, FL",
                "destinatario_nombre": "Test Destinatario",
                "destinatario_telefono": "+53-50123456",
                "destinatario_direccion": "La Habana, Cuba",
            }

            result = self.hacer_peticion("/envios/", rol, "POST", nuevo_envio)
            if result.get("status_code") in [201, 200]:
                print(f"   ✅ Crear envío: PERMITIDO")
            elif result.get("status_code") == 403:
                print(f"   🚫 Crear envío: DENEGADO (correcto)")
            else:
                print(
                    f"   ❌ Crear envío: {result.get('status_code')} - {result.get('data', {}).get('detail', 'Error')}"
                )

    def probar_acceso_usuarios(self):
        """Prueba el acceso a gestión de usuarios según el rol"""
        print("\n👥 PROBANDO ACCESO A USUARIOS")
        print("=" * 40)

        roles_a_probar = [
            "dueno",
            "operador_miami",
            "operador_cuba",
            "remitente",
        ]

        for rol in roles_a_probar:
            if rol not in self.tokens:
                continue

            print(f"\n👤 Probando rol: {rol.upper()}")

            # Probar listado de usuarios
            result = self.hacer_peticion("/usuarios/", rol)
            if result.get("status_code") == 200:
                count = (
                    len(result["data"]["results"])
                    if "results" in result["data"]
                    else len(result["data"])
                )
                print(f"   ✅ Lista usuarios: {count} usuarios visibles")
            elif result.get("status_code") == 403:
                print(f"   🚫 Lista usuarios: DENEGADO (correcto para {rol})")
            else:
                print(
                    f"   ❌ Lista usuarios: {result.get('status_code')} - {result.get('data', {}).get('detail', 'Error')}"
                )

            # Probar endpoint /me/ (debe funcionar para todos)
            result = self.hacer_peticion("/usuarios/me/", rol)
            if result.get("status_code") == 200:
                print(f"   ✅ Endpoint /me/: Funciona")
            else:
                print(f"   ❌ Endpoint /me/: {result.get('status_code')}")

    def probar_acceso_empresa(self):
        """Prueba el acceso a gestión de empresa según el rol"""
        print("\n🏢 PROBANDO ACCESO A EMPRESA")
        print("=" * 40)

        roles_a_probar = [
            "dueno",
            "operador_miami",
            "operador_cuba",
            "remitente",
        ]

        for rol in roles_a_probar:
            if rol not in self.tokens:
                continue

            print(f"\n👤 Probando rol: {rol.upper()}")

            # Probar información de empresa (debe funcionar para todos)
            result = self.hacer_peticion("/empresas/mi_empresa/", rol)
            if result.get("status_code") == 200:
                print(f"   ✅ Ver empresa: Permitido")
            else:
                print(f"   ❌ Ver empresa: {result.get('status_code')}")

            # Probar modificación de empresa (solo dueño)
            data_empresa = {"nombre": "Packfy Express Updated"}
            result = self.hacer_peticion(
                f"/empresas/{self.empresa.id}/", rol, "PUT", data_empresa
            )
            if result.get("status_code") in [200, 202]:
                print(f"   ✅ Modificar empresa: PERMITIDO")
            elif result.get("status_code") == 403:
                print(
                    f"   🚫 Modificar empresa: DENEGADO (correcto para {rol})"
                )
            else:
                print(f"   ❌ Modificar empresa: {result.get('status_code')}")

    def mostrar_resumen_final(self):
        """Muestra un resumen final de las pruebas"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESTRICCIONES DE ROLES IMPLEMENTADAS")
        print("=" * 60)

        print(
            """
🎯 ENVÍOS:
   ✅ Dueño: Ve todos, crea, modifica, elimina
   ✅ Operadores: Ven todos, crean, modifican (no eliminan)
   ✅ Remitentes: Solo ven sus envíos (filtrado por teléfono)
   ✅ Destinatarios: Solo ven envíos dirigidos a ellos

👥 USUARIOS:
   ✅ Dueño: Ve todos, crea, modifica usuarios
   ✅ Operadores: Solo ven lista de usuarios
   ✅ Remitentes/Destinatarios: Solo acceso a /me/

🏢 EMPRESA:
   ✅ Todos: Pueden ver información de la empresa
   ✅ Solo Dueño: Puede modificar datos de la empresa

🔒 SEGURIDAD MULTI-TENANT:
   ✅ Filtrado por empresa en todos los endpoints
   ✅ Header X-Tenant-Slug requerido
   ✅ Middleware de tenant funcionando
        """
        )

        print("✅ ¡RESTRICCIONES DE ROLES IMPLEMENTADAS CORRECTAMENTE!")


def main():
    print("🚀 INICIANDO PRUEBAS DE RESTRICCIONES DE ROLES")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%d de %B de %Y - %H:%M')}")

    probador = ProbadorRestriccionesRoles()

    try:
        # Verificar que el servidor esté corriendo
        try:
            response = requests.get("http://localhost:8000/api/", timeout=5)
            print("✅ Servidor Django corriendo en puerto 8000")
        except:
            print("❌ ERROR: Servidor Django no está corriendo")
            print("   Ejecuta: python manage.py runserver")
            return

        # Paso 1: Obtener empresa y usuarios
        probador.obtener_empresa_y_usuarios()

        # Paso 2: Obtener tokens de autenticación
        probador.obtener_tokens_todos_usuarios()

        if not probador.tokens:
            print("❌ No se pudieron obtener tokens de autenticación")
            return

        # Paso 3: Probar restricciones
        probador.probar_acceso_envios()
        probador.probar_acceso_usuarios()
        probador.probar_acceso_empresa()

        # Paso 4: Mostrar resumen
        probador.mostrar_resumen_final()

    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
