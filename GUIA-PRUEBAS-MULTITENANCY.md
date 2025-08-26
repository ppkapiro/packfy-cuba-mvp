# 🧪 GUÍA COMPLETA DE PRUEBAS MULTITENANCY

**Packfy Cuba - Sistema Multitenancy**
**Fecha**: 25 de agosto de 2025

---

## 🎯 OBJETIVO DE LAS PRUEBAS

Validar que el sistema multitenancy funciona correctamente con:

- ✅ Detección automática por subdominios
- ✅ Aislamiento de datos por empresa
- ✅ Usuario multi-empresa
- ✅ Cambio dinámico de contexto
- ✅ 170 envíos distribuidos correctamente

---

## 📋 CHECKLIST PRE-PRUEBAS

### **1. Verificar Estado del Sistema**

```bash
# En backend/
python verificacion_completa.py
```

### **2. Iniciar Servicios**

```bash
# Terminal 1: Backend Django
cd backend
python manage.py runserver 8000

# Terminal 2: Frontend React
cd frontend
npm start
# O si usas el multitenant:
cd frontend-multitenant
npm start
```

### **3. Verificar URLs Base**

- ✅ Backend: `http://localhost:8000/api/`
- ✅ Frontend: `http://localhost:5173/`
- ✅ Admin Django: `http://localhost:8000/admin/`

---

## 🧪 PRUEBAS FASE 1: DETECCIÓN AUTOMÁTICA

### **Test 1.1: Subdominios de Empresa**

1. **Abrir navegador en modo incógnito**
2. **Navegar a**: `http://cuba-express.localhost:5173`
3. **Verificar en DevTools Console**:
   ```
   🌐 TenantContext: Detectando dominio: cuba-express.localhost:5173
   🏢 TenantContext: Subdominio de empresa detectado: cuba-express
   ✅ TenantContext: Empresa válida encontrada: Cuba Express Cargo
   ```

### **Test 1.2: Parámetro URL**

1. **Navegar a**: `http://localhost:5173?empresa=miami-shipping`
2. **Verificar console**:
   ```
   🔗 TenantContext: Empresa detectada por URL: miami-shipping
   ✅ TenantContext: Empresa encontrada: Miami Shipping Express
   ```

### **Test 1.3: Dominio Administrativo**

1. **Navegar a**: `http://localhost:5173`
2. **Verificar**: Debe mostrar selector de empresa en header
3. **Console debe mostrar**:
   ```
   👨‍💼 TenantContext: ¿Es dominio admin? true
   ```

---

## 🔐 PRUEBAS FASE 2: AUTENTICACIÓN Y CONTEXTO

### **Test 2.1: Login Usuario Multi-Empresa**

1. **Ir a**: `http://localhost:5173/login`
2. **Credenciales**:
   ```
   Email: consultor@packfy.com
   Password: consultor123
   ```
3. **Verificar**: Login exitoso y redirección al dashboard

### **Test 2.2: Selector de Empresa**

1. **En el header**: Buscar selector de empresa
2. **Verificar opciones disponibles**:
   - ✅ Cuba Express Cargo
   - ✅ Habana Premium Logistics
   - ✅ Miami Shipping Express
   - ✅ Packfy Express
3. **Seleccionar empresa diferente**
4. **Verificar cambio de contexto en console**

### **Test 2.3: Headers API Automáticos**

1. **Abrir DevTools → Network**
2. **Hacer cualquier acción que llame API**
3. **Verificar request headers incluyen**:
   ```
   X-Tenant-Slug: [empresa-actual]
   Authorization: Bearer [jwt-token]
   ```

---

## 📦 PRUEBAS FASE 3: AISLAMIENTO DE DATOS

### **Test 3.1: Envíos por Empresa**

Con usuario `consultor@packfy.com` logueado:

1. **Cuba Express** (`cuba-express.localhost:5173`):

   - **Esperar ver**: ~45 envíos
   - **Verificar**: Solo envíos de Cuba Express
   - **Estados**: Variados (RECIBIDO, EN_TRANSITO, etc.)

2. **Miami Shipping** (`miami-shipping.localhost:5173`):

   - **Esperar ver**: ~44 envíos
   - **Verificar**: Solo envíos de Miami Shipping
   - **Datos diferentes**: A los de Cuba Express

3. **Habana Premium** (`habana-premium.localhost:5173`):

   - **Esperar ver**: ~26 envíos
   - **Verificar**: Solo envíos premium

4. **Packfy Express** (`packfy-express.localhost:5173`):
   - **Esperar ver**: ~55 envíos
   - **Verificar**: Solo envíos express

### **Test 3.2: Cambio Dinámico**

1. **Iniciar en**: `cuba-express.localhost:5173`
2. **Contar envíos mostrados**
3. **Usar selector para cambiar a**: Miami Shipping
4. **Verificar**:
   - URL cambia automáticamente
   - Datos mostrados cambian
   - Conteo de envíos es diferente

### **Test 3.3: Persistencia de Sesión**

1. **Estar en**: `habana-premium.localhost:5173`
2. **Cerrar y reabrir navegador**
3. **Volver a**: `habana-premium.localhost:5173`
4. **Verificar**: Sesión se mantiene en Habana Premium

---

## 🌐 PRUEBAS FASE 4: NAVEGACIÓN MULTITENANCY

### **Test 4.1: URLs Directas**

Probar acceso directo a cada empresa:

```bash
# Cada una debe abrir automáticamente en su contexto
http://cuba-express.localhost:5173
http://habana-premium.localhost:5173
http://miami-shipping.localhost:5173
http://packfy-express.localhost:5173
```

### **Test 4.2: Redirección entre Empresas**

1. **Estar en**: `cuba-express.localhost:5173`
2. **En selector, cambiar a**: Miami Shipping
3. **Verificar**: URL cambia a `miami-shipping.localhost:5173`
4. **Datos**: Cambian automáticamente

### **Test 4.3: Fallback a Admin**

1. **Navegar a URL inválida**: `empresa-inexistente.localhost:5173`
2. **Verificar**: Redirección a `localhost:5173`
3. **Mostrar**: Selector de empresa disponible

---

## 🛠️ PRUEBAS FASE 5: FUNCIONALIDADES ESPECÍFICAS

### **Test 5.1: Creación de Envío**

1. **En**: `miami-shipping.localhost:5173`
2. **Crear nuevo envío**
3. **Verificar**: Se asigna automáticamente a Miami Shipping
4. **Cambiar a otra empresa**
5. **Verificar**: Nuevo envío NO aparece en otra empresa

### **Test 5.2: API Endpoints**

Probar endpoints con diferentes headers:

```bash
# Cuba Express
curl -H "X-Tenant-Slug: cuba-express" \
     -H "Authorization: Bearer [token]" \
     http://localhost:8000/api/envios/

# Miami Shipping
curl -H "X-Tenant-Slug: miami-shipping" \
     -H "Authorization: Bearer [token]" \
     http://localhost:8000/api/envios/
```

**Verificar**: Cada endpoint devuelve solo datos de su empresa

### **Test 5.3: Middleware en Backend**

1. **Ver logs del servidor Django**
2. **Hacer requests a diferentes empresas**
3. **Verificar logs muestran**:
   ```
   🚀 MIDDLEWARE process_request para /api/envios/
   🌐 HOST: cuba-express.localhost:5173
   🏢 SUBDOMAIN SLUG: cuba-express
   ✅ EMPRESA POR SUBDOMAIN: Cuba Express Cargo
   ```

---

## 📊 RESULTADOS ESPERADOS

### **Datos por Empresa** (Aproximados)

```
📋 Cuba Express Cargo: ~45 envíos
📋 Habana Premium Logistics: ~26 envíos
📋 Miami Shipping Express: ~44 envíos
📋 Packfy Express: ~55 envíos
```

### **Console Logs Correctos**

```
✅ Detección automática funcionando
✅ Cambio de empresa sin errores
✅ API headers incluidos automáticamente
✅ Datos aislados por tenant
✅ URLs actualizándose correctamente
```

### **Navegación Fluida**

```
✅ Subdominios abriendo empresa correcta
✅ Selector cambiando contexto automáticamente
✅ URLs actualizándose en cambios
✅ Persistencia de sesión funcionando
✅ Fallback a admin en URLs inválidas
```

---

## 🚨 PROBLEMAS COMUNES Y SOLUCIONES

### **Error: "Empresa no encontrada"**

```bash
# Verificar que las empresas existen
python backend/verificacion_completa.py
```

### **Error: Headers no incluidos**

```bash
# Verificar configuración API client
console.log(apiClient.defaultHeaders)
```

### **Error: Subdominio no detectado**

```bash
# Verificar configuración hosts (Windows)
# Agregar a C:\Windows\System32\drivers\etc\hosts:
127.0.0.1 cuba-express.localhost
127.0.0.1 miami-shipping.localhost
127.0.0.1 habana-premium.localhost
127.0.0.1 packfy-express.localhost
```

### **Error: Datos mezclados**

```bash
# Verificar middleware en settings.py
MIDDLEWARE debe incluir: 'empresas.middleware.TenantMiddleware'
```

---

## ✅ CHECKLIST FINAL

- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 5173
- [ ] 4 empresas creadas y activas
- [ ] ~170 envíos distribuidos
- [ ] Usuario consultor funcional
- [ ] Subdominios detectando automáticamente
- [ ] Selector de empresa funcionando
- [ ] Datos aislados por empresa
- [ ] APIs con headers correctos
- [ ] URLs actualizándose automáticamente
- [ ] Console logs sin errores críticos

---

## 🎯 PRÓXIMO PASO

**¡Comenzar las pruebas!**

1. **Ejecutar verificación inicial**
2. **Iniciar servicios**
3. **Seguir guía paso a paso**
4. **Reportar cualquier problema encontrado**

**¿Listo para empezar?** 🚀
