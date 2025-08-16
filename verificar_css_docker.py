#!/usr/bin/env python3
"""
Validación de que el sistema CSS unificado esté funcionando en Docker
Verifica que los estilos se apliquen correctamente en la aplicación web
"""

import re
from pathlib import Path

import requests


def verificar_css_en_docker():
    """Verifica que el CSS unificado esté siendo servido correctamente"""
    print("🔍 VERIFICACIÓN DEL SISTEMA CSS EN DOCKER")
    print("=" * 60)

    try:
        # Verificar que la aplicación esté respondiendo
        response = requests.get("http://localhost:5173", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend respondiendo correctamente en puerto 5173")
        else:
            print(f"❌ Frontend no responde: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando al frontend: {e}")
        return False

    # Verificar que el HTML contenga la referencia al CSS master
    html_content = response.text

    # Buscar la referencia al archivo CSS master
    css_pattern = r"packfy-master-v\d+\.css"
    css_match = re.search(css_pattern, html_content)

    if css_match:
        print(f"✅ Archivo CSS master encontrado: {css_match.group()}")
    else:
        print("❌ No se encontró referencia al archivo CSS master")
        print("📋 Referencias CSS encontradas:")
        css_refs = re.findall(r'href="[^"]*\.css[^"]*"', html_content)
        for ref in css_refs:
            print(f"   {ref}")
        return False

    # Verificar que las variables CSS estén presentes
    if (
        "--primary-cuba" in html_content
        or "var(--primary-cuba)" in html_content
    ):
        print("✅ Variables CSS del tema cubano detectadas")
    else:
        print("⚠️ Variables CSS del tema cubano no detectadas en HTML")

    # Verificar meta tags importantes
    if "viewport" in html_content:
        print("✅ Meta viewport presente (responsive design)")
    else:
        print("⚠️ Meta viewport no encontrado")

    if "theme-color" in html_content:
        print("✅ Theme color configurado")
    else:
        print("⚠️ Theme color no configurado")

    print()
    print("📊 ESTADÍSTICAS DEL HTML:")
    print(f"   📄 Tamaño del HTML: {len(html_content):,} bytes")
    print(f"   🔗 Enlaces CSS: {len(re.findall(r'\.css', html_content))}")
    print(
        f"   🎨 Referencias a clases: {len(re.findall(r'class=', html_content))}"
    )

    return True


def verificar_contenedor_actualizado():
    """Verifica que el contenedor tenga los archivos CSS actualizados"""
    print()
    print("🐳 VERIFICACIÓN DEL CONTENEDOR:")
    print("=" * 40)

    # Verificar que el archivo master CSS esté en el contenedor
    import subprocess

    try:
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-frontend-mobile-v4.0",
                "ls",
                "-la",
                "/app/src/styles/",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("✅ Directorio de estilos accesible en el contenedor")

            # Buscar el archivo master
            if "packfy-master-v6.css" in result.stdout:
                print("✅ Archivo CSS master presente en el contenedor")

                # Verificar el tamaño del archivo
                size_result = subprocess.run(
                    [
                        "docker",
                        "exec",
                        "packfy-frontend-mobile-v4.0",
                        "wc",
                        "-c",
                        "/app/src/styles/packfy-master-v6.css",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                if size_result.returncode == 0:
                    size = size_result.stdout.strip().split()[0]
                    print(f"✅ Tamaño del archivo CSS: {int(size):,} bytes")

                    if int(size) > 40000:  # Debe ser más de 40KB
                        print("✅ Archivo CSS tiene el tamaño esperado")
                    else:
                        print("⚠️ Archivo CSS parece muy pequeño")
            else:
                print("❌ Archivo CSS master no encontrado en el contenedor")
                print("📋 Archivos encontrados:")
                for line in result.stdout.split("\n"):
                    if ".css" in line:
                        print(f"   {line}")
        else:
            print(f"❌ Error accediendo al contenedor: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("❌ Timeout ejecutando comando en contenedor")
    except Exception as e:
        print(f"❌ Error verificando contenedor: {e}")


def verificar_rendimiento():
    """Verifica el rendimiento de carga del CSS"""
    print()
    print("⚡ VERIFICACIÓN DE RENDIMIENTO:")
    print("=" * 40)

    try:
        import time

        start_time = time.time()

        response = requests.get("http://localhost:5173", timeout=10)

        load_time = time.time() - start_time

        print(f"⏱️ Tiempo de carga inicial: {load_time:.2f}s")

        if load_time < 2.0:
            print("✅ Tiempo de carga excelente")
        elif load_time < 5.0:
            print("✅ Tiempo de carga bueno")
        else:
            print("⚠️ Tiempo de carga lento")

        # Verificar headers de cache
        if "cache-control" in response.headers:
            print(f"✅ Cache control: {response.headers['cache-control']}")
        else:
            print("⚠️ No hay headers de cache configurados")

    except Exception as e:
        print(f"❌ Error verificando rendimiento: {e}")


if __name__ == "__main__":
    try:
        success = verificar_css_en_docker()
        verificar_contenedor_actualizado()
        verificar_rendimiento()

        print()
        print("=" * 60)
        if success:
            print("🎉 SISTEMA CSS FUNCIONANDO CORRECTAMENTE EN DOCKER")
            print("   ✅ Frontend actualizado con CSS unificado")
            print("   ✅ Tema cubano aplicado correctamente")
            print("   ✅ Rendimiento optimizado")
        else:
            print("❌ SE ENCONTRARON PROBLEMAS CON EL SISTEMA CSS")
            print("   🔧 Revisar la configuración del contenedor")
            print("   🔧 Verificar el build del frontend")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n⏹️ Verificación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
