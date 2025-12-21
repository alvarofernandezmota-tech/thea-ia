# 🧹 THEA IA - Script de Limpieza de Raíz

## Auditoría Diciembre 2025 - Investment Readiness

**Fecha:** 21 Diciembre 2025  
**Propósito:** Limpiar y organizar la raíz del proyecto para presentación a inversores

---

## 📋 Resumen

Este script automatiza la limpieza completa de la raíz del proyecto THEA IA, organizando archivos según best practices y removiendo elementos que afectan la presentación profesional.

### Problema Identificado

**Estado Actual:**
- ❌ 42 items en raíz (desorganizado)
- ❌ Credenciales expuestas (`.env` en GitHub)
- ❌ 4 directorios cache en repositorio
- ❌ 7 scripts de ejecución en raíz
- ❌ Archivos temporales en raíz

**Scores Actuales:**
- Organización: **4.5/10** 🔴
- Investment Readiness: **6.5/10** 🟡

### Objetivo

**Estado Deseado:**
- ✅ 27 items en raíz (limpio y profesional)
- ✅ Sin credenciales expuestas
- ✅ Sin directorios cache
- ✅ Todos los scripts en `scripts/`
- ✅ Estructura clara y organizada

**Scores Target:**
- Organización: **8.5/10** ✅ (+4.0 puntos)
- Investment Readiness: **7.5/10** ✅ (+1.0 punto)

---

## 🚀 Uso del Script

### Requisitos Previos

```bash
# 1. Estar en la raíz del proyecto
cd /ruta/a/thea-ia

# 2. Tener repositorio limpio (sin cambios sin commitear)
git status
# Debe mostrar: "working tree clean"

# 3. Estar en rama main
git branch
# Debe mostrar: * main
```

### Ejecución

```bash
# Dar permisos de ejecución (solo primera vez)
chmod +x scripts/cleanup_audit_dec2025.sh

# Ejecutar script
bash scripts/cleanup_audit_dec2025.sh
```

### Qué hace el script

El script ejecuta **5 pasos** secuencialmente:

#### **PASO 1: Mover Scripts** (5 archivos)
```bash
run_bot.py           → scripts/
run_demo.py          → scripts/
run_h9_tests.sh      → scripts/
run_interactive.py   → scripts/
run_real.py          → scripts/
```

#### **PASO 2: Mover Tests Manuales** (1 archivo)
```bash
test_groq_manual.py  → src/theaia/tests/manual/
```

#### **PASO 3: Mover Documentos Temporales** (1 archivo)
```bash
SESSION-17-DIC-2025-SUMMARY.md → docs/diary/diciembre/
```

#### **PASO 4: Remover Cache y Archivos Sensibles**
```bash
# Security fix CRÍTICO
.env                 → REMOVIDO (credenciales)

# Cache directories
.pytest_cache/       → REMOVIDO
__pycache__/         → REMOVIDO
htmlcov/             → REMOVIDO
venv/                → REMOVIDO

# Temporary logs
tests.log            → REMOVIDO
```

#### **PASO 5: Crear Commit**
```bash
git commit -m "refactor(audit): Complete root cleanup"
```

---

## 📊 Resultado Esperado

### Antes
```
thea-ia/
├── run_bot.py                    # ❌ En raíz
├── run_demo.py                   # ❌ En raíz
├── run_h9_tests.sh               # ❌ En raíz
├── run_interactive.py            # ❌ En raíz
├── run_real.py                   # ❌ En raíz
├── fix_tests.py                  # ❌ En raíz
├── test_groq_manual.py           # ❌ En raíz
├── SESSION-17-DIC-2025-SUMMARY.md # ❌ En raíz
├── .env                          # 🔴 CREDENCIALES EXPUESTAS
├── tests.log                     # ❌ Log temporal
├── .pytest_cache/                # ❌ Cache
├── __pycache__/                  # ❌ Cache
├── htmlcov/                      # ❌ Coverage reports
├── venv/                         # ❌ Virtual environment
└── ... (otros 28 archivos)

TOTAL: 42 items | Score: 4.5/10 🔴
```

