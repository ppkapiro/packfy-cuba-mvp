#!/usr/bin/env python
"""
Script para crear usuarios de prueba en Packfy Cuba - ESTABLE
"""
import os
import sys
import django

# Configurar Django con ruta absoluta correcta
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    from django.contrib.auth import get_user_model
    from usuarios.models import Usuario
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def crear_usuarios_prueba():
    """Crear usuarios de prueba estables para la aplicación"""
    
    usuarios_prueba = [
        {
            'email': 'admin@packfy.cu',
            'username': 'admin',
            'nombre': 'Administrador',
            'apellidos': 'Packfy Cuba',
            'password': 'admin123',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        },
        {
            'email': 'empresa@test.cu',
            'username': 'empresa',
            'nombre': 'Empresa',
            'apellidos': 'Test',
            'password': 'empresa123',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True
        },
        {
            'email': 'cliente@test.cu',
            'username': 'cliente',
            'nombre': 'Cliente',
            'apellidos': 'Test',
            'password': 'cliente123',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True
        }
    ]
    
    print("🔄 Creando usuarios de prueba...")
    
    for usuario_data in usuarios_prueba:
        try:
            # Verificar si el usuario ya existe
            if Usuario.objects.filter(email=usuario_data['email']).exists():
                print(f"   ⚠️ Usuario {usuario_data['email']} ya existe, actualizando...")
                usuario = Usuario.objects.get(email=usuario_data['email'])
                usuario.nombre = usuario_data['nombre']
                usuario.apellidos = usuario_data['apellidos']
                usuario.is_staff = usuario_data['is_staff']
                usuario.is_superuser = usuario_data['is_superuser']
                usuario.is_active = usuario_data['is_active']
                usuario.set_password(usuario_data['password'])
                usuario.save()
                print(f"   ✅ Usuario {usuario_data['email']} actualizado")
            else:
                # Crear nuevo usuario
                usuario = Usuario.objects.create_user(
                    email=usuario_data['email'],
                    username=usuario_data['username'],
                    nombre=usuario_data['nombre'],
                    apellidos=usuario_data['apellidos'],
                    password=usuario_data['password']
                )
                usuario.is_staff = usuario_data['is_staff']
                usuario.is_superuser = usuario_data['is_superuser']
                usuario.is_active = usuario_data['is_active']
                usuario.save()
                print(f"   ✅ Usuario {usuario_data['email']} creado")
                
        except Exception as e:
            print(f"   ❌ Error creando {usuario_data['email']}: {e}")
    
    print("\n📊 Resumen de usuarios:")
    total_usuarios = Usuario.objects.count()
    admins = Usuario.objects.filter(is_superuser=True).count()
    activos = Usuario.objects.filter(is_active=True).count()
    
    print(f"   Total de usuarios: {total_usuarios}")
    print(f"   Administradores: {admins}")
    print(f"   Usuarios activos: {activos}")
    
    print("\n🔑 Credenciales de acceso:")
    for usuario_data in usuarios_prueba:
        print(f"   {usuario_data['email']} / {usuario_data['password']}")

if __name__ == "__main__":
    print("🚀 INICIANDO CREACIÓN DE USUARIOS DE PRUEBA")
    print("==========================================")
    crear_usuarios_prueba()
    print("\n✅ PROCESO COMPLETADO")
