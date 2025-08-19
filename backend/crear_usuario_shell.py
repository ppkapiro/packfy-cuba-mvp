from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email="admin@packfy.com").exists():
    user = User.objects.create_superuser(
        email="admin@packfy.com",
        username="admin",
        password="packfy123",
        first_name="Admin",
        last_name="Packfy",
    )
    print("✅ Superusuario creado exitosamente:")
    print(f"  📧 Email: {user.email}")
    print(f"  👤 Username: {user.username}")
    print(f"  🔑 Password: packfy123")
else:
    print("⚠️ El superusuario ya existe")
