# Script para crear datos usando Django Shell
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from empresas.models import Empresa, PerfilEmpresa

User = get_user_model()

print("🚀 Creando datos básicos...")

# Crear empresa
empresa, created = Empresa.objects.get_or_create(
    slug="packfy-express-cuba",
    defaults={"nombre": "PackFy Express Cuba", "activa": True},
)
print(f'Empresa: {empresa.nombre} - {"Creada" if created else "Ya existía"}')

# Crear usuario
usuario, created = User.objects.get_or_create(
    email="dueno@packfy.com",
    defaults={
        "nombre": "Carlos",
        "apellido": "Rodriguez",
        "password": make_password("dueno123!"),
        "is_staff": True,
        "is_superuser": True,
    },
)
print(f'Usuario: {usuario.email} - {"Creado" if created else "Ya existía"}')

# Crear perfil
perfil, created = PerfilEmpresa.objects.get_or_create(
    usuario=usuario, empresa=empresa, defaults={"rol": "dueno", "activo": True}
)
print(f'Perfil: {perfil.rol} - {"Creado" if created else "Ya existía"}')

print("✅ Datos creados exitosamente!")
print(f"Total empresas: {Empresa.objects.count()}")
print(f"Total usuarios: {User.objects.count()}")
print(f"Total perfiles: {PerfilEmpresa.objects.count()}")
