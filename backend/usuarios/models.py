from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Crear y guardar un usuario con email y password"""
        if not email:
            raise ValueError('El email debe ser proporcionado')
        # Mapear nombres en español a los campos de Django
        nombre = extra_fields.pop('nombre', None)
        apellidos = extra_fields.pop('apellidos', None)
        if nombre is not None:
            extra_fields['first_name'] = nombre
        if apellidos is not None:
            extra_fields['last_name'] = apellidos

        email = self.normalize_email(email)
        # Asignar un username si no viene en extra_fields
        username = extra_fields.get('username') or email
        extra_fields.setdefault('username', username)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crear y guardar un superusuario con email y password"""
        extra_fields.setdefault('username', email)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario para la aplicación.
    Extiende el modelo AbstractUser de Django y agrega campos adicionales.
    """
    email = models.EmailField(_('email address'), unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    es_administrador_empresa = models.BooleanField(default=False)
    
    # Campos para el seguimiento de cambios
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email
