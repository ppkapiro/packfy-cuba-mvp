# 🔧 PLAN DE REPARACIÓN SEGURA - SIN DAÑAR LO QUE FUNCIONA

## 🎯 OBJETIVO

Arreglar el backend sin modificar código que funciona

## 🔍 DIAGNÓSTICO

- ✅ Frontend funcionando (puerto 5173)
- ✅ Base de datos funcionando (puerto 5433)
- ❌ Backend fallando: script run_migrations.sh "not found"
- 📋 Archivos SÍ existen en el repositorio
- 🐳 Problema: Cache/build de Docker corrupto

## 🛡️ ESTRATEGIA SEGURA

### PASO 1: BACKUP DE SEGURIDAD

```powershell
# Crear backup del estado actual funcionante
docker commit packfy-frontend packfy-frontend-backup
docker commit packfy-database packfy-database-backup
```

### PASO 2: REBUILD LIMPIO SOLO DEL BACKEND

```powershell
# Detener solo backend (mantener frontend y DB)
docker-compose stop backend

# Eliminar imagen backend corrupta
docker rmi packfy-mvp-backend

# Rebuild solo backend con cache limpio
docker-compose build --no-cache backend

# Reiniciar solo backend
docker-compose up -d backend
```

### PASO 3: VERIFICACIÓN

```powershell
# Verificar logs
docker logs packfy-backend --tail 10

# Verificar servicios
docker-compose ps
```

## 🚨 ROLLBACK SI ALGO SALE MAL

```powershell
# Si algo falla, restaurar backup
docker tag packfy-frontend-backup packfy-mvp-frontend
```

## ✅ RESULTADO ESPERADO

- Frontend: Sigue funcionando ✅
- Base de datos: Sigue funcionando ✅
- Backend: Reparado ✅
- API: Disponible en http://localhost:8000

¿Proceder con esta estrategia segura?
