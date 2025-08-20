# 🔍 **PLAN: TESTING DE PERMISOS ESPECÍFICOS**

---

## 🎯 **OBJETIVO**

Validar que cada rol de usuario tiene acceso únicamente a los endpoints y datos que le corresponden según su nivel de permisos.

---

## 📋 **ESTRATEGIA DE TESTING**

### **FASE 1: MAPEO DE ENDPOINTS** 🗺️

1. **Descubrir todos los endpoints disponibles**

   - Listar todas las URLs del backend
   - Identificar endpoints protegidos vs públicos
   - Categorizar por funcionalidad

2. **Clasificar endpoints por nivel de acceso**
   - Públicos (sin autenticación)
   - Autenticados (cualquier usuario logueado)
   - Específicos por rol
   - Solo administradores

### **FASE 2: TESTING POR ROL** 👥

Para cada rol, probar:

#### **A. SUPERADMIN** 👑

- Debe tener acceso a TODOS los endpoints
- Gestión de usuarios, empresas, sistema
- Operaciones de administración global

#### **B. DUEÑO** 👔

- Gestión completa de su empresa
- Crear/editar/eliminar usuarios de su empresa
- Ver todos los envíos de su empresa
- Configuración de empresa

#### **C. OPERADORES (Miami/Cuba)** 🌴🏝️

- Gestión de envíos asignados a su región
- Ver envíos de su área geográfica
- Actualizar estado de envíos
- NO crear/eliminar usuarios

#### **D. REMITENTES** 📦

- Crear nuevos envíos
- Ver sus propios envíos
- Editar envíos en estado "borrador"
- NO ver envíos de otros remitentes

#### **E. DESTINATARIOS** 🎯

- Ver envíos dirigidos a ellos
- Confirmar recepción
- Solo lectura de sus datos
- NO crear envíos

### **FASE 3: TESTING DE SEGURIDAD** 🔒

1. **Cross-tenant access**

   - Verificar que usuarios no accedan a datos de otras empresas
   - Probar bypass de filtros por empresa

2. **Escalación de privilegios**

   - Intentar acceder a endpoints de mayor nivel
   - Manipular headers o tokens

3. **Filtrado de datos**
   - Verificar que las listas solo muestren datos permitidos
   - Probar búsquedas y filtros

---

## 🛠️ **HERRAMIENTAS A USAR**

1. **PowerShell** para requests HTTP
2. **cURL** para requests específicos
3. **Scripts automatizados** para testing masivo
4. **Base de datos** para verificar filtros

---

## 📊 **MÉTRICAS DE ÉXITO**

- ✅ **100% de endpoints** mapeados
- ✅ **Cada rol** accede solo a lo permitido
- ✅ **0 accesos no autorizados** detectados
- ✅ **Filtrado por empresa** funcionando
- ✅ **Seguridad validada** sin vulnerabilidades

---

## 🚀 **INICIO: MAPEO DE ENDPOINTS**

**¿Comenzamos con el descubrimiento de todos los endpoints disponibles en el backend?**
