# 🇨🇺 Packfy Cuba MVP - Sistema de Gestión de Envíos

**Sistema moderno de gestión de envíos para Cuba con interfaz glassmorphism y identidad visual cubana.**

## 🎉 **VERSIÓN ACTUAL - V4.0**

✅ **Interfaz Moderna con Glassmorphism**
✅ **Sistema CSS Unificado**
✅ **Identidad Visual Cubana Completa**
✅ **Formularios Premium y Simple**
✅ **Dashboard Optimizado**
✅ **Sistema Responsive Completo**
✅ **Backend API Django REST**
✅ **Base de Datos PostgreSQL**
✅ **Docker Compose Productivo**

---

## 🚀 **Inicio Rápido**

### **1. Clonar el proyecto**

```bash
git clone https://github.com/ppkapiro/packfy-cuba-mvp.git
cd packfy-cuba-mvp
```

### **2. Iniciar el proyecto**

```bash
docker-compose up -d
```

### **3. Acceder a la aplicación**

- **🌐 Frontend:** https://localhost:5173
- **🔧 Backend API:** http://localhost:8000
- **📊 Admin Django:** http://localhost:8000/admin

### **4. Credenciales de prueba**

```
Email: test@test.com
Password: 123456
```

---

## 🎨 **Características de Diseño V4.0**

### **🇨🇺 Identidad Visual Cubana**

- **Colores:** Azul Océano (#0066cc), Rojo Pasión (#e53e3e), Dorado Sol (#ffd700)
- **Efectos:** Glassmorphism con blur y transparencias
- **Tipografía:** Segoe UI / Roboto optimizada
- **Iconografía:** Elementos visuales cubanos integrados

### **💎 Efectos Modernos**

- **Glassmorphism:** Tarjetas translúcidas con blur
- **Animaciones:** Transiciones suaves y micro-interacciones
- **Responsive:** Diseño adaptativo para móviles y desktop
- **Performance:** CSS optimizado para carga rápida

---

## 📱 **Funcionalidades**

### **📦 Gestión de Envíos**

- ✅ **Modo Simple:** Formulario básico y rápido
- ✅ **Modo Premium:** Formulario avanzado con todas las opciones
- ✅ **Dashboard:** Vista consolidada de envíos y estadísticas
- ✅ **Filtros:** Búsqueda y filtrado avanzado de envíos

### **🎯 Experiencia de Usuario**

- ✅ **Navegación Intuitiva:** Menú simplificado y accesible
- ✅ **Acciones Rápidas:** Botones de acción destacados
- ✅ **Feedback Visual:** Estados y notificaciones claras
- ✅ **Carga Optimizada:** Sistema CSS crítico para rendimiento

---

## 🛠 **Arquitectura Técnica**

### **Frontend - React + TypeScript**

```
📁 frontend/
├── 📁 src/
│   ├── 📁 components/     # Componentes React modulares
│   ├── 📁 pages/          # Páginas principales
│   ├── 📁 services/       # API y servicios
│   └── 📁 styles/         # Sistema CSS unificado
│       ├── critical.css       # Estilos críticos inmediatos
│       ├── global-modern.css  # Estilos globales glassmorphism
│       ├── pages-specific.css # Estilos específicos por página
│       └── 📁 core/           # Variables y fundamentos
└── 📄 vite.config.ts      # Configuración Vite optimizada
```

### **Backend - Django REST Framework**

```
📁 backend/
├── 📁 config/         # Configuración Django
├── 📁 envios/         # App principal de envíos
├── 📁 empresas/       # Gestión de empresas
├── 📁 usuarios/       # Autenticación y usuarios
└── � requirements.txt # Dependencias Python
```

### **Sistema CSS Unificado V4.0**

```css
/* Orden de carga optimizado */
@import "./critical.css"; /* Estilos críticos inmediatos */
@import "./global-modern.css"; /* Glassmorphism global */
@import "./pages-specific.css"; /* Optimizaciones específicas */
@import "./core/variables.css"; /* Variables centralizadas */
```

---

## � **Docker y Producción**

### **Servicios Docker**

- **🎨 Frontend:** Vite + Nginx (Puerto 5173)
- **🔧 Backend:** Django + uWSGI (Puerto 8000)
- **🗄️ Database:** PostgreSQL 16 (Puerto 5433)

### **Comandos útiles**

```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs
docker-compose logs frontend
docker-compose logs backend

# Reconstruir contenedores
docker-compose build --no-cache

# Limpiar sistema
docker-compose down -v
docker system prune -f
```

---

## � **Desarrollo**

### **Frontend (Desarrollo local)**

```bash
cd frontend
npm install
npm run dev
```

### **Backend (Desarrollo local)**

```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### **Base de datos**

```bash
# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

- **TypeScript** - Tipado estático para JavaScript
- **Vite** - Build tool ultrarrápido
- **PWA** - Progressive Web App con Service Worker
- **Responsive Design** - Adaptable a todos los dispositivos

### Backend

- **Django 5.2** - Framework web Python de alto nivel
- **Django REST Framework** - API REST robusta
- **JWT Authentication** - Autenticación segura con tokens
- **PostgreSQL** - Base de datos relacional potente
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
   - Base de datos: localhost:5433

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

```powershell
# Acceder a la base de datos
docker-compose exec database psql -U packfy_user -d packfy_db

# Crear datos de prueba
docker-compose exec backend python manage.py shell < scripts/create_demo_data.py

# Migrations
docker-compose exec backend python manage.py migrate
```

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

| Servicio             | Puerto | URL                         |
| -------------------- | ------ | --------------------------- |
| Frontend (React)     | 5173   | http://localhost:5173       |
| Backend API (Django) | 8000   | http://localhost:8000       |
| PostgreSQL           | 5433   | localhost:5433              |
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
