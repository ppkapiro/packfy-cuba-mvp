#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from usuarios.models import Usuario

print("=== VERIFICANDO CREDENCIALES ===")

# Verificar usuarios existentes
print("Usuarios en BD:")
for user in Usuario.objects.all():
    print(f"- {user.email} (activo: {user.is_active})")

print("\n=== PROBANDO CREDENCIALES ===")

# Probar credenciales
credenciales = [
    ('admin@packfy.com', 'admin123'),
    ('demo@packfy.com', 'demo123'), 
    ('test@test.com', '123456'),
    ('operador@packfy.com', 'operador123')
]

for email, password in credenciales:
    user = authenticate(email=email, password=password)
    status = "✅ OK" if user else "❌ FAIL"
    print(f"{email} / {password}: {status}")

# Intentar resetear passwords
print("\n=== RESETEANDO PASSWORDS ===")
for email, password in credenciales[:3]:  # Solo los primeros 3
    try:
        user = Usuario.objects.get(email=email)
        user.set_password(password)
        user.save()
        print(f"✅ Password actualizado para {email}")
    except Usuario.DoesNotExist:
        print(f"❌ Usuario {email} no existe")
    except Exception as e:
        print(f"❌ Error con {email}: {e}")

print("\n=== PROBANDO CREDENCIALES DESPUÉS DEL RESET ===")
for email, password in credenciales[:3]:
    user = authenticate(email=email, password=password)
    status = "✅ OK" if user else "❌ FAIL" 
    print(f"{email} / {password}: {status}")
