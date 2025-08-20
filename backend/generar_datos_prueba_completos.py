#!/usr/bin/env python3
"""
CREACIÓN DE DATOS DE PRUEBA COMPLETOS PARA PACKFY CUBA MVP
========================================================

Este script genera datos de prueba realistas para validar el sistema multi-tenant
y las restricciones de roles en el sistema.

Fecha: 20 de agosto de 2025
"""

import os
import random
from datetime import datetime, timedelta
from decimal import Decimal

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from empresas.models import Empresa, PerfilUsuario
from envios.models import Envio, HistorialEstado

Usuario = get_user_model()


def main():
    print("🚀 INICIANDO CREACIÓN DE DATOS DE PRUEBA PARA PACKFY CUBA MVP")
    print("=" * 60)

    try:
        # Verificar empresa
        empresa = Empresa.objects.get(slug="packfy-express")
        print(f"✅ Empresa encontrada: {empresa.nombre}")

        # Obtener usuarios
        perfiles = PerfilUsuario.objects.filter(empresa=empresa, activo=True)
        usuarios = {}
        for perfil in perfiles:
            usuarios[perfil.rol] = perfil.usuario
            print(
                f"   📋 {perfil.get_rol_display()}: {perfil.usuario.get_full_name()}"
            )

        # Limpiar envíos existentes
        envios_existentes = Envio.objects.filter(empresa=empresa).count()
        if envios_existentes > 0:
            print(f"\n🗑️  Eliminando {envios_existentes} envíos existentes...")
            Envio.objects.filter(empresa=empresa).delete()

        # Datos para generar envíos
        nombres_cubanos = [
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
        ]

        # Cubanos viviendo en Miami (que envían a familia en Cuba)
        nombres_cubanos_miami = [
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
        ]

        direcciones_cuba = [
            "Calle 23 #456, Vedado, La Habana",
            "Ave. Salvador Allende #789, Cerro, La Habana",
            "Calle Real #123, Santiago de Cuba",
            "Ave. de los Mártires #321, Santa Clara",
        ]

        direcciones_miami = [
            "8525 NW 53rd St, Doral, FL 33166",
            "1450 Brickell Ave #2301, Miami, FL 33131",
            "2100 SW 8th St, Miami, FL 33135",
            "12550 Biscayne Blvd #405, North Miami, FL 33181",
        ]

        productos = [
            "Medicamentos (Ibuprofeno, Paracetamol)",
            "Ropa (Camisas, pantalones, zapatos)",
            "Productos electrónicos (Celular, audífonos)",
            "Artículos de higiene personal",
            "Alimentos no perecederos",
        ]

        estados = [
            "RECIBIDO",
            "EN_TRANSITO",
            "EN_REPARTO",
            "ENTREGADO",
            "DEVUELTO",
        ]

        print(f"\n📦 Generando 50 envíos de prueba...")

        envios_creados = 0
        dueno = usuarios.get("dueno")
        operador_miami = usuarios.get("operador_miami")
        operador_cuba = usuarios.get("operador_cuba")

        for i in range(50):
            try:
                # Generar número de guía único
                numero_guia = f"PCK{random.randint(100000, 999999)}"
                while Envio.objects.filter(numero_guia=numero_guia).exists():
                    numero_guia = f"PCK{random.randint(100000, 999999)}"

                # Seleccionar estado
                estado = random.choice(estados)

                # Fechas
                dias_atras = random.randint(1, 30)
                fecha_creacion = timezone.now() - timedelta(days=dias_atras)
                fecha_estimada = fecha_creacion + timedelta(
                    days=random.randint(7, 14)
                )

                # Crear envío
                envio = Envio.objects.create(
                    numero_guia=numero_guia,
                    estado_actual=estado,
                    descripcion=random.choice(productos),
                    peso=Decimal(str(round(random.uniform(0.5, 15.0), 2))),
                    valor_declarado=Decimal(
                        str(round(random.uniform(20.0, 500.0), 2))
                    ),
                    # Remitente (Cubano viviendo en Miami)
                    remitente_nombre=random.choice(nombres_cubanos_miami),
                    remitente_telefono=f"+1-305-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    remitente_direccion=random.choice(direcciones_miami),
                    # Destinatario (Cuba)
                    destinatario_nombre=random.choice(nombres_cubanos),
                    destinatario_telefono=f"+53-{random.randint(50000000, 59999999)}",
                    destinatario_direccion=random.choice(direcciones_cuba),
                    # Sistema
                    fecha_creacion=fecha_creacion,
                    fecha_estimada_entrega=fecha_estimada,
                    ultima_actualizacion=timezone.now(),
                    creado_por=random.choice([dueno, operador_miami]),
                    actualizado_por=random.choice(
                        [dueno, operador_miami, operador_cuba]
                    ),
                    empresa=empresa,
                )

                # Crear historial básico
                HistorialEstado.objects.create(
                    envio=envio,
                    estado="RECIBIDO",
                    fecha=fecha_creacion,
                    comentario="Paquete recibido en almacén",
                    ubicacion="Almacén Miami, FL",
                    registrado_por=operador_miami or dueno,
                )

                if estado != "RECIBIDO":
                    HistorialEstado.objects.create(
                        envio=envio,
                        estado=estado,
                        fecha=fecha_creacion
                        + timedelta(days=random.randint(1, 5)),
                        comentario=f"Estado actualizado a {estado}",
                        ubicacion=(
                            "En tránsito"
                            if estado == "EN_TRANSITO"
                            else "La Habana, Cuba"
                        ),
                        registrado_por=operador_cuba or dueno,
                    )

                envios_creados += 1
                if envios_creados % 10 == 0:
                    print(f"   ✅ Creados {envios_creados} envíos...")

            except Exception as e:
                print(f"   ❌ Error en envío {i+1}: {e}")

        # Mostrar resumen
        print(f"\n📊 RESUMEN FINAL:")
        print(f"   ✅ Envíos creados: {envios_creados}")

        for estado in estados:
            count = Envio.objects.filter(
                empresa=empresa, estado_actual=estado
            ).count()
            if count > 0:
                print(f"   📦 {estado}: {count} envíos")

        total_historial = HistorialEstado.objects.filter(
            envio__empresa=empresa
        ).count()
        print(f"   📋 Registros de historial: {total_historial}")

        print(f"\n🎉 ¡DATOS DE PRUEBA CREADOS EXITOSAMENTE!")
        print(f"🔄 Siguiente paso: Implementar restricciones de roles")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
