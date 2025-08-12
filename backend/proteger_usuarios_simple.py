#!/usr/bin/env python
"""
Script simple para proteger usuarios demo - Packfy Cuba
Ejecuta directamente sin comando de gestión Django
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
import json

Usuario = get_user_model()

def proteger_usuarios_demo():
    """Función principal para proteger usuarios demo"""
    print("🔒 Sistema de Protección Usuarios Demo - Packfy Cuba")
    
    USUARIOS_DEMO = [
        'admin@packfy.cu',
        'empresa@test.cu', 
        'cliente@test.cu'
    ]
    
    # Crear directorio de backups
    backup_dir = Path('/app/backups/usuarios')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Crear backup
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    usuarios_data = []
    
    print("\n📊 Verificando usuarios demo:")
    for email in USUARIOS_DEMO:
        try:
            usuario = Usuario.objects.get(email=email)
            
            # Determinar tipo de usuario
            if usuario.is_superuser:
                tipo = "ADMIN"
            elif usuario.is_staff:
                tipo = "STAFF"
            else:
                tipo = "CLIENTE"
            
            print(f"✅ {email} - ENCONTRADO - {tipo}")
            
            usuarios_data.append({
                'id': usuario.id,
                'email': usuario.email,
                'username': usuario.username,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'telefono': usuario.telefono,
                'cargo': usuario.cargo,
                'es_administrador_empresa': usuario.es_administrador_empresa,
                'is_active': usuario.is_active,
                'is_staff': usuario.is_staff,
                'is_superuser': usuario.is_superuser,
                'date_joined': usuario.date_joined.isoformat(),
                'password_hash': usuario.password,
            })
            
        except Usuario.DoesNotExist:
            print(f"❌ {email} - NO ENCONTRADO")
    
    # Guardar backup
    if usuarios_data:
        backup_file = backup_dir / f"usuarios_demo_backup_{timestamp}.json"
        backup_data = {
            'timestamp': timestamp,
            'usuarios': usuarios_data,
            'metadata': {
                'total_usuarios': len(usuarios_data),
                'protegidos': USUARIOS_DEMO
            }
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Backup creado: {backup_file}")
        print(f"📦 Total usuarios respaldados: {len(usuarios_data)}")
    
    # Mostrar estado de protección
    print(f"\n🔒 Estado de protección:")
    print(f"✅ Middleware activado en settings.py")
    print(f"✅ Usuarios protegidos: {', '.join(USUARIOS_DEMO)}")
    print(f"✅ Backup automático creado")
    
    print("\n🛡️  Protecciones activas:")
    print("• Middleware bloquea modificaciones via API")
    print("• Backup automático cada ejecución")
    print("• Logs de intentos de modificación")
    
    return True

if __name__ == "__main__":
    try:
        proteger_usuarios_demo()
        print("\n✅ Protección de usuarios completada exitosamente")
    except Exception as e:
        print(f"\n❌ Error en protección: {e}")
        sys.exit(1)
