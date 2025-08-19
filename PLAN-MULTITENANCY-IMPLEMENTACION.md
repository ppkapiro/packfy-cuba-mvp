# 🏢 PLAN DE IMPLEMENTACIÓN MULTI-TENANCY

**Packfy Cuba MVP - Sistema Multi-Empresa**

## 🎯 OBJETIVO

Transformar el sistema actual en una plataforma multi-tenant donde múltiples empresas de paquetería pueden operar de forma independiente y competitiva.

## 🏗️ ARQUITECTURA DEFINIDA

### 👥 ROLES DEL SISTEMA

```
🏢 EMPRESA (Tenant aislado)
├── 👑 DUEÑO - Administrador total de la empresa
├── 🚛 OPERADOR MIAMI - Recogida + Logística Miami→Aeropuerto
├── 🇨🇺 OPERADOR CUBA - Recepción + Entrega Cuba
├── 📤 REMITENTE - Cliente que envía paquetes
└── 📥 DESTINATARIO - Persona que recibe paquetes
```

### 🔐 PRINCIPIOS DE AISLAMIENTO

- ✅ **Datos completamente separados** por empresa
- ✅ **Empleados exclusivos** de cada empresa
- ✅ **Clientes pueden migrar** entre empresas
- ✅ **Competencia real** entre empresas
- ✅ **Base de clientes protegida** por empresa

## 📅 FASE 1: BACKEND ARCHITECTURE (1-2 semanas)

### 🗄️ PASO 1: MODELOS DE DATOS

**Archivo**: `backend/empresas/models.py`

```python
# Modelo principal de Empresa (Tenant)
class Empresa:
    - nombre
    - slug (identificador único)
    - activa
    - fecha_creacion
    - configuracion (JSON para futuras customizaciones)

# Roles de usuario expandidos
class PerfilUsuario:
    - usuario (OneToOne User)
    - empresa (ForeignKey Empresa)
    - rol (CHOICES: dueño, operador_miami, operador_cuba, remitente, destinatario)
    - activo
    - fecha_vinculacion
```

### 🔧 PASO 2: MIDDLEWARE DE TENANT

**Archivo**: `backend/empresas/middleware.py`

- Detectar empresa por subdominio o header
- Inyectar contexto de empresa en cada request
- Validar permisos de acceso

### 🛡️ PASO 3: SISTEMA DE PERMISOS

**Archivo**: `backend/empresas/permissions.py`

- Permisos basados en empresa y rol
- Decoradores para vistas
- Filtros automáticos por empresa

### 📦 PASO 4: ACTUALIZAR MODELOS EXISTENTES

**Archivos**: `backend/envios/models.py`, `backend/usuarios/models.py`

- Agregar ForeignKey a Empresa en todos los modelos
- Mantener compatibilidad con datos existentes
- Migraciones seguras

### 🔄 PASO 5: MIGRACIONES DE DATOS

**Archivo**: `backend/empresas/management/commands/migrar_a_multitenancy.py`

- Crear empresa por defecto
- Migrar usuarios existentes
- Asignar envíos a empresa por defecto
- Validar integridad de datos

## 📊 FASE 2: API MULTI-TENANT (1 semana)

### 🌐 PASO 6: ACTUALIZAR SERIALIZERS

**Archivos**: `backend/*/serializers.py`

- Filtrar datos por empresa automáticamente
- Validar permisos en serializers
- Contexto de empresa en todas las respuestas

### 🔗 PASO 7: ACTUALIZAR VIEWSETS

**Archivos**: `backend/*/views.py`

- Queryset filtrado por empresa
- Permisos basados en rol
- Acciones específicas por rol

### 📋 PASO 8: ENDPOINTS ESPECÍFICOS

- `/api/empresas/` - Gestión de empresas (solo súper admin)
- `/api/empresa/actual/` - Datos de empresa actual
- `/api/usuarios/roles/` - Gestión de roles de usuarios
- `/api/dashboard/empresa/` - Estadísticas por empresa

## 🧪 FASE 3: TESTING Y VALIDACIÓN (3-5 días)

### ✅ PASO 9: TESTS AUTOMATIZADOS

- Test de aislamiento de datos
- Test de permisos por rol
- Test de migraciones
- Test de APIs multi-tenant

### 🎭 PASO 10: DATOS DE PRUEBA

- Crear 3 empresas de ejemplo
- Usuarios con diferentes roles
- Envíos distribuidos entre empresas
- Validar separación total

## 🚀 HITOS DE ENTREGA

### 🏁 MILESTONE 1: Backend Multi-Tenant (Semana 1)

- ✅ Modelos de empresa implementados
- ✅ Middleware funcionando
- ✅ Migraciones completadas
- ✅ APIs básicas operativas

### 🏁 MILESTONE 2: Sistema Completo (Semana 2)

- ✅ Todos los endpoints adaptados
- ✅ Permisos implementados
- ✅ Tests pasando
- ✅ Datos de prueba funcionando

## 📝 NOTAS IMPORTANTES

### 🔄 COMPATIBILIDAD

- Mantener funcionamiento actual durante desarrollo
- Migraciones reversibles
- Datos existentes preservados

### 🎯 FUTURAS MEJORAS (Fase 2+)

- Múltiples dueños por empresa
- Dueños-operadores híbridos
- Dashboard personalizable por empresa
- Configuraciones específicas por empresa

---

**Creado**: 19 de Agosto, 2025
**Rama**: `feature/multitenancy`
**Estado**: 🚀 Iniciando implementación
