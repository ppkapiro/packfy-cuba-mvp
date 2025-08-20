#!/usr/bin/env python3
"""
Script simple para resetear credenciales admin
"""

import json
import subprocess

# Script Django sin caracteres especiales
django_script = """
from usuarios.models import Usuario
from empresas.models import Empresa, PerfilUsuario

# Eliminar usuario admin si existe
try:
    old_user = Usuario.objects.get(email='admin@packfy.com')
    old_user.delete()
    print('Usuario anterior eliminado')
except Usuario.DoesNotExist:
    print('No habia usuario anterior')

# Crear empresa
empresa, created = Empresa.objects.get_or_create(
    slug='miami-shipping',
    defaults={
        'nombre': 'Miami Shipping Co',
        'activo': True
    }
)

# Crear nuevo usuario admin
admin_user = Usuario.objects.create_user(
    email='admin@packfy.com',
    password='admin123!',
    username='admin@packfy.com',
    first_name='Administrador',
    last_name='Sistema',
    is_active=True,
    is_staff=True,
    is_superuser=True
)

# Crear perfil
perfil, created = PerfilUsuario.objects.get_or_create(
    usuario=admin_user,
    empresa=empresa,
    defaults={
        'rol': 'dueno',
        'activo': True
    }
)

print('===== CREDENCIALES =====')
print('Email: admin@packfy.com')
print('Password: admin123!')
print('Empresa: Miami Shipping Co')
print('========================')
"""

# Ejecutar
result = subprocess.run(
    ["docker", "exec", "packfy-backend", "python", "manage.py", "shell"],
    input=django_script,
    text=True,
    capture_output=True,
)

print("SALIDA:")
print(result.stdout)

if result.stderr:
    print("ERRORES:")
    print(result.stderr)
