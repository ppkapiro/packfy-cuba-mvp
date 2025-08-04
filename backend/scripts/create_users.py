#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from empresas.models import Empresa

def main():
    print("=== CREANDO USUARIOS DE PRUEBA ===")
    
    # Crear empresa si no existe
    empresa, created = Empresa.objects.get_or_create(
        nombre='Packfy Demo',
        defaults={
            'dominio': 'demo.packfy.com',
            'direccion': 'Calle 23 #512, La Habana, Cuba',
            'telefono': '+53 555-1234',
            'email': 'info@packfy.com',
            'activo': True,
            'ruc': '12345678901'
        }
    )
    print(f"Empresa: {empresa.nombre} ({'creada' if created else 'existente'})")

    # Crear usuarios
    usuarios_data = [
        {'email': 'admin@packfy.com', 'nombre': 'Admin', 'apellido': 'Sistema', 'password': 'admin123'},
        {'email': 'demo@packfy.com', 'nombre': 'Demo', 'apellido': 'Usuario', 'password': 'demo123'},
        {'email': 'test@test.com', 'nombre': 'Test', 'apellido': 'User', 'password': '123456'}
    ]

    for data in usuarios_data:
        try:
            # Eliminar usuario si ya existe para recrearlo con nueva contraseña
            Usuario.objects.filter(email=data['email']).delete()
            
            usuario = Usuario.objects.create_user(
                email=data['email'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                empresa=empresa,
                password=data['password']
            )
            print(f"✅ Usuario creado: {usuario.email} / {data['password']}")
        except Exception as e:
            print(f"❌ Error creando {data['email']}: {e}")

    # Verificar usuarios creados
    print("\n=== USUARIOS EN BASE DE DATOS ===")
    for usuario in Usuario.objects.all():
        print(f"- {usuario.email} ({usuario.nombre} {usuario.apellido})")
    
    print(f"\nTotal usuarios: {Usuario.objects.count()}")

if __name__ == '__main__':
    main()
