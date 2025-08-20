#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗑️ LIMPIEZA COMPLETA Y ESTRUCTURA SIMPLE

Este script elimina toda la base de datos y crea una estructura limpia y simple.
"""

import subprocess
from datetime import datetime

import requests


def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")


def reset_database():
    """Resetear completamente la base de datos"""
    log("🗑️ PASO 1: Eliminando base de datos completa...")

    commands = [
        # Parar containers
        ["docker-compose", "down"],
        # Eliminar volumen de la base de datos
        ["docker", "volume", "rm", "paqueteria-cuba-mvp_postgres_data"],
        # Levantar solo la base de datos
        ["docker-compose", "up", "-d", "db"],
    ]

    for cmd in commands:
        try:
            log(f"Ejecutando: {' '.join(cmd)}")
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            log("✅ Comando exitoso")
        except subprocess.CalledProcessError as e:
            log(f"⚠️ Comando falló (puede ser normal): {e}")

    # Esperar a que la DB esté lista
    log("⏳ Esperando a que la base de datos esté lista...")
    import time

    time.sleep(10)


def run_migrations():
    """Ejecutar migraciones en base de datos limpia"""
    log("🔄 PASO 2: Ejecutando migraciones...")

    # Levantar backend
    subprocess.run(["docker-compose", "up", "-d", "backend"], check=True)

    # Esperar a que backend esté listo
    import time

    time.sleep(15)

    # Ejecutar migraciones
    result = subprocess.run(
        ["docker", "exec", "packfy-backend", "python", "manage.py", "migrate"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        log("✅ Migraciones ejecutadas correctamente")
    else:
        log(f"❌ Error en migraciones: {result.stderr}")
        return False

    return True


def create_simple_structure():
    """Crear estructura simple y organizada"""
    log("🏗️ PASO 3: Creando estructura simple...")

    django_script = """
from usuarios.models import Usuario
from empresas.models import Empresa, PerfilUsuario
from django.contrib.auth.hashers import make_password

print("=== CREANDO ESTRUCTURA SIMPLE ===")

# 1. CREAR SUPERADMINISTRADOR DEL SISTEMA
print("1. Creando superadministrador...")
superadmin = Usuario.objects.create_user(
    email='superadmin@packfy.com',
    password='super123!',
    username='superadmin@packfy.com',
    first_name='Super',
    last_name='Administrador',
    is_active=True,
    is_staff=True,
    is_superuser=True
)
print(f"✅ Superadmin creado: {superadmin.email}")

# 2. CREAR UNA EMPRESA DE PRUEBA
print("2. Creando empresa de prueba...")
empresa = Empresa.objects.create(
    nombre='Packfy Express',
    slug='packfy-express',
    activo=True
)
print(f"✅ Empresa creada: {empresa.nombre}")

# 3. CREAR DUEÑO DE EMPRESA
print("3. Creando dueño de empresa...")
dueno = Usuario.objects.create_user(
    email='dueno@packfy.com',
    password='dueno123!',
    username='dueno@packfy.com',
    first_name='Carlos',
    last_name='Empresario',
    is_active=True
)

PerfilUsuario.objects.create(
    usuario=dueno,
    empresa=empresa,
    rol='dueno',
    activo=True
)
print(f"✅ Dueño creado: {dueno.email}")

# 4. CREAR OPERADOR MIAMI
print("4. Creando operador Miami...")
miami = Usuario.objects.create_user(
    email='miami@packfy.com',
    password='miami123!',
    username='miami@packfy.com',
    first_name='Ana',
    last_name='Miami',
    is_active=True
)

PerfilUsuario.objects.create(
    usuario=miami,
    empresa=empresa,
    rol='operador_miami',
    activo=True
)
print(f"✅ Operador Miami creado: {miami.email}")

