import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario

print("=== CREANDO PERFILES MANUALMENTE ===")

# 1. Arreglar superadmin
superadmin = Usuario.objects.get(email="superadmin@packfy.com")
superadmin.is_staff = True
superadmin.is_superuser = True
superadmin.save()
print(
    f"✅ Superadmin configurado: staff={superadmin.is_staff}, super={superadmin.is_superuser}"
)

# 2. Crear empresa
empresa, created = Empresa.objects.get_or_create(
    slug="packfy-express",
    defaults={"nombre": "Packfy Express", "activo": True},
)
print(f"✅ Empresa: {empresa.nombre} (nueva: {created})")

# 3. Crear perfil dueño
dueno = Usuario.objects.get(email="dueno@packfy.com")
perfil_dueno, created = PerfilUsuario.objects.get_or_create(
    usuario=dueno, empresa=empresa, defaults={"rol": "dueno", "activo": True}
)
print(f"✅ Perfil dueño: {perfil_dueno.rol} (nuevo: {created})")

# 4. Verificación final
print(f"\nTotal perfiles: {PerfilUsuario.objects.count()}")
for perfil in PerfilUsuario.objects.all():
    print(
        f"  - {perfil.usuario.email} -> {perfil.empresa.nombre} ({perfil.rol})"
    )

print("✅ COMPLETADO")
