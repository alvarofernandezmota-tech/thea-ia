📊 Coverage Report & Analysis — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: QA / DevOps Team
Estado: ✅ Activo

📋 Propósito
Guía para medir, analizar y mejorar la cobertura de tests en THEA IA. Incluye métricas globales, por módulo, herramientas, reportes y targets.

Audiencia:

Desarrolladores verificando cobertura local

QA monitoreando métricas globales

DevOps generando reportes automáticos

Auditores validando estándares

📊 Qué es la cobertura
Cobertura de tests = % de líneas de código ejecutadas durante tests

Fórmula
text
Cobertura = (Líneas ejecutadas / Líneas totales) × 100%
Tipos de cobertura
Tipo	Definición	Valor
Line	% de líneas ejecutadas	Principal
Branch	% de ramas IF/ELSE ejecutadas	Importante
Function	% de funciones ejecutadas	Secundario
Statement	% de statements ejecutados	Similar a Line
🎯 Targets THEA IA
Cobertura global por tipo de test
Tipo	Target	Actual	Status
Unit	90%	🟡 85%	Mejorando
Integration	80%	🟡 75%	Mejorando
E2E	70%	🟡 60%	En progreso
Global	85%	🟡 78%	Meta: S36
Cobertura por módulo
Módulo	Target	Actual	Prioridad
core/fsm	95%	🟡 92%	🔴 Alta
core/managers	90%	🟡 88%	🔴 Alta
agents/agenda	85%	🟡 80%	🟡 Media
agents/note	85%	🟡 78%	🟡 Media
agents/query	85%	🟡 75%	🟡 Media
adapters/telegram	80%	🟡 70%	🟠 Baja
adapters/rest	80%	⏳ 65%	🟠 Baja
🛠️ Herramientas y setup
pytest-cov
bash
pip install pytest-cov
Archivo de configuración: pyproject.toml o .coveragerc
text
[coverage:run]
branch = True
source = src/theaia
omit =
    */tests/*
    */migrations/*
    */__pycache__/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
🚀 Comandos de medición
Cobertura total
bash
pytest src/theaia/tests/ --cov=src/theaia --cov-report=term-missing
Cobertura con reporte HTML
bash
pytest src/theaia/tests/ --cov=src/theaia --cov-report=html
# Abre htmlcov/index.html en navegador
Cobertura de módulo específico
bash
pytest src/theaia/tests/unit/ --cov=src/theaia.core.fsm --cov-report=term-missing
Cobertura con branches
bash
pytest src/theaia/tests/ --cov=src/theaia --cov-branch --cov-report=term-missing
Cobertura por tipo de test
bash
# Unit solamente
pytest src/theaia/tests/unit/ --cov=src/theaia --cov-report=term-missing

# Integration solamente
pytest src/theaia/tests/integration/ --cov=src/theaia --cov-report=term-missing

# E2E solamente
pytest src/theaia/tests/e2e/ --cov=src/theaia --cov-report=term-missing
📈 Interpretar reportes
Reporte terminal
text
Name                                Stmts   Miss  Cover
─────────────────────────────────────────────────────
src/theaia/__init__.py                  2      0   100%
src/theaia/core/fsm.py               245     19    92%
src/theaia/core/managers.py           156     19    88%
src/theaia/agents/agenda.py           123     26    79%
src/theaia/adapters/telegram.py       189     58    69%
─────────────────────────────────────────────────────
TOTAL                               1245    147    78%
Columnas:

Stmts: Líneas totales de código

Miss: Líneas no ejecutadas

Cover: % de cobertura

Reporte HTML (más detallado)
Abre htmlcov/index.html:

Código fuente con líneas testeadas (verde) y no testeadas (rojo)

Estadísticas por archivo

Navegación interactiva

🎯 Cómo mejorar cobertura
Paso 1: Identificar gaps
bash
pytest src/theaia/tests/ --cov=src/theaia --cov-report=term-missing

