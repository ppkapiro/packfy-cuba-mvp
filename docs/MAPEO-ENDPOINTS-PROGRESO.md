# 🗺️ **MAPEO DE ENDPOINTS - SISTEMA PACKFY**

---

## 📊 **ENDPOINTS PRINCIPALES IDENTIFICADOS**

### ✅ **ENDPOINTS FUNCIONALES**

| Endpoint                  | Método | Descripción               | Acceso Superadmin | Tipo Respuesta         |
| ------------------------- | ------ | ------------------------- | ----------------- | ---------------------- |
| `/api/usuarios/me/`       | GET    | Perfil del usuario actual | ✅                | Objeto individual      |
| `/api/empresas/`          | GET    | Lista de empresas         | ✅                | Paginado (1 elemento)  |
| `/api/envios/`            | GET    | Lista de envíos           | ✅                | Paginado (0 elementos) |
| `/api/historial-estados/` | GET    | Historial de estados      | ✅                | Paginado (0 elementos) |
| `/api/sistema-info/`      | GET    | Información del sistema   | ✅                | Objeto individual      |
| `/api/health/`            | GET    | Health check              | ✅                | Objeto individual      |

### ❌ **ENDPOINTS RESTRINGIDOS**

| Endpoint         | Método | Error         | Posible Causa                   |
| ---------------- | ------ | ------------- | ------------------------------- |
| `/api/usuarios/` | GET    | 403 Forbidden | Permisos específicos requeridos |

### 🔐 **ENDPOINTS DE AUTENTICACIÓN**

| Endpoint             | Método | Descripción              | Público    |
| -------------------- | ------ | ------------------------ | ---------- |
| `/api/auth/login/`   | POST   | Login con email/password | ✅ Público |
| `/api/auth/refresh/` | POST   | Refresh del token JWT    | ✅ Público |

---

## 🎯 **ANÁLISIS INICIAL**

### ✅ **OBSERVACIONES POSITIVAS**

1. **Autenticación funciona**: El superadmin puede obtener tokens
2. **Multitenancy operativo**: El header `X-Tenant-Slug` funciona
3. **Endpoints básicos accesibles**: La mayoría responde correctamente
4. **Estructura de permisos**: Existe un sistema de permisos granular

### ⚠️ **OBSERVACIONES IMPORTANTES**

1. **`/api/usuarios/` bloqueado**: Incluso para superadmin (revisar permisos)
2. **Datos vacíos**: Los envíos e historial están vacíos (esperado en testing)
3. **Paginación**: Todos los endpoints usan paginación de DRF

---

## 🔍 **SIGUIENTE PASO: ANÁLISIS DE PERMISOS**

**¿Por qué el superadmin no puede acceder a `/api/usuarios/`?**

Necesitamos revisar:

1. Los permisos definidos en `UsuarioViewSet`
2. Las clases de permisos específicas del multitenancy
3. Si hay filtros adicionales que bloquean el acceso

---

## 🚀 **PLAN DE TESTING POR ROLES**

Ahora que conocemos los endpoints base, vamos a probar cada rol:

1. **Superadmin** - Revisar por qué no accede a usuarios
2. **Dueño** - Debería gestionar usuarios de su empresa
3. **Operadores** - Solo ver usuarios, no gestionar
4. **Remitentes/Destinatarios** - Acceso limitado

**¿Continuamos investigando los permisos de `/api/usuarios/`?**
