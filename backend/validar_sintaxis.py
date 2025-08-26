#!/usr/bin/env python
"""
🔍 VALIDADOR SINTAXIS BACKEND
Verifica que no hay errores de sintaxis en el código Python
"""
import os
import py_compile
import sys


def verificar_sintaxis(archivo):
    """Verifica sintaxis de un archivo Python"""
    try:
        py_compile.compile(archivo, doraise=True)
        return True, "✅ Sintaxis correcta"
    except py_compile.PyCompileError as e:
        return False, f"❌ Error de sintaxis: {e}"


def main():
    """Verifica archivos clave del backend"""
    backend_dir = os.path.dirname(__file__)
    archivos_clave = [
        "empresas/permissions.py",
        "empresas/views.py",
        "empresas/models.py",
        "empresas/middleware.py",
        "config/urls.py",
        "config/settings.py",
    ]

    print("🔍 VERIFICANDO SINTAXIS DEL BACKEND")
    print("=" * 50)

    errores_encontrados = 0

    for archivo in archivos_clave:
        ruta_completa = os.path.join(backend_dir, archivo)
        if os.path.exists(ruta_completa):
            valido, mensaje = verificar_sintaxis(ruta_completa)
            print(f"{archivo}: {mensaje}")
            if not valido:
                errores_encontrados += 1
        else:
            print(f"{archivo}: ⚠️ Archivo no encontrado")

    print("\n" + "=" * 50)
    if errores_encontrados == 0:
        print("🎉 ¡TODOS LOS ARCHIVOS TIENEN SINTAXIS CORRECTA!")
        print("✅ El backend debería iniciarse sin problemas")
        return 0
    else:
        print(f"❌ {errores_encontrados} archivos con errores de sintaxis")
        print("🔧 Corrige los errores antes de continuar")
        return 1


if __name__ == "__main__":
    sys.exit(main())
