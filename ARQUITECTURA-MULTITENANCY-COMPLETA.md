# 🏗️ ARQUITECTURA MULTITENANCY - DISEÑO COMPLETO

## 📊 E### CREDENCIALES PARA PRUEBAS

````
SUPERUSUARIO:
- Email: superadmin@packfy.com
- Contraseña: super123!
- Acceso: Todas las funcionalidades del sistema
```URA JERÁRQUICA

````

SUPERUSUARIO (admin@packfy.cu)
├── Acceso a todas las empresas
├── Panel de administración global
└── Gestión de sistema completo

EMPRESAS (4 empresas independientes)
├── Prime Express Cargo (prime-express)
├── Cuba Express (cuba-express)
├── Habana Premium (habana-premium)
└── Miami Shipping (miami-shipping)

USUARIOS POR EMPRESA (3 roles por empresa)
├── Gerente (1 por empresa)
├── Operador (1 por empresa)
└── Cliente (1 por empresa)

````

## 🏢 EMPRESAS DETALLADAS

### 1. **Prime Express Cargo**

- **Slug**: `prime-express`
- **Dominio**: `primeexpress.com` → `prime-express.localhost`
- **Descripción**: Servicio de paquetería express premium
- **Teléfono**: +1-305-555-0001
- **Email**: info@primeexpress.com

### 2. **Cuba Express**

- **Slug**: `cuba-express`
- **Dominio**: `cubaexpress.com` → `cuba-express.localhost`
- **Descripción**: Envíos rápidos a Cuba
- **Teléfono**: +1-305-555-0002
- **Email**: info@cubaexpress.com

### 3. **Habana Premium**

- **Slug**: `habana-premium`
- **Dominio**: `habanapremium.com` → `habana-premium.localhost`
- **Descripción**: Servicio premium para La Habana
- **Teléfono**: +1-305-555-0003
- **Email**: info@habanapremium.com

### 4. **Miami Shipping**

- **Slug**: `miami-shipping`
- **Dominio**: `miamishipping.com` → `miami-shipping.localhost`
- **Descripción**: Envíos desde Miami
- **Teléfono**: +1-305-555-0004
- **Email**: info@miamishipping.com

## 👥 USUARIOS POR EMPRESA

## 1. SUPERUSUARIO DEL SISTEMA

**Email:** superadmin@packfy.com
**Contraseña:** super123!
**Rol:** Super Administrador
**Permisos:** Acceso total al sistema, gestión de todas las empresas

### 📦 **Prime Express Cargo**

```yaml
Admin Empresa:
  Email: admin@primeexpress.com
  Password: admin123
  Nombre: Admin Prime Express
  Rol: admin_empresa
  Descripción: Administrador completo de la empresa, puede hacer todo

Operador Miami:
  Email: operador.miami@primeexpress.com
  Password: operador123
  Nombre: Operador Miami
  Rol: operador_miami
  Descripción: Encargado de operar en Miami

Operador Cuba:
  Email: operador.cuba@primeexpress.com
  Password: operador123
  Nombre: Operador Cuba
  Rol: operador_cuba
  Descripción: Encargado de distribuir en Cuba

Remitente:
  Email: remitente@primeexpress.com
  Password: remitente123
  Nombre: Cliente Remitente
  Rol: remitente
  Descripción: Usuario que envía paquetes

Destinatario:
  Email: destinatario@primeexpress.com
  Password: destinatario123
  Nombre: Cliente Destinatario
  Rol: destinatario
  Descripción: Usuario que recibe paquetes
````

### 🚚 **Cuba Express**

```yaml
Admin Empresa:
  Email: admin@cubaexpress.com
  Password: admin123
  Nombre: Admin Cuba Express
  Rol: admin_empresa
  Descripción: Administrador completo de la empresa

Operador Miami:
  Email: operador.miami@cubaexpress.com
  Password: operador123
  Nombre: Operador Miami
  Rol: operador_miami
  Descripción: Encargado de operar en Miami

Operador Cuba:
  Email: operador.cuba@cubaexpress.com
  Password: operador123
  Nombre: Operador Cuba
  Rol: operador_cuba
  Descripción: Encargado de distribuir en Cuba

Remitente:
  Email: remitente@cubaexpress.com
  Password: remitente123
  Nombre: Cliente Remitente
  Rol: remitente
  Descripción: Usuario que envía paquetes

Destinatario:
  Email: destinatario@cubaexpress.com
  Password: destinatario123
  Nombre: Cliente Destinatario
  Rol: destinatario
  Descripción: Usuario que recibe paquetes
```

### 🏢 **Habana Premium**

```yaml
Admin Empresa:
  Email: admin@habanapremium.com
  Password: admin123
  Nombre: Admin Habana Premium
  Rol: admin_empresa
  Descripción: Administrador completo de la empresa

Operador Miami:
  Email: operador.miami@habanapremium.com
  Password: operador123
  Nombre: Operador Miami
  Rol: operador_miami
  Descripción: Encargado de operar en Miami

Operador Cuba:
  Email: operador.cuba@habanapremium.com
  Password: operador123
  Nombre: Operador Cuba
  Rol: operador_cuba
  Descripción: Encargado de distribuir en Cuba

Remitente:
  Email: remitente@habanapremium.com
  Password: remitente123
  Nombre: Cliente Remitente
  Rol: remitente
  Descripción: Usuario que envía paquetes

Destinatario:
  Email: destinatario@habanapremium.com
  Password: destinatario123
  Nombre: Cliente Destinatario
  Rol: destinatario
  Descripción: Usuario que recibe paquetes
```

