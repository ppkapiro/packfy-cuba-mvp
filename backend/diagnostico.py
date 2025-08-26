import json
import urllib.request

print("=== DIAGNÓSTICO DE CONECTIVIDAD ===")

# Test 1: Verificar que el servidor responde
try:
    response = urllib.request.urlopen("http://localhost:8000/")
    print("✅ Servidor Django responde")
except Exception as e:
    print(f"❌ Servidor Django no responde: {e}")

# Test 2: Probar endpoint de login
try:
    url = "http://localhost:8000/api/auth/login/"
    data = json.dumps(
        {"email": "admin@cubaexpress.com", "password": "admin123"}
    ).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-Tenant-Slug": "cuba-express"}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        print("✅ Login endpoint funciona")
        print(f"Status: {response.getcode()}")
except Exception as e:
    print(f"❌ Login endpoint falla: {e}")

print("=== FIN DIAGNÓSTICO ===")
