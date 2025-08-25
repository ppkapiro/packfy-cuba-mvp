from django.core.management.base import BaseCommand
from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


class Command(BaseCommand):
    help = "Corrige roles de usuario dueño"

    def handle(self, *args, **options):
        self.stdout.write("🔧 CORRIGIENDO ROLES DE USUARIO...")

        # Buscar usuario dueño
        try:
            usuario = Usuario.objects.get(email="dueno@packfy.com")
            self.stdout.write(f"✅ Usuario encontrado: {usuario.email}")
        except Usuario.DoesNotExist:
            self.stdout.write("❌ Usuario dueno@packfy.com no encontrado")
            return

        # Ver perfiles actuales
        perfiles = PerfilUsuario.objects.filter(usuario=usuario)
        self.stdout.write(f"👤 Perfiles antes: {perfiles.count()}")
        for perfil in perfiles:
            self.stdout.write(
                f"   - {perfil.empresa.nombre}: rol='{perfil.rol}'"
            )

        # Corregir rol en PackFy Express (ID: 3)
        try:
            packfy_empresa = Empresa.objects.get(id=3)
            perfil_packfy, created = PerfilUsuario.objects.get_or_create(
                usuario=usuario,
                empresa=packfy_empresa,
                defaults={"rol": "dueno", "activo": True},
            )

            if created:
                self.stdout.write(
                    f"✅ Perfil creado para {packfy_empresa.nombre} con rol 'dueno'"
                )
            else:
                perfil_packfy.rol = "dueno"
                perfil_packfy.activo = True
                perfil_packfy.save()
                self.stdout.write(
                    f"✅ Rol actualizado a 'dueno' en {packfy_empresa.nombre}"
                )

        except Empresa.DoesNotExist:
            self.stdout.write(
                "❌ Empresa PackFy Express (ID: 3) no encontrada"
            )

        # Verificar resultado final
        perfiles_final = PerfilUsuario.objects.filter(usuario=usuario)
        self.stdout.write(
            f"\n🎯 RESULTADO FINAL: {perfiles_final.count()} perfiles"
        )
        for perfil in perfiles_final:
            self.stdout.write(
                f"   - {perfil.empresa.nombre}: rol='{perfil.rol}' (activo: {perfil.activo})"
            )

        self.stdout.write(
            self.style.SUCCESS("🎉 Roles corregidos exitosamente!")
        )
