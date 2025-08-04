from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo de Usuario
    """
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password',
                  'telefono', 'cargo', 'foto_perfil', 'es_administrador_empresa',
                  'is_active', 'date_joined', 'fecha_creacion', 'ultima_actualizacion']
        read_only_fields = ['id', 'date_joined', 'fecha_creacion', 'ultima_actualizacion']
    
    def create(self, validated_data):
        """
        Crea un nuevo usuario con la contraseña cifrada
        """
        password = validated_data.pop('password', None)
        usuario = Usuario.objects.create(**validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario
    
    def update(self, instance, validated_data):
        """
        Actualiza un usuario, gestionando correctamente el campo de contraseña
        """
        password = validated_data.pop('password', None)
        usuario = super().update(instance, validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario
