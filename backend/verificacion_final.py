#!/usr/bin/env python3
"""
VERIFICACIÓN FINAL - PROBLEMA RESUELTO
======================================

Confirma que el problema de autenticación está completamente resuelto.
"""

import requests
import json

def test_complete_flow():
    """Prueba el flujo completo: login + API con token"""
    print("🔍 VERIFICACIÓN FINAL DEL SISTEMA")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    headers = {
        "Content-Type": "application/json",
        "X-Tenant-Slug": "packfy-express"
    }
    
    # 1. Login
    login_data = {
        "email": "admin@packfy.cu",
        "password": "admin123"
    }
    
    print("📤 1. PROBANDO LOGIN...")
    response = requests.post(f"{base_url}/api/auth/login/", json=login_data, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Login falló: {response.status_code}")
        return False
    
    tokens = response.json()
    print("✅ Login exitoso")
    print(f"   🔑 Token recibido: {tokens['access'][:50]}...")
    
    # 2. Probar API con token
    auth_headers = {
        **headers,
        "Authorization": f"Bearer {tokens['access']}"
    }
    
    print("\n📤 2. PROBANDO API CON TOKEN...")
    response = requests.get(f"{base_url}/api/envios/", headers=auth_headers)
    
    if response.status_code != 200:
        print(f"❌ API falló: {response.status_code}")
        return False
    
    envios = response.json()
    print("✅ API respondió correctamente")
    print(f"   📦 Envíos encontrados: {len(envios.get('results', []))}")
    
    return True

if __name__ == "__main__":
    success = test_complete_flow()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 PROBLEMA COMPLETAMENTE RESUELTO!")
        print("   ✅ Backend: Funcionando")
        print("   ✅ Login con email: Funcionando") 
        print("   ✅ JWT tokens: Funcionando")
        print("   ✅ API con autenticación: Funcionando")
        print("\n💡 EL FRONTEND AHORA DEBERÍA CONECTARSE CORRECTAMENTE")
        print("   Recargar la página del frontend para probar.")
    else:
        print("❌ PROBLEMA AÚN EXISTE")
        print("   Revisar logs del servidor.")
