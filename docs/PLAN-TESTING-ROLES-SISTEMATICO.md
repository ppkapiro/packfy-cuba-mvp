# 🧪 PLAN DE TESTING SISTEMÁTICO DE ROLES

**Fecha:** 20 de agosto de 2025
**Objetivo:** Validación completa de todos los roles de usuario en el sistema multitenancy
**Sistema:** Packfy Cuba MVP - 10 usuarios, 1 empresa (Packfy Express)

---

## 📋 **ESTRUCTURA DE USUARIOS PARA TESTING**

### 👑 **SUPERADMINISTRADOR**

- **Usuario:** `superadmin@packfy.com`
- **Contraseña:** `super123!`
- **Permisos esperados:** Acceso total al Django Admin, gestión de todas las empresas

### 🏢 **ROLES DE EMPRESA (Packfy Express)**

#### 👔 **DUEÑO**

- **Usuario:** `dueno@packfy.com` (Carlos Empresario)
- **Contraseña:** `dueno123!`
- **Permisos esperados:**
  - Gestión completa de la empresa
  - Ver todos los envíos de la empresa
  - Gestionar usuarios de la empresa
  - Acceso a reportes y estadísticas

#### 🌴 **OPERADOR MIAMI**

- **Usuario:** `miami@packfy.com` (Ana Miami)
- **Contraseña:** `miami123!`
- **Permisos esperados:**
  - Gestionar envíos desde Miami
  - Ver envíos de su región
  - Crear y editar envíos
  - NO puede gestionar usuarios

#### 🏝️ **OPERADOR CUBA**

- **Usuario:** `cuba@packfy.com` (Jose Habana)
- **Contraseña:** `cuba123!`
- **Permisos esperados:**
  - Gestionar envíos hacia Cuba
  - Ver envíos de su región
  - Crear y editar envíos
  - NO puede gestionar usuarios

#### 📦 **REMITENTES**

- **Usuario 1:** `remitente1@packfy.com` (Maria Rodriguez)
- **Usuario 2:** `remitente2@packfy.com` (Pedro Gonzalez)
- **Usuario 3:** `remitente3@packfy.com` (Luis Martinez)
- **Contraseña:** `remitente123!` (para todos)
- **Permisos esperados:**
  - Crear envíos propios
  - Ver solo sus envíos
  - Editar envíos en estado "creado"
  - NO puede ver envíos de otros

#### 🎯 **DESTINATARIOS**

- **Usuario 1:** `destinatario1@cuba.cu` (Carmen Perez)
- **Usuario 2:** `destinatario2@cuba.cu` (Elena Fernandez)
- **Usuario 3:** `destinatario3@cuba.cu` (Roberto Silva)
- **Permisos esperados:**
  - Ver envíos dirigidos a ellos
  - Confirmar recepción de envíos
  - NO puede crear envíos
  - NO puede ver envíos de otros

---

## 🔬 **CASOS DE PRUEBA POR ROL**

### **TEST 1: SUPERADMINISTRADOR**

- [ ] Login exitoso en Django Admin
- [ ] Acceso a gestión de usuarios
- [ ] Acceso a gestión de empresas
- [ ] Acceso a gestión de perfiles de usuario
- [ ] Puede crear/editar/eliminar cualquier registro

### **TEST 2: DUEÑO DE EMPRESA**

- [ ] Login exitoso en frontend
- [ ] Ve TenantSelector con Packfy Express
- [ ] Acceso a dashboard con estadísticas completas
- [ ] Puede ver todos los envíos de la empresa
- [ ] Puede gestionar usuarios de la empresa
- [ ] NO puede acceder a otras empresas

### **TEST 3: OPERADOR MIAMI**

- [ ] Login exitoso en frontend
- [ ] Ve TenantSelector con Packfy Express
- [ ] Acceso a dashboard operativo
- [ ] Puede crear nuevos envíos
- [ ] Puede editar envíos existentes
- [ ] Ve envíos de toda la empresa
- [ ] NO puede gestionar usuarios

### **TEST 4: OPERADOR CUBA**

- [ ] Login exitoso en frontend
- [ ] Ve TenantSelector con Packfy Express
- [ ] Acceso a dashboard operativo
- [ ] Puede gestionar estado de envíos
- [ ] Puede marcar envíos como recibidos
- [ ] Ve envíos de toda la empresa
- [ ] NO puede gestionar usuarios

### **TEST 5: REMITENTE**

- [ ] Login exitoso en frontend
- [ ] Ve TenantSelector con Packfy Express
- [ ] Acceso a dashboard personal
- [ ] Puede crear nuevos envíos
- [ ] Ve SOLO sus envíos
- [ ] Puede editar envíos en estado "creado"
- [ ] NO puede ver envíos de otros usuarios
- [ ] NO puede gestionar usuarios

### **TEST 6: DESTINATARIO**

- [ ] Login exitoso en frontend
- [ ] Ve TenantSelector con Packfy Express
- [ ] Acceso a dashboard de recepción
- [ ] Ve SOLO envíos dirigidos a él
- [ ] Puede confirmar recepción
- [ ] NO puede crear envíos
- [ ] NO puede ver envíos de otros
- [ ] NO puede gestionar usuarios

---

## 🛡️ **PRUEBAS DE SEGURIDAD**

### **AISLAMIENTO DE DATOS**

- [ ] Usuario de una empresa NO puede ver datos de otra
- [ ] Remitente NO puede ver envíos de otro remitente
- [ ] Destinatario NO puede ver envíos de otro destinatario
- [ ] Headers X-Tenant-Slug son obligatorios

### **CONTROL DE ACCESO**

- [ ] URLs protegidas requieren autenticación
- [ ] Roles no autorizados reciben 403
- [ ] Acceso directo a APIs sin token falla
- [ ] Manipulación de headers no permite acceso

### **INTEGRIDAD FUNCIONAL**

- [ ] Cambio de empresa actualiza contexto
- [ ] Logout limpia sesión y contexto
- [ ] Refresh del browser mantiene sesión
- [ ] APIs devuelven datos correctos por rol

---

## 📊 **MÉTRICAS DE ÉXITO**

### **Criterios de Aprobación:**

- ✅ **100% de logins exitosos** para usuarios válidos
- ✅ **0% de acceso cross-tenant** no autorizado
- ✅ **Roles funcionando según especificación**
- ✅ **UI mostrando datos correctos por rol**
- ✅ **APIs filtrando datos correctamente**

### **Criterios de Fallo:**

- ❌ Cualquier acceso no autorizado a datos
- ❌ Error en login de usuarios válidos
- ❌ Funcionalidades no disponibles para roles autorizados
- ❌ Datos incorrectos mostrados en UI

---

## 🚀 **PROCESO DE EJECUCIÓN**

1. **Preparación:** Verificar estado de datos iniciales
2. **Testing por rol:** Ejecutar cada caso de prueba
3. **Documentación:** Registrar resultados de cada test
4. **Verificación cruzada:** Probar accesos no autorizados
5. **Reporte final:** Consolidar resultados

---

## 📋 **CHECKLIST DE PREPARACIÓN**

- [ ] Contenedores Docker ejecutándose
- [ ] Base de datos con 10 usuarios verificada
- [ ] Frontend accesible en localhost:5173
- [ ] Backend accesible en localhost:8000
- [ ] Django Admin accesible en localhost:8000/admin
- [ ] Credenciales de todos los usuarios disponibles

**ESTADO:** 🔄 Listo para iniciar testing
