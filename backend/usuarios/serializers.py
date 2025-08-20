from rest_framework import serializers

from .models import Usuario


class EmpresaBasicaSerializer(serializers.Serializer):
    """Serializer simplificado para empresas en el contexto de usuario"""

    id = serializers.IntegerField()
    nombre = serializers.CharField()
    slug = serializers.CharField()


class PerfilEmpresaSerializer(serializers.Serializer):
    """Serializer para el perfil del usuario en una empresa"""

    empresa = EmpresaBasicaSerializer()
    rol = serializers.CharField()
    activo = serializers.BooleanField()


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo de Usuario
    """

    password = serializers.CharField(write_only=True, required=False)
    empresas = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "telefono",
            "cargo",
            "foto_perfil",
            "es_administrador_empresa",
            "is_active",
            "date_joined",
            "fecha_creacion",
            "ultima_actualizacion",
            "empresas",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "fecha_creacion",
            "ultima_actualizacion",
        ]

    def get_empresas(self, obj):
        """Obtener todas las empresas del usuario con su rol"""
        perfiles = obj.perfiles_empresa.filter(
            activo=True, empresa__activo=True
        ).select_related("empresa")
        return [
            {
                "id": perfil.empresa.id,
                "nombre": perfil.empresa.nombre,
                "slug": perfil.empresa.slug,
                "rol": perfil.rol,
            }
            for perfil in perfiles
        ]

    def create(self, validated_data):
        """
        Crea un nuevo usuario con la contraseña cifrada
        """
        password = validated_data.pop("password", None)
        usuario = Usuario.objects.create(**validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario

    def update(self, instance, validated_data):
        """
        Actualiza un usuario, gestionando correctamente el campo de contraseña
        """
        password = validated_data.pop("password", None)
        usuario = super().update(instance, validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario
