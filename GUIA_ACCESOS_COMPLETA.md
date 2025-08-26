# 🚀 GUÍA COMPLETA DE ACCESOS - PACKFY MULTITENANCY

## 🔗 **URLs PRINCIPALES**

### 🌐 **Frontend (React/Vite)**

```
http://localhost:5173
```

### 🔧 **Backend Django**

```
http://localhost:8000
```

### 👑 **Django Admin Panel (Solo Superadmin)**

```
http://localhost:8000/admin/
```

### 📚 **API Documentation**

```
http://localhost:8000/api/
http://localhost:8000/api/docs/    (Si está configurado Swagger)
```

---

## 👑 **SUPERADMINISTRADOR**

### 🔐 **Acceso Django Admin**

- **URL:** `http://localhost:8000/admin/`
- **Email:** `superadmin@packfy.com`
- **Password:** `super123`
- **Capacidades:** Control total del sistema, gestión de empresas, usuarios, configuraciones

### 🧪 **Login via API (Opcional)**

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"superadmin@packfy.com","password":"super123"}'
```

---

## 🏢 **ADMINISTRADORES DE EMPRESA**

### 📊 **1. CUBA EXPRESS CARGO**

#### 🔐 **Login Frontend**

- **URL:** `http://localhost:5173`
- **Email:** `admin@cubaexpress.com`
- **Password:** `admin123`
- **Tenant:** `cuba-express`

#### 🧪 **Login via API**

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Slug: cuba-express" \
  -d '{"email":"admin@cubaexpress.com","password":"admin123"}'
```

#### 🧪 **PowerShell Test**

```powershell
$headers = @{
    'Content-Type' = 'application/json'
    'X-Tenant-Slug' = 'cuba-express'
}
$body = @{
    'email' = 'admin@cubaexpress.com'
    'password' = 'admin123'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Headers $headers -Body $body
```

---

### 📊 **2. HABANA PREMIUM LOGISTICS**

#### 🔐 **Login Frontend**

- **URL:** `http://localhost:5173`
- **Email:** `admin@habanapremium.com`
- **Password:** `admin123`
- **Tenant:** `habana-premium`

#### 🧪 **Login via API**

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Slug: habana-premium" \
  -d '{"email":"admin@habanapremium.com","password":"admin123"}'
```

#### 🧪 **PowerShell Test**

```powershell
$headers = @{
    'Content-Type' = 'application/json'
    'X-Tenant-Slug' = 'habana-premium'
}
$body = @{
    'email' = 'admin@habanapremium.com'
    'password' = 'admin123'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Headers $headers -Body $body
```

---

### 📊 **3. MIAMI SHIPPING EXPRESS**

#### 🔐 **Login Frontend**

- **URL:** `http://localhost:5173`
- **Email:** `admin@miamishipping.com`
- **Password:** `admin123`
- **Tenant:** `miami-shipping`

#### 🧪 **Login via API**

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Slug: miami-shipping" \
  -d '{"email":"admin@miamishipping.com","password":"admin123"}'
```

#### 🧪 **PowerShell Test**

```powershell
$headers = @{
    'Content-Type' = 'application/json'
    'X-Tenant-Slug' = 'miami-shipping'
}
$body = @{
    'email' = 'admin@miamishipping.com'
    'password' = 'admin123'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Headers $headers -Body $body
```

---

### 📊 **4. PACKFY EXPRESS**

#### 🔐 **Login Frontend**

- **URL:** `http://localhost:5173`
- **Email:** `admin@packfy.com`
- **Password:** `admin123`
- **Tenant:** `packfy-express`

#### 🧪 **Login via API**

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Slug: packfy-express" \
  -d '{"email":"admin@packfy.com","password":"admin123"}'
```

#### 🧪 **PowerShell Test**

```powershell
$headers = @{
    'Content-Type' = 'application/json'
    'X-Tenant-Slug' = 'packfy-express'
}
$body = @{
    'email' = 'admin@packfy.com'
    'password' = 'admin123'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Headers $headers -Body $body
```

---

## 🧪 **ENDPOINTS DE PRUEBA**

### 📋 **Listar Empresas**

```bash
curl -X GET http://localhost:8000/api/empresas/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 👥 **Listar Usuarios de Empresa**

```bash
curl -X GET http://localhost:8000/api/usuarios/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "X-Tenant-Slug: cuba-express"
```

### 📦 **Listar Paquetes**

```bash
curl -X GET http://localhost:8000/api/paquetes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "X-Tenant-Slug: cuba-express"
```

---

## 🔄 **SECUENCIA DE PRUEBA COMPLETA**

### 1️⃣ **Verificar Contenedores**

```powershell
docker-compose ps
```

### 2️⃣ **Probar Django Admin**

1. Ir a: `http://localhost:8000/admin/`
2. Login: `superadmin@packfy.com` / `super123`
3. Verificar acceso completo

### 3️⃣ **Probar Frontend**

1. Ir a: `http://localhost:5173`
2. Seleccionar empresa
3. Login con admin correspondiente

### 4️⃣ **Probar API directamente**

```powershell
# Test Cuba Express
$headers = @{
    'Content-Type' = 'application/json'
    'X-Tenant-Slug' = 'cuba-express'
}
$body = @{
    'email' = 'admin@cubaexpress.com'
    'password' = 'admin123'
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Headers $headers -Body $body
Write-Host "JWT Token: $($response.refresh)"
```

---

## 🚨 **IMPORTANTE - MULTITENANCY**

### ⚠️ **Header Obligatorio para API**

**TODOS** los requests de API (excepto login) deben incluir:

```
X-Tenant-Slug: [slug-de-la-empresa]
```

### 🏢 **Slugs de Empresas**

- `cuba-express` → Cuba Express Cargo
- `habana-premium` → Habana Premium Logistics
- `miami-shipping` → Miami Shipping Express
- `packfy-express` → Packfy Express

### 🔐 **Separación de Accesos**

- **Superadmin:** Solo Django Admin (`/admin/`)
- **Admin Empresa:** Solo Frontend y API (NO Django Admin)
- **Usuarios Operativos:** Solo funciones específicas vía Frontend

---

## 🛠️ **COMANDOS DE DESARROLLO**

### 🔄 **Reiniciar Backend**

```powershell
docker-compose restart backend
```

### 🔄 **Reiniciar Frontend**

```powershell
docker-compose restart frontend
```

### 📊 **Ver Logs Backend**

```powershell
docker-compose logs -f backend
```

### 📊 **Ver Logs Frontend**

```powershell
docker-compose logs -f frontend
```

### 🔍 **Verificar Estructura**

```powershell
cd backend
python limpiar_estructura_usuarios.py
```

---

**✅ TODOS LOS ACCESOS VERIFICADOS Y FUNCIONALES**
**🗓️ Actualizado:** 26 de Agosto 2025
