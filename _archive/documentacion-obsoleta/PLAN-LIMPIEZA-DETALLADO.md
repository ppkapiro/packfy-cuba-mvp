# 🧹 PLAN DE LIMPIEZA DETALLADO - PACKFY

## 📊 DIAGNÓSTICO INICIAL

- **38 archivos Python** en directorio raíz (muchos temporales)
- **117 archivos PowerShell** en directorio raíz (scripts de desarrollo)
- **26 archivos Markdown** en directorio raíz (documentación fragmentada)
- **Total estimado:** ~200+ archivos temporales/obsoletos

---

## 🎯 ESTRATEGIA DE LIMPIEZA SEGURA

### ✅ PASO 1: IDENTIFICAR ARCHIVOS CRÍTICOS (NO TOCAR)

#### 📁 Backend (Django) - CRÍTICOS

```
backend/
├── manage.py ✅ CRÍTICO
├── packfy/
│   ├── __init__.py ✅ CRÍTICO
│   ├── settings.py ✅ CRÍTICO
│   ├── urls.py ✅ CRÍTICO
│   └── wsgi.py ✅ CRÍTICO
├── empresas/
│   ├── models.py ✅ CRÍTICO
│   ├── views.py ✅ CRÍTICO (SuperAdmin API)
│   ├── serializers.py ✅ CRÍTICO
│   └── permissions.py ✅ CRÍTICO
├── envios/
│   ├── models.py ✅ CRÍTICO
│   ├── views.py ✅ CRÍTICO
│   └── serializers.py ✅ CRÍTICO
└── usuarios/
    ├── models.py ✅ CRÍTICO
    ├── views.py ✅ CRÍTICO
    └── serializers.py ✅ CRÍTICO
```

#### 📁 Frontend (React) - CRÍTICOS

```
frontend/
├── package.json ✅ CRÍTICO
├── vite.config.ts ✅ CRÍTICO (proxy config)
├── src/
│   ├── main.tsx ✅ CRÍTICO
│   ├── App.tsx ✅ CRÍTICO (SuperAdmin routing)
│   ├── contexts/
│   │   ├── AuthContext.tsx ✅ CRÍTICO
│   │   └── TenantContext.tsx ✅ CRÍTICO (multitenancy)
│   ├── components/
│   │   ├── SuperAdminPanel.tsx ✅ CRÍTICO (recién desarrollado)
│   │   ├── Layout.tsx ✅ CRÍTICO
│   │   ├── DashboardRouter.tsx ✅ CRÍTICO
│   │   └── TenantSelector.tsx ✅ CRÍTICO
│   └── services/
│       └── api.ts ✅ CRÍTICO (makeSuperAdminRequest)
```

#### 📁 Docker - CRÍTICOS

```
docker-compose.yml ✅ CRÍTICO
docker-compose.override.yml ✅ CRÍTICO
docker-compose.prod.yml ✅ CRÍTICO
backend/Dockerfile ✅ CRÍTICO
frontend/Dockerfile ✅ CRÍTICO
```

---

### 🗑️ PASO 2: ARCHIVOS PARA ELIMINAR/MOVER

#### 🔥 Categoría A: ELIMINAR COMPLETAMENTE

```
# Scripts de diagnóstico obsoletos
diagnostico-*.ps1 (15+ archivos)
debug-*.ps1 (5+ archivos)
check_*.py (varios archivos)

# Documentación fragmentada/obsoleta
ANALISIS-PROFUNDO-*.md
APIS-MULTI-TENANT-*.md
BUSQUEDA-COMPLETA-*.md
COMMIT-FINAL-*.md
COMPILACION-EXITOSA.txt
CONEXION-MOVIL-*.md
CONFIGURACION-ROBUSTA-*.md
CREDENCIALES-TESTING.md
DIAGNOSTICO_*.md
DISEÑO-PREMIUM-*.md
DOCKER-BUILD-*.md
ENTORNO-IDEAL-*.md
ESTADO-*.md

# Archivos temporales
diagnostico_*.json
diagnostico_*.html
estado-sistema-*.html
BD_PROTECTION_STATUS.lock
temp-*.txt
```

#### 📦 Categoría B: MOVER A CARPETA `_archive/`

```
# Scripts que pueden ser útiles pero no críticos
aplicar_*.py
arreglar_*.py
blindar_*.py
completar_*.py
configurar_*.py (algunos)
crear_*.py (muchos)
fix_*.py
limpieza_*.py
proteger_*.py

# Scripts PowerShell útiles pero no críticos
build-*.ps1
configurar-*.ps1 (algunos)
corregir-*.ps1
crear-*.ps1
inicio-*.ps1
instrucciones-*.ps1
modo-*.ps1
```

#### 🔧 Categoría C: REORGANIZAR

```
# Scripts útiles para desarrollo
dev.ps1 → scripts/dev.ps1
deploy.ps1 → scripts/deploy.ps1
ABRIR-PACKFY.ps1 → scripts/start.ps1

# Documentación actual
README.md ✅ MANTENER
auditoria-README.md → docs/auditoria.md
CHANGELOG.md → docs/changelog.md
```

---

### 📋 PASO 3: ESTRUCTURA FINAL DESEADA

```
paqueteria-cuba-mvp/
├── 📁 backend/ (Django app - limpio)
├── 📁 frontend/ (React app - limpio)
├── 📁 scripts/ (scripts útiles organizados)
├── 📁 docs/ (documentación consolidada)
├── 📁 _archive/ (archivos históricos)
├── docker-compose.yml
├── docker-compose.override.yml
├── docker-compose.prod.yml
├── README.md (actualizado)
└── .gitignore (actualizado)
```

---

## 🚀 EJECUCIÓN DEL PLAN

### Fase 1: Preparación

- [x] Crear backup branch ✅
- [ ] Crear carpetas de destino
- [ ] Documentar dependencias críticas

### Fase 2: Limpieza gradual

- [ ] Mover archivos categoría B a `_archive/`
- [ ] Eliminar archivos categoría A (con confirmación)
- [ ] Reorganizar archivos categoría C

### Fase 3: Validación

- [ ] Probar Docker compose
- [ ] Verificar SuperAdminPanel
- [ ] Testear multitenancy
- [ ] Confirmar autenticación

### Fase 4: Documentación

- [ ] Actualizar README.md
- [ ] Consolidar documentación
- [ ] Crear .gitignore robusto

---

## ⚠️ REGLAS DE SEGURIDAD

1. **NUNCA ELIMINAR** sin mover primero a `_archive/`
2. **PROBAR SISTEMA** después de cada fase
3. **MANTENER BACKUP** accesible en todo momento
4. **DOCUMENTAR CAMBIOS** para posible rollback
5. **VALIDAR DOCKER** antes de confirmar limpieza

---

¿Proceder con la **Fase 1: Preparación**?
