import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from empresas.models import Empresa

print("🚀 CREANDO ESTRUCTURA SEGÚN ARQUITECTURA MULTITENANCY")
print("=" * 60)

try:
    with transaction.atomic():
        Usuario = get_user_model()

        # 1. Crear grupos de roles
        print("\n📋 Creando grupos de roles...")
        roles = [
            "super_admin",
            "admin_empresa",
            "operador_miami",
            "operador_cuba",
            "remitente",
            "destinatario",
        ]
        for rol in roles:
            grupo, created = Group.objects.get_or_create(name=rol)
            if created:
                print(f"✅ Grupo creado: {rol}")

        # 2. Crear empresas
        print("\n🏢 Creando empresas...")
        empresas_data = [
            {
                "nombre": "Prime Express Cargo",
                "slug": "prime-express",
                "email": "info@primeexpress.com",
            },
            {
                "nombre": "Cuba Express",
                "slug": "cuba-express",
                "email": "info@cubaexpress.com",
            },
            {
                "nombre": "Habana Premium",
                "slug": "habana-premium",
                "email": "info@habanapremium.com",
            },
            {
                "nombre": "Miami Shipping",
                "slug": "miami-shipping",
                "email": "info@miamishipping.com",
            },
        ]

        for data in empresas_data:
            empresa, created = Empresa.objects.get_or_create(
                slug=data["slug"], defaults=data
            )
            if created:
                print(f"✅ Empresa creada: {empresa.nombre}")

        # 3. Crear superusuario
        print("\n👑 Creando superusuario...")
        email = "superadmin@packfy.com"
        if not Usuario.objects.filter(email=email).exists():
            superuser = Usuario.objects.create_superuser(
                email=email,
                password="super123!",
                first_name="Super",
                last_name="Administrador",
            )
            grupo_super_admin = Group.objects.get(name="super_admin")
            superuser.groups.add(grupo_super_admin)
            print(f"✅ Superusuario creado: {email}")
        else:
            print(f"ℹ️  Superusuario ya existe: {email}")

        # 4. Crear usuarios por empresa
        print("\n👥 Creando usuarios por empresa...")
        dominios = {
            "prime-express": "primeexpress.com",
            "cuba-express": "cubaexpress.com",
            "habana-premium": "habanapremium.com",
            "miami-shipping": "miamishipping.com",
        }

        total_usuarios = 0
        for empresa in Empresa.objects.all():
            print(f"\n--- Creando usuarios para {empresa.nombre} ---")
            dominio = dominios.get(empresa.slug, "empresa.com")

            usuarios_data = [
                {
                    "email": f"admin@{dominio}",
                    "password": "admin123",
                    "first_name": "Admin",
                    "last_name": empresa.nombre.split()[0],
                    "rol": "admin_empresa",
                },
                {
                    "email": f"operador.miami@{dominio}",
                    "password": "operador123",
                    "first_name": "Operador",
                    "last_name": "Miami",
                    "rol": "operador_miami",
                },
                {
                    "email": f"operador.cuba@{dominio}",
                    "password": "operador123",
                    "first_name": "Operador",
                    "last_name": "Cuba",
                    "rol": "operador_cuba",
                },
                {
                    "email": f"remitente@{dominio}",
                    "password": "remitente123",
                    "first_name": "Cliente",
                    "last_name": "Remitente",
                    "rol": "remitente",
                },
                {
                    "email": f"destinatario@{dominio}",
                    "password": "destinatario123",
                    "first_name": "Cliente",
                    "last_name": "Destinatario",
                    "rol": "destinatario",
                },
            ]

            for data in usuarios_data:
                if not Usuario.objects.filter(email=data["email"]).exists():
                    usuario = Usuario.objects.create_user(
                        email=data["email"],
                        password=data["password"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        is_active=True,
                    )
                    grupo = Group.objects.get(name=data["rol"])
                    usuario.groups.add(grupo)
                    total_usuarios += 1
                    print(f"✅ Usuario creado: {data['email']} ({data['rol']})")
                else:
                    print(f"ℹ️  Usuario ya existe: {data['email']}")

        print(f"\n🎉 ESTRUCTURA CREADA EXITOSAMENTE!")
        print(f"📊 RESUMEN: 1 Superusuario + {total_usuarios} usuarios")

        # Verificación final específica
        print(f"\n🔍 VERIFICACIÓN: admin@primeexpress.com")
        usuario_test = Usuario.objects.filter(email="admin@primeexpress.com").first()
        if usuario_test:
            print(f"✅ Usuario encontrado: {usuario_test.email}")
            print(f"✅ Activo: {usuario_test.is_active}")
            print(f"✅ Nombre: {usuario_test.first_name} {usuario_test.last_name}")
            print(f"✅ Grupos: {[g.name for g in usuario_test.groups.all()]}")

            # Test de autenticación
            from django.contrib.auth import authenticate

            auth_test = authenticate(
                username="admin@primeexpress.com", password="admin123"
            )
            if auth_test:
                print("✅ AUTENTICACIÓN EXITOSA con admin123")
            else:
                print("❌ AUTENTICACIÓN FALLÓ")
        else:
            print("❌ Usuario admin@primeexpress.com NO ENCONTRADO")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback

    traceback.print_exc()
