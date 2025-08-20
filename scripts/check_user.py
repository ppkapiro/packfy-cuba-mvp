from usuarios.models import Usuario

try:
    user = Usuario.objects.get(email="remitente2@packfy.com")
    print(f"✅ Usuario encontrado: {user.username} - {user.email}")
    print(f"Usuario activo: {user.is_active}")
    print(f'Password válido: {user.check_password("remitente123!")}')
except Usuario.DoesNotExist:
    print("❌ Usuario remitente2@packfy.com NO existe")
    print("Usuarios disponibles:")
    for u in Usuario.objects.all():
        print(f"  - {u.email} ({u.username})")
