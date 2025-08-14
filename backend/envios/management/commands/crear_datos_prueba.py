"""
🇨🇺 PACKFY CUBA - Comando Django para crear datos de prueba
"""

import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from envios.models import Envio

Usuario = get_user_model()


class Command(BaseCommand):
    help = "Crea 20 envíos de prueba para PACKFY CUBA"

    def handle(self, *args, **options):
        self.stdout.write("🇨🇺 CREANDO DATOS DE PRUEBA PARA PACKFY CUBA...")

        # Datos realistas cubanos
        nombres_cubanos = [
            "María José García",
            "Carlos Manuel Rodríguez",
            "Ana Beatriz López",
            "José Antonio Martínez",
            "Carmen Elena Pérez",
            "Roberto Carlos Sánchez",
            "Yolanda María Fernández",
            "Miguel Ángel González",
            "Laura Isabel Díaz",
            "Francisco Javier Herrera",
            "Rosa María Castro",
            "Eduardo Luis Torres",
            "Marisol Esperanza Ruiz",
            "Antonio José Ramírez",
            "Silvia Carolina Morales",
            "Rafael Alberto Jiménez",
            "Esperanza del Carmen Vargas",
            "Luis Miguel Ortega",
            "Carmen Rosa Delgado",
            "Jorge Alberto Mendoza",
        ]

        direcciones_cuba = [
            "Calle 23 #456, Vedado, La Habana",
            "Avenida 26 #123, Nuevo Vedado, La Habana",
            "Calle Real #89, Centro Habana",
            "Malecón #234, Habana Vieja",
            "5ta Avenida #567, Miramar, Playa",
            "Calle L #345, Vedado, La Habana",
            "Avenida Carlos III #678, Centro Habana",
            "Calle 17 #890, Vedado, La Habana",
            "Paseo #123, Plaza de la Revolución",
            "Línea #456, Vedado, La Habana",
            "Calle Obispo #789, Habana Vieja",
            "Avenida Rancho Boyeros #234, Arroyo Naranjo",
            "Calle San Lázaro #567, Centro Habana",
            "Calle G #890, Vedado, La Habana",
            "Avenida Salvador Allende #123, Cerro",
            "Calle Zanja #456, Centro Habana",
            "Calle 21 #789, Vedado, La Habana",
            "Avenida 41 #234, Playa",
            "Calle Galiano #567, Centro Habana",
            "Calle San Rafael #890, Centro Habana",
        ]

        productos_cubanos = [
            "Medicamentos para diabetes",
            "Ropa de bebé",
            "Teléfono móvil Samsung",
            "Productos de aseo personal",
            "Suplementos vitamínicos",
            "Ropa de mujer talla M",
            "Zapatos deportivos Nike",
            "Laptop HP",
            "Productos de belleza",
            "Herramientas de trabajo",
            "Juguetes para niños",
            "Ropa de hombre talla L",
            "Electrodomésticos pequeños",
            "Productos para el cabello",
            "Medicamentos cardiológicos",
            "Equipos electrónicos",
            "Cosméticos y perfumes",
            "Ropa deportiva",
            "Productos alimenticios",
            "Accesorios para teléfonos",
        ]

        ciudades_origen = [
            "Miami, FL",
            "Madrid, España",
            "México DF, México",
            "Toronto, Canadá",
            "Ciudad de Panamá, Panamá",
            "Caracas, Venezuela",
            "Buenos Aires, Argentina",
            "Roma, Italia",
            "París, Francia",
            "Nueva York, NY",
        ]

        estados_posibles = [
            "pendiente",
            "en_transito",
            "en_aduana",
            "entregado",
        ]
        tipos_envio = ["estandar", "express", "premium"]

        # Obtener o crear usuario de prueba
        try:
            usuario = Usuario.objects.get(username="admin")
        except Usuario.DoesNotExist:
            self.stdout.write("⚠️ Creando usuario admin para las pruebas...")
            usuario = Usuario.objects.create_user(
                username="admin",
                email="admin@packfy.cu",
                password="admin123",
                first_name="Administrador",
                last_name="Sistema",
            )

        # Limpiar envíos existentes de prueba
        envios_existentes = Envio.objects.filter(
            numero_tracking__startswith="PKY"
        )
        if envios_existentes.exists():
            self.stdout.write(
                f"🗑️ Eliminando {envios_existentes.count()} envíos existentes..."
            )
            envios_existentes.delete()

        envios_creados = []

        self.stdout.write("📦 Creando 20 envíos de prueba...")

        for i in range(20):
            # Generar datos aleatorios pero realistas
            numero_tracking = f"PKY{2025}{(i+1):03d}{random.randint(100, 999)}"
            nombre_destinatario = nombres_cubanos[i]
            direccion_destinatario = direcciones_cuba[i]
            descripcion = productos_cubanos[i]
            peso = round(random.uniform(0.5, 15.0), 2)
            valor_declarado = round(random.uniform(50.0, 1500.0), 2)
            ciudad_origen = random.choice(ciudades_origen)
            estado = random.choice(estados_posibles)
            tipo_envio = random.choice(tipos_envio)

            # Fechas realistas
            fecha_envio = datetime.now() - timedelta(
                days=random.randint(1, 30)
            )

            if estado == "entregado":
                fecha_entrega = fecha_envio + timedelta(
                    days=random.randint(7, 21)
                )
            else:
                fecha_entrega = None

            # Calcular costo basado en peso y tipo
            costo_base = peso * 12.50  # $12.50 por kg
            if tipo_envio == "express":
                costo_base *= 1.5
            elif tipo_envio == "premium":
                costo_base *= 2.0

            costo_envio = round(costo_base, 2)

            # Crear el envío
            envio = Envio.objects.create(
                numero_tracking=numero_tracking,
                usuario=usuario,
                nombre_destinatario=nombre_destinatario,
                direccion_destinatario=direccion_destinatario,
                telefono_destinatario=f"537{random.randint(1000, 9999)}{random.randint(1000, 9999)}",
                descripcion=descripcion,
                peso=Decimal(str(peso)),
                valor_declarado=Decimal(str(valor_declarado)),
                costo_envio=Decimal(str(costo_envio)),
                ciudad_origen=ciudad_origen,
                estado=estado,
                tipo_envio=tipo_envio,
                fecha_envio=fecha_envio,
                fecha_entrega=fecha_entrega,
                notas_especiales=f"Envío #{i+1} - Datos de prueba generados automáticamente",
            )

            envios_creados.append(envio)

            # Mostrar progreso
            self.stdout.write(
                f"  ✅ {numero_tracking} - {nombre_destinatario} - {descripcion[:30]}... - {estado}"
            )

        self.stdout.write(
            f"\n🎉 ¡COMPLETADO! Se crearon {len(envios_creados)} envíos de prueba exitosamente."
        )

        # Estadísticas
        estadisticas = {}
        for estado in estados_posibles:
            count = len([e for e in envios_creados if e.estado == estado])
            estadisticas[estado] = count

        self.stdout.write("\n📊 ESTADÍSTICAS DE LOS ENVÍOS CREADOS:")
        for estado, count in estadisticas.items():
            self.stdout.write(f"  📦 {estado.upper()}: {count} envíos")

        peso_total = sum([float(e.peso) for e in envios_creados])
        valor_total = sum([float(e.valor_declarado) for e in envios_creados])
        costo_total = sum([float(e.costo_envio) for e in envios_creados])

        self.stdout.write(f"\n💰 TOTALES:")
        self.stdout.write(f"  ⚖️ Peso total: {peso_total:.2f} kg")
        self.stdout.write(f"  💎 Valor declarado total: ${valor_total:,.2f}")
        self.stdout.write(f"  💵 Costo envío total: ${costo_total:,.2f}")

        self.stdout.write(
            self.style.SUCCESS("\n✅ Proceso completado exitosamente!")
        )
