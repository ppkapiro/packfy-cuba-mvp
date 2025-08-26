# � Packfy Cuba MVP - PWA

Sistema moderno de gestión de envíos para Cuba con **Progressive Web App (PWA)** funcional en móvil.

## 🎉 **PROYECTO COMPLETADO - V2.0.0**

✅ **PWA 100% Funcional en Móvil**
✅ **Backend API Completo**
✅ **Frontend React Responsive**
✅ **Autenticación JWT**
✅ **Base de Datos Configurada**
✅ **Docker Compose Listo**

---

## 🚀 **Inicio Rápido**

### **1. Iniciar el proyecto**

```powershell
docker-compose up -d
```

### **2. Acceder a la aplicación**

- **Web:** http://localhost:5173
- **Móvil:** http://[TU-IP]:5173

### **3. Credenciales de prueba**

```
Email: test@test.com
Password: 123456
```

---

## 📱 **Características PWA**

- 🎯 **Gestión completa de envíos** (crear, editar, cancelar, seguimiento)
- 👥 **Sistema de autenticación JWT** robusto
- 🏢 **Gestión de empresas** simplificada
- 📧 **Sistema de notificaciones** automáticas
- 📱 **PWA instalable** en móviles
- 🔄 **Service Worker** optimizado
- 🎨 **UI responsive** para todos los dispositivos

---

## 🛠 **Tecnologías**

### Frontend

- **React 18** - Framework de UI moderno
- **TypeScript** - Tipado estático para JavaScript
- **Vite** - Build tool ultrarrápido
- **PWA** - Progressive Web App con Service Worker
- **Responsive Design** - Adaptable a todos los dispositivos

### Backend

- **Django 5.2** - Framework web Python de alto nivel
- **Django REST Framework** - API REST robusta
- **JWT Authentication** - Autenticación segura con tokens
- **SQLite** - Base de datos optimizada para MVP (migración a PostgreSQL preparada)
- **Multi-tenancy** - Sistema multiempresa implementado
- **CORS** - Configurado para desarrollo y producción

### DevOps & Herramientas

- **Docker** - Containerización completa
- **Docker Compose** - Orquestación de servicios
- **Git** - Control de versiones
- **PowerShell Scripts** - Automatización de desarrollo

---

## 📋 **Instalación y Configuración**

### Prerequisitos

- Docker Desktop instalado y en ejecución
- Git para clonar el repositorio
- PowerShell (Windows) o Terminal (Linux/Mac)

### Pasos de instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/ppkapiro/packfy-cuba-mvp.git
   cd packfy-cuba-mvp
   ```

2. **Iniciar con Docker** (recomendado)

   ```powershell
   docker-compose up -d
   ```

3. **Verificar que todo funcione**

   ```bash
   docker-compose ps
   ```

4. **Acceder a la aplicación**
   - Frontend: <http://localhost:5173>
   - Backend API: <http://localhost:8000>
   - Base de datos: SQLite (archivo local `backend/db.sqlite3`)

---

## 🔑 **Usuarios de Prueba**

```text
Email: test@test.com
Password: 123456

Admin: admin@packfy.com
Password: admin123
```

---

## 📱 **Acceso Móvil**

### Para probar en móvil (misma red WiFi):

1. **Obtener IP de tu computadora**

   ```powershell
   ipconfig
   ```

2. **Acceder desde móvil**

   - Reemplaza `[TU-IP]` con tu IP local
   - Ejemplo: `http://192.168.1.100:5173`

3. **Instalar PWA** (opcional)
   - El navegador sugerirá instalar la app
   - Funciona como app nativa una vez instalada

---

## 🚀 **Comandos Útiles**

### Desarrollo

```powershell
# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Parar todos los servicios
docker-compose down

# Rebuild completo (si hay cambios)
.\rebuild-total.ps1

# Limpiar y reiniciar todo
.\deep-clean.ps1
```

### Base de Datos

**📊 Configuración Actual: SQLite (Estándar MVP)**

