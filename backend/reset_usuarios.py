#!/usr/bin/env python
"""
Script simple para gestionar usuarios - Packfy Cuba
"""
import os
import django

# Configuración Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario

def main():
    print("🔍 REVISANDO USUARIOS EXISTENTES...")
    
    # Listar todos los usuarios
    usuarios = Usuario.objects.all()
    print(f"Total usuarios encontrados: {usuarios.count()}")
    
    if usuarios.exists():
        print("\n📋 USUARIOS ACTUALES:")
        for user in usuarios:
            print(f"   📧 {user.email} (username: {user.username})")
            print(f"      Nombre: {user.first_name} {user.last_name}")
            print(f"      Activo: {user.is_active}, Admin: {user.is_superuser}")
    
    print("\n🔄 RECREANDO USUARIOS DE PRUEBA...")
    
    # Eliminar usuarios existentes
    Usuario.objects.all().delete()
    print("   ✅ Usuarios anteriores eliminados")
    
    # Crear usuarios nuevos
    usuarios_nuevos = [
        {
            'email': 'admin@packfy.cu',
            'username': 'admin',
            'first_name': 'Admin',
            'last_name': 'Packfy',
            'password': 'admin123',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'email': 'empresa@test.cu', 
            'username': 'empresa',
            'first_name': 'Empresa',
            'last_name': 'Test',
            'password': 'empresa123',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'email': 'cliente@test.cu',
            'username': 'cliente', 
            'first_name': 'Cliente',
            'last_name': 'Test',
            'password': 'cliente123',
            'is_staff': False,
            'is_superuser': False
        }
    ]
    
    for datos in usuarios_nuevos:
        user = Usuario.objects.create_user(
            email=datos['email'],
            username=datos['username'],
            first_name=datos['first_name'],
            last_name=datos['last_name'],
            password=datos['password']
        )
        user.is_staff = datos['is_staff']
        user.is_superuser = datos['is_superuser']
        user.is_active = True
        user.save()
        print(f"   ✅ Creado: {datos['email']}")
    
    print("\n🔑 CREDENCIALES DE ACCESO:")
    print("========================")
    for datos in usuarios_nuevos:
        tipo = "👑 ADMIN" if datos['is_superuser'] else "👤 USER"
        print(f"{tipo} | Email: {datos['email']} | Password: {datos['password']}")
    
    print("\n✅ PROCESO COMPLETADO")

if __name__ == "__main__":
    main()
