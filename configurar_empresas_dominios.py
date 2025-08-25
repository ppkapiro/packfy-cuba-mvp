#!/usr/bin/env python3
"""
🌐 CONFIGURAR EMPRESAS PARA MULTITENANCY CON DOMINIOS
Packfy Cuba - Setup de empresas con slugs para subdominios
"""

import os
import sys

import django

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa
from usuarios.models import PerfilUsuario, Usuario


def crear_empresas_multitenancy():
    """Crear empresas con slugs apropiados para multitenancy por dominios"""

    print("🌐 CONFIGURANDO EMPRESAS PARA MULTITENANCY...")
    print("=" * 50)

    # Definir empresas con sus slugs
    empresas_data = [
        {
            "nombre": "Miami Shipping Express",
            "slug": "miami-shipping",
            "descripcion": "Empresa de envíos Miami-Cuba especializada en logística rápida",
            "configuracion": {
                "tipo_negocio": "envios_internacionales",
                "mercado_principal": "miami_cuba",
                "servicios": [
                    "envio_aereo",
                    "envio_maritimo",
                    "combo_familiar",
                ],
            },
        },
        {
            "nombre": "Cuba Express Cargo",
            "slug": "cuba-express",
            "descripcion": "Servicio de carga y envíos express dentro de Cuba",
            "configuracion": {
                "tipo_negocio": "envios_domesticos",
                "mercado_principal": "cuba_nacional",
                "servicios": [
                    "envio_nacional",
                    "entrega_rapida",
                    "carga_pesada",
                ],
            },
        },
        {
            "nombre": "Habana Premium Logistics",
            "slug": "habana-cargo",
            "descripcion": "Logística premium para envíos de alto valor",
            "configuracion": {
                "tipo_negocio": "logistica_premium",
                "mercado_principal": "habana_metropolitana",
                "servicios": [
                    "envio_premium",
                    "seguro_completo",
                    "tracking_avanzado",
                ],
            },
        },
        {
            "nombre": "Packfy Demostraciones",
            "slug": "empresa1",
            "descripcion": "Empresa de pruebas para desarrollo y demostraciones",
            "configuracion": {
                "tipo_negocio": "demo",
                "mercado_principal": "testing",
                "servicios": ["todos_los_servicios"],
            },
        },
    ]

    empresas_creadas = []

    for empresa_data in empresas_data:
        # Verificar si ya existe
        empresa_existente = Empresa.objects.filter(
            slug=empresa_data["slug"]
        ).first()

        if empresa_existente:
            print(
                f"✅ Empresa ya existe: {empresa_existente.nombre} ({empresa_existente.slug})"
            )
            empresas_creadas.append(empresa_existente)
        else:
            # Crear nueva empresa
            empresa = Empresa.objects.create(
                nombre=empresa_data["nombre"],
                slug=empresa_data["slug"],
                descripcion=empresa_data["descripcion"],
                configuracion=empresa_data["configuracion"],
                activo=True,
            )
            print(f"🆕 Empresa creada: {empresa.nombre} ({empresa.slug})")
            empresas_creadas.append(empresa)

    return empresas_creadas


