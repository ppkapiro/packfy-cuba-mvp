# 🧪 Guía Completa de Pruebas - Sistema Multitenancy por Dominios

## 📋 Resumen del Sistema Reestructurado

### 🎯 Objetivo Completado

- ✅ **Cada empresa tiene usuarios con su dominio propio**
- ✅ **Un solo superusuario global** (superadmin@packfy.com)
- ✅ **Estructura coherente empresa-dominio-usuarios**

### 🏢 Estructura Final de Empresas y Dominios

| Empresa                  | Dominio           | Admin Principal         | Slug           |
| ------------------------ | ----------------- | ----------------------- | -------------- |
| Cuba Express Cargo       | cubaexpress.com   | admin@cubaexpress.com   | cuba-express   |
| Habana Premium Logistics | habanapremium.com | admin@habanapremium.com | habana-premium |
| Miami Shipping Express   | miamishipping.com | admin@miamishipping.com | miami-shipping |
| Packfy Express           | packfy.com        | admin@packfy.com        | packfy-express |

## 🔐 Credenciales de Acceso

### 👑 Superadmin Global

```
Email: superadmin@packfy.com
Password: [password existente del superusuario]
Acceso: TODAS las empresas
Rol: super_admin
```

### 🏢 Administradores por Empresa

```
# Cuba Express Cargo
Email: admin@cubaexpress.com
Password: admin123
Empresa: Cuba Express Cargo
Rol: admin_empresa

# Habana Premium Logistics
Email: admin@habanapremium.com
Password: admin123
Empresa: Habana Premium Logistics
Rol: admin_empresa

# Miami Shipping Express
Email: admin@miamishipping.com
Password: admin123
Empresa: Miami Shipping Express
Rol: admin_empresa

# Packfy Express
Email: admin@packfy.com
Password: admin123
Empresa: Packfy Express
Rol: admin_empresa
```

## 🧪 Archivos de Prueba Creados

### 1. 🐍 Pruebas Backend (Python)

**Archivo:** `backend/pruebas_login.py`

```bash
cd backend
python pruebas_login.py
```

### 2. 🌐 Pruebas Frontend (HTML/JS)

**Archivo:** `test_login_frontend.html`

- Abrir en navegador: `file:///ruta-proyecto/test_login_frontend.html`
- Pruebas automáticas de login con interfaz visual
- Detección automática de tenant por dominio

## 🚀 Cómo Probar el Sistema

### Paso 1: Verificar Backend Funcionando

```bash
cd backend
python manage.py runserver
```

### Paso 2: Probar con Python Script

```bash
cd backend
python pruebas_login.py
```

### Paso 3: Probar con Frontend

1. Abrir `test_login_frontend.html` en navegador
2. Hacer clic en "🚀 Probar Todos los Logins Automáticamente"
3. Verificar que todos muestren ✅ Login OK

### Paso 4: Probar Frontend React (Multitenant)

```bash
cd frontend-multitenant
npm start
```

## 🔧 Configuración Técnica

### Backend Django

- **Tenant Detection:** Header `X-Tenant-Slug`
- **Authentication:** JWT con tenant context
- **Database:** SQLite con datos separados por empresa

### Frontend React

- **Tenant Detection:** Automático por dominio en `tenantDetector.ts`
- **Domain Mapping:**
  - `cubaexpress.com` → `cuba-express`
  - `habanapremium.com` → `habana-premium`
  - `miamishipping.com` → `miami-shipping`
  - `packfy.com` → `packfy-express`

### API Endpoints

```
POST /api/auth/login/
Headers:
  X-Tenant-Slug: [tenant-slug]
  Content-Type: application/json
Body:
  {
    "email": "admin@empresa.com",
    "password": "password"
  }
```

## ✅ Lista de Verificación

### Estructura de Datos ✅

- [x] Empresas tienen dominios configurados
- [x] Usuarios tienen emails con dominio de su empresa
- [x] Un solo superusuario global
- [x] Admins específicos por empresa

### Autenticación ✅

- [x] Login funciona para todos los usuarios
- [x] Tenant detection automático por dominio
- [x] JWT tokens generados correctamente
- [x] Permisos por rol funcionando

### Frontend ✅

- [x] Detección automática de tenant
- [x] UI adapta según empresa detectada
- [x] Login forms por empresa
- [x] Pruebas automatizadas

## 🐛 Troubleshooting

### Problema: "Login falló"

1. Verificar que backend esté corriendo en puerto 8000
2. Comprobar headers `X-Tenant-Slug` correctos
3. Verificar credenciales en base de datos

### Problema: "Tenant no detectado"

1. Verificar dominio en `tenantDetector.ts`
2. Comprobar configuración de empresa en Django admin
3. Verificar slug de empresa en base de datos

### Verificación Rápida Backend

```bash
cd backend
python -c "
from django.contrib.auth import authenticate
from core.models import *
user = authenticate(username='admin@cubaexpress.com', password='admin123')
print(f'Login OK: {user is not None}')
print(f'Empresa: {user.perfil_usuario.empresa.nombre if user else None}')
"
```

## 📊 Estado del Proyecto

### ✅ Completado

- Análisis de problemas de estructura
- Reestructuración completa de dominios
- Creación de usuarios admin por empresa
- Configuración de superusuario único
- Actualización de tenant detection
- Creación de scripts de pruebas
- Verificación de funcionamiento

### 🎯 Sistema Listo Para

- Producción con dominios reales
- Pruebas de usuario final
- Despliegue con subdomínios
- Configuración de DNS

## 🔄 Próximos Pasos Opcionales

1. **Configurar dominios reales** en hosting
2. **SSL/HTTPS** para cada dominio
3. **Email verification** para nuevos usuarios
4. **Password recovery** por dominio
5. **Audit logs** por tenant
6. **Backup strategies** por empresa

---

## 📞 Soporte

Si hay algún problema:

1. Ejecutar `backend/pruebas_login.py` para diagnóstico
2. Revisar logs en `logs/`
3. Verificar `test_login_frontend.html` para pruebas visuales

**✨ El sistema multitenancy está 100% funcional y listo para uso.**
