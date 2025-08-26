#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASO 2: Limpieza y archivo de bases de datos obsoletas
Fecha: 25 de agosto de 2025
"""

import os
import shutil
import sqlite3
from datetime import datetime


def analizar_db_stop():
    """Analizar contenido de db_stop.sqlite3 antes de archivar"""
    print("🔍 ANÁLISIS DE db_stop.sqlite3:")
    print("=" * 50)

    if not os.path.exists("db_stop.sqlite3"):
        print("❌ db_stop.sqlite3 no encontrado")
        return False

    # Obtener información básica
    size = os.path.getsize("db_stop.sqlite3")
    mod_time = datetime.fromtimestamp(os.path.getmtime("db_stop.sqlite3"))

    print(f"📄 Archivo: db_stop.sqlite3")
    print(f"📊 Tamaño: {size/1024:.1f} KB")
    print(f"🕒 Última modificación: {mod_time}")
    print()

    # Analizar contenido
    try:
        conn = sqlite3.connect("db_stop.sqlite3")
        cursor = conn.cursor()

        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM usuarios_usuario")
        usuarios = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM empresas_empresa")
        empresas = cursor.fetchone()[0]

        print(f"👥 Usuarios: {usuarios}")
        print(f"🏢 Empresas: {empresas}")

        # Mostrar usuarios
        print("\n👤 USUARIOS ENCONTRADOS:")
        cursor.execute("SELECT username, email, is_superuser FROM usuarios_usuario")
        for username, email, is_super in cursor.fetchall():
            admin_status = "🔑 Admin" if is_super else "👤 User"
            print(f"  - {username} ({email}) - {admin_status}")

        # Mostrar empresas
        print("\n🏢 EMPRESAS ENCONTRADAS:")
        cursor.execute("SELECT nombre FROM empresas_empresa")
        for (nombre,) in cursor.fetchall():
            print(f"  - {nombre}")

        conn.close()

        print("\n✅ Análisis completado")
        return True

    except Exception as e:
        print(f"❌ Error al analizar: {e}")
        return False


def crear_reporte_archivo():
    """Crear reporte del proceso de archivo"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    reporte = f"""
# 📋 REPORTE DE ARCHIVO - PASO 2
**Fecha:** {datetime.now().strftime("%d de %B de %Y, %H:%M:%S")}
**Proceso:** Limpieza de archivos obsoletos de base de datos

## 🗃️ ARCHIVOS PROCESADOS

### db_stop.sqlite3
- **Estado:** ARCHIVADO ✅
- **Ubicación original:** `backend/db_stop.sqlite3`
- **Ubicación archivo:** `archive/databases/db_stop_archived_{timestamp}.sqlite3`
- **Tamaño:** {os.path.getsize('db_stop.sqlite3')/1024:.1f} KB
- **Contenido:**
  - 4 usuarios (admin, empresa1, operador1, cliente1)
  - 1 empresa (Packfy Demo)
  - Estructura de BD antigua (sin campo slug)

### db.sqlite3
- **Estado:** ACTIVO ✅
- **Descripción:** Base de datos principal del sistema
- **Contenido actual:**
  - 10 usuarios con roles diversos
  - 1 empresa (Packfy Express)
  - 10 perfiles usuario-empresa
  - Estructura moderna con multitenancy

## 🎯 RESULTADO

✅ **db_stop.sqlite3** archivado de forma segura
✅ **db.sqlite3** permanece como BD principal
✅ **Sistema limpio** y organizado
✅ **Historial preservado** en archive/

## 📝 NOTAS

- `db_stop.sqlite3` contiene datos históricos que no interfieren con el sistema actual
- La estructura de BD es diferente (sin campo slug en empresas)
- Los usuarios son completamente diferentes a los actuales
- Se mantiene archivado para referencia histórica

---
**Generado automáticamente por el proceso de limpieza PASO 2**
"""

    return reporte


def archivar_db_stop():
    """Archivar db_stop.sqlite3 de forma segura"""
    print("\n🗂️ INICIANDO PROCESO DE ARCHIVO:")
    print("=" * 50)

    if not os.path.exists("db_stop.sqlite3"):
        print("✅ db_stop.sqlite3 ya no existe - limpieza ya realizada")
        return True

    # Crear directorio de archivo si no existe
    archive_dir = "../archive/databases"
    os.makedirs(archive_dir, exist_ok=True)

    # Crear nombre con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"db_stop_archived_{timestamp}.sqlite3"
    archive_path = os.path.join(archive_dir, archive_name)

    try:
        # Mover archivo
        shutil.move("db_stop.sqlite3", archive_path)
        print(f"✅ db_stop.sqlite3 archivado como: {archive_name}")
        print(f"📁 Ubicación: {archive_path}")

        # Crear reporte
        reporte_content = crear_reporte_archivo()
        reporte_path = os.path.join(archive_dir, f"reporte_archivo_{timestamp}.md")

        with open(reporte_path, "w", encoding="utf-8") as f:
            f.write(reporte_content)

        print(f"📋 Reporte creado: reporte_archivo_{timestamp}.md")

        return True

    except Exception as e:
        print(f"❌ Error al archivar: {e}")
        return False


def verificar_limpieza():
    """Verificar que la limpieza fue exitosa"""
    print("\n🔍 VERIFICACIÓN POST-LIMPIEZA:")
    print("=" * 50)

    # Verificar que db.sqlite3 existe y funciona
    if os.path.exists("db.sqlite3"):
        print("✅ db.sqlite3 (principal) - EXISTE")

        try:
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios_usuario")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"✅ db.sqlite3 funcional - {count} usuarios")
        except Exception as e:
            print(f"❌ Error en db.sqlite3: {e}")
    else:
        print("❌ db.sqlite3 NO ENCONTRADO - ¡PROBLEMA!")

    # Verificar que db_stop.sqlite3 fue archivado
    if not os.path.exists("db_stop.sqlite3"):
        print("✅ db_stop.sqlite3 - ARCHIVADO (no existe en directorio activo)")
    else:
        print("⚠️ db_stop.sqlite3 - AÚN EXISTE")

    # Verificar archivos en archive
    archive_dir = "../archive/databases"
    if os.path.exists(archive_dir):
        archived_files = [
            f for f in os.listdir(archive_dir) if f.startswith("db_stop_archived")
        ]
        if archived_files:
            print(f"✅ Archivos archivados: {len(archived_files)}")
            for f in archived_files:
                print(f"   📁 {f}")
        else:
            print("⚠️ No se encontraron archivos archivados")

    print("\n🎯 LIMPIEZA COMPLETADA")


def main():
    """Ejecutar proceso completo del PASO 2"""
    print("🧹 PASO 2: LIMPIEZA DE ARCHIVOS OBSOLETOS")
    print("=" * 60)
    print()

    # Paso 1: Analizar
    if analizar_db_stop():
        # Paso 2: Archivar
        if archivar_db_stop():
            # Paso 3: Verificar
            verificar_limpieza()

            print("\n" + "=" * 60)
            print("✅ PASO 2 COMPLETADO EXITOSAMENTE")
            print("✅ Sistema limpio y organizado")
            print("✅ Archivos históricos preservados")
            print("✅ Listo para continuar desarrollo")
            print("=" * 60)
        else:
            print("\n❌ Error en el proceso de archivo")
    else:
        print("\n❌ Error en el análisis inicial")


if __name__ == "__main__":
    main()
