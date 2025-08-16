#!/usr/bin/env python3
"""
Validación final del sistema CSS unificado
Verifica que todas las clases utilizadas estén definidas en el archivo master
"""

import os
import re
from pathlib import Path


def extraer_clases_del_master():
    """Extrae todas las clases definidas en el archivo master CSS"""
    master_file = Path("frontend/src/styles/packfy-master-v6.css")
    if not master_file.exists():
        print(f"❌ No se encontró el archivo master: {master_file}")
        return set()

    with open(master_file, "r", encoding="utf-8") as f:
        contenido = f.read()

    # Buscar todas las clases CSS definidas
    clases_definidas = set()

    # Patrón para clases CSS (incluyendo pseudo-clases y media queries)
    patron_clases = r"\.([a-zA-Z0-9_-]+)(?:\s*[:{,]|\s*\.[a-zA-Z0-9_-]+)*"
    matches = re.findall(patron_clases, contenido)

    for match in matches:
        # Filtrar pseudo-clases y elementos específicos
        if not any(
            pseudo in match
            for pseudo in [
                "hover",
                "focus",
                "active",
                "before",
                "after",
                "first-child",
                "last-child",
            ]
        ):
            clases_definidas.add(match)

    return clases_definidas


def extraer_clases_utilizadas():
    """Extrae todas las clases utilizadas en los archivos TSX/JSX"""
    clases_utilizadas = set()
    frontend_dir = Path("frontend/src")

    if not frontend_dir.exists():
        print(f"❌ No se encontró el directorio frontend: {frontend_dir}")
        return set()

    # Buscar archivos TSX y JSX
    archivos_tsx = list(frontend_dir.rglob("*.tsx")) + list(
        frontend_dir.rglob("*.jsx")
    )

    print(f"📂 Analizando {len(archivos_tsx)} archivos TSX/JSX...")

    for archivo in archivos_tsx:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()

            # Buscar className="..." y className={...}
            patrones = [
                r'className=["\']([^"\']+)["\']',  # className="class1 class2"
                r'className=\{["\']([^"\']+)["\']\}',  # className={"class1 class2"}
                r"className=\{`([^`]+)`\}",  # className={`class1 ${var} class2`}
            ]

            for patron in patrones:
                matches = re.findall(patron, contenido)
                for match in matches:
                    # Dividir por espacios y filtrar clases vacías
                    clases = [
                        c.strip()
                        for c in match.split()
                        if c.strip() and not c.startswith("${")
                    ]
                    clases_utilizadas.update(clases)

        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")

    return clases_utilizadas


def validar_cobertura():
    """Valida que todas las clases utilizadas estén definidas en el master"""
    print("🔍 VALIDACIÓN FINAL DEL SISTEMA CSS UNIFICADO")
    print("=" * 60)

    clases_definidas = extraer_clases_del_master()
    clases_utilizadas = extraer_clases_utilizadas()

    print(f"📊 Clases definidas en master: {len(clases_definidas)}")
    print(f"📊 Clases utilizadas en código: {len(clases_utilizadas)}")
    print()

    # Clases faltantes
    clases_faltantes = clases_utilizadas - clases_definidas

    # Clases no utilizadas (posibles para eliminar)
    clases_no_utilizadas = clases_definidas - clases_utilizadas

    if clases_faltantes:
        print("❌ CLASES FALTANTES EN EL MASTER:")
        for clase in sorted(clases_faltantes):
            print(f"   - {clase}")
        print()

    if clases_no_utilizadas:
        print("⚠️ CLASES DEFINIDAS PERO NO UTILIZADAS:")
        # Filtrar clases de utilidad comunes que es normal que no se usen todas
        clases_utilidad = {
            c
            for c in clases_no_utilizadas
            if any(
                prefijo in c
                for prefijo in [
                    "m-",
                    "p-",
                    "mt-",
                    "mb-",
                    "ml-",
                    "mr-",
                    "pt-",
                    "pb-",
                    "pl-",
                    "pr-",
                    "w-",
                    "h-",
                    "d-",
                    "text-",
                    "bg-",
                    "border-",
                    "rounded",
                    "shadow",
                    "flex-",
                    "justify-",
                    "align-",
                ]
            )
        }
        clases_custom_no_utilizadas = clases_no_utilizadas - clases_utilidad

        if clases_custom_no_utilizadas:
            print("   Clases personalizadas no utilizadas:")
            for clase in sorted(clases_custom_no_utilizadas):
                print(f"   - {clase}")

        print(f"   Clases de utilidad definidas: {len(clases_utilidad)}")
        print()

    # Estadísticas finales
    cobertura = (
        (len(clases_utilizadas - clases_faltantes) / len(clases_utilizadas))
        * 100
        if clases_utilizadas
        else 100
    )

    print("📈 RESUMEN FINAL:")
    print(f"   ✅ Cobertura: {cobertura:.1f}%")
    print(
        f"   ✅ Clases cubiertas: {len(clases_utilizadas - clases_faltantes)}"
    )
    print(f"   ❌ Clases faltantes: {len(clases_faltantes)}")
    print(f"   📦 Total definidas: {len(clases_definidas)}")
    print()

    if cobertura >= 95:
        print("🎉 ¡SISTEMA CSS UNIFICADO COMPLETADO CON ÉXITO!")
        print("   El sistema tiene una cobertura excelente.")
    elif cobertura >= 85:
        print("✅ Sistema CSS unificado en buen estado.")
        print("   Solo faltan algunas clases menores.")
    else:
        print("⚠️ Sistema CSS necesita mejoras.")
        print("   Hay clases importantes faltantes.")

    return cobertura >= 95


def mostrar_estadisticas_master():
    """Muestra estadísticas del archivo master CSS"""
    master_file = Path("frontend/src/styles/packfy-master-v6.css")
    if not master_file.exists():
        return

    with open(master_file, "r", encoding="utf-8") as f:
        contenido = f.read()

    lineas = len(contenido.splitlines())
    tamaño_kb = len(contenido.encode("utf-8")) / 1024

    # Contar secciones
    secciones = len(re.findall(r"/\* ={10,} \*/", contenido))

    # Contar variables CSS
    variables = len(re.findall(r"--[a-zA-Z0-9-]+:", contenido))

    # Contar media queries
    media_queries = len(re.findall(r"@media", contenido))

    print("📊 ESTADÍSTICAS DEL ARCHIVO MASTER:")
    print(f"   📄 Líneas: {lineas}")
    print(f"   💾 Tamaño: {tamaño_kb:.1f} KB")
    print(f"   📑 Secciones: {secciones}")
    print(f"   🎨 Variables CSS: {variables}")
    print(f"   📱 Media queries: {media_queries}")
    print()


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    mostrar_estadisticas_master()
    validar_cobertura()
