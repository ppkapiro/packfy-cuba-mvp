#!/usr/bin/env python
"""
Script para configurar acceso HTTP y HTTPS al frontend
"""
import subprocess
import time


def configurar_acceso_frontend():
    """Configura el frontend para acceso HTTP y HTTPS"""

    print("🚀 CONFIGURACIÓN ACCESO FRONTEND")
    print("=" * 50)

    # URLs de acceso
    urls_acceso = [
        "http://localhost:5173",
        "https://localhost:5173",
        "http://127.0.0.1:5173",
        f"http://{subprocess.getoutput('hostname').strip()}:5173",
    ]

    print("\n🌐 URLs de acceso disponibles:")
    for i, url in enumerate(urls_acceso, 1):
        print(f"   {i}. {url}")

    print("\n📋 Estado del frontend:")
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=packfy-frontend"],
            capture_output=True,
            text=True,
        )
        if "packfy-frontend" in result.stdout:
            print("   ✅ Frontend container activo")

            # Verificar HTTP
            try:
                result = subprocess.run(
                    [
                        "curl",
                        "-I",
                        "http://localhost:5173/",
                        "--max-time",
                        "5",
                    ],
                    capture_output=True,
                    text=True,
                )
                if "200 OK" in result.stdout:
                    print("   ✅ HTTP accesible: http://localhost:5173")
                else:
                    print("   ❌ HTTP no accesible")
            except:
                print("   ❌ Error verificando HTTP")

        else:
            print("   ❌ Frontend container no encontrado")
    except:
        print("   ❌ Error verificando Docker")

    print("\n🔧 Soluciones si no puedes acceder:")
    print("   1. Usar: http://localhost:5173 (HTTP estándar)")
    print("   2. Limpiar cache del navegador (Ctrl+F5)")
    print("   3. Probar en navegador privado/incógnito")
    print("   4. Verificar firewall/antivirus")
    print("   5. Usar 127.0.0.1:5173 en lugar de localhost")

    print("\n💡 Para acceso desde móvil en LAN:")
    try:
        import socket

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"   📱 URL móvil: http://{local_ip}:5173")
    except:
        print("   📱 No se pudo obtener IP local")

    print("\n🎯 Para habilitar HTTPS (opcional):")
    print("   - Descomenta las líneas HTTPS en vite.config.ts")
    print("   - Reinicia el contenedor: docker restart packfy-frontend")
    print("   - Acepta certificado autofirmado en navegador")


if __name__ == "__main__":
    configurar_acceso_frontend()