El sistema utiliza **SQLite** como base de datos estándar para la fase MVP, optimizado para desarrollo ágil y simplicidad.

```powershell
# Verificar estado de la base de datos
cd backend
python -c "import sqlite3; print(f'BD activa: {sqlite3.connect(\"db.sqlite3\").execute(\"SELECT COUNT(*) FROM usuarios_usuario\").fetchone()[0]} usuarios')"

# Crear backup de la base de datos
Copy-Item db.sqlite3 "backups/backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sqlite3"

# Acceder a la consola de Django
python manage.py shell

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

#### 🎯 **¿Por qué SQLite?**

- ✅ **Simplicidad**: Cero configuración, funciona inmediatamente
- ✅ **Rendimiento**: Para MVPs es más rápido que PostgreSQL
- ✅ **Portabilidad**: Un solo archivo, fácil backup/restore
- ✅ **Desarrollo**: Sin dependencias externas ni configuración compleja

#### 📋 **Datos Actuales**

- **👥 Usuarios**: 10 usuarios con roles diversos
- **🏢 Empresas**: 1 empresa (Packfy Express)
- **👔 Perfiles**: 10 perfiles usuario-empresa configurados
- **📦 Envíos**: Listo para crear datos de prueba

#### 🚀 **Migración Futura a PostgreSQL**

Cuando el sistema escale (>1000 usuarios), la migración está preparada:

```powershell
# Ver configuración PostgreSQL preparada
Get-Content backend/config/settings.py | Select-String "postgresql" -A 5 -B 2
```

Para más detalles: [📚 Guía completa de BD](docs/database-configuration.md)

---

## 📂 **Estructura del Proyecto**

```text
packfy-cuba-mvp/
├── 📁 backend/              # Django API
│   ├── config/             # Configuración principal
│   ├── usuarios/           # App de usuarios
│   ├── empresas/           # App de empresas
│   ├── envios/             # App de envíos
│   └── scripts/            # Scripts de inicialización
├── 📁 frontend/            # React PWA
│   ├── src/               # Código fuente
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas principales
│   │   ├── services/      # Servicios API
│   │   └── stores/        # Estado global
│   └── public/            # Assets estáticos y PWA
├── 📁 docs/               # Documentación
├── 📁 scripts/            # Scripts de desarrollo
├── compose.yml           # Docker Compose
└── README.md            # Este archivo
```

---

## � **Características Destacadas**

### PWA (Progressive Web App)

- ✅ **Instalable** en dispositivos móviles
- ✅ **Funciona offline** (básico)
- ✅ **Service Worker** optimizado
- ✅ **Responsive** en todos los tamaños de pantalla
- ✅ **Icons** adaptativos para diferentes dispositivos

### Backend Robusto

- ✅ **API REST** completa con documentación automática
- ✅ **Autenticación JWT** con refresh tokens
- ✅ **Multi-tenancy** para diferentes empresas
- ✅ **Validación** de datos exhaustiva
- ✅ **Health checks** para monitoreo

### 🏢 **Sistema Multitenancy**

El sistema implementa **multitenancy completo** para gestión de múltiples empresas:

- **🔐 Aislamiento por empresa**: Cada empresa ve solo sus datos
- **👥 Roles específicos**: Dueño, Operador Miami, Operador Cuba, Remitente, Destinatario
- **🏷️ Identificación única**: Sistema de slugs para empresas (`packfy-express`)
- **🔄 Cambio de contexto**: Frontend permite cambiar entre empresas
- **🛡️ Seguridad**: Middleware asegura aislamiento de datos

#### **Estado Actual del Sistema**:

- **1 empresa activa**: Packfy Express
- **10 usuarios configurados** con roles diversos
- **10 perfiles empresa-usuario** funcionando

### Desarrollo Optimizado

- ✅ **Hot reload** en desarrollo
- ✅ **TypeScript** para mejor mantenibilidad
- ✅ **Docker** para consistency entre entornos
- ✅ **Scripts automatizados** para tareas comunes
- ✅ **Logs estructurados** para debugging

---

## 🔧 **Configuración Avanzada**

### Variables de Entorno

#### Frontend (`.env`)

```env
VITE_API_BASE_URL=http://localhost:8000
```

#### Backend (settings.py)

```python
DEBUG = True  # Solo para desarrollo
ALLOWED_HOSTS = ['*']  # Configurar para producción
```

### Personalización

- **Logo y branding**: `frontend/public/`
- **Colores y tema**: `frontend/src/styles/`
- **Configuración API**: `frontend/src/services/api.ts`

---

## 🧪 **Testing**

### Tests Automáticos

```powershell
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests (cuando se implementen)
docker-compose exec frontend npm test
```

### Testing Manual

- **Web**: <http://localhost:5173>
- **API Docs**: <http://localhost:8000/api/swagger/>
- **Admin**: <http://localhost:8000/admin/>

---

## � **Resolución de Problemas**

### Problemas Comunes

#### "No se puede conectar al servidor"

```powershell
# Verificar que los contenedores estén corriendo
docker-compose ps

