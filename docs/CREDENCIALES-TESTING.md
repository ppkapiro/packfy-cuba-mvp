# 🔑 CREDENCIALES PACKFY CUBA - LISTADO COMPLETO

## 📋 **USUARIOS DE LA APLICACIÓN**

### 🛡️ **ADMINISTRADOR PRINCIPAL**
- **Email:** `admin@packfy.com`
- **Username:** `admin`
- **Password:** `admin123` *(temporal)*
- **Permisos:** Superusuario + Staff
- **Descripción:** Acceso completo al sistema

---

### 👤 **USUARIO ESTÁNDAR**
- **Email:** `usuario@packfy.com`
- **Username:** `usuario`
- **Password:** `usuario123`
- **Permisos:** Usuario normal
- **Descripción:** Para pruebas de funcionalidad básica

---

### 👨‍💼 **OPERADOR DE ENVÍOS**
- **Email:** `operador@packfy.com`
- **Username:** `operador`
- **Password:** `operador123`
- **Permisos:** Staff (sin superusuario)
- **Descripción:** Gestión de envíos y operaciones

---

### 🇨🇺 **CLIENTE CUBA**
- **Email:** `cliente@packfy.com`
- **Username:** `cliente`
- **Password:** `cliente123`
- **Permisos:** Usuario normal
- **Descripción:** Cliente típico de Cuba

---

## 🌐 **URLs DE ACCESO**

### **Frontend (PWA)**
- **Desarrollo:** http://192.168.12.178:5173
- **Local:** http://localhost:5173

### **Backend (API)**
- **Desarrollo:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin/
- **API Docs:** http://localhost:8000/api/swagger/

---

## 🔐 **NOTAS DE SEGURIDAD**

⚠️ **IMPORTANTE:** Estas son credenciales de **DESARROLLO/TESTING**

### **Para Producción:**
1. Cambiar todas las contraseñas
2. Usar contraseñas seguras (mínimo 12 caracteres)
3. Activar autenticación de dos factores
4. Configurar certificados SSL/HTTPS

### **Política de Contraseñas:**
- Mínimo 8 caracteres
- Incluir mayúsculas, minúsculas y números
- Evitar palabras comunes
- Cambiar cada 90 días

---

## 🧪 **TESTING**

### **Login Web (Frontend):**
1. Ve a: http://192.168.12.178:5173
2. Haz clic en "Iniciar Sesión"
3. Usa cualquiera de las credenciales de arriba

### **Admin Django:**
1. Ve a: http://localhost:8000/admin/
2. Usa credenciales de admin: `admin@packfy.com` / `admin123`

### **API Testing:**
1. Ve a: http://localhost:8000/api/swagger/
2. Prueba endpoints con credenciales

---

## 📱 **PWA (Progressive Web App)**

### **Instalación Manual:**
1. Chrome móvil → http://192.168.12.178:5173
2. Menú Chrome (⋮) → "Agregar a pantalla de inicio"
3. Login con cualquier usuario de arriba

### **Funcionalidades PWA:**
- ✅ Trabajo offline
- ✅ Instalación en móvil
- ✅ Notificaciones push (futuro)
- ✅ Sincronización en background

---

## 🐛 **TROUBLESHOOTING**

### **Si no funciona el login:**
1. Verificar que el backend esté corriendo (puerto 8000)
2. Verificar que el frontend esté corriendo (puerto 5173)
3. Comprobar credenciales en este documento
4. Revisar consola del navegador para errores

### **Comandos útiles:**
```bash
# Resetear password de usuario
cd backend
python manage.py changepassword admin@packfy.com

# Ver todos los usuarios
python manage.py shell -c "from usuarios.models import Usuario; [print(f'{u.email} - {u.username}') for u in Usuario.objects.all()]"

# Crear nuevo superusuario
python manage.py createsuperuser
```

---

**🇨🇺 PACKFY CUBA v2.0 - Sistema de Paquetería**  
*Documentación actualizada: 11 de agosto de 2025*
