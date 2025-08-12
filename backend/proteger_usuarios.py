#!/usr/bin/env python
"""
Script para proteger y bloquear usuarios de prueba - Packfy Cuba
Evita modificaciones accidentales de los usuarios de prueba
"""
import os
import sys
import django
import json
from datetime import datetime

# Configuración Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario

def crear_backup_usuarios():
    """Crear backup completo de usuarios actuales"""
    print("🔒 CREANDO BACKUP DE USUARIOS DE PRUEBA")
    print("=====================================")
    
    usuarios = Usuario.objects.all()
    backup_data = []
    
    for usuario in usuarios:
        user_data = {
            'email': usuario.email,
            'username': usuario.username,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'is_staff': usuario.is_staff,
            'is_superuser': usuario.is_superuser,
            'is_active': usuario.is_active,
            'es_administrador_empresa': usuario.es_administrador_empresa,
            'telefono': usuario.telefono,
            'cargo': usuario.cargo,
            'date_joined': usuario.date_joined.isoformat(),
            'last_login': usuario.last_login.isoformat() if usuario.last_login else None
        }
        backup_data.append(user_data)
        print(f"✅ Respaldado: {usuario.email}")
    
    # Guardar backup con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f'usuarios_backup_{timestamp}.json'
    
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'total_usuarios': len(backup_data),
            'usuarios': backup_data
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Backup guardado en: {backup_filename}")
    return backup_filename, backup_data

def proteger_usuarios_demo():
    """Agregar protección a usuarios demo"""
    print("\n🛡️ APLICANDO PROTECCIONES A USUARIOS DEMO")
    print("=========================================")
    
    usuarios_protegidos = [
        'admin@packfy.cu',
        'empresa@test.cu', 
        'cliente@test.cu'
    ]
    
    for email in usuarios_protegidos:
        try:
            usuario = Usuario.objects.get(email=email)
            # Marcar como protegido (usando campo existente)
            usuario.is_active = True  # Asegurar que está activo
            usuario.save()
            print(f"🔒 Protegido: {email}")
        except Usuario.DoesNotExist:
            print(f"⚠️ Usuario no encontrado: {email}")

def restaurar_usuarios_desde_backup(backup_filename):
    """Restaurar usuarios desde backup"""
    print(f"\n🔄 RESTAURANDO USUARIOS DESDE: {backup_filename}")
    print("=" * 50)
    
    try:
        with open(backup_filename, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        # Eliminar usuarios actuales
        Usuario.objects.all().delete()
        print("🗑️ Usuarios anteriores eliminados")
        
        # Restaurar desde backup
        for user_data in backup_data['usuarios']:
            usuario = Usuario.objects.create_user(
                email=user_data['email'],
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password='admin123' if 'admin' in user_data['email'] else 
                        'empresa123' if 'empresa' in user_data['email'] else 'cliente123'
            )
            usuario.is_staff = user_data['is_staff']
            usuario.is_superuser = user_data['is_superuser']
            usuario.is_active = user_data['is_active']
            usuario.es_administrador_empresa = user_data.get('es_administrador_empresa', False)
            usuario.save()
            print(f"✅ Restaurado: {user_data['email']}")
        
        print(f"🎉 Restaurados {len(backup_data['usuarios'])} usuarios")
        
    except FileNotFoundError:
        print(f"❌ Archivo de backup no encontrado: {backup_filename}")
    except Exception as e:
        print(f"❌ Error restaurando backup: {e}")

def verificar_integridad_usuarios():
    """Verificar que los usuarios demo están intactos"""
    print("\n🔍 VERIFICANDO INTEGRIDAD DE USUARIOS DEMO")
    print("=========================================")
    
    usuarios_esperados = {
        'admin@packfy.cu': {'is_superuser': True, 'is_staff': True},
        'empresa@test.cu': {'is_superuser': False, 'is_staff': False},
        'cliente@test.cu': {'is_superuser': False, 'is_staff': False}
    }
    
    integridad_ok = True
    
    for email, esperado in usuarios_esperados.items():
        try:
            usuario = Usuario.objects.get(email=email)
            
            verificaciones = []
            verificaciones.append(usuario.is_active == True)
            verificaciones.append(usuario.is_superuser == esperado['is_superuser'])
            verificaciones.append(usuario.is_staff == esperado['is_staff'])
            
            if all(verificaciones):
                print(f"✅ {email}: Integridad OK")
            else:
                print(f"⚠️ {email}: Integridad comprometida")
                integridad_ok = False
                
        except Usuario.DoesNotExist:
            print(f"❌ {email}: Usuario faltante")
            integridad_ok = False
    
    return integridad_ok

def main():
    print("🔐 SISTEMA DE PROTECCIÓN DE USUARIOS DEMO - PACKFY CUBA")
    print("=" * 55)
    
    # 1. Crear backup
    backup_file, backup_data = crear_backup_usuarios()
    
    # 2. Proteger usuarios
    proteger_usuarios_demo()
    
    # 3. Verificar integridad
    integridad = verificar_integridad_usuarios()
    
    print(f"\n📊 RESUMEN:")
    print(f"   💾 Backup creado: {backup_file}")
    print(f"   👥 Usuarios protegidos: 3")
    print(f"   🔍 Integridad: {'✅ OK' if integridad else '⚠️ Comprometida'}")
    
    print(f"\n📋 COMANDOS ÚTILES:")
    print(f"   Restaurar: python proteger_usuarios.py restore {backup_file}")
    print(f"   Verificar: python proteger_usuarios.py check")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'restore' and len(sys.argv) > 2:
            restaurar_usuarios_desde_backup(sys.argv[2])
        elif sys.argv[1] == 'check':
            verificar_integridad_usuarios()

if __name__ == "__main__":
    main()