# Revisar logs para errores
docker-compose logs backend
```

#### "Página en blanco en el frontend"

```powershell
# Reconstruir el frontend
docker-compose restart frontend

# Verificar logs
docker-compose logs frontend
```

#### "Error de base de datos"

```powershell
# Recrear la base de datos
docker-compose down
docker volume rm packfy-cuba-mvp_postgres_data
docker-compose up -d
```

### Scripts de Diagnóstico

```powershell
# Test completo del sistema
.\verificar-pwa.ps1

# Test de conectividad móvil
.\test-conectividad-movil.ps1
```

---

## 📈 **Roadmap y Próximas Funcionalidades**

### 🎯 Corto Plazo

- [ ] Notificaciones push en PWA
- [ ] Modo offline avanzado
- [ ] Tests unitarios completos
- [ ] Optimización de performance

### 🚀 Mediano Plazo

- [ ] Geolocalización y mapas
- [ ] Códigos QR para tracking
- [ ] Panel de analytics
- [ ] API pública para integraciones

### 🌟 Largo Plazo

- [ ] App móvil nativa
- [ ] Inteligencia artificial para predicciones
- [ ] Marketplace de paqueterías
- [ ] Blockchain para tracking inmutable

---

## 🤝 **Contribuir**

### Para desarrolladores

1. **Fork** el repositorio
2. **Crear** una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** tus cambios: `git commit -m 'Añadir nueva funcionalidad'`
4. **Push** a la rama: `git push origin feature/nueva-funcionalidad`
5. **Abrir** un Pull Request

### Reportar Bugs

- Usar GitHub Issues
- Incluir pasos para reproducir
- Adjuntar logs relevantes
- Especificar entorno (OS, browser, etc.)

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 **Equipo y Soporte**

**Desarrollado con ❤️ para la comunidad cubana**

### Contacto

- **GitHub**: [@ppkapiro](https://github.com/ppkapiro)
- **Issues**: [GitHub Issues](https://github.com/ppkapiro/packfy-cuba-mvp/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/ppkapiro/packfy-cuba-mvp/wiki)

### Reconocimientos

- Comunidad Django y React
- Contributors de código abierto
- Beta testers y feedback temprano

---

## 🎉 **¡Gracias por usar Packfy!**

Si este proyecto te ha sido útil, considera:

- ⭐ **Dar una estrella** al repositorio
- 🐛 **Reportar bugs** que encuentres
- 💡 **Sugerir mejoras** vía Issues
- 🤝 **Contribuir** con código o documentación

**¡Juntos podemos mejorar la logística en Cuba! 🇨🇺**

- 📊 **Dashboard interactivo** con métricas y estadísticas en tiempo real
- 🔄 **API REST completa** con documentación automática
- 🛡️ **Middleware de seguridad** y validación de datos
- 🎨 **UI moderna** con React, TypeScript y Tailwind CSS
- 🔍 **Rastreo público** para clientes sin iniciar sesión
- 📖 **Paginación avanzada** para grandes conjuntos de datos

## 🛠️ Tecnologías Utilizadas

### Frontend

- **React 18** - Framework de UI moderno
- **TypeScript** - Tipado estático para mayor robustez
- **Vite** - Build tool y dev server ultrarrápido
- **Tailwind CSS** - Framework CSS utility-first
- **Zustand** - Gestión de estado ligera
- **React Router** - Enrutamiento declarativo
- **React Hook Form** - Manejo eficiente de formularios
- **Axios** - Cliente HTTP con interceptores

### Backend

- **Django 5.2** - Framework web Python de alto nivel
- **Django REST Framework** - Toolkit para APIs REST
- **SQLite** - Base de datos optimizada para MVP (escalable a PostgreSQL)
- **JWT** - Autenticación basada en tokens
- **Django CORS Headers** - Manejo de CORS
- **Rate Limiting** - Protección contra abuso de API

### DevOps & Herramientas

- **Docker** - Containerización de aplicaciones
- **Docker Compose** - Orquestación de servicios
- **PowerShell** - Scripts de automatización
- **Git** - Control de versiones

## ⚡ Inicio Rápido

### Prerequisitos

- Docker Desktop instalado y en ejecución
- PowerShell (Windows) o Bash (Linux/Mac)
- Git

### Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone <repository-url>
   cd paqueteria-cuba-mvp
   ```

