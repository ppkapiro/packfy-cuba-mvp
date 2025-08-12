# INSTRUCCIONES PARA SUBIR PROYECTO A GITHUB
Write-Host "SUBIENDO PROYECTO PACKFY A GITHUB" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

Write-Host "`n1. VERIFICAR GIT INSTALADO:" -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git no instalado - Descargar de: https://git-scm.com/" -ForegroundColor Red
    exit 1
}

Write-Host "`n2. INICIALIZAR REPOSITORIO LOCAL:" -ForegroundColor Yellow
if (!(Test-Path ".git")) {
    Write-Host "Inicializando repositorio git..." -ForegroundColor Cyan
    git init
    Write-Host "✅ Repositorio inicializado" -ForegroundColor Green
} else {
    Write-Host "✅ Repositorio git ya existe" -ForegroundColor Green
}

Write-Host "`n3. CREAR .gitignore:" -ForegroundColor Yellow
if (!(Test-Path ".gitignore")) {
    Write-Host "Creando .gitignore..." -ForegroundColor Cyan
    @"
# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis

# OS Files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build outputs
dist/
build/
*.egg-info/

# Docker
*.log

# Database
*.db
*.sqlite3

# Media files (uploads)
media/

# Static files (will be collected)
staticfiles/

# Backup files
*.bak
*.backup

# Temporary files
*.tmp
*.temp

# Ngrok
ngrok/
ngrok.zip
node.zip
node-v*/
"@ | Out-File -FilePath ".gitignore" -Encoding utf8
    Write-Host "✅ .gitignore creado" -ForegroundColor Green
} else {
    Write-Host "✅ .gitignore ya existe" -ForegroundColor Green
}

Write-Host "`n4. CREAR README.md ACTUALIZADO:" -ForegroundColor Yellow
@"
# 📦 Packfy - Sistema de Paquetería para Cuba

## 🚀 Descripción
Sistema completo de gestión de envíos para Cuba con funcionalidad PWA (Progressive Web App) para uso en móviles.

## ✨ Características
- 🏢 **Multi-tenant**: Múltiples empresas
- 📱 **PWA**: Instalable en móviles como app nativa
- 🔐 **Autenticación**: Sistema de usuarios seguro
- 📊 **Dashboard**: Panel de control completo
- 🚚 **Gestión de envíos**: CRUD completo de paquetes
- 📧 **Notificaciones**: Sistema de alertas por email
- 🐳 **Docker**: Totalmente containerizado

## 🛠️ Stack Tecnológico

### Backend
- **Django** 4.2+ con DRF
- **PostgreSQL** 16
- **Python** 3.11+

### Frontend
- **React** 18+ con TypeScript
- **Vite** para build y desarrollo
- **PWA** con Service Workers
- **Responsive Design**

## 🚀 Instalación y Uso

### Prerrequisitos
- Docker y Docker Compose
- Git

