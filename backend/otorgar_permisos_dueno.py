#!/usr/bin/env python3
"""
🔧 Script para otorgar permisos específicos al dueño de empresa
Carlos necesita permisos explícitos para ver/editar modelos en el admin
"""
import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.append("/app")
django.setup()

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def otorgar_permisos_dueno():
    """Otorgar permisos específicos al dueño de empresa"""

    print("=== 🔧 OTORGANDO PERMISOS AL DUEÑO ===")

    try:
        # 1. Obtener Carlos
        carlos = Usuario.objects.get(email="dueno@packfy.com")
        print(f"✅ Usuario encontrado: {carlos.email}")

        # 2. Configurar estado básico
        carlos.is_active = True
        carlos.is_staff = True
        carlos.is_superuser = False  # NO superuser
        carlos.save()
        print(
            f"✅ Estado configurado: activo={carlos.is_active}, staff={carlos.is_staff}, superuser={carlos.is_superuser}"
        )

        # 3. Limpiar permisos existentes
        carlos.user_permissions.clear()
        print("🧹 Permisos previos limpiados")

        # 4. Otorgar permisos específicos para modelos de la aplicación
        modelos_permisos = [
            # Usuarios
            (
                "usuarios",
                "usuario",
                ["view", "add", "change"],
            ),  # NO delete para evitar problemas
            # Empresas
            (
                "empresas",
                "empresa",
                ["view", "change"],
            ),  # Solo ver y cambiar su empresa
            ("empresas", "perfilusuario", ["view", "add", "change", "delete"]),
            # Envíos
            ("envios", "envio", ["view", "add", "change", "delete"]),
            ("envios", "historialestado", ["view", "add", "change"]),
        ]

        permisos_otorgados = []

        for app_label, model_name, permisos in modelos_permisos:
            try:
                content_type = ContentType.objects.get(
                    app_label=app_label, model=model_name
                )

                for permiso in permisos:
                    codename = f"{permiso}_{model_name}"
                    try:
                        permission = Permission.objects.get(
                            content_type=content_type, codename=codename
                        )
                        carlos.user_permissions.add(permission)
                        permisos_otorgados.append(f"{app_label}.{codename}")
                        print(f"  ✅ {app_label}.{codename}")
                    except Permission.DoesNotExist:
                        print(
                            f"  ⚠️ Permiso no encontrado: {app_label}.{codename}"
                        )

            except ContentType.DoesNotExist:
                print(
                    f"  ❌ ContentType no encontrado: {app_label}.{model_name}"
                )

        # 5. Verificar perfil de empresa
        empresa = Empresa.objects.get(slug="packfy-express")
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=carlos,
            empresa=empresa,
            defaults={"rol": "dueno", "activo": True},
        )

        if created:
            print(f"✅ Perfil de empresa creado: {perfil.rol}")
        else:
            perfil.activo = True
            perfil.save()
            print(f"✅ Perfil de empresa verificado: {perfil.rol}")

        # 6. Resumen final
        print(f"\n=== 📋 RESUMEN ===")
        print(f"Usuario: {carlos.email}")
        print(
            f"Estado: activo={carlos.is_active}, staff={carlos.is_staff}, superuser={carlos.is_superuser}"
        )
        print(f"Empresa: {perfil.empresa.nombre} (rol: {perfil.rol})")
        print(f"Permisos otorgados: {len(permisos_otorgados)}")

        print(f"\n✅ ¡Permisos configurados correctamente!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    otorgar_permisos_dueno()
