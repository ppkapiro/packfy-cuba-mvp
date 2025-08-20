# 📋 ANÁLISIS DE FORMULARIOS DE ENVÍO

## ✅ **ESTADO ACTUAL**

### **Frontend - Formularios Existentes:**

1. **`SimpleForm.tsx`** - Formulario básico/gratuito

   - ✅ Interfaz simple para usuarios básicos
   - ✅ Cálculo de precios integrado
   - ✅ Campos: destinatario, peso, descripción, urgencia
   - ⚠️ **PROBLEMA**: No integrado con nuevo sistema multitenancy

2. **`AdvancedPackageForm.tsx`** - Formulario avanzado por pasos

   - ✅ Proceso step-by-step (Info → Precio → Fotos → Etiqueta)
   - ✅ Calculadora de precios
   - ✅ Captura de fotos
   - ✅ Generación de etiquetas QR
   - ⚠️ **PROBLEMA**: No integrado con backend real

3. **`ModernAdvancedForm.tsx`** - Formulario modernizado
   - ✅ UI mejorada
   - ⚠️ **PROBLEMA**: Duplicado del anterior

### **Backend - API de Envíos:**

1. **`Envio` Model** - ✅ Completo y robusto

   - ✅ Campos completos: remitente, destinatario, peso, valor
   - ✅ Estados: recibido, en_transito, en_reparto, entregado
   - ✅ Multitenancy: Campo `empresa` integrado
   - ✅ Historial de estados completo
   - ✅ Número de guía auto-generado

2. **`EnvioViewSet`** - ✅ API funcional con permisos
   - ✅ Filtrado multi-tenant por empresa
   - ✅ Permisos por rol:
     - Dueño/Operadores: ven todos los envíos
     - Remitentes: solo sus envíos
     - Destinatarios: solo envíos dirigidos a ellos
   - ✅ Acciones: cambio de estado, notificaciones

## ❌ **PROBLEMAS IDENTIFICADOS**

### 1. **DESCONEXIÓN FRONTEND-BACKEND**

- Los formularios no usan la API real de envíos
- No hay integración con el sistema de autenticación
- No respetan los roles y permisos implementados

### 2. **DUPLICACIÓN DE CÓDIGO**

- Múltiples formularios similares
- Lógica de precios repetida
- No hay un componente unificado

### 3. **FALTA DE INTEGRACIÓN MULTITENANCY**

- Los formularios no usan el contexto de tenant
- No se aplican filtros por empresa
- No se valida el rol del usuario

## 🎯 **PLAN DE ACCIÓN**

### **PASO 1: Formulario Unificado**

- [ ] Crear `UnifiedEnvioForm.tsx` que reemplace todos los existentes
- [ ] Integrar con TenantContext y AuthContext
- [ ] Adaptar campos según rol del usuario

### **PASO 2: Integración con Backend**

- [ ] Conectar formulario con API `/api/envios/`
- [ ] Usar JWT tokens para autenticación
- [ ] Aplicar headers X-Tenant-Slug automáticamente

### **PASO 3: Permisos y Validaciones**

- [ ] **Remitentes**: Solo pueden crear envíos
- [ ] **Operadores**: Pueden crear y cambiar estados
- [ ] **Dueño**: Acceso completo a gestión

### **PASO 4: UI Según Rol**

- [ ] **Vista Remitente**: Formulario simple de envío
- [ ] **Vista Operador**: Formulario + gestión de estados
- [ ] **Vista Dueño**: Dashboard completo + reportes

## 🔧 **COMPONENTES A CREAR**

### 1. **`EnvioFormContainer.tsx`**

```tsx
// Componente principal que decide qué vista mostrar según rol
export const EnvioFormContainer = () => {
  const { user } = useAuth();
  const { currentTenant } = useTenant();

  if (user.rol === "remitente") return <RemitenteForm />;
  if (user.rol === "operador_miami" || user.rol === "operador_cuba")
    return <OperadorForm />;
  if (user.rol === "dueno") return <AdminForm />;
};
```

### 2. **`RemitenteForm.tsx`**

```tsx
// Formulario simple para crear envíos
// Campos: destinatario, peso, descripción, valor
// Submit directo a POST /api/envios/
```

### 3. **`OperadorForm.tsx`**

```tsx
// Formulario avanzado + gestión de estados
// Incluye: crear envíos + cambiar estados + ver historial
```

### 4. **`AdminForm.tsx`**

```tsx
// Dashboard completo con formulario + estadísticas
// Vista de todos los envíos + reportes
```

## 📊 **INTEGRACIÓN CON ADMIN ORGANIZADO**

### **Flujo Esperado:**

1. **Carlos (Dueño)** ve dashboard completo con todos los envíos
2. **Ana (Operador Miami)** ve formulario operativo + envíos pendientes
3. **Jose (Operador Cuba)** ve formulario + gestión de entrega
4. **Maria (Remitente)** ve formulario simple para crear envíos
5. **Carmen (Destinatario)** ve solo estado de sus envíos

## 🚀 **PRÓXIMO PASO**

**¿Comenzamos creando el `EnvioFormContainer` unificado que integre con el sistema multitenancy y organizado que acabamos de implementar?**

---

**Estado:** 📋 ANÁLISIS COMPLETADO - LISTO PARA IMPLEMENTACIÓN
**Prioridad:** 🔥 ALTA - Base para funcionalidad principal del sistema
