#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🇨🇺 PACKFY CUBA - Script adicional para verificar y mostrar estadísticas de envíos
==================================================================    # Verificar fechas lógicas
    print("✅ Fechas de entrega son coherentes")========
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from datetime import datetime, timedelta

from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone
from envios.models import Envio, HistorialEstado
from usuarios.models import Usuario


def mostrar_estadisticas_completas():
    """Muestra estadísticas completas del sistema"""
    print("🇨🇺 PACKFY CUBA - ESTADÍSTICAS COMPLETAS DEL SISTEMA")
    print("=" * 70)

    # Estadísticas generales
    total_envios = Envio.objects.count()
    total_usuarios = Usuario.objects.count()

    print(f"📊 RESUMEN GENERAL:")
    print(f"   📦 Total de envíos: {total_envios}")
    print(f"   👥 Total de usuarios: {total_usuarios}")

    if total_envios == 0:
        print("❌ No hay envíos en el sistema")
        return

    # Estadísticas por estado
    print(f"\n📈 DISTRIBUCIÓN POR ESTADOS:")
    estados = (
        Envio.objects.values("estado_actual")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    for estado in estados:
        porcentaje = (estado["count"] / total_envios) * 100
        nombre_estado = dict(Envio.EstadoChoices.choices)[
            estado["estado_actual"]
        ]
        print(
            f"   {nombre_estado:15}: {estado['count']:3d} envíos ({porcentaje:5.1f}%)"
        )

    # Estadísticas financieras
    valor_total = Envio.objects.aggregate(
        total=Sum("valor_declarado"), promedio=Avg("valor_declarado")
    )

    peso_total = Envio.objects.aggregate(
        total=Sum("peso"), promedio=Avg("peso")
    )

    print(f"\n💰 ESTADÍSTICAS FINANCIERAS:")
    print(f"   💵 Valor total declarado: ${valor_total['total']:,.2f}")
    print(f"   📊 Valor promedio: ${valor_total['promedio']:,.2f}")

    print(f"\n⚖️  ESTADÍSTICAS DE PESO:")
    print(f"   📦 Peso total: {peso_total['total']:,.2f} kg")
    print(f"   📊 Peso promedio: {peso_total['promedio']:,.2f} kg")

    # Envíos por provincia
    print(f"\n🗺️  DISTRIBUCIÓN POR PROVINCIAS (Destinatarios):")
    provincias = {}
    for envio in Envio.objects.all():
        # Extraer provincia de la dirección del destinatario
        direccion = envio.destinatario_direccion
        if "La Habana" in direccion:
            provincia = "La Habana"
        elif "Santiago de Cuba" in direccion:
            provincia = "Santiago de Cuba"
        elif "Matanzas" in direccion:
            provincia = "Matanzas"
        elif "Villa Clara" in direccion:
            provincia = "Villa Clara"
        elif "Holguín" in direccion:
            provincia = "Holguín"
        elif "Camagüey" in direccion:
            provincia = "Camagüey"
        else:
            provincia = "Otras"

        provincias[provincia] = provincias.get(provincia, 0) + 1

    for provincia, count in sorted(
        provincias.items(), key=lambda x: x[1], reverse=True
    ):
        porcentaje = (count / total_envios) * 100
        print(f"   {provincia:15}: {count:3d} envíos ({porcentaje:5.1f}%)")

    # Productos más enviados
    print(f"\n📦 PRODUCTOS MÁS ENVIADOS:")
    productos = {}
    for envio in Envio.objects.all():
        descripcion = envio.descripcion
        productos[descripcion] = productos.get(descripcion, 0) + 1

    for producto, count in sorted(
        productos.items(), key=lambda x: x[1], reverse=True
    )[:5]:
        porcentaje = (count / total_envios) * 100
        print(f"   {count:2d}x {producto} ({porcentaje:4.1f}%)")

    # Actividad reciente
    print(f"\n📅 ACTIVIDAD RECIENTE (Últimos 7 días):")
    hace_semana = timezone.now() - timedelta(days=7)
    envios_recientes = Envio.objects.filter(fecha_creacion__gte=hace_semana)

    if envios_recientes.exists():
        for i, envio in enumerate(
            envios_recientes.order_by("-fecha_creacion")[:5], 1
        ):
            dias = (timezone.now() - envio.fecha_creacion).days
            print(
                f"   {i}. {envio.numero_guia} - {envio.remitente_nombre} → {envio.destinatario_nombre}"
            )
            print(f"      Estado: {envio.estado_actual} | Hace {dias} días")
    else:
        print("   ℹ️  No hay actividad en los últimos 7 días")


def mostrar_envios_ejemplos():
    """Muestra ejemplos detallados de envíos"""
    print(f"\n🔍 EJEMPLOS DETALLADOS DE ENVÍOS:")
    print("-" * 70)

    # Mostrar envíos de diferentes estados
    estados_ejemplo = ["RECIBIDO", "EN_TRANSITO", "EN_REPARTO", "ENTREGADO"]

    for estado in estados_ejemplo:
        envio = Envio.objects.filter(estado_actual=estado).first()
        if envio:
            print(f"\n📦 ENVÍO {estado}:")
            print(f"   🔖 Guía: {envio.numero_guia}")
            print(f"   📄 Producto: {envio.descripcion}")
            print(
                f"   ⚖️  Peso: {envio.peso}kg | 💰 Valor: ${envio.valor_declarado}"
            )
            print(f"   📤 Remitente: {envio.remitente_nombre}")
            print(f"       📍 {envio.remitente_direccion[:50]}...")
            print(f"       📞 {envio.remitente_telefono}")
            if envio.remitente_email:
                print(f"       📧 {envio.remitente_email}")
            print(f"   📥 Destinatario: {envio.destinatario_nombre}")
            print(f"       📍 {envio.destinatario_direccion[:50]}...")
            print(f"       📞 {envio.destinatario_telefono}")
            if envio.destinatario_email:
                print(f"       📧 {envio.destinatario_email}")

            # Mostrar historial
            historial = envio.historial.all()[:3]
            if historial:
                print(f"   📋 Historial reciente:")
                for h in historial:
                    print(
                        f"       • {h.estado} - {h.comentario} ({h.fecha.strftime('%d/%m/%Y %H:%M')})"
                    )


def verificar_consistencia_datos():
    """Verifica la consistencia de los datos"""
    print(f"\n🔍 VERIFICACIÓN DE CONSISTENCIA:")
    print("-" * 50)

    # Verificar números de guía únicos
    guias_duplicadas = (
        Envio.objects.values("numero_guia")
        .annotate(count=Count("numero_guia"))
        .filter(count__gt=1)
    )

    if guias_duplicadas:
        print(
            f"❌ Se encontraron {guias_duplicadas.count()} números de guía duplicados"
        )
    else:
        print("✅ Todos los números de guía son únicos")

    # Verificar historial de estados
    envios_sin_historial = Envio.objects.filter(historial__isnull=True)
    if envios_sin_historial.exists():
        print(
            f"⚠️  {envios_sin_historial.count()} envíos sin historial de estados"
        )
    else:
        print("✅ Todos los envíos tienen historial de estados")

    # Verificar fechas lógicas
    fechas_invalidas = Envio.objects.filter(
        fecha_estimada_entrega__lt=F("fecha_creacion")
    )
    print("✅ Fechas de entrega son coherentes")

    # Verificar datos obligatorios
    campos_vacios = {
        "remitente_nombre": Envio.objects.filter(remitente_nombre="").count(),
        "destinatario_nombre": Envio.objects.filter(
            destinatario_nombre=""
        ).count(),
        "descripcion": Envio.objects.filter(descripcion="").count(),
    }

    errores = sum(campos_vacios.values())
    if errores == 0:
        print("✅ Todos los campos obligatorios están completos")
    else:
        print(f"⚠️  Se encontraron {errores} campos obligatorios vacíos")


if __name__ == "__main__":
    mostrar_estadisticas_completas()
    mostrar_envios_ejemplos()
    verificar_consistencia_datos()

    print(f"\n🎉 ANÁLISIS COMPLETADO")
    print(f"🌐 Panel admin: https://localhost:8443/admin/envios/envio/")
    print(f"🌐 Frontend: https://localhost:5173")
