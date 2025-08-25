#!/usr/bin/env python3
"""# Configurar Django
project_root = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()ACIÓN DE DATOS DE PRUEBA COMPLETOS PARA PACKFY CUBA MVP
========================================================

Este script genera datos de prueba realistas para validar el sistema multi-tenant
y las restricciones de roles en el sistema.

DATOS A CREAR:
- 50 envíos con estados variados
- Remitentes y destinatarios reales
- Distribución por roles y ubicaciones
- Historial de estados realista
- Fechas coherentes

Fecha: 20 de agosto de 2025
"""

import os
import random
import sys
from datetime import datetime, timedelta
from decimal import Decimal

import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from empresas.models import Empresa, PerfilUsuario
from envios.models import Envio, HistorialEstado

Usuario = get_user_model()


class GeneradorDatosPrueba:
    def __init__(self):
        self.empresa = None
        self.usuarios = {}
        self.perfiles = {}

        # Datos realistas para envíos
        self.nombres_cubanos = [
            "Carlos Rodríguez",
            "María González",
            "José Martínez",
            "Ana López",
            "Luis Fernández",
            "Carmen Díaz",
            "Pedro Sánchez",
            "Isabel García",
            "Miguel Hernández",
            "Rosa Pérez",
            "Antonio Ruiz",
            "Esperanza Cruz",
            "Rafael Torres",
            "Marisol Jiménez",
            "Alejandro Castro",
            "Yolanda Ramos",
            "Fernando Silva",
            "Caridad Morales",
            "Ramón Vargas",
            "Miriam Ortega",
        ]

        # Cubanos viviendo en Miami que envían a familia en Cuba
        self.nombres_cubanos_miami = [
            "Rafael Hernández",
            "Yolanda Pérez",
            "Orlando García",
            "Marisol Rodríguez",
            "Ramón Fernández",
            "Caridad Martínez",
            "Alejandro López",
            "Miriam Sánchez",
            "Fernando Díaz",
            "Teresa González",
            "Armando Cruz",
            "Esperanza Ruiz",
            "Carlos Alberto Vega",
            "Lourdes Herrera",
            "Roberto Castellanos",
            "Carmen Rosa Molina",
            "José Luis Delgado",
            "Nidia Santana",
            "Enrique Moreno",
            "Bárbara Jiménez",
        ]

        self.direcciones_cuba = [
            "Calle 23 #456, Vedado, La Habana",
            "Ave. Salvador Allende #789, Cerro, La Habana",
            "Calle Real #123, Santiago de Cuba",
            "Ave. de los Mártires #321, Santa Clara",
            "Calle Maceo #654, Matanzas",
            "Ave. Independencia #987, Camagüey",
            "Calle José Martí #147, Holguín",
            "Ave. Lenin #258, Las Tunas",
            "Calle Céspedes #369, Bayamo",
            "Ave. de la Libertad #741, Cienfuegos",
        ]

        self.direcciones_miami = [
            "8525 NW 53rd St, Doral, FL 33166",
            "1450 Brickell Ave #2301, Miami, FL 33131",
            "2100 SW 8th St, Miami, FL 33135",
            "12550 Biscayne Blvd #405, North Miami, FL 33181",
            "9700 Collins Ave #1234, Bal Harbour, FL 33154",
            "3401 NE 1st Ave #507, Miami, FL 33137",
            "7900 Harbor Island Dr #1501, North Bay Village, FL 33141",
            "2020 N Bayshore Dr #2508, Miami, FL 33137",
            "1500 Bay Rd #1128S, Miami Beach, FL 33139",
            "999 Brickell Bay Dr #2302, Miami, FL 33131",
        ]

        self.productos_tipicos = [
            "Medicamentos (Ibuprofeno, Paracetamol)",
            "Ropa (Camisas, pantalones, zapatos)",
            "Productos electrónicos (Celular, audífonos)",
            "Artículos de higiene personal",
            "Alimentos no perecederos",
            "Productos para el hogar",
            "Libros y material educativo",
            "Herramientas básicas",
            "Cosméticos y perfumes",
            "Juguetes para niños",
            "Suplementos vitamínicos",
            "Artículos deportivos",
            "Productos de belleza",
            "Accesorios para celulares",
            "Ropa interior y calcetines",
        ]

        # Estados y probabilidades realistas
        self.estados_probabilidades = {
            "RECIBIDO": 0.15,  # 15% - Recién llegados
            "EN_TRANSITO": 0.25,  # 25% - En proceso
            "EN_REPARTO": 0.20,  # 20% - Para entrega
            "ENTREGADO": 0.35,  # 35% - Completados
            "DEVUELTO": 0.03,  # 3% - Problemas
            "CANCELADO": 0.02,  # 2% - Cancelaciones
        }

    def obtener_empresa_y_usuarios(self):
        """Obtiene la empresa y usuarios existentes"""
        print("🔍 Obteniendo empresa y usuarios existentes...")

        try:
            self.empresa = Empresa.objects.get(slug="packfy-express")
            print(f"✅ Empresa encontrada: {self.empresa.nombre}")

            # Obtener usuarios por rol
            perfiles = PerfilUsuario.objects.filter(
                empresa=self.empresa, activo=True
            )

            for perfil in perfiles:
                self.usuarios[perfil.rol] = perfil.usuario
                self.perfiles[perfil.rol] = perfil
                print(
                    f"   📋 {perfil.get_rol_display()}: {perfil.usuario.get_full_name()}"
                )

            print(f"✅ Se encontraron {len(self.usuarios)} usuarios activos")

        except Empresa.DoesNotExist:
            print("❌ ERROR: No se encontró la empresa 'packfy-express'")
            print(
                "   Ejecuta primero: python restaurar_estructura_20250820_095645.py"
            )
            sys.exit(1)
        except Exception as e:
            print(f"❌ ERROR inesperado: {e}")
            sys.exit(1)

    def generar_numero_guia(self):
        """Genera un número de guía único"""
        while True:
            numero = f"PCK{random.randint(100000, 999999)}"
            if not Envio.objects.filter(numero_guia=numero).exists():
                return numero

    def obtener_fechas_coherentes(self, estado):
        """Genera fechas coherentes según el estado del envío"""
        ahora = timezone.now()

        if estado == "RECIBIDO":
            # Recibidos en los últimos 2 días
            fecha_creacion = ahora - timedelta(days=random.randint(0, 2))
            fecha_estimada = fecha_creacion + timedelta(
                days=random.randint(7, 14)
            )

        elif estado == "EN_TRANSITO":
            # En tránsito hace 3-10 días
            fecha_creacion = ahora - timedelta(days=random.randint(3, 10))
            fecha_estimada = fecha_creacion + timedelta(
                days=random.randint(7, 14)
            )

        elif estado == "EN_REPARTO":
            # Para reparto hace 5-12 días
            fecha_creacion = ahora - timedelta(days=random.randint(5, 12))
            fecha_estimada = fecha_creacion + timedelta(
                days=random.randint(7, 14)
            )

        elif estado == "ENTREGADO":
            # Entregados hace 1-30 días
            fecha_creacion = ahora - timedelta(days=random.randint(7, 30))
            fecha_estimada = fecha_creacion + timedelta(
                days=random.randint(7, 14)
            )

        elif estado in ["DEVUELTO", "CANCELADO"]:
            # Devueltos/cancelados hace 5-20 días
            fecha_creacion = ahora - timedelta(days=random.randint(5, 20))
            fecha_estimada = fecha_creacion + timedelta(
                days=random.randint(7, 14)
            )

        return fecha_creacion, fecha_estimada

    def seleccionar_usuario_por_accion(self, accion):
        """Selecciona el usuario apropiado según la acción"""
        if accion in ["crear", "recibir"]:
            # Operadores de Miami reciben envíos
            return random.choice(
                [
                    self.usuarios.get("operador_miami"),
                    self.usuarios.get("dueno"),
                ]
            )
        elif accion in ["transito", "reparto"]:
            # Operadores de Cuba manejan distribución
            return random.choice(
                [
                    self.usuarios.get("operador_cuba"),
                    self.usuarios.get("dueno"),
                ]
            )
        elif accion == "entrega":
            # Cualquier operador puede entregar
            return random.choice(
                [
                    self.usuarios.get("operador_cuba"),
                    self.usuarios.get("operador_miami"),
                    self.usuarios.get("dueno"),
                ]
            )
        else:
            # Por defecto, dueño
            return self.usuarios.get("dueno")

    def crear_envio_con_historial(self, datos_envio):
        """Crea un envío con su historial completo"""
        try:
            # Crear el envío
            envio = Envio.objects.create(**datos_envio)

            # Crear historial según el estado actual
            estados_secuencia = self.obtener_secuencia_estados(
                datos_envio["estado_actual"]
            )
            fecha_base = datos_envio["fecha_creacion"]

            for i, estado in enumerate(estados_secuencia):
                # Calcular fecha del estado (progresiva)
                if i == 0:
                    fecha_estado = fecha_base
                else:
                    dias_adicionales = random.randint(1, 3)
                    fecha_estado = fecha_base + timedelta(
                        days=i * dias_adicionales
                    )

                # Seleccionar usuario apropiado
                usuario = self.seleccionar_usuario_por_accion(estado.lower())

                # Crear registro de historial
                HistorialEstado.objects.create(
                    envio=envio,
                    estado=estado,
                    fecha=fecha_estado,
                    comentario=self.obtener_comentario_estado(estado),
                    ubicacion=self.obtener_ubicacion_estado(estado),
                    registrado_por=usuario,
                )

            return envio

        except Exception as e:
            print(f"❌ Error creando envío: {e}")
            return None

    def obtener_secuencia_estados(self, estado_final):
        """Devuelve la secuencia de estados hasta el estado final"""
        secuencias = {
            "RECIBIDO": ["RECIBIDO"],
            "EN_TRANSITO": ["RECIBIDO", "EN_TRANSITO"],
            "EN_REPARTO": ["RECIBIDO", "EN_TRANSITO", "EN_REPARTO"],
            "ENTREGADO": [
                "RECIBIDO",
                "EN_TRANSITO",
                "EN_REPARTO",
                "ENTREGADO",
            ],
            "DEVUELTO": ["RECIBIDO", "EN_TRANSITO", "EN_REPARTO", "DEVUELTO"],
            "CANCELADO": ["RECIBIDO", "CANCELADO"],
        }
        return secuencias.get(estado_final, ["RECIBIDO"])

    def obtener_comentario_estado(self, estado):
        """Devuelve comentarios realistas según el estado"""
        comentarios = {
            "RECIBIDO": [
                "Paquete recibido en almacén de Miami",
                "Envío registrado y procesado",
                "Documentación verificada y aprobada",
            ],
            "EN_TRANSITO": [
                "Paquete en ruta hacia Cuba",
                "Envío despachado en vuelo comercial",
                "En proceso de exportación",
            ],
            "EN_REPARTO": [
                "Paquete llegó a Cuba, preparando entrega",
                "Asignado para reparto local",
                "Coordinando entrega con destinatario",
            ],
            "ENTREGADO": [
                "Paquete entregado exitosamente",
                "Recibido por destinatario",
                "Entrega confirmada y completada",
            ],
            "DEVUELTO": [
                "Destinatario no localizado",
                "Dirección incorrecta",
                "Paquete devuelto por solicitud del cliente",
            ],
            "CANCELADO": [
                "Cancelado por solicitud del remitente",
                "Envío cancelado por documentación incompleta",
                "Cancelación por cambio de planes del cliente",
            ],
        }
        return random.choice(
            comentarios.get(estado, ["Actualización de estado"])
        )

    def obtener_ubicacion_estado(self, estado):
        """Devuelve ubicaciones realistas según el estado"""
        ubicaciones = {
            "RECIBIDO": ["Almacén Miami, FL", "Centro de Procesamiento Miami"],
            "EN_TRANSITO": [
                "En ruta aérea",
                "Aeropuerto José Martí",
                "En tránsito",
            ],
            "EN_REPARTO": [
                "Centro de Distribución La Habana",
                "En reparto local",
            ],
            "ENTREGADO": ["Domicilio del destinatario", "Punto de entrega"],
            "DEVUELTO": ["Centro de Devoluciones", "Almacén Miami"],
            "CANCELADO": ["Procesamiento cancelado", "Almacén Miami"],
        }
        return random.choice(
            ubicaciones.get(estado, ["Ubicación no especificada"])
        )

    def generar_envios(self, cantidad=50):
        """Genera la cantidad especificada de envíos"""
        print(f"\n📦 Generando {cantidad} envíos de prueba...")

        envios_creados = 0
        errores = 0

        for i in range(cantidad):
            try:
                # Seleccionar estado según probabilidades
                estado = random.choices(
                    list(self.estados_probabilidades.keys()),
                    weights=list(self.estados_probabilidades.values()),
                )[0]

                # Generar fechas coherentes
                fecha_creacion, fecha_estimada = (
                    self.obtener_fechas_coherentes(estado)
                )

                # Datos del envío
                datos_envio = {
                    "numero_guia": self.generar_numero_guia(),
                    "estado_actual": estado,
                    "descripcion": random.choice(self.productos_tipicos),
                    "peso": Decimal(str(round(random.uniform(0.5, 15.0), 2))),
                    "valor_declarado": Decimal(
                        str(round(random.uniform(20.0, 500.0), 2))
                    ),
                    # Remitente (desde Miami)
                    "remitente_nombre": random.choice(
                        self.nombres_cubanos_miami
                    ),
                    "remitente_telefono": f"+1-305-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    "remitente_direccion": random.choice(
                        self.direcciones_miami
                    ),
                    # Destinatario (en Cuba)
                    "destinatario_nombre": random.choice(self.nombres_cubanos),
                    "destinatario_telefono": f"+53-{random.randint(50000000, 59999999)}",
                    "destinatario_direccion": random.choice(
                        self.direcciones_cuba
                    ),
                    # Fechas y usuario
                    "fecha_creacion": fecha_creacion,
                    "fecha_estimada_entrega": fecha_estimada,
                    "ultima_actualizacion": timezone.now(),
                    "creado_por": self.seleccionar_usuario_por_accion("crear"),
                    "actualizado_por": self.seleccionar_usuario_por_accion(
                        "crear"
                    ),
                    "empresa": self.empresa,
                }

                # Crear envío con historial
                envio = self.crear_envio_con_historial(datos_envio)

                if envio:
                    envios_creados += 1
                    if envios_creados % 10 == 0:
                        print(f"   ✅ Creados {envios_creados} envíos...")
                else:
                    errores += 1

            except Exception as e:
                errores += 1
                print(f"   ❌ Error en envío {i+1}: {e}")

        print(f"\n📊 RESULTADO:")
        print(f"   ✅ Envíos creados: {envios_creados}")
        print(f"   ❌ Errores: {errores}")

        return envios_creados

    def mostrar_resumen_final(self):
        """Muestra un resumen de los datos creados"""
        print(f"\n📊 RESUMEN FINAL DE DATOS CREADOS")
        print("=" * 50)

        # Contar envíos por estado
        print("\n🚀 ENVÍOS POR ESTADO:")
        for estado, _ in Envio.EstadoChoices.choices:
            count = Envio.objects.filter(
                empresa=self.empresa, estado_actual=estado
            ).count()
            if count > 0:
                print(f"   {estado}: {count} envíos")

        # Total de registros de historial
        total_historial = HistorialEstado.objects.filter(
            envio__empresa=self.empresa
        ).count()
        print(f"\n📋 REGISTROS DE HISTORIAL: {total_historial}")

        # Envíos por usuario creador
        print(f"\n👥 ENVÍOS POR USUARIO CREADOR:")
        for rol, usuario in self.usuarios.items():
            count = Envio.objects.filter(
                empresa=self.empresa, creado_por=usuario
            ).count()
            if count > 0:
                print(
                    f"   {self.perfiles[rol].get_rol_display()}: {count} envíos"
                )

        print(f"\n✅ Sistema listo para pruebas de restricciones de roles!")