### Instalación
\`\`\`bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/packfy-cuba-mvp.git
cd packfy-cuba-mvp

# Iniciar servicios
docker compose up -d

# Crear superusuario
docker exec -i packfy-backend python /app/scripts/create_admin.py
\`\`\`

### URLs
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

### Credenciales por defecto
- **Email**: admin@correo.com
- **Password**: admin123

## 📱 PWA (Progressive Web App)

### Instalación en móvil
1. Abrir en navegador móvil: \`http://TU_IP:5173\`
2. Seguir instrucciones de instalación
3. Para desarrollo local, configurar Chrome flags para HTTP

### URLs de prueba
- **Test PWA**: \`http://TU_IP:5173/test-pwa.html\`
- **Verificación**: Ejecutar \`.\test-pwa.ps1\`

## 🐳 Docker Services

### Servicios incluidos
- **packfy-frontend**: React + Vite (Puerto 5173)
- **packfy-backend**: Django + DRF (Puerto 8000)  
- **packfy-database**: PostgreSQL 16 (Puerto 5433)

### Comandos útiles
\`\`\`bash
# Ver estado de servicios
docker compose ps

# Ver logs
docker logs packfy-frontend
docker logs packfy-backend

# Reiniciar servicios
docker compose restart

# Parar servicios
docker compose down
\`\`\`

## 🔧 Scripts de Utilidad

- **\`test-pwa.ps1\`**: Verificación completa de PWA
- **\`guia-movil.ps1\`**: Instrucciones para móvil
- **\`instrucciones-finales.ps1\`**: Configuración final

## 🌐 Deployment

### Para producción
1. Configurar variables de entorno
2. Usar HTTPS (requerido para PWA)
3. Configurar dominio personalizado

## 📝 Desarrollo

### Estructura del proyecto
\`\`\`
packfy-cuba-mvp/
├── backend/           # Django API
├── frontend/          # React PWA
├── docs/             # Documentación
├── compose.yml       # Docker Compose
└── *.ps1            # Scripts de utilidad
\`\`\`

## 🤝 Contribución
1. Fork el repositorio
2. Crear branch para feature
3. Commit cambios
4. Push y crear Pull Request

## 📄 Licencia
MIT License

## 📞 Soporte
Para soporte técnico, crear un issue en GitHub.

---

⭐ **¡Dale una estrella si te gusta el proyecto!** ⭐
"@ | Out-File -FilePath "README.md" -Encoding utf8

Write-Host "✅ README.md actualizado" -ForegroundColor Green

Write-Host "`n5. AGREGAR ARCHIVOS AL STAGING:" -ForegroundColor Yellow
git add .
Write-Host "✅ Archivos agregados" -ForegroundColor Green

Write-Host "`n6. HACER COMMIT INICIAL:" -ForegroundColor Yellow
git commit -m "🚀 Initial commit: Packfy Cuba MVP with PWA functionality

✨ Features:
- Multi-tenant Django backend with DRF
- React TypeScript frontend with PWA
- Docker containerization
- PostgreSQL database
- Service Workers for offline functionality
- Mobile-responsive design
- Admin panel and user authentication

🛠️ Technical Stack:
- Backend: Django 4.2+ + PostgreSQL 16
- Frontend: React 18 + TypeScript + Vite
- Infrastructure: Docker Compose
- PWA: Service Workers + Web App Manifest

📱 PWA Ready:
- Installable on mobile devices
- Offline functionality
- Native app-like experience
- Test page included for verification"

Write-Host "✅ Commit inicial creado" -ForegroundColor Green

Write-Host "`n7. PASOS PARA SUBIR A GITHUB:" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow
Write-Host "AHORA NECESITAS:" -ForegroundColor Red
Write-Host "1. Ir a: https://github.com" -ForegroundColor Cyan
Write-Host "2. Crear nuevo repositorio llamado: packfy-cuba-mvp" -ForegroundColor Cyan
Write-Host "3. NO marcar 'Initialize with README' (ya tenemos uno)" -ForegroundColor Cyan
Write-Host "4. Copiar la URL del repositorio (ej: https://github.com/TU_USUARIO/packfy-cuba-mvp.git)" -ForegroundColor Cyan
Write-Host "5. Volver aqui y ejecutar:" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/TU_USUARIO/packfy-cuba-mvp.git" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White

Write-Host "`n8. COMANDOS LISTOS PARA COPIAR:" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow
Write-Host "# Reemplaza TU_USUARIO con tu usuario de GitHub:" -ForegroundColor Green
Write-Host "git remote add origin https://github.com/TU_USUARIO/packfy-cuba-mvp.git" -ForegroundColor Cyan
Write-Host "git branch -M main" -ForegroundColor Cyan
Write-Host "git push -u origin main" -ForegroundColor Cyan

Write-Host "`n✅ PREPARACION COMPLETADA!" -ForegroundColor Green
Write-Host "Ahora crea el repositorio en GitHub y ejecuta los comandos finales." -ForegroundColor Yellow
