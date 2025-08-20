#!/usr/bin/env python
import os

import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.db import connection


def check_migrations():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT app, name, applied FROM django_migrations ORDER BY app, id;"
    )
    rows = cursor.fetchall()

    print("Estado de migraciones en la base de datos:")
    print("=" * 60)
    print(f"{'App':<15} {'Migration':<35} {'Applied'}")
    print("=" * 60)

    for row in rows:
        status = "✓" if row[2] else "✗"
        print(f"{row[0]:<15} {row[1]:<35} {status}")

    # Verificar específicamente las migraciones críticas
    critical_migrations = [
        ("empresas", "0002_add_multitenancy_fields"),
        ("empresas", "0003_fix_usuario_relation"),
        ("envios", "0004_alter_envio_empresa"),
    ]

    print("\n" + "=" * 60)
    print("ESTADO DE MIGRACIONES CRÍTICAS:")
    print("=" * 60)

    applied_migrations = [(row[0], row[1]) for row in rows if row[2]]

    for app, migration in critical_migrations:
        if (app, migration) in applied_migrations:
            print(f"✓ {app}.{migration} - APLICADA")
        else:
            print(f"✗ {app}.{migration} - NO APLICADA")


if __name__ == "__main__":
    check_migrations()
