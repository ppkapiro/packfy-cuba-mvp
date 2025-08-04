# 📦 Paquetería Cuba MVP

Sistema moderno de gestión de envíos para Cuba basado en Django REST Framework y React con TypeScript.

## 🚀 Estado del Proyecto

✅ **Sistema Completamente Funcional**
- ✅ Backend Django REST API operativo
- ✅ Frontend React + TypeScript + Vite funcionando
- ✅ Base de datos PostgreSQL configurada
- ✅ Sistema de autenticación implementado
- ✅ Docker Compose completamente configurado
- ✅ Problema de página en blanco resuelto

## 🎯 Características Principales

- 🎯 **Gestión completa de envíos** (crear, editar, cancelar, seguimiento)
- 👥 **Sistema de autenticación y autorización** robusto
- 🏢 **Gestión multi-empresa** con middleware de tenant
- 📧 **Sistema de notificaciones automáticas** por email
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
- **PostgreSQL 16** - Base de datos relacional robusta
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
| Servicio | Puerto | URL |
|----------|--------|-----|
| Frontend (React) | 5173 | http://localhost:5173 |
| Backend API (Django) | 8000 | http://localhost:8000 |
| PostgreSQL | 5433 | localhost:5433 |
| Admin Django | 8000 | http://localhost:8000/admin |

### Variables de Entorno

**Frontend (.env)**:
```env
VITE_API_BASE_URL=http://localhost:8000
```

El archivo se crea automáticamente con `dev.ps1`.

## 👤 Usuarios de Prueba

El sistema incluye usuarios de demostración ya creados:

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| **Administrador** | admin@packfy.com | admin123 | Super Admin |
| **Usuario Demo** | demo@packfy.com | demo123 | Usuario Regular |

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
│   ├── empresas/        # Gestión de empresas (multi-tenant)
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
```bash
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

## 🏢 Sistema Multi-tenant

El sistema soporta múltiples empresas con:

✅ **Aislamiento de Datos**: Cada empresa tiene su propio esquema  
✅ **Personalización**: Configuraciones independientes por empresa  
✅ **Seguridad**: Datos completamente separados entre empresas  

**Tenants por defecto**:
- **public**: Tenant principal (Packfy Cuba)
- **ejemplo**: Empresa de ejemplo (Envíos Express)

## 🔍 Solución de Problemas

### Problema: Página en Blanco
Si experimentas una página en blanco después de crear un envío:

1. **Limpiar caché del navegador**:
   ```javascript
   // En la consola del navegador (F12)
   localStorage.clear(); 
   sessionStorage.clear(); 
   location.reload();
   ```

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