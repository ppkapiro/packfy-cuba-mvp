from django.core.management.base import BaseCommand
import psycopg2
from django.conf import settings
from django.db import connection

class Command(BaseCommand):
    help = 'Limpia completamente la base de datos eliminando todos los esquemas. USAR CON PRECAUCIÓN.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar la ejecución sin confirmación',
        )

    def handle(self, *args, **kwargs):
        if not kwargs.get('force'):
            self.stdout.write(self.style.WARNING(
                'ADVERTENCIA: Este comando eliminará TODOS los esquemas y datos de la base de datos.\n'
                'Para continuar, ejecuta nuevamente con el parámetro --force'
            ))
            return

        # Conectar directamente a PostgreSQL para borrar esquemas
        db_settings = settings.DATABASES['default']
        conn = psycopg2.connect(
            dbname=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            host=db_settings['HOST'],
            port=db_settings['PORT']
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Obtener todos los esquemas excepto los del sistema
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT LIKE 'pg_%' AND schema_name != 'information_schema';")
        schemas = [row[0] for row in cursor.fetchall()]
        
        # Borrar cada esquema
        for schema in schemas:
            if schema == 'public':
                self.stdout.write(self.style.WARNING(f'Limpiando esquema público en lugar de eliminarlo...'))
                # Para public, solo borramos las tablas pero mantenemos el esquema
                cursor.execute(f"DROP SCHEMA {schema} CASCADE;")
                cursor.execute(f"CREATE SCHEMA {schema};")
            else:
                self.stdout.write(self.style.WARNING(f'Eliminando esquema: {schema}'))
                cursor.execute(f"DROP SCHEMA {schema} CASCADE;")
        
        cursor.close()
        conn.close()
        
        self.stdout.write(self.style.SUCCESS('Base de datos limpiada exitosamente. Se han eliminado todos los esquemas.'))
        self.stdout.write(self.style.WARNING('Recuerda ejecutar las migraciones nuevamente para reconstruir la base de datos.'))
