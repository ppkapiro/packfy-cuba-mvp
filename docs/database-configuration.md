# 📊 Configuración de Base de Datos - Packfy MVP

## 🎯 Estándar Actual: SQLite

### ✅ ¿Por qué SQLite?

**Para la fase MVP actual, SQLite es la opción óptima:**

- **🚀 Simplicidad**: Cero configuración, funciona inmediatamente
- **⚡ Rendimiento**: Para <1000 usuarios es más rápido que PostgreSQL
- **🔧 Desarrollo**: Sin dependencias externas, fácil testing y backup
- **💾 Escalabilidad**: Soporta hasta 281TB y millones de registros
- **🏗️ Compatibilidad**: Funciona perfectamente con multitenancy

### 📋 Configuración Actual

```python
# config/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 60,
            "check_same_thread": False,
        },
    }
}
```

### 📁 Archivos de Base de Datos

- **`db.sqlite3`** - Base de datos principal (ACTIVA)
- **`db_stop.sqlite3`** - Base histórica (ARCHIVADA)

### 🔄 Backup y Restauración

```bash
# Crear backup
cp db.sqlite3 backups/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Restaurar backup
cp backups/db_backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3
```

### 🚀 Migración Futura a PostgreSQL

**Cuándo migrar:**

- Más de 1000 usuarios activos simultáneos
- Más de 100GB de datos
- Necesidades de replicación avanzada
- Múltiples aplicaciones escritoras

**Preparación:**

1. Usar `python manage.py dumpdata` para exportar
2. Configurar PostgreSQL en Docker
3. Usar `python manage.py loaddata` para importar

### 🛠️ Comandos Útiles

```bash
# Verificar estado de la BD
python manage.py dbshell -c ".schema"

# Crear backup con datos
python manage.py dumpdata --indent 2 > backup_data.json

# Verificar integridad
python manage.py check --deploy
```

### 📊 Monitoreo

```bash
# Tamaño actual de la BD
ls -lh db.sqlite3

# Estadísticas de uso
sqlite3 db.sqlite3 "PRAGMA database_list; PRAGMA table_info(usuarios_usuario);"
```

---

**Última actualización**: 25 de agosto de 2025
**Estado**: ✅ Configuración estándar activa
