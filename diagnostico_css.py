#!/usr/bin/env python
"""
Script para analizar los problemas de CSS y crear un plan de corrección
"""
import os


def analyze_css_structure():
    """Analiza la estructura de archivos CSS"""
    print("🔍 ANÁLISIS DE ESTRUCTURA CSS")
    print("=" * 50)

    frontend_path = (
        "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend"
    )
    css_files = []

    # Buscar archivos CSS
    for root, dirs, files in os.walk(f"{frontend_path}/src"):
        for file in files:
            if file.endswith(".css"):
                css_files.append(os.path.join(root, file))

    print(f"📁 Archivos CSS encontrados: {len(css_files)}")
    for file in css_files:
        rel_path = file.replace(frontend_path, "")
        size = os.path.getsize(file) if os.path.exists(file) else 0
        print(f"  - {rel_path} ({size} bytes)")

    # Verificar archivos duplicados o conflictivos
    print("\n⚠️ POSIBLES PROBLEMAS IDENTIFICADOS:")

    # Nombres similares que pueden causar conflictos
    problematic_patterns = [
        ("main.css", "main-clean.css", "master-unified.css"),
        ("mobile-optimized.css", "mobile-safe.css", "mobile-pwa.css"),
        ("navigation.css", "nav-*", "header-*"),
    ]

    for pattern in problematic_patterns:
        matching_files = [f for f in css_files if any(p in f for p in pattern)]
        if len(matching_files) > 1:
            print(f"  🔴 Múltiples archivos similares:")
            for match in matching_files:
                print(f"    - {match.replace(frontend_path, '')}")

    return css_files


def create_css_optimization_plan():
    """Crea un plan de optimización CSS"""
    print("\n📋 PLAN DE OPTIMIZACIÓN CSS")
    print("=" * 50)

    plan = {
        "1_cleanup": [
            "Consolidar archivos CSS duplicados",
            "Eliminar imports innecesarios en main.tsx",
            "Crear un solo archivo CSS principal",
        ],
        "2_header_fixes": [
            "Corregir problemas del menú de cabecera",
            "Mejorar responsividad del header",
            "Unificar estilos de navegación",
        ],
        "3_layout_consistency": [
            "Aplicar estilos consistentes en todas las páginas",
            "Corregir problemas de layout móvil",
            "Mejorar contraste y legibilidad",
        ],
        "4_performance": [
            "Minimizar CSS crítico",
            "Optimizar carga de estilos",
            "Eliminar CSS no utilizado",
        ],
    }

    for phase, tasks in plan.items():
        print(f"\n{phase.upper().replace('_', ' ')}:")
        for task in tasks:
            print(f"  ✓ {task}")

    return plan


def main():
    print("🇨🇺 PACKFY CUBA - DIAGNÓSTICO CSS COMPLETO")
    print("=" * 60)

    css_files = analyze_css_structure()
    plan = create_css_optimization_plan()

    print(f"\n📊 RESUMEN:")
    print(f"  - Total archivos CSS: {len(css_files)}")
    print(f"  - Fases de optimización: {len(plan)}")
    print(f"  - Estado: REQUIERE OPTIMIZACIÓN")


if __name__ == "__main__":
    main()
