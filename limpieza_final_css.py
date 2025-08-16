#!/usr/bin/env python3
"""
Script de limpieza final del sistema CSS
Elimina archivos CSS antiguos que ya no se necesitan
"""

import os
import shutil
from pathlib import Path


def limpiar_archivos_css_obsoletos():
    """Elimina archivos CSS que ya no se necesitan tras la unificación"""
    print("🧹 LIMPIEZA FINAL DEL SISTEMA CSS")
    print("=" * 50)

    styles_dir = Path("frontend/src/styles")
    if not styles_dir.exists():
        print("❌ Directorio de estilos no encontrado")
        return

    # Archivos que deben mantenerse
    archivos_mantener = {
        "packfy-master-v6.css",  # Archivo principal
    }

    # Directorios que pueden eliminarse completamente
    directorios_eliminar = {"components", "core", "layouts", "utilities"}

    archivos_eliminados = 0
    directorios_eliminados = 0

    print("📁 Eliminando directorios obsoletos...")
    for dir_name in directorios_eliminar:
        dir_path = styles_dir / dir_name
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"   ✅ Eliminado: {dir_name}/")
                directorios_eliminados += 1
            except Exception as e:
                print(f"   ❌ Error eliminando {dir_name}: {e}")

    print("\n📄 Eliminando archivos CSS obsoletos...")
    for archivo in styles_dir.glob("*.css"):
        if archivo.name not in archivos_mantener:
            try:
                archivo.unlink()
                print(f"   ✅ Eliminado: {archivo.name}")
                archivos_eliminados += 1
            except Exception as e:
                print(f"   ❌ Error eliminando {archivo.name}: {e}")

    print("\n📊 RESUMEN DE LIMPIEZA:")
    print(f"   🗂️ Directorios eliminados: {directorios_eliminados}")
    print(f"   📄 Archivos eliminados: {archivos_eliminados}")

    # Verificar que solo quede el archivo master
    archivos_restantes = list(styles_dir.glob("*.css"))
    print(f"   📋 Archivos CSS restantes: {len(archivos_restantes)}")

    for archivo in archivos_restantes:
        tamaño = archivo.stat().st_size
        print(f"      ✅ {archivo.name} ({tamaño:,} bytes)")

    return archivos_eliminados > 0 or directorios_eliminados > 0


def verificar_imports_en_codigo():
    """Verifica que no haya imports CSS obsoletos en el código"""
    print("\n🔍 VERIFICANDO IMPORTS CSS EN CÓDIGO...")
    print("=" * 50)

    frontend_dir = Path("frontend/src")
    archivos_con_imports = []

    for archivo in frontend_dir.rglob("*.tsx"):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()

            # Buscar imports CSS que no sean el master
            lineas = contenido.split("\n")
            for i, linea in enumerate(lineas, 1):
                if (
                    "import" in linea
                    and ".css" in linea
                    and "packfy-master-v6.css" not in linea
                    and linea.strip().startswith("import")
                ):
                    archivos_con_imports.append((archivo, i, linea.strip()))

        except Exception as e:
            print(f"   ⚠️ Error leyendo {archivo}: {e}")

    if archivos_con_imports:
        print("   ❌ Encontrados imports CSS obsoletos:")
        for archivo, linea, import_line in archivos_con_imports:
            rel_path = archivo.relative_to(Path.cwd())
            print(f"      {rel_path}:{linea} -> {import_line}")
    else:
        print("   ✅ No se encontraron imports CSS obsoletos")

    return len(archivos_con_imports) == 0


def crear_backup_antes_limpieza():
    """Crea un backup antes de la limpieza"""
    backup_dir = Path("css-backup-pre-limpieza")
    styles_dir = Path("frontend/src/styles")

    if backup_dir.exists():
        shutil.rmtree(backup_dir)

    try:
        shutil.copytree(styles_dir, backup_dir)
        print(f"✅ Backup creado en: {backup_dir}")
        return True
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        return False


if __name__ == "__main__":
    print("🇨🇺 PACKFY CUBA - Limpieza Final del Sistema CSS v6.0")
    print("=" * 60)

    # Crear backup
    if crear_backup_antes_limpieza():
        print()

        # Limpiar archivos
        if limpiar_archivos_css_obsoletos():
            print("\n🔄 REBUILD NECESARIO:")
            print("   Para aplicar los cambios, ejecuta:")
            print("   docker-compose build frontend --no-cache")
            print("   docker-compose up frontend -d")

        # Verificar imports
        imports_ok = verificar_imports_en_codigo()

        print("\n" + "=" * 60)
        if imports_ok:
            print("🎉 LIMPIEZA COMPLETADA EXITOSAMENTE")
            print("   ✅ Solo queda el archivo CSS master")
            print("   ✅ No hay imports CSS obsoletos")
            print("   ✅ Sistema CSS totalmente unificado")
        else:
            print("⚠️ LIMPIEZA PARCIAL COMPLETADA")
            print("   🔧 Revisar imports CSS obsoletos")
        print("=" * 60)
    else:
        print("❌ No se pudo crear backup. Limpieza cancelada.")
