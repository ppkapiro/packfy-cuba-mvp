#!/usr/bin/env python
"""
🔍 AUDITORÍA COMPLETA DEL FRONTEND
Análisis profundo de configuraciones, archivos obsoletos y problemas
"""

import json
import os
import re
from pathlib import Path


def main():
    print("🔍 AUDITORÍA COMPLETA DEL FRONTEND MULTITENANCY")
    print("=" * 80)

    frontend_path = Path("../frontend-multitenant")

    if not frontend_path.exists():
        print("❌ Directorio frontend-multitenant no encontrado")
        return

    print(f"📁 Analizando: {frontend_path.absolute()}")
    print()

    analizar_estructura_general(frontend_path)
    analizar_configuraciones_api(frontend_path)
    analizar_contextos_tenant(frontend_path)
    analizar_archivos_obsoletos(frontend_path)
    analizar_importaciones_duplicadas(frontend_path)
    analizar_configuracion_vite(frontend_path)
    analizar_dependencias(frontend_path)
    generar_recomendaciones()


def analizar_estructura_general(frontend_path):
    """Análisis de la estructura general del proyecto"""
    print("📂 ANÁLISIS DE ESTRUCTURA GENERAL")
    print("-" * 50)

    # Buscar archivos de configuración de API
    api_files = list(frontend_path.glob("**/*api*.ts"))
    print(f"🔧 Archivos de API encontrados: {len(api_files)}")
    for api_file in api_files:
        rel_path = api_file.relative_to(frontend_path)
        print(f"   • {rel_path}")

    # Buscar archivos relacionados con tenant
    tenant_files = list(frontend_path.glob("**/*tenant*.ts*"))
    print(f"\n🏢 Archivos de Tenant encontrados: {len(tenant_files)}")
    for tenant_file in tenant_files:
        rel_path = tenant_file.relative_to(frontend_path)
        print(f"   • {rel_path}")

    # Buscar archivos de contexto
    context_files = list(frontend_path.glob("**/contexts/*.tsx"))
    print(f"\n🔄 Archivos de Contexto encontrados: {len(context_files)}")
    for context_file in context_files:
        rel_path = context_file.relative_to(frontend_path)
        print(f"   • {rel_path}")

    print()


def analizar_configuraciones_api(frontend_path):
    """Análisis de configuraciones de API"""
    print("🌐 ANÁLISIS DE CONFIGURACIONES DE API")
    print("-" * 50)

    api_files = list(frontend_path.glob("**/*api*.ts"))

    for api_file in api_files:
        if api_file.is_file():
            rel_path = api_file.relative_to(frontend_path)
            print(f"\n📄 Analizando: {rel_path}")

            try:
                content = api_file.read_text(encoding="utf-8")

                # Buscar URLs base
                base_urls = re.findall(r'baseURL.*?["\']([^"\']+)["\']', content)
                if base_urls:
                    print(f"   🔗 URLs base encontradas: {base_urls}")

                # Buscar configuraciones de tenant
                tenant_configs = re.findall(r'[Tt]enant.*?["\']([^"\']+)["\']', content)
                if tenant_configs:
                    print(f"   🏢 Configuraciones de tenant: {tenant_configs}")

                # Buscar imports problemáticos
                imports = re.findall(r'import.*?from.*?["\']([^"\']+)["\']', content)
                problematic_imports = [
                    imp for imp in imports if "../" in imp and imp.count("../") > 2
                ]
                if problematic_imports:
                    print(f"   ⚠️ Imports problemáticos: {problematic_imports}")

                # Buscar duplicación de clases/funciones
                classes = re.findall(r"class (\w+)", content)
                if len(classes) > 1:
                    print(f"   🔄 Múltiples clases: {classes}")

            except Exception as e:
                print(f"   ❌ Error leyendo archivo: {e}")


