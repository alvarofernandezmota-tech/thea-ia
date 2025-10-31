# CONTRIBUTING — THEA IA

**Proyecto:** THEA IA  
**Versión:** 2.0 / v0.14.0  
**Actualizado:** 2025-10-31  
**Autor:** Álvaro Fernández Mota (CEO THEA IA)

---

> **IMPORTANTE PARA COLABORADORES Y AUDITORES**
>
> - Todos los cambios deben alinearse con los **17 hitos principales** y el roadmap global.
> - Cada carpeta (core, agents, adapters, tests, ml, docs) tiene su propio README, ROADMAP y CHANGELOG.
> - Trabajo colaborativo y auditable: transparencia, trazabilidad y documentación en todo momento.
> - Antes de hacer PR, actualiza README y ROADMAP de tu módulo.

---

## 🎯 Normas de contribución

### 1. Ramas y versionado (Git)

Usa Git flow estricto:

main/
├── develop (rama principal de desarrollo)
│ ├── feature/[hito]-[feature-name]
│ ├── bugfix/[hito]-[bug-name]
│ ├── hotfix/[hito]-critical-issue
│ └── refactor/[hito]-[module-name]

text

**Ejemplos:**
- `feature/H01-test-compatibility`
- `bugfix/H05-agent-agenda-timeout`
- `hotfix/H03-fsm-critical-state-error`
- `refactor/H06-ml-intent-detector`

**Reglas:**
- Nunca trabajes directamente en `main` o `develop`.
- Una rama = un hito/feature/bugfix.
- Merge a `develop` solo tras PR aprobado y tests verdes.
- Release a `main` solo tras auditoría y changelog actualizado.

---

### 2. Commits y mensajes (Conventional Commits)

Formato obligatorio:

<type>([hito]): <description>

[optional body]
[optional footer]

text

**Tipos válidos:**
- `feat`: Nueva feature/hito
- `fix`: Corrección de bug
- `docs`: Cambios documentación
- `refactor`: Cambio estructura sin alterar funcionalidad
- `test`: Nuevos tests o mejoras de cobertura
- `perf`: Optimización/performance
- `chore`: Cambios build, deps, infra
- `audit`: Cambios auditoría, seguridad, logs

**Ejemplos:**
feat(H01): añade compatibilidad tests y organización ecosistema
fix(H05): corrige timeout agent agenda
docs(H14): actualiza onboarding y README core
refactor(H03): mejora FSM transitions y manager universal
test(H07): aumenta coverage a 85% e2e tests
audit(H13): hardening seguridad y encriptación

text

---

### 3. Pull Requests (PR)

**Proceso obligatorio:**

1. Crea rama desde `develop` con nombre claro.
2. Desarrolla feature/fix/refactor.
3. **Actualiza README, ROADMAP, CHANGELOG de tu módulo.**
4. Ejecuta tests locales y cubre ≥80%.
5. Haz PR con:
   - **Título:** `[HITO] - Descripción clara`
   - **Descripción:** Qué cambia, por qué, referencias a hitos/issues.
   - **Checklist:** Ver plantilla abajo.
6. Equipo revisa y aprueba.
7. Merge a `develop`.
8. Release manager actualiza versión y libera a `main`.

---

### 4. Checklist de PR (Obligatorio)

Cambios propuestos
 Feature nueva / Bug fix / Refactor / Docs

 Asociado a hito H##

 Enlace a issue/ticket (si aplica)

Documentación
 README.md actualizado (si es módulo/carpeta)

 ROADMAP.md actualizado (micro-hitos completados)

 CHANGELOG.md local actualizado (con fecha y autor)

 Docstrings y comentarios en código

Tests y Cobertura
 Nuevos tests unitarios (pytest)

 Tests integración si aplica

 Coverage ≥ 80% en líneas nuevas

 Tests e2e pasan

 No hay warnings de linting

Seguridad y Auditoría
 No hay secretos hardcodeados

 .env.example actualizado si hay nuevas variables

 No hay dependencias no auditadas

 Logs de auditoría adecuados

Compatibilidad
 Compatible con versión anterior (si es Breaking, documentar)

 Variables en .env.example explicadas

 Migraciones DB si aplica (sin datos perdidos)

Revisión final
 Código limpio y sin TODO pendientes

 Commits limpios y squashed si es necesario

 Merge ready: aprobado por ≥1 revisor técnico

text

---

## 🧪 Testing y Cobertura

