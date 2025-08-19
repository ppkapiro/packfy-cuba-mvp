"""
Comando para crear datos de prueba multi-tenant.
Crea empresas, usuarios y roles para validar el sistema.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from empresas.models import Empresa, PerfilUsuario
from empresas.utils import TenantUtils

User = get_user_model()


class Command(BaseCommand):
    help = "Crea datos de prueba multi-tenant para validar el sistema"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Eliminar datos existentes antes de crear nuevos",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("🗑️ Eliminando datos existentes...")
            self.clear_existing_data()

        self.stdout.write("🏗️ Creando datos de prueba multi-tenant...")

        try:
            with transaction.atomic():
                # Crear empresas con sus equipos
                empresas_data = self.create_empresas_data()

                for empresa_info in empresas_data:
                    empresa, usuarios_creados = self.create_empresa_completa(
                        empresa_info
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Empresa "{empresa.nombre}" creada con {len(usuarios_creados)} usuarios'
                        )
                    )
                    self.display_empresa_summary(empresa, usuarios_creados)

            self.stdout.write(
                self.style.SUCCESS(
                    "\n🎉 Datos de prueba creados exitosamente!"
                )
            )
            self.display_final_summary()

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creando datos de prueba: {str(e)}")
            )
            raise

    def clear_existing_data(self):
        """Elimina datos existentes de empresas y perfiles."""
        PerfilUsuario.objects.all().delete()
        # No eliminamos usuarios para mantener superuser
        Empresa.objects.all().delete()
        self.stdout.write("✅ Datos existentes eliminados")

    def create_empresas_data(self):
        """Define los datos de las empresas de prueba."""
        return [
            {
                "nombre": "PackFy Express",
                "dueno": {
                    "email": "admin@packfy.com",
                    "password": "admin123",
                    "nombre": "Carlos",
                    "apellido": "Rodriguez",
                },
                "empleados": [
                    {
                        "email": "miami@packfy.com",
                        "password": "miami123",
                        "nombre": "Maria",
                        "apellido": "Gonzalez",
                        "rol": PerfilUsuario.RolChoices.OPERADOR_MIAMI,
                    },
                    {
                        "email": "cuba@packfy.com",
                        "password": "cuba123",
                        "nombre": "Pedro",
                        "apellido": "Martinez",
                        "rol": PerfilUsuario.RolChoices.OPERADOR_CUBA,
                    },
                ],
                "clientes": [
                    {
                        "email": "cliente1@packfy.com",
                        "password": "cliente123",
                        "nombre": "Ana",
                        "apellido": "Perez",
                        "rol": PerfilUsuario.RolChoices.REMITENTE,
                    },
                    {
                        "email": "destino1@packfy.com",
                        "password": "destino123",
                        "nombre": "Luis",
                        "apellido": "Herrera",
                        "rol": PerfilUsuario.RolChoices.DESTINATARIO,
                    },
                ],
            },
            {
                "nombre": "Cuba Fast Delivery",
                "dueno": {
                    "email": "admin@cubafast.com",
                    "password": "admin123",
                    "nombre": "Roberto",
                    "apellido": "Silva",
                },
                "empleados": [
                    {
                        "email": "miami@cubafast.com",
                        "password": "miami123",
                        "nombre": "Carmen",
                        "apellido": "Lopez",
                        "rol": PerfilUsuario.RolChoices.OPERADOR_MIAMI,
                    },
                    {
                        "email": "cuba@cubafast.com",
                        "password": "cuba123",
                        "nombre": "Jorge",
                        "apellido": "Ramirez",
                        "rol": PerfilUsuario.RolChoices.OPERADOR_CUBA,
                    },
                ],
                "clientes": [
                    {
                        "email": "cliente1@cubafast.com",
                        "password": "cliente123",
                        "nombre": "Lucia",
                        "apellido": "Torres",
                        "rol": PerfilUsuario.RolChoices.REMITENTE,
                    },
                    {
                        "email": "destino1@cubafast.com",
                        "password": "destino123",
                        "nombre": "Miguel",
                        "apellido": "Castro",
                        "rol": PerfilUsuario.RolChoices.DESTINATARIO,
                    },
                ],
            },
            {
                "nombre": "Habana Cargo",
                "dueno": {
                    "email": "admin@habanacargo.com",
                    "password": "admin123",
                    "nombre": "Elena",
                    "apellido": "Fernandez",
                },
                "empleados": [
                    {
                        "email": "miami@habanacargo.com",
                        "password": "miami123",
                        "nombre": "David",
                        "apellido": "Morales",
                        "rol": PerfilUsuario.RolChoices.OPERADOR_MIAMI,
                    },
                    {
                        "email": "cuba@habanacargo.com",
                        "password": "cuba123",
                        "nombre": "Isabel",
                        "apellido": "Vargas",
                        "rol": PerfilUsuario.RolChoices.OPERADOR_CUBA,
                    },
                ],
                "clientes": [
                    {
                        "email": "cliente1@habanacargo.com",
                        "password": "cliente123",
                        "nombre": "Gabriel",
                        "apellido": "Jimenez",
                        "rol": PerfilUsuario.RolChoices.REMITENTE,
                    },
                    {
                        "email": "destino1@habanacargo.com",
                        "password": "destino123",
                        "nombre": "Sofia",
                        "apellido": "Mendoza",
                        "rol": PerfilUsuario.RolChoices.DESTINATARIO,
                    },
                ],
            },
        ]

    def create_empresa_completa(self, empresa_data):
        """Crea una empresa completa con todos sus usuarios."""
        usuarios_creados = []

        # Crear empresa con dueño
        empresa, usuario_dueno, perfil_dueno = (
            TenantUtils.crear_empresa_con_dueno(
                nombre_empresa=empresa_data["nombre"],
                email_dueno=empresa_data["dueno"]["email"],
                password_dueno=empresa_data["dueno"]["password"],
                nombre_dueno=empresa_data["dueno"]["nombre"],
                apellido_dueno=empresa_data["dueno"]["apellido"],
            )
        )

        usuarios_creados.append(
            {"usuario": usuario_dueno, "perfil": perfil_dueno, "tipo": "Dueño"}
        )

        # Agregar empleados
        for empleado_data in empresa_data.get("empleados", []):
            usuario, perfil, es_nuevo = TenantUtils.agregar_usuario_a_empresa(
                empresa=empresa,
                email_usuario=empleado_data["email"],
                rol=empleado_data["rol"],
                password=empleado_data["password"],
                nombre=empleado_data["nombre"],
                apellido=empleado_data["apellido"],
            )

            usuarios_creados.append(
                {"usuario": usuario, "perfil": perfil, "tipo": "Empleado"}
            )

        # Agregar clientes
        for cliente_data in empresa_data.get("clientes", []):
            usuario, perfil, es_nuevo = TenantUtils.agregar_usuario_a_empresa(
                empresa=empresa,
                email_usuario=cliente_data["email"],
                rol=cliente_data["rol"],
                password=cliente_data["password"],
                nombre=cliente_data["nombre"],
                apellido=cliente_data["apellido"],
            )

            usuarios_creados.append(
                {"usuario": usuario, "perfil": perfil, "tipo": "Cliente"}
            )

        return empresa, usuarios_creados

    def display_empresa_summary(self, empresa, usuarios_creados):
        """Muestra resumen de la empresa creada."""
        self.stdout.write(
            f"  📋 Empresa: {empresa.nombre} (Slug: {empresa.slug})"
        )

        for info in usuarios_creados:
            perfil = info["perfil"]
            usuario = info["usuario"]
            self.stdout.write(
                f'    👤 {info["tipo"]}: {usuario.get_full_name()} '
                f"({usuario.email}) - {perfil.get_rol_display()}"
            )

    def display_final_summary(self):
        """Muestra resumen final de todos los datos creados."""
        total_empresas = Empresa.objects.count()
        total_usuarios = PerfilUsuario.objects.count()

        self.stdout.write("\n📊 RESUMEN FINAL:")
        self.stdout.write(f"  🏢 Empresas creadas: {total_empresas}")
        self.stdout.write(f"  👥 Total usuarios: {total_usuarios}")

        # Estadísticas por rol
        for rol_value, rol_display in PerfilUsuario.RolChoices.choices:
            count = PerfilUsuario.objects.filter(rol=rol_value).count()
            self.stdout.write(f"    • {rol_display}: {count}")

        self.stdout.write("\n🔑 CREDENCIALES DE ACCESO:")
        for empresa in Empresa.objects.all():
            dueno = PerfilUsuario.objects.filter(
                empresa=empresa, rol=PerfilUsuario.RolChoices.DUENO
            ).first()
            if dueno:
                self.stdout.write(
                    f"  🏢 {empresa.nombre}: {dueno.usuario.email} / "
                    f"admin123 (Slug: {empresa.slug})"
                )
