#!/usr/bin/env python
"""
Script para asignar empresa al usuario admin
"""
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_development")
django.setup()

from empresas.models import Empresa
from usuarios.models import Usuario


def main():
    print("🔧 Asignando empresa al usuario admin...")

    # Obtener el usuario admin
    try:
        admin_user = Usuario.objects.get(email="admin@packfy.cu")
        print(f"✅ Usuario encontrado: {admin_user.email}")
        print(f"   Empresa actual: {admin_user.empresa}")
    except Usuario.DoesNotExist:
        print("❌ Usuario admin no encontrado")
        return

    # Obtener o crear la empresa demo
    empresa, created = Empresa.objects.get_or_create(
        nombre="Packfy Cuba Demo",
        defaults={
            "direccion": "La Habana, Cuba",
            "telefono": "+53 7 123-4567",
            "email": "demo@packfy.cu",
            "activa": True,
        },
    )
    print(
        f"✅ Empresa: {empresa.nombre} ({'creada' if created else 'existente'})"
    )

    # Asignar la empresa al usuario admin
    admin_user.empresa = empresa
    admin_user.save()
    print(
        f"✅ Usuario actualizado - Empresa asignada: {admin_user.empresa.nombre}"
    )

    # Verificar que los envíos estén asignados a esta empresa
    from envios.models import Envio

    envios_sin_empresa = Envio.objects.filter(empresa=None)
    if envios_sin_empresa.exists():
        print(f"🔄 Asignando empresa a {envios_sin_empresa.count()} envíos...")
        envios_sin_empresa.update(empresa=empresa)
        print("✅ Envíos actualizados")

    envios_total = Envio.objects.filter(empresa=empresa).count()
    print(f"📦 Total de envíos en la empresa: {envios_total}")


if __name__ == "__main__":
    main()