### Ejecutar tests locales:

Tests unitarios
pytest src/theaia/tests/unit/ -v

Tests integración
pytest src/theaia/tests/integration/ -v

Tests e2e y FSM
pytest src/theaia/tests/e2e/ -v

Coverage global (mínimo 80%)
pytest --cov=src/theaia --cov-report=term-missing --cov-report=html

text

### Reglas de testing:

- **Mínimo 80% coverage** en módulos nuevos/modificados.
- **Todos los agentes** tienen tests unitarios + integración.
- **FSM transitions** validadas en e2e.
- **Adapters** tienen tests de webhook/payload.
- **ML models** validados con fixtures de datos.

---

## 📂 Estructura por módulo/carpeta

Cada carpeta (core, agents, adapters, ml, tests, docs) debe tener:

├── README.md # Guía del módulo
├── ROADMAP.md # Micro-hitos y estado
├── CHANGELOG.md # Cambios locales por versión
├── src/ # Código fuente
├── tests/ # Tests unitarios e integración
└── docs/ # Documentación específica (si aplica)

text

---

## 📝 Documentación

### Actualizar siempre:

1. **README.md** del módulo
   - Descripción clara
   - Dependencias
   - Ejemplo de uso
   - Link a ROADMAP y docs

2. **ROADMAP.md** del módulo
   - Micro-hitos completados/pendientes
   - Dependencias
   - Responsable y fechas

3. **CHANGELOG.md** del módulo
   - Versión y fecha
   - Qué cambió (Added, Changed, Fixed, Docs)
   - Autoría y PR/commit reference

4. **Docstrings en código**
   - Clase: describe propósito, parámetros, excepciones
   - Función/método: describe comportamiento y ejemplos
   - Parámetros: tipo y descripción

---

## 🔍 Code Review y Auditoría

### Criterios de aprobación:

- ✅ Tests pasan (100%)
- ✅ Coverage ≥80%
- ✅ Documentación actualizada
- ✅ Sin secretos hardcodeados
- ✅ Commits limpios y bien descritos
- ✅ Compatible con roadmap/hitos
- ✅ Aprobado por ≥1 revisor técnico

### Responsables por área:

- **core**: Álvaro Fernández Mota (CEO)
- **agents**: Equipo Agents Engineering
- **adapters**: Equipo Adapters Engineering
- **ml**: Equipo ML Engineering
- **tests**: Equipo QA & Auditoría
- **docs**: Equipo Docs & Onboarding

---

## 🚀 Release y Deploy

### Antes de liberar a `main`:

1. Todos los tests pasan (100%)
2. Coverage ≥85%
3. CHANGELOG.md raíz actualizado
4. ROADMAP.md raíz actualizado
5. Versión en código bumpeada (semver)
6. Auditoría técnica aprobada
7. Documentación extendida en docs/ actualizada

### Versioning (Semantic Versioning):

- **Mayor (2.x.x)**: Cambios breaking, nueva arquitectura
- **Menor (x.1.x)**: Features nuevas, hitos grandes
- **Patch (x.x.1)**: Bugfixes, mejoras pequeñas

---

## 📋 Checklist de onboarding para nuevos colaboradores

- [ ] Fork del repositorio
- [ ] Clonado en local
- [ ] `.env` configurado (copia `.env.example`)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Tests locales pasan (`pytest`)
- [ ] Rama `develop` actualizada
- [ ] README.md y CONTRIBUTING.md leídos
- [ ] Asignado a un hito H##
- [ ] Primera PR lista con checklist completo

---

## 🆘 Problemas y soporte

- **Dudas técnicas:** Consulta README y ROADMAP de tu módulo
- **Bugs:** Abre issue con label `bug` + hito asociado
- **Features:** Abre issue con label `feature` + hito asociado
- **Auditoría:** Contacta a equipo QA & Auditoría

---

## 📧 Contacto y liderazgo

- **CEO / Líder THEA IA:** Álvaro Fernández Mota (alvarofernandezmota@gmail.com)
- **Equipo Core:** thea-core@theaia.com
- **Equipo Agents:** thea-agents@theaia.com
- **Equipo QA & Auditoría:** thea-qa@theaia.com

---

**Gracias por contribuir a THEA IA.  
Juntos, estamos orquestando el futuro de la IA modular, auditable y escalable.**

> Última actualización: 2025-10-31 · Álvaro Fernández Mota (CEO THEA IA)