2. **Ejecutar el script de desarrollo** (recomendado):

   ```powershell
   .\dev.ps1
   ```

   O manualmente:

   ```bash
   docker-compose up --build
   ```

3. **Acceder a la aplicación**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Admin Django: http://localhost:8000/admin

## 🔧 Configuración Técnica

### Puertos del Sistema

| Servicio             | Puerto | URL                         |
| -------------------- | ------ | --------------------------- |
| Frontend (React)     | 5173   | http://localhost:5173       |
| Backend API (Django) | 8000   | http://localhost:8000       |
| Base de Datos        | -      | SQLite (archivo local)      |
| Admin Django         | 8000   | http://localhost:8000/admin |

### Variables de Entorno

**Frontend (.env)**:

```env
VITE_API_BASE_URL=http://localhost:8000
```

El archivo se crea automáticamente con `dev.ps1`.

## 👤 Usuarios de Prueba

El sistema incluye usuarios de demostración ya creados:

| Usuario           | Email            | Contraseña | Rol             |
| ----------------- | ---------------- | ---------- | --------------- |
| **Administrador** | admin@packfy.com | admin123   | Super Admin     |
| **Usuario Demo**  | demo@packfy.com  | demo123    | Usuario Regular |

## 🏗️ Estructura del Proyecto

```
📦 paqueteria-cuba-mvp/
├── 🎨 frontend/          # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/   # Componentes reutilizables
│   │   ├── contexts/     # Contextos de React (Auth, etc.)
│   │   ├── pages/        # Páginas principales de la app
│   │   ├── services/     # Servicios de API y HTTP client
│   │   ├── stores/       # Gestión de estado (Zustand)
│   │   └── types/        # Definiciones de TypeScript
│   └── Dockerfile
│
├── 🔧 backend/           # Django REST Framework
│   ├── config/          # Configuración principal del proyecto
│   ├── empresas/        # Gestión de empresas
│   ├── envios/          # Gestión de envíos y seguimiento
│   ├── usuarios/        # Sistema de usuarios y autenticación
│   ├── scripts/         # Scripts de automatización
│   └── Dockerfile
│
├── 📚 docs/             # Documentación técnica consolidada
├── 🐳 compose.yml       # Configuración Docker Compose
└── 🔧 dev.ps1          # Script principal de desarrollo
```

## 🛠️ Scripts de Desarrollo

### Script Principal

```powershell
.\dev.ps1
```

**Funciones**:

