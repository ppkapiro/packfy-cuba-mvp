#!/usr/bin/env python3
"""
Script simple para verificar usuarios en Docker
"""

import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model


def verificar_usuarios():
    User = get_user_model()
    usuarios = User.objects.all().order_by("id")
    print(f"📊 Total usuarios: {usuarios.count()}")
    for u in usuarios:
        print(f"{u.id}: {u.email}")


if __name__ == "__main__":
    verificar_usuarios()