# Output muestra líneas no cubiertas
src/theaia/core/fsm.py:145  # Línea 145 sin cobertura
Paso 2: Escribir tests para esas líneas
python
# Si línea 145 en fsm.py no está cubierta:
def test_fsm_transition_error_case():
    """Cubre línea 145: manejo de error en transición"""
    fsm = FSMEngine()
    with pytest.raises(ValueError):
        fsm.transition('invalid_state')  # Esto ejecuta línea 145
Paso 3: Validar aumento
bash
pytest src/theaia/tests/ --cov=src/theaia --cov-report=term-missing
# Verificar que línea 145 ahora tiene ✓
Estrategia por módulo
Módulo	Status	Acción
fsm (92%)	Bueno	Mejorar ramas complejas
managers (88%)	Bueno	Cubrir edge cases
agents (75-80%)	Regular	Agregar tests integration
adapters (65-70%)	Bajo	Aumentar unit + mocks
🚨 Líneas que OK NO cubrir
python
# OK: No cubrir (pragma: no cover)
if __name__ == "__main__":  # pragma: no cover
    main()

# OK: No cubrir (lógica defensiva casi imposible)
except Exception as e:  # pragma: no cover
    log_critical_error(e)

# NO OK: Cubrir (lógica de negocio)
def create_event(title):
    if not title:  # ❌ DEBE ESTAR CUBIERTO
        raise ValueError("Title required")
    return Event(title)
📊 Métricas y reporting
Badge de cobertura (para README)
text
![Coverage](https://img.shields.io/badge/coverage-78%25-yellow)
Generador de badge automático
bash
# Opción 1: Coverage.py
coverage xml
# Sube coverage.xml a codecov.io

# Opción 2: GitHub Actions (ver ci_cd.md)
# Automático en cada PR
Comparación período a período
bash
# Guardar reporte actual
pytest --cov=src/theaia --cov-report=json coverage.json

# Comparar
coverage report --data-file=coverage.json --show-missing
🔄 Integración CI/CD
La cobertura se calcula automáticamente en cada PR:

Tests se ejecutan

pytest-cov genera reporte

Badge se actualiza

Reporte se comenta en PR

PR se rechaza si cobertura baja (threshold)

Ver ci_cd.md para configuración.

✅ Checklist para mantener cobertura
 Cobertura global >= 85% antes de merge

 Módulos críticos >= 90% (core/fsm, core/managers)

 Módulos agents >= 80%

 Módulos adapters >= 75%

 Cada PR incluye tests para nuevo código

 Reporte de cobertura generado en CI/CD

 Badge actualizado en README

 Líneas edge case explicadas (pragma: no cover)

 No hay degradación en PR

 Métricas registradas en CHANGELOG

📝 Ejemplo: Mejora de cobertura
Situación inicial
text
src/theaia/agents/agenda.py: 79% (líneas 45, 123, 189 sin cubrir)
Acción
python
# Test para cubrir línea 45 (error handling)
def test_agenda_create_event_invalid_date():
    agent = AgendaAgent()
    with pytest.raises(ValueError):
        agent.create_event('Reunión', 'invalid_date')  # Cubre línea 45

# Test para cubrir línea 123 (edge case)
def test_agenda_create_event_with_timezone():
    agent = AgendaAgent()
    result = agent.create_event('Reunión', '2025-11-08 10:00 UTC')
    assert result.timezone == 'UTC'  # Cubre línea 123
Resultado
text
src/theaia/agents/agenda.py: 88% (líneas 45, 123 cubiertas ✓)
🔗 Referencias y enlaces
Testing Overview — Estrategia general

Unit Tests — Tests unitarios

Integration Tests — Tests integración

E2E Tests — Tests end-to-end

CI/CD Pipeline — Reportes automáticos

Audit Checklist — Validación de calidad

📌 Meta-información
Campo	Valor
Archivo	docs/testing/coverage_report.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	QA / DevOps Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 35.1.2 (docs/testing/)

Sigue estándar THEA IA: Modular, auditable, escalable

Targets validados en cada release

Cambios reflejados en CHANGELOG

Validado en sesión 35

Nota: Métricas se actualizan mensualmente. Contactar QA lead para reportes detallados.

8/10/25 a las 16.40 
