#!/usr/bin/env python
"""
Script para probar la protección de usuarios demo
Intenta hacer modificaciones que deberían ser bloqueadas
"""
import requests
import json

def test_proteccion_usuarios():
    """Probar que los usuarios demo están protegidos"""
    print("🧪 Probando protección de usuarios demo")
    
    base_url = "http://localhost:8000"
    
    # Intentar modificar usuario admin
    print("\n1. Intentando modificar usuario admin...")
    try:
        response = requests.patch(
            f"{base_url}/api/usuarios/4/",
            json={"first_name": "Admin Modificado"},
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 403:
            print("   ✅ PROTEGIDO - Modificación bloqueada correctamente")
        else:
            print(f"   ❌ NO PROTEGIDO - Respuesta: {response.text}")
    except Exception as e:
        print(f"   ⚠️  Error de conexión: {e}")
    
    # Intentar crear usuario con email protegido
    print("\n2. Intentando crear usuario con email protegido...")
    try:
        response = requests.post(
            f"{base_url}/api/auth/register/",
            json={
                "email": "admin@packfy.cu",
                "password": "nueva123",
                "first_name": "Nuevo",
                "last_name": "Admin"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 403:
            print("   ✅ PROTEGIDO - Creación bloqueada correctamente")
        else:
            print(f"   ❌ NO PROTEGIDO - Respuesta: {response.text}")
    except Exception as e:
        print(f"   ⚠️  Error de conexión: {e}")
    
    # Verificar que usuarios normales sí se pueden crear
    print("\n3. Intentando crear usuario normal (debería funcionar)...")
    try:
        response = requests.post(
            f"{base_url}/api/auth/register/",
            json={
                "email": "test.normal@example.com",
                "password": "test123",
                "first_name": "Usuario",
                "last_name": "Normal"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print("   ✅ FUNCIONANDO - Usuario normal creado correctamente")
        else:
            print(f"   ⚠️  Usuario normal no se pudo crear: {response.text}")
    except Exception as e:
        print(f"   ⚠️  Error de conexión: {e}")

if __name__ == "__main__":
    test_proteccion_usuarios()
    print("\n✅ Prueba de protección completada")
