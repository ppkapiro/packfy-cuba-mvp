#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario

print("📊 USUARIOS EN LA BASE DE DATOS:")
print("================================")

try:
    usuarios = Usuario.objects.all()
    if usuarios.exists():
        for usuario in usuarios:
            print(f"✅ Email: {usuario.email}")
            print(f"   Username: {usuario.username}")
            print(f"   Nombre completo: {usuario.nombre} {usuario.apellidos}")
            print(f"   Activo: {usuario.is_active}")
            print(f"   Admin: {usuario.is_superuser}")
            print(f"   Staff: {usuario.is_staff}")
            print("-" * 40)
        
        print(f"\n📈 Total usuarios: {usuarios.count()}")
        
        print("\n🔑 CREDENCIALES PARA PRUEBAS:")
        print("============================")
        print("Para hacer login, usa estas credenciales:")
        for usuario in usuarios:
            # Las contraseñas están hasheadas, así que muestro las del script
            if usuario.email == 'admin@packfy.cu':
                print(f"📧 {usuario.email} | 🔐 admin123")
            elif usuario.email == 'empresa@test.cu':
                print(f"📧 {usuario.email} | 🔐 empresa123")
            elif usuario.email == 'cliente@test.cu':
                print(f"📧 {usuario.email} | 🔐 cliente123")
            else:
                print(f"📧 {usuario.email} | 🔐 (contraseña desconocida)")
    else:
        print("⚠️ No hay usuarios en la base de datos")
        
except Exception as e:
    print(f"❌ Error consultando usuarios: {e}")
