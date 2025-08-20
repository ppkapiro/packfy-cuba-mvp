from empresas.models import Empresa
from usuarios.models import Usuario

print("=== ESTADO ACTUAL ===")
empresas = Empresa.objects.all()
print(f"Empresas disponibles: {len(empresas)}")
for emp in empresas:
    print(f"  - {emp.nombre} (slug: {emp.slug})")

print(f"\nUsuarios:")
for user in Usuario.objects.all():
    empresas_count = user.empresas.count()
    print(f"  - {user.email} (empresas: {empresas_count})")

print("\n=== ARREGLANDO ASIGNACIONES ===")
try:
    empresa_demo = Empresa.objects.get(slug="packfy-demo")
    print(f"Empresa encontrada: {empresa_demo.nombre}")

    for usuario in Usuario.objects.all():
        if not usuario.empresas.filter(slug="packfy-demo").exists():
            usuario.empresas.add(empresa_demo)
            print(f"✅ Asignado a {usuario.email}")
        else:
            print(f"ℹ️ {usuario.email} ya tiene la empresa")

    print("\n=== RESULTADO FINAL ===")
    for user in Usuario.objects.all():
        empresas_list = [emp.nombre for emp in user.empresas.all()]
        print(f"  {user.email}: {empresas_list}")

except Exception as e:
    print(f"Error: {e}")
