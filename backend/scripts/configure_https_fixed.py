#!/usr/bin/env python3
"""
Configuración HTTPS para Packfy Cuba
Genera certificados SSL autofirmados y configura el servidor HTTPS
"""

import os
import subprocess
import sys
from pathlib import Path


def ensure_directory(path):
    """Asegura que el directorio existe"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def generate_ssl_certificates():
    """Genera certificados SSL autofirmados"""
    cert_dir = ensure_directory("/app/certs")
    cert_file = os.path.join(cert_dir, "cert.crt")
    key_file = os.path.join(cert_dir, "cert.key")

    # Si ya existen los certificados, no los regeneramos
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("✅ Certificados SSL ya existen")
        return True

    print("🔧 Generando certificados SSL autofirmados...")

    try:
        # Comando OpenSSL para generar certificados autofirmados
        cmd = [
            "openssl",
            "req",
            "-x509",
            "-newkey",
            "rsa:4096",
            "-keyout",
            key_file,
            "-out",
            cert_file,
            "-days",
            "365",
            "-nodes",
            "-subj",
            "/C=CU/ST=Havana/L=Havana/O=Packfy Cuba/CN=localhost",
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )

        # Configurar permisos apropiados
        os.chmod(key_file, 0o600)
        os.chmod(cert_file, 0o644)

        print("✅ Certificados SSL generados correctamente")
        print(f"   📄 Certificado: {cert_file}")
        print(f"   🔑 Clave privada: {key_file}")

        return True

    except FileNotFoundError:
        print("❌ OpenSSL no está instalado. Instalando...")
        try:
            # Intentar instalar OpenSSL
            subprocess.run(
                ["apt-get", "update"], check=True, capture_output=True
            )
            subprocess.run(
                ["apt-get", "install", "-y", "openssl"],
                check=True,
                capture_output=True,
            )

            # Intentar nuevamente
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )

            os.chmod(key_file, 0o600)
            os.chmod(cert_file, 0o644)

            print("✅ OpenSSL instalado y certificados generados")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando OpenSSL: {e}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Error generando certificados: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return False


def configure_django_https():
    """Configura Django para HTTPS"""
    print("🔧 Configurando Django para HTTPS...")

    # Variables de entorno para HTTPS
    os.environ["SECURE_SSL_REDIRECT"] = "False"  # Lo manejamos manualmente
    os.environ["SECURE_PROXY_SSL_HEADER"] = "1"
    os.environ["USE_TLS"] = "True"

    print("✅ Django configurado para HTTPS")


def verify_configuration():
    """Verifica que la configuración HTTPS esté correcta"""
    cert_file = "/app/certs/cert.crt"
    key_file = "/app/certs/cert.key"

    if not os.path.exists(cert_file):
        print(f"❌ Certificado no encontrado: {cert_file}")
        return False

    if not os.path.exists(key_file):
        print(f"❌ Clave privada no encontrada: {key_file}")
        return False

    # Verificar permisos
    cert_stat = os.stat(cert_file)
    key_stat = os.stat(key_file)

    print(
        f"📄 Certificado: {cert_file} (permisos: {oct(cert_stat.st_mode)[-3:]})"
    )
    print(
        f"🔑 Clave privada: {key_file} (permisos: {oct(key_stat.st_mode)[-3:]})"
    )

    return True


def main():
    """Función principal"""
    print("🇨🇺 PACKFY CUBA - Configuración HTTPS")
    print("=" * 50)

    try:
        # Generar certificados SSL
        if not generate_ssl_certificates():
            print("❌ Error generando certificados SSL")
            sys.exit(1)

        # Configurar Django
        configure_django_https()

        # Verificar configuración
        if not verify_configuration():
            print("❌ Error en la verificación de configuración")
            sys.exit(1)

        print("=" * 50)
        print("✅ Configuración HTTPS completada correctamente")
        print("🌐 El servidor podrá usar tanto HTTP como HTTPS")
        print("   📍 HTTP:  http://localhost:8000")
        print("   🔒 HTTPS: https://localhost:8443")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