def analizar_contextos_tenant(frontend_path):
    """Análisis específico de contextos de tenant"""
    print("\n🏢 ANÁLISIS DE CONTEXTOS DE TENANT")
    print("-" * 50)

    context_files = list(frontend_path.glob("**/contexts/*.tsx"))

    for context_file in context_files:
        if context_file.is_file():
            rel_path = context_file.relative_to(frontend_path)
            print(f"\n📄 Analizando: {rel_path}")

            try:
                content = context_file.read_text(encoding="utf-8")

                # Buscar providers
                providers = re.findall(r"(\w+Provider)", content)
                if providers:
                    print(f"   🔧 Providers encontrados: {set(providers)}")

                # Buscar hooks
                hooks = re.findall(r"use(\w+)", content)
                if hooks:
                    print(f"   🪝 Hooks encontrados: {set(hooks)}")

                # Buscar estado relacionado con tenant
                tenant_states = re.findall(r"useState.*?[Tt]enant", content)
                if tenant_states:
                    print(f"   🏢 Estados de tenant: {len(tenant_states)}")

                # Verificar inicialización de tenant
                if "detectTenant" in content or "initializeTenant" in content:
                    print("   ✅ Inicialización de tenant encontrada")
                else:
                    print("   ⚠️ No se encontró inicialización de tenant")

            except Exception as e:
                print(f"   ❌ Error leyendo archivo: {e}")


def analizar_archivos_obsoletos(frontend_path):
    """Detectar archivos potencialmente obsoletos"""
    print("\n🗑️ ANÁLISIS DE ARCHIVOS POTENCIALMENTE OBSOLETOS")
    print("-" * 50)

    # Buscar archivos con nombres que sugieren que son obsoletos
    obsolete_patterns = [
        "**/*backup*",
        "**/*old*",
        "**/*deprecated*",
        "**/*legacy*",
        "**/*temp*",
        "**/*test*",
        "**/*example*",
    ]

    for pattern in obsolete_patterns:
        files = list(frontend_path.glob(pattern))
        if files:
            print(f"\n📋 Patrón '{pattern}':")
            for file in files:
                rel_path = file.relative_to(frontend_path)
                size = file.stat().st_size if file.is_file() else 0
                print(f"   • {rel_path} ({size} bytes)")

    # Buscar archivos duplicados por nombre similar
    print(f"\n🔄 ANÁLISIS DE DUPLICADOS POTENCIALES:")

    ts_files = list(frontend_path.glob("**/*.ts*"))
    file_groups = {}

    for file in ts_files:
        base_name = file.stem.lower()
        # Quitar sufijos comunes
        base_name = re.sub(
            r"[-_](v\d+|backup|old|new|fixed|simple|robust|unified)$", "", base_name
        )

        if base_name not in file_groups:
            file_groups[base_name] = []
        file_groups[base_name].append(file)

    for base_name, files in file_groups.items():
        if len(files) > 1:
            print(f"\n   📄 Grupo '{base_name}':")
            for file in files:
                rel_path = file.relative_to(frontend_path)
                size = file.stat().st_size if file.is_file() else 0
                print(f"      • {rel_path} ({size} bytes)")


def analizar_importaciones_duplicadas(frontend_path):
    """Análisis de importaciones duplicadas o problemáticas"""
    print("\n🔗 ANÁLISIS DE IMPORTACIONES")
    print("-" * 50)

    ts_files = list(frontend_path.glob("**/*.ts*"))
    import_analysis = {}

    for file in ts_files:
        if file.is_file():
            try:
                content = file.read_text(encoding="utf-8")
                imports = re.findall(r'import.*?from.*?["\']([^"\']+)["\']', content)

                rel_path = file.relative_to(frontend_path)
                import_analysis[str(rel_path)] = imports

            except Exception:
                continue

    # Buscar imports problemáticos
    problematic_files = []
    for file_path, imports in import_analysis.items():
        problems = []

        # Imports con muchos "../"
        deep_imports = [imp for imp in imports if "../" in imp and imp.count("../") > 2]
        if deep_imports:
            problems.append(f"Imports profundos: {deep_imports}")

        # Imports duplicados en el mismo archivo
        import_counts = {}
        for imp in imports:
            import_counts[imp] = import_counts.get(imp, 0) + 1

        duplicates = [imp for imp, count in import_counts.items() if count > 1]
        if duplicates:
            problems.append(f"Imports duplicados: {duplicates}")

        if problems:
            problematic_files.append((file_path, problems))

    if problematic_files:
        print("⚠️ Archivos con imports problemáticos:")
        for file_path, problems in problematic_files[
            :10
        ]:  # Mostrar solo los primeros 10
            print(f"\n   📄 {file_path}")
            for problem in problems:
                print(f"      • {problem}")
    else:
        print("✅ No se encontraron imports problemáticos")


