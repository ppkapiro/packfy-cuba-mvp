import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario

print("=== LIMPIEZA COMPLETA DE USUARIOS ===")

# Limpiar todos los usuarios existentes
usuarios_count = Usuario.objects.count()
print(f"Eliminando {usuarios_count} usuarios existentes...")
Usuario.objects.all().delete()

# Limpiar todas las empresas existentes
empresas_count = Empresa.objects.count()
print(f"Eliminando {empresas_count} empresas existentes...")
Empresa.objects.all().delete()

print("✅ Base de datos limpia")

print("\n=== CREANDO ESTRUCTURA SIMPLE ===")

# 1. CREAR SUPERADMINISTRADOR DEL SISTEMA
print("1. Creando superadministrador...")
superadmin = Usuario.objects.create_user(
    email="superadmin@packfy.com",
    password="super123!",
    username="superadmin@packfy.com",
    first_name="Super",
    last_name="Administrador",
    is_active=True,
    is_staff=True,
    is_superuser=True,
)
print(f"✅ Superadmin creado: {superadmin.email}")

# 2. CREAR UNA EMPRESA DE PRUEBA
print("2. Creando empresa de prueba...")
empresa = Empresa.objects.create(
    nombre="Packfy Express", slug="packfy-express", activo=True
)
print(f"✅ Empresa creada: {empresa.nombre}")

# 3. CREAR DUEÑO DE EMPRESA
print("3. Creando dueño de empresa...")
dueno = Usuario.objects.create_user(
    email="dueno@packfy.com",
    password="dueno123!",
    username="dueno@packfy.com",
    first_name="Carlos",
    last_name="Empresario",
    is_active=True,
)

PerfilUsuario.objects.create(
    usuario=dueno, empresa=empresa, rol="dueno", activo=True
)
print(f"✅ Dueño creado: {dueno.email}")

# 4. CREAR OPERADOR MIAMI
print("4. Creando operador Miami...")
miami = Usuario.objects.create_user(
    email="miami@packfy.com",
    password="miami123!",
    username="miami@packfy.com",
    first_name="Ana",
    last_name="Miami",
    is_active=True,
)

PerfilUsuario.objects.create(
    usuario=miami, empresa=empresa, rol="operador_miami", activo=True
)
print(f"✅ Operador Miami creado: {miami.email}")

# 5. CREAR OPERADOR CUBA
print("5. Creando operador Cuba...")
cuba = Usuario.objects.create_user(
    email="cuba@packfy.com",
    password="cuba123!",
    username="cuba@packfy.com",
    first_name="Jose",
    last_name="Habana",
    is_active=True,
)

PerfilUsuario.objects.create(
    usuario=cuba, empresa=empresa, rol="operador_cuba", activo=True
)
print(f"✅ Operador Cuba creado: {cuba.email}")

# 6. CREAR REMITENTES
print("6. Creando remitentes...")
remitentes = [
    ("remitente1@packfy.com", "Maria", "Rodriguez"),
    ("remitente2@packfy.com", "Pedro", "Gonzalez"),
    ("remitente3@packfy.com", "Luis", "Martinez"),
]

for email, nombre, apellido in remitentes:
    user = Usuario.objects.create_user(
        email=email,
        password="remitente123!",
        username=email,
        first_name=nombre,
        last_name=apellido,
        is_active=True,
    )

    PerfilUsuario.objects.create(
        usuario=user, empresa=empresa, rol="remitente", activo=True
    )
    print(f"✅ Remitente creado: {email}")

# 7. CREAR DESTINATARIOS
print("7. Creando destinatarios...")
destinatarios = [
    ("destinatario1@cuba.cu", "Carmen", "Perez"),
    ("destinatario2@cuba.cu", "Roberto", "Silva"),
    ("destinatario3@cuba.cu", "Elena", "Fernandez"),
]

for email, nombre, apellido in destinatarios:
    user = Usuario.objects.create_user(
        email=email,
        password="destinatario123!",
        username=email,
        first_name=nombre,
        last_name=apellido,
        is_active=True,
    )

    PerfilUsuario.objects.create(
        usuario=user, empresa=empresa, rol="destinatario", activo=True
    )
    print(f"✅ Destinatario creado: {email}")

print("\n=== ESTRUCTURA CREADA EXITOSAMENTE ===")
print("CREDENCIALES PRINCIPALES:")
print("• Superadmin: superadmin@packfy.com / super123!")
print("• Dueño: dueno@packfy.com / dueno123!")
print("• Miami: miami@packfy.com / miami123!")
print("• Cuba: cuba@packfy.com / cuba123!")
print("• Remitentes: remitente1@packfy.com / remitente123!")
print("• Destinatarios: destinatario1@cuba.cu / destinatario123!")

print(f"\nTotal usuarios creados: {Usuario.objects.count()}")
print(f"Total empresas creadas: {Empresa.objects.count()}")
