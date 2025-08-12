"""
Comando Django para proteger usuarios demo de Packfy Cuba
Uso: python manage.py proteger_usuarios [--backup] [--restaurar ARCHIVO]
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import json
import os
from pathlib import Path

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Protege usuarios demo creando backups y aplicando restricciones'
    
    USUARIOS_DEMO = [
        'admin@packfy.cu',
        'empresa@test.cu',
        'cliente@test.cu'
    ]
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Crear backup de usuarios demo'
        )
        
        parser.add_argument(
            '--restaurar',
            type=str,
            help='Restaurar usuarios desde archivo backup'
        )
        
        parser.add_argument(
            '--verificar',
            action='store_true', 
            help='Verificar integridad de usuarios demo'
        )
        
        parser.add_argument(
            '--listar-backups',
            action='store_true',
            help='Listar archivos de backup disponibles'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🔒 Sistema de Protección Usuarios Demo - Packfy Cuba"))
        
        if options['backup']:
            self.crear_backup()
        elif options['restaurar']:
            self.restaurar_backup(options['restaurar'])
        elif options['verificar']:
            self.verificar_usuarios()
        elif options['listar_backups']:
            self.listar_backups()
        else:
            self.mostrar_estado()
    
    def crear_backup(self):
        """Crear backup de usuarios demo"""
        try:
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = Path('backups/usuarios')
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            usuarios_data = []
            for email in self.USUARIOS_DEMO:
                try:
                    usuario = Usuario.objects.get(email=email)
                    usuarios_data.append({
                        'id': usuario.id,
                        'email': usuario.email,
                        'first_name': usuario.first_name,
                        'last_name': usuario.last_name,
                        'tipo_usuario': usuario.tipo_usuario,
                        'is_active': usuario.is_active,
                        'is_staff': usuario.is_staff,
                        'is_superuser': usuario.is_superuser,
                        'date_joined': usuario.date_joined.isoformat(),
                        'password_hash': usuario.password,
                    })
                    self.stdout.write(f"✅ Backup creado para: {email}")
                except Usuario.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"⚠️  Usuario no encontrado: {email}"))
            
            backup_file = backup_dir / f"usuarios_demo_backup_{timestamp}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': timestamp,
                    'usuarios': usuarios_data,
                    'metadata': {
                        'total_usuarios': len(usuarios_data),
                        'protegidos': self.USUARIOS_DEMO
                    }
                }, f, indent=2, ensure_ascii=False)
            
            self.stdout.write(self.style.SUCCESS(f"💾 Backup guardado en: {backup_file}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error creando backup: {e}"))
    
    def restaurar_backup(self, archivo_backup):
        """Restaurar usuarios desde backup"""
        try:
            backup_path = Path(archivo_backup)
            if not backup_path.exists():
                # Buscar en directorio de backups
                backup_path = Path('backups/usuarios') / archivo_backup
                if not backup_path.exists():
                    self.stdout.write(self.style.ERROR(f"❌ Archivo no encontrado: {archivo_backup}"))
                    return
            
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            self.stdout.write(f"📂 Restaurando desde: {backup_path}")
            self.stdout.write(f"📅 Backup del: {backup_data.get('timestamp', 'Desconocido')}")
            
            for usuario_data in backup_data['usuarios']:
                email = usuario_data['email']
                try:
                    usuario, created = Usuario.objects.get_or_create(
                        email=email,
                        defaults={
                            'first_name': usuario_data['first_name'],
                            'last_name': usuario_data['last_name'],
                            'tipo_usuario': usuario_data['tipo_usuario'],
                            'is_active': usuario_data['is_active'],
                            'is_staff': usuario_data['is_staff'],
                            'is_superuser': usuario_data['is_superuser'],
                            'password': usuario_data['password_hash'],
                        }
                    )
                    
                    if not created:
                        # Actualizar usuario existente
                        usuario.first_name = usuario_data['first_name']
                        usuario.last_name = usuario_data['last_name']
                        usuario.tipo_usuario = usuario_data['tipo_usuario']
                        usuario.is_active = usuario_data['is_active']
                        usuario.is_staff = usuario_data['is_staff']
                        usuario.is_superuser = usuario_data['is_superuser']
                        usuario.password = usuario_data['password_hash']
                        usuario.save()
                        self.stdout.write(f"🔄 Usuario actualizado: {email}")
                    else:
                        self.stdout.write(f"✅ Usuario creado: {email}")
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Error con usuario {email}: {e}"))
            
            self.stdout.write(self.style.SUCCESS("✅ Restauración completada"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error en restauración: {e}"))
    
    def verificar_usuarios(self):
        """Verificar estado de usuarios demo"""
        self.stdout.write("🔍 Verificando usuarios demo...")
        
        for email in self.USUARIOS_DEMO:
            try:
                usuario = Usuario.objects.get(email=email)
                estado = "✅ ACTIVO" if usuario.is_active else "❌ INACTIVO"
                tipo = usuario.get_tipo_usuario_display()
                self.stdout.write(f"👤 {email} - {estado} - {tipo}")
            except Usuario.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"❌ FALTA: {email}"))
    
    def listar_backups(self):
        """Listar archivos de backup disponibles"""
        backup_dir = Path('backups/usuarios')
        if not backup_dir.exists():
            self.stdout.write("📁 No hay directorio de backups")
            return
        
        backups = list(backup_dir.glob("usuarios_demo_backup_*.json"))
        if not backups:
            self.stdout.write("📁 No hay backups disponibles")
            return
        
        self.stdout.write("📁 Backups disponibles:")
        for backup in sorted(backups, reverse=True):
            size = backup.stat().st_size
            self.stdout.write(f"  📄 {backup.name} ({size} bytes)")
    
    def mostrar_estado(self):
        """Mostrar estado actual del sistema"""
        self.stdout.write("📊 Estado actual del sistema:")
        self.verificar_usuarios()
        self.stdout.write("\n📁 Archivos de backup:")
        self.listar_backups()
        self.stdout.write("\n💡 Comandos disponibles:")
        self.stdout.write("  --backup          Crear backup")
        self.stdout.write("  --verificar       Verificar usuarios")
        self.stdout.write("  --restaurar FILE  Restaurar backup")
        self.stdout.write("  --listar-backups  Ver backups")
