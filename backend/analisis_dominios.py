#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ANALISIS ACTUAL DE DOMINIOS
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from empresas.models import Empresa, PerfilUsuario
from usuarios.models import Usuario


def analizar_estado_actual():
    print("=== ANALISIS ACTUAL DE DOMINIOS ===")
    print()

    # 1. Empresas y dominios
    print("1. EMPRESAS Y SUS DOMINIOS:")
    empresas = Empresa.objects.filter(activo=True)

    for empresa in empresas:
        print(f"   {empresa.nombre}:")
        print(f"     ID: {empresa.id}")
        dominio = empresa.dominio or "NO CONFIGURADO"
        print(f"     Dominio: {dominio}")
        slug = empresa.slug or "NO CONFIGURADO"
        print(f"     Slug: {slug}")

        # Usuarios de esta empresa
        usuarios = PerfilUsuario.objects.filter(empresa=empresa, activo=True)
        print(f"     Usuarios ({usuarios.count()}):")
        for perfil in usuarios:
            email_domain = perfil.usuario.email.split("@")[1]
            print(f"       - {perfil.usuario.email} ({perfil.rol}) [@{email_domain}]")
        print()

    print("2. ANALISIS POR DOMINIO DE EMAIL:")

    # Agrupar usuarios por dominio de email
    dominios_email = {}
    usuarios = Usuario.objects.filter(is_active=True)

    for usuario in usuarios:
        dominio = usuario.email.split("@")[1] if "@" in usuario.email else "SIN_DOMINIO"
        if dominio not in dominios_email:
            dominios_email[dominio] = []
        dominios_email[dominio].append(usuario)

    for dominio, usuarios_dominio in dominios_email.items():
        print(f"   @{dominio}: {len(usuarios_dominio)} usuarios")
        for usuario in usuarios_dominio:
            perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
            empresas_count = perfiles.count()
            if empresas_count > 0:
                empresas_nombres = [p.empresa.nombre for p in perfiles]
                print(
                    f"     - {usuario.email} -> {empresas_count} empresas: {empresas_nombres}"
                )
            else:
                print(f"     - {usuario.email} -> Sin empresas")
        print()

    print("3. PROBLEMAS IDENTIFICADOS:")
    problemas = []

    # Usuarios @packfy.com en empresas que no son Packfy Express
    usuarios_packfy = Usuario.objects.filter(
        email__endswith="@packfy.com", is_active=True
    )

    for usuario in usuarios_packfy:
        if usuario.email == "superadmin@packfy.com":
            continue  # Este debe ser global

        perfiles = PerfilUsuario.objects.filter(usuario=usuario, activo=True)
        empresas_no_packfy = perfiles.exclude(empresa__nombre="Packfy Express")

        if empresas_no_packfy.exists():
            empresas_problematicas = [p.empresa.nombre for p in empresas_no_packfy]
            problemas.append(
                f"❌ {usuario.email} en empresas no-Packfy: {empresas_problematicas}"
            )

    # Empresas sin dominios configurados
    for empresa in empresas:
        if not empresa.dominio:
            problemas.append(f"❌ {empresa.nombre} sin dominio configurado")

    # Usuarios de dominios incorrectos
    mapeo_esperado = {
        "Cuba Express Cargo": "cubaexpress.com",
        "Habana Premium Logistics": "habanapremium.com",
        "Miami Shipping Express": "miamishipping.com",
        "Packfy Express": "packfy.com",
    }

    for empresa in empresas:
        dominio_esperado = mapeo_esperado.get(empresa.nombre)
        if dominio_esperado:
            usuarios_empresa = PerfilUsuario.objects.filter(
                empresa=empresa, activo=True
            )
            for perfil in usuarios_empresa:
                email_domain = perfil.usuario.email.split("@")[1]
                if (
                    email_domain != dominio_esperado
                    and perfil.usuario.email != "superadmin@packfy.com"
                ):
                    problemas.append(
                        f"❌ {perfil.usuario.email} debería ser @{dominio_esperado} para {empresa.nombre}"
                    )

    if problemas:
        for problema in problemas:
            print(f"   {problema}")
    else:
        print("   ✅ No se encontraron problemas")

    print()
    print("4. PROPUESTA DE REESTRUCTURACIÓN:")
    print("   🎯 OBJETIVO: Usuarios por dominio de empresa")
    print("   👑 superadmin@packfy.com -> ACCESO GLOBAL")
    print("   🏢 admin@cubaexpress.com -> Cuba Express Cargo")
    print("   🏢 admin@habanapremium.com -> Habana Premium Logistics")
    print("   🏢 admin@miamishipping.com -> Miami Shipping Express")
    print("   🏢 admin@packfy.com -> Packfy Express")


if __name__ == "__main__":
    analizar_estado_actual()
