#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ BLINDAJE DE ESTRUCTURA DE DATOS

Este script crea respaldos y protecciones para mantener la estructura durante desarrollo.
"""

import json
import os
import subprocess
from datetime import datetime


def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] 🛡️ {message}")


def crear_respaldo_estructura():
    """Crear respaldo completo de la estructura de datos"""

    log("CREANDO RESPALDO DE ESTRUCTURA...")

    # 1. Crear directorio de respaldos
    backup_dir = "backups_estructura"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        log(f"Directorio {backup_dir} creado")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 2. Respaldo de base de datos
    log("Respaldando base de datos...")
    db_backup_file = f"{backup_dir}/db_estructura_{timestamp}.sql"

    try:
        cmd = [
            "docker",
            "exec",
            "packfy-database",
            "pg_dump",
            "-U",
            "packfy_user",
            "-d",
            "packfy_db",
            "-f",
            f"/tmp/backup_{timestamp}.sql",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            # Copiar desde container al host
            subprocess.run(
                [
                    "docker",
                    "cp",
                    f"packfy-database:/tmp/backup_{timestamp}.sql",
                    db_backup_file,
                ]
            )
            log(f"✅ DB respaldada: {db_backup_file}")
        else:
            log(f"❌ Error respaldando DB: {result.stderr}")
    except Exception as e:
        log(f"❌ Error en respaldo DB: {e}")

    # 3. Crear script de restauración
    crear_script_restauracion(timestamp)

    # 4. Documentar estructura actual
    documentar_estructura_actual(backup_dir, timestamp)

    log("✅ Respaldo completo creado")


def crear_script_restauracion(timestamp):
    """Crear script para restaurar la estructura"""

    script_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 RESTAURAR ESTRUCTURA BLINDADA
Generado automáticamente el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from empresas.models import Empresa, PerfilUsuario

def restaurar_estructura():
    print("🔄 RESTAURANDO ESTRUCTURA BLINDADA...")

    # 1. Limpiar datos actuales
    print("🗑️ Limpiando datos actuales...")
    PerfilUsuario.objects.all().delete()
    Usuario.objects.all().delete()
    Empresa.objects.all().delete()

    # 2. Crear empresa base
    print("🏢 Creando empresa...")
    empresa = Empresa.objects.create(
        nombre='Packfy Express',
        slug='packfy-express',
        activo=True
    )

    # 3. Crear superadministrador
    print("👑 Creando superadministrador...")
    superadmin = Usuario.objects.create_user(
        email='superadmin@packfy.com',
        password='super123!',
        username='superadmin@packfy.com',
        first_name='Super',
        last_name='Administrador',
        is_active=True,
        is_staff=True,
        is_superuser=True,
        es_administrador_empresa=True
    )

    # 4. Crear dueño de empresa
    print("👔 Creando dueño...")
    dueno = Usuario.objects.create_user(
        email='dueno@packfy.com',
        password='dueno123!',
        username='dueno@packfy.com',
        first_name='Carlos',
        last_name='Empresario',
        is_active=True,
        is_staff=True,
        es_administrador_empresa=True
    )

    PerfilUsuario.objects.create(
        usuario=dueno,
        empresa=empresa,
        rol='dueno',
        activo=True
    )

    # 5. Crear operadores
    print("🌴 Creando operadores...")
    miami = Usuario.objects.create_user(
        email='miami@packfy.com',
        password='miami123!',
        username='miami@packfy.com',
        first_name='Ana',
        last_name='Miami',
        is_active=True,
        es_administrador_empresa=True
    )

    PerfilUsuario.objects.create(
        usuario=miami,
        empresa=empresa,
        rol='operador_miami',
        activo=True
    )

    cuba = Usuario.objects.create_user(
        email='cuba@packfy.com',
        password='cuba123!',
        username='cuba@packfy.com',
        first_name='Jose',
        last_name='Habana',
        is_active=True,
        es_administrador_empresa=True
    )

    PerfilUsuario.objects.create(
        usuario=cuba,
        empresa=empresa,
        rol='operador_cuba',
        activo=True
    )

    # 6. Crear remitentes
    print("📦 Creando remitentes...")
    remitentes = [
        ('remitente1@packfy.com', 'Maria', 'Rodriguez'),
        ('remitente2@packfy.com', 'Pedro', 'Gonzalez'),
        ('remitente3@packfy.com', 'Luis', 'Martinez')
    ]

    for email, nombre, apellido in remitentes:
        user = Usuario.objects.create_user(
            email=email,
            password='remitente123!',
            username=email,
            first_name=nombre,
            last_name=apellido,
            is_active=True
        )

        PerfilUsuario.objects.create(
            usuario=user,
            empresa=empresa,
            rol='remitente',
            activo=True
        )

    # 7. Crear destinatarios
    print("🎯 Creando destinatarios...")
    destinatarios = [
        ('destinatario1@cuba.cu', 'Carmen', 'Perez'),
        ('destinatario2@cuba.cu', 'Roberto', 'Silva'),
        ('destinatario3@cuba.cu', 'Elena', 'Fernandez')
    ]

    for email, nombre, apellido in destinatarios:
        user = Usuario.objects.create_user(
            email=email,
            password='destinatario123!',
            username=email,
            first_name=nombre,
            last_name=apellido,
            is_active=True
        )

        PerfilUsuario.objects.create(
            usuario=user,
            empresa=empresa,
            rol='destinatario',
            activo=True
        )

    print(f"✅ ESTRUCTURA RESTAURADA")
    print(f"Usuarios: {{Usuario.objects.count()}}")
    print(f"Empresas: {{Empresa.objects.count()}}")
    print(f"Perfiles: {{PerfilUsuario.objects.count()}}")

if __name__ == "__main__":
    restaurar_estructura()
'''

    with open(
        f"restaurar_estructura_{timestamp}.py", "w", encoding="utf-8"
    ) as f:
        f.write(script_content)

    log(
        f"✅ Script de restauración creado: restaurar_estructura_{timestamp}.py"
    )


def documentar_estructura_actual(backup_dir, timestamp):
    """Documentar la estructura actual en JSON"""

    try:
        import requests

        # Obtener datos via API
        login_response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"email": "superadmin@packfy.com", "password": "super123!"},
            timeout=10,
        )

        if login_response.status_code == 200:
            token = login_response.json()["access"]
            headers = {"Authorization": f"Bearer {token}"}

            estructura_doc = {
                "timestamp": timestamp,
                "fecha": datetime.now().isoformat(),
                "version": "1.0",
                "descripcion": "Estructura blindada para desarrollo",
                "credenciales": {
                    "superadmin": {
                        "email": "superadmin@packfy.com",
                        "password": "super123!",
                        "acceso": "Frontend + Admin Panel",
                    },
                    "dueno": {
                        "email": "dueno@packfy.com",
                        "password": "dueno123!",
                        "acceso": "Frontend + Admin Panel",
                    },
                    "operadores": {
                        "miami": "miami@packfy.com / miami123!",
                        "cuba": "cuba@packfy.com / cuba123!",
                    },
                    "remitentes": "remitente1@packfy.com / remitente123!",
                    "destinatarios": "destinatario1@cuba.cu / destinatario123!",
                },
            }

            doc_file = f"{backup_dir}/estructura_documentada_{timestamp}.json"
            with open(doc_file, "w", encoding="utf-8") as f:
                json.dump(estructura_doc, f, indent=2, ensure_ascii=False)

            log(f"✅ Estructura documentada: {doc_file}")

    except Exception as e:
        log(f"❌ Error documentando estructura: {e}")


def main():
    """Función principal"""
    log("🛡️ INICIANDO BLINDAJE DE ESTRUCTURA")
    log("=" * 60)

    crear_respaldo_estructura()

    log("=" * 60)
    log("🛡️ BLINDAJE COMPLETADO")
    log("Files creados:")
    log("- Respaldo de DB en backups_estructura/")
    log("- Script de restauración")
    log("- Documentación de estructura")


if __name__ == "__main__":
    main()
