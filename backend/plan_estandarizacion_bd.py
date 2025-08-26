#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plan de limpieza y estandarización de configuración de BD
RECOMENDACIÓN: SQLite para fase MVP
"""

import os
import shutil
from datetime import datetime


def plan_limpieza_bd():
    print("=== PLAN DE ESTANDARIZACIÓN DE BD ===")
    print()

    print("🎯 DECISIÓN: SQLITE COMO ESTÁNDAR")
    print("✅ Razones:")
    print("  - MVP con baja complejidad")
    print("  - Datos funcionando perfectamente")
    print("  - Cero configuración adicional")
    print("  - Desarrollo más ágil")
    print()

    print("📋 PASOS A EJECUTAR:")
    print()

    print("1. 🔧 ESTANDARIZAR CONFIGURACIÓN:")
    print("   - Actualizar settings.py para SQLite")
    print("   - Limpiar referencias a PostgreSQL")
    print("   - Documentar configuración")
    print()

    print("2. 🗑️ LIMPIAR ARCHIVOS OBSOLETOS:")
    print("   - Respaldar db_stop.sqlite3")
    print("   - Mover a carpeta archive/")
    print("   - Mantener solo db.sqlite3")
    print()

    print("3. 📝 DOCUMENTAR ESTÁNDAR:")
    print("   - README actualizado")
    print("   - Configuración clara")
    print("   - Proceso de backup")
    print()

    print("4. 🚀 PREPARAR MIGRACIÓN FUTURA:")
    print("   - Script para migrar a PostgreSQL")
    print("   - Cuando escale (>1000 usuarios)")
    print("   - Sin prisa, cuando sea necesario")
    print()

    print("💡 VENTAJAS INMEDIATAS:")
    print("✅ Sistema más estable")
    print("✅ Desarrollo más rápido")
    print("✅ Menos complejidad")
    print("✅ Backups simples")
    print("✅ Portabilidad total")


if __name__ == "__main__":
    plan_limpieza_bd()