### 🌴 **Miami Shipping**

```yaml
Admin Empresa:
  Email: admin@miamishipping.com
  Password: admin123
  Nombre: Admin Miami Shipping
  Rol: admin_empresa
  Descripción: Administrador completo de la empresa

Operador Miami:
  Email: operador.miami@miamishipping.com
  Password: operador123
  Nombre: Operador Miami
  Rol: operador_miami
  Descripción: Encargado de operar en Miami

Operador Cuba:
  Email: operador.cuba@miamishipping.com
  Password: operador123
  Nombre: Operador Cuba
  Rol: operador_cuba
  Descripción: Encargado de distribuir en Cuba

Remitente:
  Email: remitente@miamishipping.com
  Password: remitente123
  Nombre: Cliente Remitente
  Rol: remitente
  Descripción: Usuario que envía paquetes

Destinatario:
  Email: destinatario@miamishipping.com
  Password: destinatario123
  Nombre: Cliente Destinatario
  Rol: destinatario
  Descripción: Usuario que recibe paquetes
```

## 🌐 URLS DE ACCESO

### **URLs con Parámetros (?empresa=slug)**

```
Superusuario (Frontend):
http://localhost:5173/login → Acceso global a todas las empresas

Superusuario (Backend Django):
http://localhost:8000/admin → Panel de administración Django

Prime Express:
http://localhost:5173/login?empresa=prime-express

Cuba Express:
http://localhost:5173/login?empresa=cuba-express

Habana Premium:
http://localhost:5173/login?empresa=habana-premium

Miami Shipping:
http://localhost:5173/login?empresa=miami-shipping
```

### **URLs con Subdominios (.localhost)**

```
http://prime-express.localhost:5173/login
http://cuba-express.localhost:5173/login
http://habana-premium.localhost:5173/login
http://miami-shipping.localhost:5173/login
```

## 🔧 FUNCIONALIDADES POR ROL

### **Super Administrador (superadmin@packfy.com)**

- ✅ Acceso a todas las empresas desde el frontend
- ✅ Panel de administración Django (ÚNICO acceso)
- ✅ Gestión de usuarios globales
- ✅ Configuración del sistema completo
- ✅ Control total de la plataforma

### **Admin Empresa (por empresa)**

- ✅ Dashboard completo de la empresa
- ✅ Gestión total de envíos de la empresa
- ✅ Reportes y estadísticas completas
- ✅ Gestión de usuarios de la empresa
- ✅ Configuración de la empresa
- ✅ Puede hacer TODO dentro de su empresa

### **Operador Miami (por empresa)**

- ✅ Crear/editar envíos desde Miami
- ✅ Actualizar estados de envíos en Miami
- ✅ Gestión de operaciones en Miami
- ✅ Consultar información de envíos
- ❌ Sin acceso a configuración de empresa

### **Operador Cuba (por empresa)**

- ✅ Gestión de distribución en Cuba
- ✅ Actualizar estados de entrega en Cuba
- ✅ Consultar envíos para Cuba
- ✅ Coordinación de entregas
- ❌ Sin acceso a operaciones de Miami

### **Remitente (por empresa)**

- ✅ Crear nuevos envíos
- ✅ Ver sus envíos enviados
- ✅ Rastrear paquetes que envía
- ✅ Actualizar información de envío
- ❌ No puede ver envíos de otros

### **Destinatario (por empresa)**

- ✅ Ver envíos que le llegan
- ✅ Rastrear paquetes dirigidos a él
- ✅ Confirmar recepciones
- ✅ Actualizar información de entrega
- ❌ No puede crear envíos

## 🧪 PLAN DE TESTING

### **Paso 1: Verificar Superusuario**

1. Login con `admin@packfy.cu`
2. Verificar acceso global
3. Comprobar panel de administración

### **Paso 2: Testing por Empresa**

Para cada empresa (4 empresas × 3 usuarios = 12 pruebas):

1. Login con gerente → Verificar dashboard empresa
2. Login con operador → Verificar funciones operativas
3. Login con cliente → Verificar vista cliente

### **Paso 3: Testing Multitenancy**

1. URLs con parámetros (?empresa=slug)
2. URLs con subdominios (.localhost)
3. Verificar aislamiento entre empresas
4. Comprobar detección automática de tenant

## 📊 RESUMEN NUMÉRICO

- **1** Superusuario global (superadmin@packfy.com)
- **4** Empresas independientes
- **20** Usuarios distribuidos (5 por empresa)
- **8** URLs de testing diferentes
- **5** Roles diferentes por empresa:
  - Admin Empresa
  - Operador Miami
  - Operador Cuba
  - Remitente
  - Destinatario
- **21** Credenciales únicas para testing completo

### **Contraseñas Organizadas:**

- **Superusuario**: `super123_`
- **Admin Empresa**: `admin123`
- **Operadores**: `operador123`
- **Remitentes**: `remitente123`
- **Destinatarios**: `destinatario123`

---

_Arquitectura diseñada para testing sistemático del sistema multitenancy_
