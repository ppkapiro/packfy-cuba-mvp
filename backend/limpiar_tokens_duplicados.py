#!/usr/bin/env python3
"""
🇨🇺 PACKFY CUBA - Script de Limpieza de Tokens Duplicados
Soluciona el error: duplicate key value violates unique constraint
"""

import os
import sys

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import models
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


def limpiar_tokens_duplicados():
    """Limpia tokens duplicados de la blacklist"""
    print("🧹 Iniciando limpieza de tokens duplicados...")

    try:
        # Obtener todos los tokens duplicados
        duplicados = (
            BlacklistedToken.objects.values("token_id")
            .annotate(count=models.Count("token_id"))
            .filter(count__gt=1)
        )

        if not duplicados:
            print("✅ No se encontraron tokens duplicados")
            return

        total_eliminados = 0

        for item in duplicados:
            token_id = item["token_id"]
            count = item["count"]

            # Mantener solo el más reciente, eliminar los demás
            tokens_duplicados = BlacklistedToken.objects.filter(
                token_id=token_id
            ).order_by("-blacklisted_at")[
                1:
            ]  # Saltar el primero (más reciente)

            eliminados = len(tokens_duplicados)
            tokens_duplicados.delete()

            total_eliminados += eliminados
            print(
                f"🗑️  Token ID {token_id}: eliminados {eliminados} duplicados"
            )

        print(f"✅ Limpieza completada. Total eliminados: {total_eliminados}")

    except Exception as e:
        print(f"❌ Error durante la limpieza: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    limpiar_tokens_duplicados()
