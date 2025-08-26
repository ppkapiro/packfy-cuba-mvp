import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from envios.models import Envio
from usuarios.models import Usuario

print("=== EMPRESAS ===")
for e in Empresa.objects.all():
    print(f"ID: {e.id}, Slug: '{e.slug}', Nombre: '{e.nombre}', Activo: {e.activo}")

print("\n=== USUARIOS ===")
for u in Usuario.objects.all():
    print(f"Username: '{u.username}', Email: '{u.email}', Activo: {u.is_active}")

print("\n=== PERFILES ===")
for p in PerfilUsuario.objects.all():
    print(
        f"Usuario: {p.usuario.username} -> Empresa: {p.empresa.nombre} (Rol: {p.rol})"
    )

print("\n=== ENVÍOS ===")
for empresa in Empresa.objects.all():
    envios_count = Envio.objects.filter(empresa=empresa).count()
    print(f"Empresa: {empresa.nombre} -> {envios_count} envíos")

print(
    f"\nTOTAL: {Empresa.objects.count()} empresas, {Usuario.objects.count()} usuarios, {PerfilUsuario.objects.count()} perfiles, {Envio.objects.count()} envíos"
)