def configurar_usuarios_multitenancy(empresas):
    """Configurar usuarios con perfiles en múltiples empresas"""

    print("\n👥 CONFIGURANDO USUARIOS MULTITENANCY...")
    print("=" * 50)

    # Usuario admin principal (acceso a todas las empresas)
    admin_user, created = Usuario.objects.get_or_create(
        email="admin@packfy.com",
        defaults={
            "username": "admin@packfy.com",
            "first_name": "Administrador",
            "last_name": "Principal",
            "is_staff": True,
            "is_superuser": True,
        },
    )

    if created:
        admin_user.set_password("admin123")
        admin_user.save()
        print(f"🆕 Usuario admin creado: {admin_user.email}")
    else:
        print(f"✅ Usuario admin ya existe: {admin_user.email}")

    # Crear perfiles del admin en todas las empresas
    for empresa in empresas:
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=admin_user,
            empresa=empresa,
            defaults={
                "rol": "dueno",
                "activo": True,
                "configuracion": {
                    "acceso_completo": True,
                    "empresa_principal": empresa.slug == "miami-shipping",
                },
            },
        )

        if created:
            print(f"🆕 Perfil admin creado en {empresa.nombre}")
        else:
            print(f"✅ Perfil admin ya existe en {empresa.nombre}")

    # Usuarios específicos por empresa
    usuarios_empresa = [
        {
            "email": "miami@packfy.com",
            "empresa_slug": "miami-shipping",
            "rol": "operador_miami",
            "nombre": "Operador",
            "apellido": "Miami",
        },
        {
            "email": "cuba@packfy.com",
            "empresa_slug": "cuba-express",
            "rol": "operador_cuba",
            "nombre": "Operador",
            "apellido": "Cuba",
        },
        {
            "email": "habana@packfy.com",
            "empresa_slug": "habana-cargo",
            "rol": "dueno",
            "nombre": "Director",
            "apellido": "Habana",
        },
        {
            "email": "demo@packfy.com",
            "empresa_slug": "empresa1",
            "rol": "dueno",
            "nombre": "Usuario",
            "apellido": "Demo",
        },
    ]

    for user_data in usuarios_empresa:
        # Crear usuario
        user, created = Usuario.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "username": user_data["email"],
                "first_name": user_data["nombre"],
                "last_name": user_data["apellido"],
            },
        )

        if created:
            user.set_password("password123")
            user.save()
            print(f"🆕 Usuario creado: {user.email}")
        else:
            print(f"✅ Usuario ya existe: {user.email}")

        # Encontrar empresa
        empresa = next(
            (e for e in empresas if e.slug == user_data["empresa_slug"]), None
        )

        if empresa:
            # Crear perfil
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=user,
                empresa=empresa,
                defaults={
                    "rol": user_data["rol"],
                    "activo": True,
                    "configuracion": {"empresa_principal": True},
                },
            )

            if created:
                print(
                    f"🆕 Perfil creado: {user.email} → {empresa.nombre} ({user_data['rol']})"
                )
            else:
                print(f"✅ Perfil ya existe: {user.email} → {empresa.nombre}")


def mostrar_resumen_configuracion():
    """Mostrar resumen de la configuración multitenancy"""

    print("\n📊 RESUMEN DE CONFIGURACIÓN MULTITENANCY")
    print("=" * 50)

    empresas = Empresa.objects.filter(activo=True).order_by("nombre")

    for empresa in empresas:
        print(f"\n🏢 {empresa.nombre}")
        print(f"   🌐 Subdominio: {empresa.slug}.packfy.com")
        print(f"   🌐 Desarrollo: {empresa.slug}.localhost:5173")
        print(f"   📝 Descripción: {empresa.descripcion}")

        perfiles = PerfilUsuario.objects.filter(empresa=empresa, activo=True)
        print(f"   👥 Usuarios ({perfiles.count()}):")

        for perfil in perfiles:
            print(f"      • {perfil.usuario.email} → {perfil.rol}")

    print(f"\n📋 CREDENCIALES DE ACCESO:")
    print(f"   🔐 Admin global: admin@packfy.com / admin123")
    print(f"   🔐 Operador Miami: miami@packfy.com / password123")
    print(f"   🔐 Operador Cuba: cuba@packfy.com / password123")
    print(f"   🔐 Director Habana: habana@packfy.com / password123")
    print(f"   🔐 Usuario Demo: demo@packfy.com / password123")

    print(f"\n🌐 DOMINIOS DE PRUEBA:")
    for empresa in empresas:
        print(f"   • http://{empresa.slug}.localhost:5173")


def main():
    """Función principal"""

    print("🇨🇺 PACKFY CUBA - CONFIGURACIÓN MULTITENANCY DOMINIOS")
    print("=" * 60)

    try:
        # 1. Crear empresas
        empresas = crear_empresas_multitenancy()

        # 2. Configurar usuarios
        configurar_usuarios_multitenancy(empresas)

        # 3. Mostrar resumen
        mostrar_resumen_configuracion()

        print(f"\n✅ CONFIGURACIÓN COMPLETADA")
        print(f"🚀 Ahora puedes probar: probar-dominios-multitenancy.ps1")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