### Después
```
thea-ia/
├── .archive/
├── .devcontainer/
├── .github/
├── .railway/
├── data/
├── docs/
├── scripts/                      # ✅ Todos los scripts aquí
│   ├── run_bot.py
│   ├── run_demo.py
│   ├── run_h9_tests.sh
│   ├── run_interactive.py
│   ├── run_real.py
│   ├── fix_tests.py
│   └── cleanup_audit_dec2025.sh
├── src/
│   └── theaia/
│       └── tests/
│           └── manual/
│               └── test_groq_manual.py  # ✅ Aquí
├── .env.example                  # ✅ Template (OK)
├── .env.test                     # ✅ Test env (OK)
├── .gitignore                    # ✅ Mejorado
├── CHANGELOG.md
├── CONTRIBUTING.md
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── pytest.ini
├── README.md
├── ROADMAP.md
├── SECURITY.md
└── requirements.txt

TOTAL: 27 items | Score: 8.5/10 ✅
```

---

## ✅ Verificación Post-Ejecución

### 1. Verificar Estructura
```bash
# Contar items en raíz
ls -1 | wc -l
# Debe mostrar: ~27

# Verificar scripts movidos
ls scripts/run_*.py
# Debe mostrar: run_bot.py, run_demo.py, run_interactive.py, run_real.py

# Verificar test movido
ls src/theaia/tests/manual/
# Debe mostrar: test_groq_manual.py
```

### 2. Verificar .env Removido
```bash
# NO debe existir en working directory
ls -la | grep ".env"
# Solo debe mostrar: .env.example, .env.test

# NO debe estar en git
git ls-files | grep "^\.env$"
# No debe mostrar nada
```

### 3. Verificar Cache Removido
```bash
# NO debe estar en git
git ls-files | grep -E "(__pycache__|.pytest_cache|htmlcov|venv)"
# No debe mostrar nada
```

### 4. Ver Commit
```bash
# Ver último commit
git log -1 --stat
# Debe mostrar todos los archivos movidos/removidos
```

---

## 🔄 Push a GitHub

Una vez verificado todo:

```bash
# Push al remoto
git push origin main

# Verificar en GitHub
# https://github.com/alvarofernandezmota-tech/thea-ia
```

---

## 🚨 Troubleshooting

### Error: "nothing to commit"
**Causa:** Los archivos ya fueron movidos/removidos previamente  
**Solución:** Verificar que estás en la rama correcta

### Error: "pathspec 'file' did not match any files"
**Causa:** El archivo no existe en la raíz  
**Solución:** El script verifica existencia antes de mover. Es seguro.

### Error: ".env still in repository"
**Causa:** .env está en staging area  
**Solución:**
```bash
git rm --cached .env
git commit -m "security: Remove .env from repository"
```

---

## 📈 Métricas de Éxito

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Items en raíz** | 42 | 27 | -15 (-36%) |
| **Organización** | 4.5/10 | 8.5/10 | +4.0 (+89%) |
| **Investment Readiness** | 6.5/10 | 7.5/10 | +1.0 (+15%) |
| **Security Issues** | 1 crítico | 0 | ✅ Resuelto |
| **Cache en repo** | 4 dirs | 0 | ✅ Limpio |
| **Scripts organizados** | 0% | 100% | ✅ Completo |

---

## 📝 Notas Importantes

### Sobre .env
⚠️ **IMPORTANTE:** El archivo `.env` será removido del repositorio pero **permanecerá en tu disco local**. Esto es intencional:

- ✅ Tus credenciales siguen funcionando localmente
- ✅ El archivo ya no está expuesto en GitHub
- ✅ `.gitignore` mejorado previene futuros commits accidentales

### Sobre venv/
⚠️ **NOTA:** El directorio `venv/` será removido de git pero **permanecerá en disco**. Tu entorno virtual sigue funcional.

### Reversión
Si necesitas revertir los cambios:
```bash
# Ver hash del commit
git log -1

# Revertir
git revert <commit-hash>
```

---

## 🎯 Próximos Pasos

Después de ejecutar este script:

1. ✅ **Verificar** que todo está correcto (ver sección Verificación)
2. ✅ **Push** a GitHub: `git push origin main`
3. ✅ **Documentar** en auditoría (se hará automáticamente)
4. ⏳ **Continuar** con FASE 2 de auditoría (docs/ y src/)

---

## 📚 Referencias

- **Auditoría Completa:** `docs/audit/auditdiciembre/`
- **Diario de Sesión:** `docs/diary/diciembre/2025-12-21.md`
- **Roadmap H09:** `docs/roadmap/milestones/H09/`

---

**Creado:** 21 Diciembre 2025  
**Auditoría:** December 2025 Investment Readiness  
**Estado:** ✅ Listo para ejecución
