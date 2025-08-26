# 🔐 GUÍA DE CREDENCIALES - SISTEMA MULTITENANCY

## 📋 CREDENCIALES PARA LOGIN

### 👑 SUPERADMIN GLOBAL (Acceso a todas las empresas)

```
Email: superadmin@packfy.com
Password: [usar password existente del superusuario]
Acceso: TODAS las empresas
Rol: super_admin
Tenant: packfy-express (cualquier tenant funciona)
```

### 🏢 ADMINISTRADORES POR EMPRESA

#### 🇨🇺 Cuba Express Cargo

```
Email: admin@cubaexpress.com
Password: admin123
Tenant: cuba-express
Rol: admin_empresa
Dominio: cubaexpress.com
```

#### 🏛️ Habana Premium Logistics

```
Email: admin@habanapremium.com
Password: admin123
Tenant: habana-premium
Rol: admin_empresa
Dominio: habanapremium.com
```

#### 🌊 Miami Shipping Express

```
Email: admin@miamishipping.com
Password: admin123
Tenant: miami-shipping
Rol: admin_empresa
Dominio: miamishipping.com
```

#### 📦 Packfy Express

```
Email: admin@packfy.com
Password: admin123
Tenant: packfy-express
Rol: admin_empresa
Dominio: packfy.com
```

---

## 🌐 CONFIGURACIÓN DE ENDPOINTS

### 🖥️ Backend API

```
Base URL: http://localhost:8000
Login Endpoint: http://localhost:8000/api/auth/login/
Health Check: http://localhost:8000/api/health/
```

### 📱 Frontend de Pruebas

```
Servidor HTTP: http://localhost:8080
Página de Pruebas: http://localhost:8080/test_login_frontend.html
```

---

## 🔧 EJEMPLO DE REQUEST LOGIN

### Headers requeridos:

```json
{
  "Content-Type": "application/json",
  "X-Tenant-Slug": "[slug-de-empresa]"
}
```

### Body del request:

```json
{
  "email": "admin@cubaexpress.com",
  "password": "admin123"
}
```

### Ejemplo completo con curl:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Slug: cuba-express" \
  -d '{"email":"admin@cubaexpress.com","password":"admin123"}'
```

---

## 🎯 MAPEO DOMINIO → TENANT

| Dominio           | Tenant Slug    | Empresa                  |
| ----------------- | -------------- | ------------------------ |
| cubaexpress.com   | cuba-express   | Cuba Express Cargo       |
| habanapremium.com | habana-premium | Habana Premium Logistics |
| miamishipping.com | miami-shipping | Miami Shipping Express   |
| packfy.com        | packfy-express | Packfy Express           |
| localhost         | packfy-express | (desarrollo)             |

---

## 🧪 SCRIPTS DE PRUEBA DISPONIBLES

### Backend (Python):

```bash
cd backend
python prueba_final.py        # Prueba completa
python test_all_logins.py     # Prueba todos los logins
python diagnostico.py         # Diagnóstico de conectividad
```

### Frontend (Navegador):

```
http://localhost:8080/test_login_frontend.html
- Clic en "🚀 Probar Todos los Logins Automáticamente"
```

---

## 📊 RESPUESTA EXITOSA DE LOGIN

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 66,
    "email": "admin@cubaexpress.com",
    "is_superuser": false,
    "empresa_actual": {
      "id": 13,
      "nombre": "Cuba Express Cargo",
      "slug": "cuba-express"
    },
    "rol": "admin_empresa"
  }
}
```

---

## 🚀 COMANDOS PARA INICIAR SERVIDORES

### Django Backend:

```bash
cd backend
python manage.py runserver
# Servidor en: http://localhost:8000
```

### Servidor HTTP para Frontend:

```bash
cd paqueteria-cuba-mvp
python -m http.server 8080
# Servidor en: http://localhost:8080
```

---

## ⚠️ TROUBLESHOOTING

### Si login falla:

1. ✅ Verificar que backend esté corriendo (puerto 8000)
2. ✅ Comprobar X-Tenant-Slug en headers
3. ✅ Verificar email y password correctos
4. ✅ Ejecutar `python diagnostico.py` para diagnóstico

### Si frontend falla:

1. ✅ Verificar servidor HTTP corriendo (puerto 8080)
2. ✅ Acceder desde http://localhost:8080 no file://
3. ✅ Verificar CORS configurado
4. ✅ Abrir DevTools para ver errores de consola

---

## 🎯 ESTADO ACTUAL

✅ **Backend**: 100% funcional - Todos los logins probados
✅ **Credenciales**: Configuradas y verificadas
✅ **Multitenancy**: Implementado correctamente
✅ **CORS**: Configurado para JavaScript
✅ **Documentación**: Completa y actualizada

**🚀 Sistema listo para uso inmediato!**
