#!/usr/bin/env python3
"""
Script de diagnóstico completo del sistema de autenticación de Packfy Cuba
"""

print("=== DIAGNÓSTICO SISTEMA DE AUTENTICACIÓN PACKFY CUBA ===")
print()

# 1. Configuración Django
print("1. CONFIGURACIÓN DE DJANGO:")
print("-" * 40)

try:
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    from django.conf import settings

    print(
        f"✅ AUTH_USER_MODEL: {getattr(settings, 'AUTH_USER_MODEL', 'No configurado')}"
    )
    print(
        f"✅ SECRET_KEY configurado: {'Sí' if settings.SECRET_KEY else 'No'}"
    )

    # SIMPLE_JWT config
    jwt_config = getattr(settings, "SIMPLE_JWT", {})
    print(f"✅ SIMPLE_JWT configurado: {'Sí' if jwt_config else 'No'}")
    if jwt_config:
        print(
            f"   - ACCESS_TOKEN_LIFETIME: {jwt_config.get('ACCESS_TOKEN_LIFETIME', 'No configurado')}"
        )
        print(
            f"   - REFRESH_TOKEN_LIFETIME: {jwt_config.get('REFRESH_TOKEN_LIFETIME', 'No configurado')}"
        )

    print()

except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    exit(1)

# 2. Modelo Usuario
print("2. MODELO USUARIO:")
print("-" * 40)

try:
    from usuarios.models import Usuario

    print(f"✅ Modelo Usuario importado correctamente")
    print(f"✅ USERNAME_FIELD: {Usuario.USERNAME_FIELD}")
    print(f"✅ REQUIRED_FIELDS: {Usuario.REQUIRED_FIELDS}")

    # Verificar usuarios en la BD
    total_usuarios = Usuario.objects.count()
    print(f"✅ Total usuarios en BD: {total_usuarios}")

    if total_usuarios > 0:
        print("\n   Usuarios existentes:")
        for user in Usuario.objects.all()[:5]:
            print(
                f"   - {user.email} (username: {user.username}, activo: {user.is_active})"
            )

    print()

except Exception as e:
    print(f"❌ Error con modelo Usuario: {e}")

# 3. Autenticación
print("3. SISTEMA DE AUTENTICACIÓN:")
print("-" * 40)

try:
    from django.contrib.auth import authenticate

    # Buscar usuarios admin
    admin_users = Usuario.objects.filter(email__icontains="admin")

    if admin_users.exists():
        admin_user = admin_users.first()
        print(f"✅ Usuario admin encontrado: {admin_user.email}")

        # Probar autenticación
        test_user = authenticate(
            username=admin_user.email, password="admin123"
        )
        print(
            f"✅ Autenticación con email: {'Exitosa' if test_user else 'Falló'}"
        )

        test_user2 = authenticate(
            username=admin_user.username, password="admin123"
        )
        print(
            f"✅ Autenticación con username: {'Exitosa' if test_user2 else 'Falló'}"
        )
    else:
        print("❌ No se encontró usuario admin")

    print()

except Exception as e:
    print(f"❌ Error en autenticación: {e}")

# 4. Serializers
print("4. SERIALIZERS:")
print("-" * 40)

try:
    from usuarios.serializers import (
        CustomTokenObtainPairSerializer,
        UsuarioSerializer,
    )

    print("✅ CustomTokenObtainPairSerializer importado")
    print("✅ UsuarioSerializer importado")

    # Probar el serializer
    serializer = CustomTokenObtainPairSerializer()
    print(f"✅ Campos del serializer: {list(serializer.fields.keys())}")

    print()

except Exception as e:
    print(f"❌ Error con serializers: {e}")

# 5. URLs
print("5. CONFIGURACIÓN DE URLS:")
print("-" * 40)

try:
    from django.urls import reverse

    login_url = reverse("secure_login")
    print(f"✅ URL de login: {login_url}")

    print()

except Exception as e:
    print(f"❌ Error con URLs: {e}")

print("=== FIN DEL DIAGNÓSTICO ===")
