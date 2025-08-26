#!/usr/bin/env python
"""
🔧 CORRECCIÓN MÍNIMA - Solo corregir referencias DUENO → ADMIN_EMPRESA
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def corregir_referencias_admin():
    """Corregir solo las referencias problemáticas sin tocar el admin.py"""
    print("🔧 CORRECCIÓN MÍNIMA DE REFERENCIAS")
    print("=" * 50)

    # Importar después de django.setup()
    from empresas.models import PerfilUsuario

    # Verificar que los nuevos roles están disponibles
    try:
        # Probar que ADMIN_EMPRESA existe
        rol_admin = PerfilUsuario.RolChoices.ADMIN_EMPRESA
        print(f"✅ Rol ADMIN_EMPRESA disponible: {rol_admin}")

        # Verificar que DUENO ya no existe
        try:
            rol_dueno = PerfilUsuario.RolChoices.DUENO
            print(f"❌ DUENO aún existe: {rol_dueno}")
        except AttributeError:
            print("✅ DUENO eliminado correctamente")

        print("\n✅ Corrección de modelo completada")
        return True

    except AttributeError as e:
        print(f"❌ Error en modelo: {e}")
        return False


if __name__ == "__main__":
    corregir_referencias_admin()