- Verifica y inicia Docker Desktop si es necesario
- Construye y levanta todos los servicios
- Configura automáticamente el entorno
- Crea usuarios de demostración
- Ejecuta migraciones de base de datos

### Comandos Docker Útiles

````bash
# Ver estado de todos los contenedores
docker-compose ps

# Ver logs de un servicio específico
docker-compose logs frontend
docker-compose logs backend
docker-compose logs db

# Reiniciar un servicio específico
docker-compose restart frontend

# Parar todos los servicios
docker-compose down

# Limpieza completa (incluye volúmenes y datos)
docker-compose down -v

## 📋 API Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/envios/` | Listar envíos |
| POST | `/api/envios/` | Crear nuevo envío |
| GET | `/api/envios/{id}/` | Detalles de envío |
| PUT | `/api/envios/{id}/` | Actualizar envío |
| POST | `/api/auth/login/` | Iniciar sesión |
| POST | `/api/auth/logout/` | Cerrar sesión |
| GET | `/api/empresas/` | Listar empresas |
| GET | `/api/schema/swagger-ui/` | Documentación API |

## 🚀 Uso del Sistema

### Acceso a la Aplicación
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Documentación API**: http://localhost:8000/api/schema/swagger-ui/
- **Panel de Administración**: http://localhost:8000/admin/
- **Seguimiento Público**: http://localhost:5173/rastrear

### Flujo de Trabajo Básico
1. **Iniciar sesión** con las credenciales de prueba
2. **Crear un nuevo envío** desde el dashboard
3. **Gestionar estados** del envío en tiempo real
4. **Consultar estadísticas** en el panel principal
5. **Permitir rastreo público** a los clientes

## 🔍 Solución de Problemas### Problema: Página en Blanco
Si experimentas una página en blanco después de crear un envío:

1. **Limpiar caché del navegador**:
   ```javascript
   // En la consola del navegador (F12)
   localStorage.clear();
   sessionStorage.clear();
   location.reload();
````

2. **Reiniciar el frontend**:

   ```bash
   docker-compose restart frontend
   ```

3. **Ver documentación técnica completa**:
   ```
   docs/DOCUMENTACION-TECNICA-COMPLETA.md
   ```

### Verificación del Sistema

```bash
# Verificar que todos los servicios estén saludables
docker-compose ps

# Testear la API
curl http://localhost:8000/api/health/ || echo "API no responde"

# Ver logs en tiempo real
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Problemas Comunes

- **Docker no inicia**: Verificar que Docker Desktop esté ejecutándose
- **Puerto ocupado**: Cambiar puertos en `compose.yml` si es necesario
- **Errores de permisos**: Ejecutar PowerShell como administrador

## 💻 Desarrollo Local

### Backend (sin Docker)

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend (sin Docker)

```bash
cd frontend
npm install
npm run dev
```

## 📞 Soporte y Documentación

- 📖 **Documentación técnica**: `docs/DOCUMENTACION-TECNICA-COMPLETA.md`
- 🐛 **Reporte de errores**: Crear issue en el repositorio
- 💡 **Nuevas características**: Crear issue con etiqueta 'enhancement'
- 🔧 **Scripts de ayuda**: Usar `dev.ps1` para automatización

## 🔮 Próximas Mejoras

- [ ] Sistema de notificaciones en tiempo real
- [ ] Integración con servicios de mensajería (WhatsApp, SMS)
- [ ] Reportes avanzados y analytics
- [ ] API móvil y aplicación mobile
- [ ] Integración con sistemas de pago
- [ ] Módulo de tarifas dinámicas

---

**Última actualización**: Diciembre 2024
**Versión**: 1.0
**Estado**: ✅ Producción Lista
**Soporte**: Sistema completamente funcional y documentado

```bash
# En Windows
run_tests.bat

# En Linux/Mac
./run_tests.sh
```

O manualmente:

```bash
cd backend
python manage.py test
```

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## Contacto

Para más información, contactar a: info@packfy.com
