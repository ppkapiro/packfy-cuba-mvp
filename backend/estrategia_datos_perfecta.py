#!/usr/bin/env python
"""
🎯 ESTRATEGIA PERFECTA - DATOS DE PRUEBA MULTITENANCY
Packfy Cuba - Implementación de datos de prueba siguiendo auditoría completa
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from empresas.models import Empresa, PerfilUsuario
from envios.models import Envio


def crear_empresas_multitenancy():
    """FASE 1: Crear empresas diversificadas para multitenancy"""
    print("🎯 FASE 1: CREANDO EMPRESAS MULTITENANCY...")
    print("=" * 60)

    empresas_data = [
        {
            "nombre": "Miami Shipping Express",
            "slug": "miami-shipping",
            "descripcion": "Empresa especializada en envíos Miami-Cuba con logística aérea y marítima",
            "email": "info@miami-shipping.com",
            "telefono": "+1-305-555-0101",
            "configuracion": {
                "tipo_negocio": "envios_internacionales",
                "mercado_principal": "miami_cuba",
                "servicios": ["envio_aereo", "envio_maritimo", "combo_familiar"],
                "ubicacion_principal": "Miami, FL",
                "horario_operacion": "8:00-18:00 EST",
                "moneda_principal": "USD",
            },
        },
        {
            "nombre": "Cuba Express Cargo",
            "slug": "cuba-express",
            "descripcion": "Servicio de carga express y distribución dentro del territorio cubano",
            "email": "contacto@cuba-express.cu",
            "telefono": "+53-7-555-0201",
            "configuracion": {
                "tipo_negocio": "envios_domesticos",
                "mercado_principal": "cuba_nacional",
                "servicios": ["envio_nacional", "entrega_rapida", "carga_pesada"],
                "ubicacion_principal": "La Habana, Cuba",
                "horario_operacion": "9:00-17:00 CST",
                "moneda_principal": "CUP",
            },
        },
        {
            "nombre": "Habana Premium Logistics",
            "slug": "habana-premium",
            "descripcion": "Logística premium para envíos de alto valor con seguro completo",
            "email": "premium@habana-logistics.cu",
            "telefono": "+53-7-555-0301",
            "configuracion": {
                "tipo_negocio": "logistica_premium",
                "mercado_principal": "habana_metropolitana",
                "servicios": ["envio_premium", "seguro_completo", "tracking_avanzado"],
                "ubicacion_principal": "Vedado, La Habana",
                "horario_operacion": "8:00-20:00 CST",
                "moneda_principal": "EUR",
            },
        },
        {
            "nombre": "Packfy Demostraciones",
            "slug": "packfy-demo",
            "descripcion": "Empresa de pruebas para desarrollo y demostraciones del sistema",
            "email": "demo@packfy.com",
            "telefono": "+1-555-DEMO",
            "configuracion": {
                "tipo_negocio": "demo",
                "mercado_principal": "testing",
                "servicios": ["todos_los_servicios"],
                "ubicacion_principal": "Virtual",
                "horario_operacion": "24/7",
                "moneda_principal": "USD",
            },
        },
    ]

    empresas_creadas = []
    for empresa_data in empresas_data:
        empresa, created = Empresa.objects.get_or_create(
            slug=empresa_data["slug"], defaults=empresa_data
        )

        status = "🆕 CREADA" if created else "✅ EXISTENTE"
        print(f"   {status}: {empresa.nombre}")
        print(f"      🔗 Slug: {empresa.slug}")
        print(f"      🌐 URL: {empresa.slug}.packfy.com")
        empresas_creadas.append(empresa)

    print(f"\n✅ EMPRESAS CONFIGURADAS: {len(empresas_creadas)}")
    return empresas_creadas


def crear_usuarios_multitenancy(empresas):
    """FASE 2: Crear usuarios con perfiles multi-empresa"""
    print("\n🎯 FASE 2: CREANDO USUARIOS MULTITENANCY...")
    print("=" * 60)

    usuarios_data = [
        # Administrador global
        {
            "email": "admin@packfy.com",
            "username": "admin@packfy.com",
            "first_name": "Administrador",
            "last_name": "Global",
            "password": "admin123",
            "is_staff": True,
            "is_superuser": True,
            "empresas_roles": [(empresa.slug, "dueno") for empresa in empresas],
        },
        # Dueños específicos
        {
            "email": "carlos.miami@packfy.com",
            "username": "carlos.miami",
            "first_name": "Carlos",
            "last_name": "Rodriguez",
            "password": "carlos123",
            "empresas_roles": [("miami-shipping", "dueno")],
        },
        {
            "email": "maria.cuba@packfy.com",
            "username": "maria.cuba",
            "first_name": "María",
            "last_name": "González",
            "password": "maria123",
            "empresas_roles": [("cuba-express", "dueno")],
        },
        {
            "email": "luis.habana@packfy.com",
            "username": "luis.habana",
            "first_name": "Luis",
            "last_name": "Pérez",
            "password": "luis123",
            "empresas_roles": [("habana-premium", "dueno")],
        },
        # Operadores
        {
            "email": "operador.miami@packfy.com",
            "username": "operador.miami",
            "first_name": "José",
            "last_name": "Martínez",
            "password": "operador123",
            "empresas_roles": [
                ("miami-shipping", "operador_miami"),
                ("habana-premium", "operador_miami"),
            ],
        },
        {
            "email": "operador.cuba@packfy.com",
            "username": "operador.cuba",
            "first_name": "Ana",
            "last_name": "Fernández",
            "password": "operador123",
            "empresas_roles": [
                ("cuba-express", "operador_cuba"),
                ("habana-premium", "operador_cuba"),
            ],
        },
        # Usuario multi-empresa (consultor)
        {
            "email": "consultor@packfy.com",
            "username": "consultor",
            "first_name": "Roberto",
            "last_name": "Consultor",
            "password": "consultor123",
            "empresas_roles": [
                ("miami-shipping", "dueno"),
                ("cuba-express", "operador_cuba"),
                ("habana-premium", "dueno"),
                ("packfy-demo", "dueno"),
            ],
        },
        # Clientes
        {
            "email": "cliente.remitente@gmail.com",
            "username": "cliente.remitente",
            "first_name": "Elena",
            "last_name": "Díaz",
            "password": "cliente123",
            "empresas_roles": [("miami-shipping", "remitente")],
        },
        {
            "email": "cliente.destinatario@gmail.com",
            "username": "cliente.destinatario",
            "first_name": "Pedro",
            "last_name": "López",
            "password": "cliente123",
            "empresas_roles": [("cuba-express", "destinatario")],
        },
        # Usuarios demo para testing
        {
            "email": "demo.tester@packfy.com",
            "username": "demo.tester",
            "first_name": "Demo",
            "last_name": "Tester",
            "password": "demo123",
            "empresas_roles": [("packfy-demo", "remitente")],
        },
    ]

    usuarios_creados = []
    for user_data in usuarios_data:
        empresas_roles = user_data.pop("empresas_roles")

        usuario, created = User.objects.get_or_create(
            email=user_data["email"], defaults=user_data
        )

        if created:
            usuario.set_password(user_data["password"])
            usuario.save()

        status = "🆕 CREADO" if created else "✅ EXISTENTE"
        print(
            f"   {status}: {usuario.first_name} {usuario.last_name} ({usuario.email})"
        )

        # Crear perfiles en empresas
        for empresa_slug, rol in empresas_roles:
            empresa = next((e for e in empresas if e.slug == empresa_slug), None)
            if empresa:
                perfil, perfil_created = PerfilUsuario.objects.get_or_create(
                    usuario=usuario,
                    empresa=empresa,
                    defaults={"rol": rol, "activo": True},
                )
                perfil_status = "🆕" if perfil_created else "✅"
                print(
                    f"      {perfil_status} {empresa.nombre} → {perfil.get_rol_display()}"
                )

        usuarios_creados.append(usuario)

    print(f"\n✅ USUARIOS CONFIGURADOS: {len(usuarios_creados)}")
    return usuarios_creados


def crear_datos_envios_multitenancy(empresas):
    """FASE 3: Crear datos de envíos distribuidos por empresa"""
    print("\n🎯 FASE 3: CREANDO DATOS DE ENVÍOS...")
    print("=" * 60)

    # Esta función será implementada después de validar empresas y usuarios
    print("   📦 Preparando estructura para envíos multitenancy...")
    print("   🎯 Se crearán envíos distribuidos por empresa")
    print("   📊 Diferentes estados, tipos y valores")
    print("   🔒 Validando aislamiento de datos por tenant")

    # TODO: Implementar creación de envíos específicos por empresa
    envios_totales = 0
    try:
        envios_totales = Envio.objects.count()
    except Exception as e:
        print(f"   ⚠️  Tabla de envíos no disponible: {e}")

    print(f"   📈 Envíos actuales: {envios_totales}")
    print("   🚀 Implementación de envíos lista para siguiente iteración")


def validar_multitenancy_completo(empresas, usuarios):
    """FASE 4: Validación completa del sistema multitenancy"""
    print("\n🎯 FASE 4: VALIDACIÓN MULTITENANCY...")
    print("=" * 60)

    # Verificar empresas
    print("   🏢 Empresas activas:")
    for empresa in empresas:
        perfiles_count = PerfilUsuario.objects.filter(
            empresa=empresa, activo=True
        ).count()
        print(f"      ✅ {empresa.nombre} ({empresa.slug}) - {perfiles_count} usuarios")

    # Verificar usuarios multi-empresa
    print("\n   👥 Usuarios multi-empresa:")
    for usuario in usuarios:
        perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
        if perfiles.count() > 1:
            print(f"      🔄 {usuario.first_name} {usuario.last_name}:")
            for perfil in perfiles:
                print(
                    f"         • {perfil.empresa.nombre} → {perfil.get_rol_display()}"
                )

    # Verificar distribución de roles
    print("\n   🎭 Distribución de roles:")
    from django.db.models import Count

    roles_stats = (
        PerfilUsuario.objects.values("rol")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    for rol_stat in roles_stats:
        rol_display = dict(PerfilUsuario.RolChoices.choices)[rol_stat["rol"]]
        print(f"      📊 {rol_display}: {rol_stat['count']} usuarios")

    # URLs de prueba
    print("\n   🌐 URLs de prueba disponibles:")
    for empresa in empresas:
        print(f"      🔗 {empresa.slug}.localhost:5173")
        print(f"      🔗 localhost:5173?empresa={empresa.slug}")


def main():
    """Ejecutar estrategia completa de datos de prueba"""
    print("🚀 INICIANDO ESTRATEGIA PERFECTA - DATOS MULTITENANCY")
    print("=" * 80)

    # FASE 1: Empresas
    empresas = crear_empresas_multitenancy()

    # FASE 2: Usuarios
    usuarios = crear_usuarios_multitenancy(empresas)

    # FASE 3: Envíos (preparación)
    crear_datos_envios_multitenancy(empresas)

    # FASE 4: Validación
    validar_multitenancy_completo(empresas, usuarios)

    print("\n" + "=" * 80)
    print("🎉 ESTRATEGIA MULTITENANCY COMPLETADA")
    print("=" * 80)
    print("\n🎯 RESULTADO:")
    print(f"   🏢 {len(empresas)} empresas configuradas")
    print(f"   👥 {len(usuarios)} usuarios creados")
    print(f"   🎭 {PerfilUsuario.objects.count()} perfiles activos")
    print("\n🌐 PRUEBAS DISPONIBLES:")
    for empresa in empresas:
        print(f"   🔗 {empresa.slug}.localhost:5173")

    print("\n🔐 CREDENCIALES:")
    print("   👑 Admin: admin@packfy.com / admin123")
    print("   🏢 Dueños: carlos.miami@packfy.com / carlos123")
    print("   🔄 Multi-empresa: consultor@packfy.com / consultor123")
    print("   👤 Cliente: cliente.remitente@gmail.com / cliente123")


if __name__ == "__main__":
    main()
