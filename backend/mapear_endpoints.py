#!/usr/bin/env python
"""
Script para mapear todos los endpoints disponibles en el sistema
"""

import json
import os
import sys

from django.conf import settings
from django.urls import get_resolver

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()


def extract_endpoints(resolver, prefix=""):
    """Extrae todos los endpoints de un resolver"""
    endpoints = []

    for pattern in resolver.url_patterns:
        if hasattr(pattern, "url_patterns"):
            # Es un include, recursivo
            new_prefix = prefix + str(pattern.pattern)
            endpoints.extend(extract_endpoints(pattern, new_prefix))
        else:
            # Es un endpoint final
            endpoint = {
                "pattern": prefix + str(pattern.pattern),
                "name": getattr(pattern, "name", None),
                "callback": str(getattr(pattern, "callback", None)),
            }
            endpoints.append(endpoint)

    return endpoints


def main():
    print("=== MAPEO DE ENDPOINTS DE PACKFY ===")

    # Obtener el resolver principal
    resolver = get_resolver()

    # Extraer todos los endpoints
    endpoints = extract_endpoints(resolver)

    # Filtrar y organizar
    api_endpoints = []
    admin_endpoints = []
    other_endpoints = []

    for endpoint in endpoints:
        pattern = endpoint["pattern"]
        if "api/" in pattern:
            api_endpoints.append(endpoint)
        elif "admin/" in pattern:
            admin_endpoints.append(endpoint)
        else:
            other_endpoints.append(endpoint)

    print(f"\n📊 RESUMEN:")
    print(f"Total endpoints: {len(endpoints)}")
    print(f"API endpoints: {len(api_endpoints)}")
    print(f"Admin endpoints: {len(admin_endpoints)}")
    print(f"Otros endpoints: {len(other_endpoints)}")

    print(f"\n🔥 API ENDPOINTS:")
    for endpoint in sorted(api_endpoints, key=lambda x: x["pattern"]):
        print(f"  {endpoint['pattern']} -> {endpoint['name']}")

    print(f"\n⚙️ ADMIN ENDPOINTS:")
    for endpoint in sorted(
        admin_endpoints[:10], key=lambda x: x["pattern"]
    ):  # Solo primeros 10
        print(f"  {endpoint['pattern']} -> {endpoint['name']}")

    print(f"\n🌐 OTROS ENDPOINTS:")
    for endpoint in sorted(other_endpoints, key=lambda x: x["pattern"]):
        print(f"  {endpoint['pattern']} -> {endpoint['name']}")


if __name__ == "__main__":
    main()