def analizar_configuracion_vite(frontend_path):
    """Análisis de configuración de Vite"""
    print("\n⚡ ANÁLISIS DE CONFIGURACIÓN VITE")
    print("-" * 50)

    vite_config = frontend_path / "vite.config.ts"
    if vite_config.exists():
        try:
            content = vite_config.read_text(encoding="utf-8")

            # Buscar configuración del proxy
            if "proxy" in content:
                print("✅ Configuración de proxy encontrada")
                proxy_config = re.search(r"proxy:\s*{([^}]+)}", content, re.DOTALL)
                if proxy_config:
                    print(f"   🔧 Configuración: {proxy_config.group(1).strip()}")
            else:
                print("⚠️ No se encontró configuración de proxy")

            # Buscar configuración del puerto
            port_match = re.search(r"port:\s*(\d+)", content)
            if port_match:
                print(f"🔌 Puerto configurado: {port_match.group(1)}")

            # Buscar configuración del host
            if "host:" in content:
                host_match = re.search(r'host:\s*["\']([^"\']+)["\']', content)
                if host_match:
                    print(f"🌐 Host configurado: {host_match.group(1)}")

        except Exception as e:
            print(f"❌ Error leyendo vite.config.ts: {e}")
    else:
        print("❌ vite.config.ts no encontrado")


def analizar_dependencias(frontend_path):
    """Análisis de package.json y dependencias"""
    print("\n📦 ANÁLISIS DE DEPENDENCIAS")
    print("-" * 50)

    package_json = frontend_path / "package.json"
    if package_json.exists():
        try:
            with open(package_json, "r", encoding="utf-8") as f:
                data = json.load(f)

            dependencies = data.get("dependencies", {})
            dev_dependencies = data.get("devDependencies", {})

            print(f"📋 Dependencias de producción: {len(dependencies)}")
            print(f"🔧 Dependencias de desarrollo: {len(dev_dependencies)}")

            # Buscar dependencias relacionadas con tenant/multitenancy
            tenant_deps = [
                dep for dep in dependencies.keys() if "tenant" in dep.lower()
            ]
            if tenant_deps:
                print(f"🏢 Dependencias de tenant: {tenant_deps}")

            # Buscar dependencias de React
            react_deps = [dep for dep in dependencies.keys() if "react" in dep.lower()]
            print(f"⚛️ Dependencias de React: {react_deps}")

            # Buscar scripts relevantes
            scripts = data.get("scripts", {})
            print(f"\n📜 Scripts disponibles:")
            for script_name, script_cmd in scripts.items():
                print(f"   • {script_name}: {script_cmd}")

        except Exception as e:
            print(f"❌ Error leyendo package.json: {e}")
    else:
        print("❌ package.json no encontrado")


def generar_recomendaciones():
    """Generar recomendaciones basadas en el análisis"""
    print("\n🎯 RECOMENDACIONES BASADAS EN EL ANÁLISIS")
    print("=" * 80)

    recomendaciones = [
        {
            "prioridad": "🔥 ALTA",
            "titulo": "Limpieza de archivos API duplicados",
            "descripcion": "Consolidar múltiples archivos api-*.ts en uno solo y eliminar obsoletos",
            "accion": "Mantener solo api.ts principal y eliminar api-simple, api-robust, etc.",
        },
        {
            "prioridad": "🔥 ALTA",
            "titulo": "Configuración uniforme de tenant",
            "descripcion": "Asegurar que la detección de tenant funcione consistentemente",
            "accion": "Verificar que tenantDetector.ts se use en toda la aplicación",
        },
        {
            "prioridad": "📊 MEDIA",
            "titulo": "Optimización de imports",
            "descripcion": "Simplificar imports con muchos '../' y eliminar duplicados",
            "accion": "Crear barrel exports y aliases en vite.config.ts",
        },
        {
            "prioridad": "📊 MEDIA",
            "titulo": "Validación de configuración CORS",
            "descripcion": "Asegurar que el proxy de Vite funcione correctamente",
            "accion": "Probar conexión frontend-backend paso a paso",
        },
        {
            "prioridad": "💡 BAJA",
            "titulo": "Documentación de configuración",
            "descripcion": "Documentar la configuración multitenancy para futuro desarrollo",
            "accion": "Crear README específico para configuración de tenants",
        },
    ]

    for rec in recomendaciones:
        print(f"\n{rec['prioridad']} {rec['titulo']}")
        print(f"   📝 {rec['descripcion']}")
        print(f"   🔧 Acción: {rec['accion']}")

    print("\n" + "=" * 80)
    print("📊 AUDITORÍA COMPLETADA")
    print("   Revisar recomendaciones arriba para próximos pasos")
    print("=" * 80)


if __name__ == "__main__":
    main()
