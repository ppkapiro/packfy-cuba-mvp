print("Script iniciado")

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from usuarios.models import Usuario

print("Django configurado")

# Verificar usuarios existentes
usuarios_count = Usuario.objects.count()
print(f"Usuarios existentes: {usuarios_count}")

# Crear admin
admin_user, created = Usuario.objects.get_or_create(
    email="admin@packfy.cu",
    defaults={
        "nombre": "Admin",
        "apellidos": "Packfy",
        "es_administrador": True,
        "es_staff": True,
        "es_activo": True,
        "tipo_usuario": "ADMIN",
    },
)

admin_user.set_password("admin123")
admin_user.save()

print(f"Admin {'creado' if created else 'actualizado'}: {admin_user.email}")

# Verificar final
usuarios_count = Usuario.objects.count()
print(f"Total usuarios: {usuarios_count}")

print("Script completado")
