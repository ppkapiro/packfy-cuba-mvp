#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 APLICAR PROTECCIÓN A SCRIPTS EXISTENTES
Modifica scripts existentes para que usen el sistema de protección
"""

import os
import shutil
from datetime import datetime


def aplicar_proteccion_a_scripts():
    """
    Aplica protección a scripts existentes que pueden modificar la BD
    """

    # Scripts que necesitan protección
    scripts_a_proteger = [
        "restaurar_estructura_20250820_095645.py",
        "crear_usuarios_prueba.py",
        "configurar_usuarios_demo.py",
        "eliminar_usuarios_extra.py",
    ]

    print("🔧 APLICANDO PROTECCIÓN A SCRIPTS EXISTENTES")
    print("=" * 60)

    for script in scripts_a_proteger:
        if os.path.exists(script):
            print(f"\n🛡️ Protegiendo: {script}")
            aplicar_proteccion_individual(script)
        else:
            print(f"⚠️  No encontrado: {script}")

    print("\n✅ Protección aplicada a todos los scripts disponibles")


def aplicar_proteccion_individual(script_path: str):
    """
    Aplica protección a un script individual
    """
    # Crear backup
    backup_path = (
        f"{script_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    shutil.copy2(script_path, backup_path)
    print(f"📂 Backup creado: {backup_path}")

    # Leer contenido original
    with open(script_path, "r", encoding="utf-8") as f:
        contenido_original = f.read()

    # Preparar contenido protegido
    lineas = contenido_original.split("\n")

    # Buscar la línea de imports Django
    indice_django = None
    for i, linea in enumerate(lineas):
        if "django.setup()" in linea:
            indice_django = i
            break

    if indice_django is None:
        print(f"⚠️  No se pudo aplicar protección automática a {script_path}")
        return

    # Insertar import de protección después de django.setup()
    proteccion_import = (
        "from protector_bd import requiere_autorizacion, ProtectorBaseDatos"
    )
    lineas.insert(indice_django + 1, "")
    lineas.insert(indice_django + 2, proteccion_import)

    # Buscar funciones principales y agregar decorador
    for i, linea in enumerate(lineas):
        if linea.strip().startswith("def ") and (
            "main" in linea
            or "restaurar" in linea
            or "crear" in linea
            or "eliminar" in linea
        ):
            # Determinar el tipo de operación
            if "restaurar" in linea.lower():
                operacion = "RESTAURAR ESTRUCTURA DE BD"
            elif "crear" in linea.lower():
                operacion = "CREAR USUARIOS"
            elif "eliminar" in linea.lower():
                operacion = "ELIMINAR USUARIOS"
            else:
                operacion = "MODIFICAR BASE DE DATOS"

            # Insertar decorador
            indentacion = len(linea) - len(linea.lstrip())
            decorador = f'@requiere_autorizacion("{operacion}")'
            lineas.insert(i, " " * indentacion + decorador)
            break

    # Agregar verificación al final del archivo
    verificacion = """
# 🛡️ VERIFICACIÓN DE PROTECCIÓN
if __name__ == "__main__":
    protector = ProtectorBaseDatos()
    if not protector.esta_protegida():
        print("⚠️  ADVERTENCIA: Base de datos no protegida")
        respuesta = input("¿Activar protección antes de continuar? (si/no): ")
        if respuesta.lower() in ['si', 'sí', 's']:
            protector.activar_proteccion()
"""

    # Buscar if __name__ == "__main__": existente
    main_encontrado = False
    for i, linea in enumerate(lineas):
        if "__name__" in linea and "__main__" in linea:
            # Insertar verificación antes
            lineas.insert(i, verificacion)
            main_encontrado = True
            break

    if not main_encontrado:
        lineas.extend(verificacion.split("\n"))

    # Escribir archivo protegido
    contenido_protegido = "\n".join(lineas)

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(contenido_protegido)

    print(f"✅ Protección aplicada a {script_path}")


def crear_scripts_seguros():
    """
    Crea versiones seguras de operaciones comunes
    """
    print("\n🔒 CREANDO SCRIPTS SEGUROS...")

    # Script seguro para reset completo
    script_reset = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
🔄 RESET COMPLETO PROTEGIDO
Reinicia completamente la base de datos con protección
'''

import os
import django
from protector_bd import requiere_autorizacion

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

@requiere_autorizacion("RESET COMPLETO DE BASE DE DATOS")
def reset_completo():
    '''Reset completo: flush + migrate + restaurar'''
    print("🔄 INICIANDO RESET COMPLETO...")

    print("1️⃣ Limpiando base de datos...")
    call_command('flush', '--noinput')

    print("2️⃣ Ejecutando migraciones...")
    call_command('migrate')

    print("3️⃣ Restaurando estructura...")
    exec(open('restaurar_estructura_20250820_095645.py').read())

    print("✅ RESET COMPLETO FINALIZADO")

if __name__ == "__main__":
    reset_completo()
"""

    with open("reset_completo_protegido.py", "w", encoding="utf-8") as f:
        f.write(script_reset)

    print("✅ Creado: reset_completo_protegido.py")


if __name__ == "__main__":
    aplicar_proteccion_a_scripts()
    crear_scripts_seguros()

    print("\n🎯 RESUMEN DE PROTECCIÓN:")
    print("✅ Scripts existentes protegidos con backups")
    print("✅ Scripts seguros creados")
    print("✅ Sistema de autorización activo")
    print("\n📋 Para usar:")
    print("  - python gestion_bd_protegida.py  (gestión interactiva)")
    print("  - python prueba_proteccion.py     (probar protección)")
    print("  - python reset_completo_protegido.py (reset seguro)")
    print("\n🔑 Clave de autorización: PACKFY_DB_PROTECTION_2025")
