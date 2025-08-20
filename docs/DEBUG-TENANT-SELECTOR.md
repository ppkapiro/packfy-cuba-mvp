# 🔍 DEBUG: TENANT SELECTOR CARGANDO

## 🎯 PROBLEMA IDENTIFICADO

El TenantSelector queda en estado "cargando" porque:

1. ✅ **Backend endpoint existe**: `/api/empresas/` (devuelve 401 sin auth)
2. ✅ **Frontend API configurado**: Usa `/api` como base URL
3. ❓ **Autenticación**: Posible problema con token en headers

## 🔧 PASOS DE DEBUGGING

### Paso 1: Verificar en Browser Console

Después del login de SUPERADMIN, revisar:

1. **Console log**:

   ```
   🇨🇺 Packfy API configurándose...
   🏢 Empresa cambiada a: ...
   ```

2. **Network tab**:

   - Llamada a `/api/empresas/`
   - Status code de respuesta
   - Headers enviados

3. **Local Storage**:
   - token
   - tenant-slug
   - empresa-actual

### Paso 2: Debugging TenantContext

Revisar si:

- `cargarEmpresas()` se ejecuta
- `isLoading` cambia de true a false
- `empresasDisponibles` se llena
- `empresaActual` se establece

## 🚨 ANÁLISIS PRELIMINAR

**Sospecha principal**: El endpoint está protegido por autenticación pero el token no se está enviando correctamente en los headers.

**Solución temporal**: Si el debugging confirma problema de autenticación, podemos:

1. Verificar el AuthContext
2. Revisar cómo se almacena el token después del login
3. Confirmar que apiClient.makeRequest() incluye el Authorization header

---

**ESTADO**: Debugging en progreso - Verificar browser console
