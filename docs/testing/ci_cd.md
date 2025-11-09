🚀 CI/CD Pipeline — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: DevOps / QA Team
Estado: ✅ Activo

📋 Propósito
Guía para automatizar testing, cobertura y deployment en THEA IA mediante GitHub Actions. Incluye configuración completa del pipeline, validaciones y deployment.

Audiencia:

Desarrolladores viendo feedback en PR

DevOps manteniendo pipelines

QA monitoreando métricas automáticas

Auditores validando automatización

🎯 Objetivo del pipeline
✅ En cada PR:

Linting (code style)

Tests unitarios

Tests de integración

Reporte de cobertura

Validación de seguridad

✅ En cada merge a main:

Tests E2E

Deploy a staging (opcional)

Generación de release notes

📂 Configuración GitHub Actions
Archivo: .github/workflows/tests.yml
text
name: Tests & Coverage

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    # 1. Checkout código
    - uses: actions/checkout@v4
    
    # 2. Setup Python
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    # 3. Instalar dependencias
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    # 4. Linting
    - name: Lint with ruff
      run: |
        ruff check src/theaia tests
        ruff format --check src/theaia tests
    
    # 5. Type checking
    - name: Type check with mypy
      run: |
        mypy src/theaia --ignore-missing-imports
      continue-on-error: true
    
    # 6. Tests unitarios
    - name: Run unit tests
      run: |
        pytest src/theaia/tests/unit/ -v --tb=short
    
    # 7. Tests integración
    - name: Run integration tests
      run: |
        pytest src/theaia/tests/integration/ -v --tb=short
    
    # 8. Cobertura
    - name: Generate coverage report
      run: |
        pytest src/theaia/tests/ \
          --cov=src/theaia \
          --cov-report=term-missing \
          --cov-report=xml \
          --cov-report=html
    
    # 9. Upload cobertura a codecov
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        fail_ci_if_error: false
    
    # 10. Comentar cobertura en PR
    - name: Comment coverage on PR
      if: github.event_name == 'pull_request'
      uses: py-cov-action/python-coverage-comment-action@v3
      with:
        GITHUB_TOKEN: ${{ github.token }}
    
    # 11. Publicar reporte HTML (artefacto)
    - name: Upload coverage reports as artifact
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report-${{ matrix.python-version }}
        path: htmlcov/

  e2e:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: test
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run E2E tests
      run: |
        pytest src/theaia/tests/e2e/ -v --timeout=60
      timeout-minutes: 15
🔍 Detalles de cada paso
1. Linting (ruff)
bash
# Verifica código style y errores estáticos
ruff check src/theaia  # Errores y warnings
ruff format --check src/theaia  # Formatea con black-compatible
En CI/CD:

❌ PR falla si hay errores de linting

⚠️ Warnings permitidos (continue-on-error: false)

2. Type checking (mypy)
bash
# Verifica tipos Python
mypy src/theaia --ignore-missing-imports
En CI/CD:

⚠️ Warnings permitidos (continue-on-error: true)

No es bloqueador aún (mejora gradual)

3. Tests unitarios
bash
pytest src/theaia/tests/unit/ -v --tb=short
En CI/CD:

❌ PR falla si algún test unitario falla

Reporte: stdout + artefacto

4. Tests integración
bash
pytest src/theaia/tests/integration/ -v --tb=short
En CI/CD:

❌ PR falla si test integración falla

Puede ser más lento

5. Cobertura
bash
pytest src/theaia/tests/ \
  --cov=src/theaia \
  --cov-report=term-missing \
  --cov-report=xml \
  --cov-report=html
Reportes generados:

term-missing: Stdout con líneas no cubiertas

coverage.xml: Para Codecov

htmlcov/: Reporte HTML interactivo

6. Upload a Codecov
text
- uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
    fail_ci_if_error: false  # No falla si codecov está down
Resultado:

Badge de cobertura en README

Historial de cobertura en Codecov

Comparación PR vs main

7. Comentario en PR
text
- uses: py-cov-action/python-coverage-comment-action@v3
Resultado:

Comentario automático en cada PR

% cobertura actual vs target

Líneas no cubiertas por archivo

8. E2E tests (solo en main)
text
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
Por qué solo en main:

Lentos (minutos)

No necesarios en cada PR

Validación final antes de deploy

📊 Matriz de Python
text
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
Resultado:

Tests corren en 3 versiones Python

Compatible con 3.10, 3.11, 3.12

Fallos destacados en versiones específicas

🚀 Workflows adicionales
Deployment (opcional)
text
name: Deploy to Staging

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    needs: test
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to staging
      run: |
        # Script deploy a staging
        ./scripts/deploy-staging.sh
      env:
        DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
Release automático
text
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      with:
        body_path: CHANGELOG.md
📌 Configuración local (pre-commit)
Para validar antes de hacer commit localmente:

Archivo: .pre-commit-config.yaml
text
repos:
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-merge-conflict

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
        additional_dependencies: [types-all]
Instalación:

bash
pip install pre-commit
pre-commit install
Ejecución:

Automática antes de git commit

Manual: pre-commit run --all-files

✅ Checklist por evento
En Pull Request
✅ Linting pasa

✅ Tests unitarios pasan

✅ Tests integración pasan

✅ Cobertura >= 85% global

✅ Módulos críticos >= 90%

✅ Sin degradación vs main

✅ Comentario de cobertura visible

✅ Reporte HTML disponible

En Push a main (merge)
✅ Todos los checks de PR pasan

✅ E2E tests completan exitosamente

✅ Coverage badge se actualiza

✅ Deploy a staging exitoso (opcional)

✅ Release notes generadas (si tag)

🔗 Badges para README
text
![Tests](https://github.com/alvarofernandezmota-tech/thea-ia/workflows/Tests%20&%20Coverage/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/alvarofernandezmota-tech/thea-ia/main)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
🚨 Troubleshooting
Tests fallan en CI pero pasan localmente
Causa común: Dependencia de orden de tests o estado global

Solución:

bash
# Test aislado
pytest src/theaia/tests/unit/test_specific.py -v

# Orden aleatorio
pytest src/theaia/tests/ -v --random-order

# Sin cache
pytest src/theaia/tests/ -v --cache-clear
Cobertura baja reportada
Causa: Líneas dinámicas no ejecutadas en CI

Solución:

bash
# Revisar qué no está cubierto
pytest --cov=src/theaia --cov-report=term-missing

# Agregar test o pragma: no cover
def complex_dynamic_func():  # pragma: no cover
    ...
Timeout en E2E tests
Causa: Tests demasiado lentos o cuelgue

Solución:

bash
# Aumentar timeout en CI
pytest ... --timeout=120  # 2 minutos

# Optimizar tests locales
pytest ... -v --durations=10  # Top 10 lentos
🔗 Referencias y enlaces
Testing Overview — Estrategia general

Coverage Report — Métricas de cobertura

Unit Tests — Escribir tests unitarios

Audit Checklist — Validación de auditoría

📌 Meta-información
Campo	Valor
Archivo	docs/testing/ci_cd.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	DevOps / QA Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 35.1.2 (docs/testing/)

Sigue estándar THEA IA: Modular, auditable, escalable

Pipeline validado y operativo

Cambios deben actualizarse aquí

Validado en sesión 35

Nota: Secrets (tokens, keys) se configuran en GitHub Settings → Secrets, nunca en el código.

8/10/25 a las 16.42