# 5. CREAR OPERADOR CUBA
print("5. Creando operador Cuba...")
cuba = Usuario.objects.create_user(
    email='cuba@packfy.com',
    password='cuba123!',
    username='cuba@packfy.com',
    first_name='Jose',
    last_name='Habana',
    is_active=True
)

PerfilUsuario.objects.create(
    usuario=cuba,
    empresa=empresa,
    rol='operador_cuba',
    activo=True
)
print(f"✅ Operador Cuba creado: {cuba.email}")

# 6. CREAR REMITENTES
print("6. Creando remitentes...")
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
    print(f"✅ Remitente creado: {email}")

# 7. CREAR DESTINATARIOS
print("7. Creando destinatarios...")
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
    print(f"✅ Destinatario creado: {email}")

print("\\n=== ESTRUCTURA CREADA EXITOSAMENTE ===")
print("CREDENCIALES PRINCIPALES:")
print("Superadmin: superadmin@packfy.com / super123!")
print("Dueño: dueno@packfy.com / dueno123!")
print("Miami: miami@packfy.com / miami123!")
print("Cuba: cuba@packfy.com / cuba123!")
print("Remitentes: remitente1@packfy.com / remitente123!")
print("Destinatarios: destinatario1@cuba.cu / destinatario123!")
"""

    # Ejecutar script Django
    try:
        result = subprocess.run(
            [
                "docker",
                "exec",
                "packfy-backend",
                "python",
                "manage.py",
                "shell",
            ],
            input=django_script,
            text=True,
            capture_output=True,
            timeout=60,
        )

        if result.returncode == 0:
            log("✅ Estructura creada exitosamente:")
            print(result.stdout)
            return True
        else:
            log(f"❌ Error creando estructura: {result.stderr}")
            return False
    except Exception as e:
        log(f"❌ Error ejecutando script: {e}")
        return False


def test_superadmin_login():
    """Probar login del superadministrador"""
    log("🧪 PASO 4: Probando login del superadministrador...")

    # Levantar frontend
    subprocess.run(["docker-compose", "up", "-d", "frontend"], check=True)

    # Esperar a que esté listo
    import time

    time.sleep(10)

    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"email": "superadmin@packfy.com", "password": "super123!"},
            timeout=10,
        )

        if response.status_code == 200:
            log("✅ ¡Login del superadmin funciona!")

            token_data = response.json()

            # Probar /usuarios/me/
            me_response = requests.get(
                "http://localhost:8000/api/usuarios/me/",
                headers={"Authorization": f"Bearer {token_data['access']}"},
                timeout=10,
            )

            if me_response.status_code == 200:
                user_data = me_response.json()
                log(f"✅ Datos del usuario: {user_data.get('email')}")
                return True
        else:
            log(f"❌ Error en login: {response.status_code} - {response.text}")
    except Exception as e:
        log(f"❌ Error probando login: {e}")

    return False


def main():
    """Función principal"""
    log("🚀 INICIANDO LIMPIEZA COMPLETA Y RESTRUCTURACIÓN...")
    log("=" * 60)

    # Paso 1: Resetear base de datos
    reset_database()

    # Paso 2: Ejecutar migraciones
    if not run_migrations():
        log("❌ FALLÓ: No se pudieron ejecutar las migraciones")
        return

    # Paso 3: Crear estructura simple
    if not create_simple_structure():
        log("❌ FALLÓ: No se pudo crear la estructura")
        return

    # Paso 4: Probar login
    if test_superadmin_login():
        log("\n🎉 ¡LIMPIEZA Y RESTRUCTURACIÓN COMPLETADA!")
        log("=" * 60)
        log("📧 SUPERADMIN: superadmin@packfy.com")
        log("🔐 PASSWORD: super123!")
        log("🏢 EMPRESA: Packfy Express")
        log("🌐 URL: http://localhost:5173")
        log("=" * 60)
        log("✅ Sistema listo para usar con estructura simple")
    else:
        log("❌ FALLÓ: El login no funciona correctamente")


if __name__ == "__main__":
    main()
