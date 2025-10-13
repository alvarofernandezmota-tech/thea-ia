# Scripts - Automatización y Despliegue

## 📖 Descripción

Colección de scripts de automatización para Thea IA 2.0. Incluye scripts para instalación, despliegue, migraciones de base de datos y herramientas de desarrollo.

## 📂 Estructura

scripts/
├── setup.sh # Instalación y configuración inicial
├── deploy.sh # Despliegue a producción/staging
├── migrate.sh # Migraciones de base de datos
├── lint.sh # Linting y formateo de código
├── backup.sh # Copia de seguridad de la base de datos
├── entrypoint.sh # Script de entrada para Docker/despliegue
├── test_runner.sh # Lanza todos los tests automáticamente
└── README.md # Este archivo

text

## 🔧 Scripts Disponibles

### setup.sh - Instalación y Configuración

**Propósito:** Configuración inicial del entorno de desarrollo.

**Uso:**
./scripts/setup.sh [opciones]

text

**Opciones:**
- `--dev`: Instala dependencias de desarrollo
- `--prod`: Configuración para producción
- `--docker`: Setup con Docker
- `--clean`: Limpia instalación previa

**Ejemplo:**
Setup completo desarrollo
./scripts/setup.sh --dev

Setup producción
./scripts/setup.sh --prod --docker

text

---

### deploy.sh - Despliegue Automatizado

**Propósito:** Despliegue a entornos staging/producción.

**Uso:**
./scripts/deploy.sh [entorno] [opciones]

text

**Entornos:**
- `staging`: Despliegue a staging
- `production`: Despliegue a producción
- `local`: Despliegue local con Docker

**Opciones:**
- `--build`: Rebuild completo de imágenes
- `--migrate`: Ejecuta migraciones tras despliegue
- `--rollback`: Rollback a versión anterior
- `--health-check`: Verifica salud post-despliegue

**Ejemplo:**
Deploy a staging
./scripts/deploy.sh staging --build --migrate

Deploy a producción con health check
./scripts/deploy.sh production --health-check

text

---

### migrate.sh - Migraciones Base de Datos

**Propósito:** Gestión de migraciones Alembic.

**Uso:**
./scripts/migrate.sh [comando] [opciones]

text

**Comandos:**
- `upgrade`: Aplica migraciones pendientes
- `downgrade`: Revierte migraciones
- `current`: Muestra revisión actual
- `history`: Historial de migraciones
- `generate`: Genera nueva migración

**Opciones:**
- `--revision [id]`: Migra a revisión específica
- `--sql`: Muestra SQL sin ejecutar
- `--backup`: Crea backup antes de migrar
- `--env [entorno]`: Especifica entorno

**Ejemplo:**
Aplicar todas las migraciones pendientes
./scripts/migrate.sh upgrade

Generar nueva migración
./scripts/migrate.sh generate --message "Add user profile table"

text

---

### lint.sh - Linting y Formateo

**Propósito:** Análisis de calidad y formateo de código.

**Uso:**
./scripts/lint.sh [opciones]

text

**Opciones:**
- `--fix`: Auto-corrige errores cuando es posible
- `--check`: Solo verifica, no modifica archivos
- `--strict`: Modo estricto (fallos en warnings)
- `--files [pattern]`: Analiza archivos específicos

**Herramientas incluidas:**
- **Black**: Formateo automático Python
- **isort**: Ordenamiento imports
- **flake8**: Linting y style guide
- **mypy**: Type checking
- **bandit**: Security linting

**Ejemplo:**
Lint completo con auto-fix
./scripts/lint.sh --fix

Solo verificación (CI)
./scripts/lint.sh --check --strict

text

---

### backup.sh - Copia de Seguridad de BD

**Propósito:** Copia de seguridad de la base de datos principal.

**Uso:**
./scripts/backup.sh

text

**Ejemplo:**
./scripts/backup.sh

text

---

### entrypoint.sh - Script de Entrada

**Propósito:** Script principal de entrada para Docker o despliegue.

#!/bin/bash
echo "🟢 Iniciando entorno Thea IA 2.0..."
./scripts/migrate.sh upgrade
exec "$@"

text

---

### test_runner.sh - Ejecución de Tests

**Propósito:** Lanza todos los tests del sistema automáticamente.

#!/bin/bash
echo "🚀 Lanzando tests unitarios, integración y e2e..."
pytest tests/ -v --cov=src/theaia --cov-report=html
if [ $? -eq 0 ]; then
echo "✅ Todos los tests completaron con éxito"
else
echo "❌ Algunos tests fallaron"
exit 1
fi

text

---

## 🔧 Configuración y Variables de Entorno

- Asegúrate de tener configuradas las variables en `.env` o entorno:
DATABASE_URL=postgresql://user:pass@localhost:5432/theaia_db
ENABLE_E2E=true

text
- Para scripts de despliegue y migraciones, revisa `settings.py` y `logging_config.py` en `src/theaia/config/`.

---

*Documentación de scripts actualizada: 13/10/2025*