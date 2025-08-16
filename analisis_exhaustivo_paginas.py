#!/usr/bin/env python
"""
Análisis exhaustivo página por página de Packfy Cuba MVP
Revisión profunda de código CSS y optimizaciones necesarias
"""
import os
import re


def analizar_pagina(filepath, nombre_pagina):
    """Analiza una página específica y sus estilos"""
    print(f"\n📄 ANALIZANDO: {nombre_pagina.upper()}")
    print("=" * 50)

    if not os.path.exists(filepath):
        print(f"❌ Archivo no encontrado: {filepath}")
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Análisis de imports CSS
    css_imports = re.findall(r'import.*\.css[\'"];', content)

    # Análisis de className usage
    classnames = re.findall(r'className=["\']([^"\']*)["\']', content)

    # Análisis de componentes utilizados
    components = re.findall(r"<([A-Z][a-zA-Z]*)", content)

    # Análisis de styling inline
    inline_styles = re.findall(r"style=\{([^}]*)\}", content)

    analisis = {
        "css_imports": css_imports,
        "unique_classes": list(set(classnames)),
        "components": list(set(components)),
        "inline_styles": len(inline_styles),
        "total_classes": len(classnames),
        "file_size": len(content),
    }

    print(f"  📦 Imports CSS: {len(css_imports)}")
    print(f"  🏷️  Clases únicas: {len(analisis['unique_classes'])}")
    print(f"  🧩 Componentes: {len(analisis['components'])}")
    print(f"  🎨 Estilos inline: {analisis['inline_styles']}")
    print(f"  📏 Tamaño archivo: {analisis['file_size']:,} chars")

    if css_imports:
        print(f"  ⚠️  CSS Imports encontrados:")
        for imp in css_imports:
            print(f"    - {imp}")

    # Mostrar clases más usadas
    class_counts = {}
    for cls in classnames:
        for individual_class in cls.split():
            if individual_class:
                class_counts[individual_class] = (
                    class_counts.get(individual_class, 0) + 1
                )

    top_classes = sorted(
        class_counts.items(), key=lambda x: x[1], reverse=True
    )[:5]
    if top_classes:
        print(f"  🔥 Top 5 clases más usadas:")
        for cls, count in top_classes:
            print(f"    - {cls}: {count} veces")

    return analisis


def main():
    print("🇨🇺 PACKFY CUBA MVP - ANÁLISIS EXHAUSTIVO PÁGINA POR PÁGINA")
    print("=" * 70)
    print("Revisión profunda de código CSS y arquitectura frontend")

    # Definir todas las páginas a analizar
    paginas = {
        "App.tsx": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/App.tsx",
        "Dashboard": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/Dashboard.tsx",
        "LoginPage": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/LoginPage.tsx",
        "GestionUnificada": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/GestionUnificada.tsx",
        "SimpleAdvancedPage": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/SimpleAdvancedPage.tsx",
        "PremiumFormPage": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/PremiumFormPage.tsx",
        "ShipmentDetail": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/ShipmentDetail.tsx",
        "PublicTrackingPage": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/PublicTrackingPage.tsx",
        "DiagnosticPage": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/DiagnosticPage.tsx",
        "EditarEnvio": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/EditarEnvio.tsx",
        "NewShipment": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/pages/NewShipment.tsx",
        "Layout": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/components/Layout.tsx",
        "ModeSelector": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/components/ModeSelector.tsx",
        "SimpleAdvancedForm": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/components/SimpleAdvancedForm.tsx",
        "PremiumCompleteForm": "c:/Users/pepec/Projects/Packfy/paqueteria-cuba-mvp/frontend/src/components/PremiumCompleteForm.tsx",
    }

    # Análisis de todas las páginas
    resultados = {}
    total_css_imports = 0
    total_classes = 0

    for nombre, filepath in paginas.items():
        resultado = analizar_pagina(filepath, nombre)
        resultados[nombre] = resultado
        total_css_imports += len(resultado.get("css_imports", []))
        total_classes += len(resultado.get("unique_classes", []))

    # Resumen global
    print(f"\n📊 RESUMEN GLOBAL")
    print("=" * 50)
    print(f"  📄 Páginas analizadas: {len(paginas)}")
    print(f"  📦 Total CSS imports: {total_css_imports}")
    print(f"  🏷️  Total clases únicas: {total_classes}")

    # Identificar problemas críticos
    print(f"\n🚨 PROBLEMAS CRÍTICOS IDENTIFICADOS")
    print("=" * 50)

    problemas_encontrados = []

    for nombre, resultado in resultados.items():
        if resultado.get("css_imports"):
            problemas_encontrados.append(
                f"❌ {nombre}: Imports CSS locales encontrados"
            )

        if resultado.get("inline_styles", 0) > 5:
            problemas_encontrados.append(
                f"⚠️ {nombre}: Demasiados estilos inline ({resultado['inline_styles']})"
            )

    if problemas_encontrados:
        for problema in problemas_encontrados:
            print(f"  {problema}")
    else:
        print("  ✅ No se encontraron problemas críticos")

    # Recomendaciones específicas
    print(f"\n💡 RECOMENDACIONES ESPECÍFICAS")
    print("=" * 50)

    recomendaciones = [
        "🔧 Eliminar todos los imports CSS locales",
        "🎨 Consolidar estilos inline en clases CSS",
        "📝 Estandarizar nombres de clases",
        "🧹 Limpiar clases no utilizadas",
        "⚡ Optimizar componentes con muchas clases",
        "📱 Verificar responsividad en todas las páginas",
        "🔍 Auditar accesibilidad (ARIA, focus, etc.)",
        "🚀 Implementar lazy loading donde sea necesario",
    ]

    for rec in recomendaciones:
        print(f"  {rec}")

    return resultados


if __name__ == "__main__":
    main()