def main():
    print("🚀 INICIANDO CREACIÓN DE DATOS DE PRUEBA PARA PACKFY CUBA MVP")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%d de %B de %Y - %H:%M')}")
    print()

    generador = GeneradorDatosPrueba()

    try:
        # Paso 1: Obtener empresa y usuarios
        generador.obtener_empresa_y_usuarios()

        # Paso 2: Limpiar envíos existentes (opcional)
        envios_existentes = Envio.objects.filter(
            empresa=generador.empresa
        ).count()
        if envios_existentes > 0:
            respuesta = input(
                f"\n⚠️  Existen {envios_existentes} envíos. ¿Eliminar antes de crear nuevos? (s/N): "
            )
            if respuesta.lower() in ["s", "si", "sí", "y", "yes"]:
                Envio.objects.filter(empresa=generador.empresa).delete()
                print("🗑️  Envíos anteriores eliminados")

        # Paso 3: Generar nuevos envíos
        envios_creados = generador.generar_envios(50)

        if envios_creados > 0:
            # Paso 4: Mostrar resumen
            generador.mostrar_resumen_final()

            print(f"\n🎉 ¡DATOS DE PRUEBA CREADOS EXITOSAMENTE!")
            print(f"   📦 {envios_creados} envíos con historial completo")
            print(f"   🏢 Asignados a empresa: {generador.empresa.nombre}")
            print(
                f"   👥 Distribuidos entre {len(generador.usuarios)} usuarios"
            )
            print(f"\n🔄 Siguiente paso: Implementar restricciones de roles")

        else:
            print("\n❌ No se pudieron crear datos de prueba")

    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
