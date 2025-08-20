#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SISTEMA DE PROTECCIÓN DE BASE DE DATOS
Protege contra cambios accidentales o no autorizados
"""

import datetime
import hashlib
import os
from typing import Optional


class ProtectorBaseDatos:
    """
    Sistema de protección que requiere autorización para cambios en BD
    """

    def __init__(self):
        self.archivo_proteccion = "BD_PROTECTION_STATUS.lock"
        self.clave_autorizacion = "PACKFY_DB_PROTECTION_2025"
        self.intentos_maximos = 3

    def esta_protegida(self) -> bool:
        """Verifica si la BD está protegida"""
        return os.path.exists(self.archivo_proteccion)

    def activar_proteccion(self) -> None:
        """Activa la protección de la base de datos"""
        timestamp = datetime.datetime.now().isoformat()
        contenido = f"""# 🛡️ BASE DE DATOS PROTEGIDA
# Creado: {timestamp}
#
# Esta base de datos está protegida contra cambios no autorizados.
# Para realizar cambios, debe usar el ProtectorBaseDatos.
#
# USUARIOS ACTUALES: 10 usuarios exactos según restaurar_estructura_20250820_095645.py
# ESTADO: PRODUCCIÓN ESTABLE
#
# ⚠️ NO ELIMINAR ESTE ARCHIVO SIN AUTORIZACIÓN
PROTECTION_ACTIVE=true
CREATED_AT={timestamp}
USUARIOS_ESPERADOS=10
"""
        with open(self.archivo_proteccion, "w", encoding="utf-8") as f:
            f.write(contenido)
        print("🛡️ Protección de base de datos ACTIVADA")

    def solicitar_autorizacion(self, operacion: str) -> bool:
        """
        Solicita autorización para realizar una operación
        """
        print(f"\n⚠️  OPERACIÓN DETECTADA: {operacion}")
        print("🛡️ La base de datos está PROTEGIDA")
        print(f"📊 Estado actual: {self.obtener_estado_bd()}")

        intentos = 0
        while intentos < self.intentos_maximos:
            try:
                print(
                    f"\n🔐 Autorización requerida (intento {intentos + 1}/{self.intentos_maximos})"
                )
                respuesta = (
                    input("¿Autoriza esta operación? (si/no): ")
                    .strip()
                    .lower()
                )

                if respuesta in ["si", "sí", "s", "yes", "y"]:
                    clave = input("Ingrese la clave de autorización: ").strip()
                    if self.validar_clave(clave):
                        self.registrar_operacion_autorizada(operacion)
                        print("✅ Operación AUTORIZADA")
                        return True
                    else:
                        print("❌ Clave incorrecta")
                        intentos += 1
                elif respuesta in ["no", "n"]:
                    print("🚫 Operación CANCELADA por el usuario")
                    return False
                else:
                    print("❓ Respuesta no válida. Use 'si' o 'no'")
                    intentos += 1

            except KeyboardInterrupt:
                print("\n🚫 Operación CANCELADA")
                return False

        print("❌ Máximo de intentos alcanzado. Operación DENEGADA")
        return False

    def validar_clave(self, clave: str) -> bool:
        """Valida la clave de autorización"""
        return clave == self.clave_autorizacion

    def obtener_estado_bd(self) -> str:
        """Obtiene el estado actual de la BD"""
        try:
            import django

            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
            django.setup()

            from empresas.models import Empresa, PerfilUsuario
            from usuarios.models import Usuario

            usuarios = Usuario.objects.count()
            empresas = Empresa.objects.count()
            perfiles = PerfilUsuario.objects.count()

            return f"Usuarios: {usuarios}, Empresas: {empresas}, Perfiles: {perfiles}"
        except:
            return "No disponible"

    def registrar_operacion_autorizada(self, operacion: str) -> None:
        """Registra una operación autorizada"""
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"\n# {timestamp} - OPERACIÓN AUTORIZADA: {operacion}"

        with open(self.archivo_proteccion, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def desactivar_proteccion(self) -> bool:
        """Desactiva la protección (requiere autorización)"""
        if self.solicitar_autorizacion("DESACTIVAR PROTECCIÓN DE BD"):
            if os.path.exists(self.archivo_proteccion):
                os.remove(self.archivo_proteccion)
            print("🔓 Protección de base de datos DESACTIVADA")
            return True
        return False


# Función decoradora para proteger operaciones
def requiere_autorizacion(operacion_nombre: str):
    """
    Decorador que requiere autorización antes de ejecutar una función
    """

    def decorador(func):
        def wrapper(*args, **kwargs):
            protector = ProtectorBaseDatos()
            if protector.esta_protegida():
                if not protector.solicitar_autorizacion(operacion_nombre):
                    print(f"🚫 Operación '{operacion_nombre}' CANCELADA")
                    return None
            return func(*args, **kwargs)

        return wrapper

    return decorador


# Función de utilidad para activar protección
def activar_proteccion_bd():
    """Activa la protección de la base de datos"""
    protector = ProtectorBaseDatos()
    protector.activar_proteccion()


# Función de utilidad para verificar estado
def verificar_proteccion():
    """Verifica el estado de protección"""
    protector = ProtectorBaseDatos()
    if protector.esta_protegida():
        print("🛡️ Base de datos PROTEGIDA")
        print(f"📊 Estado: {protector.obtener_estado_bd()}")
    else:
        print("⚠️  Base de datos NO PROTEGIDA")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        protector = ProtectorBaseDatos()

        if comando == "activar":
            protector.activar_proteccion()
        elif comando == "desactivar":
            protector.desactivar_proteccion()
        elif comando == "estado":
            verificar_proteccion()
        else:
            print("Comandos disponibles: activar, desactivar, estado")
    else:
        print("🛡️ PROTECTOR DE BASE DE DATOS")
        print("Uso: python protector_bd.py [activar|desactivar|estado]")
        verificar_proteccion()
