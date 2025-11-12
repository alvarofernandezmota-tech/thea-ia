Roadmap - src/tests/
Módulo: Testing Suite
Versión actual: 0.1.0 (H01 - Planificación)
Próxima versión: 0.7.0 (H07 - Suite Completa)

📊 Estado Actual (11 Nov 2025 - H01)
Completado ✅
Estrategia testing definida (pirámide 70/20/10)

Estructura organizada (unit/integration/e2e)

Fixtures planificados

Coverage targets establecidos

Documentación completa

Pendiente ⏳
Implementación tests (H02, H07)

CI/CD integration

Coverage >85%

🎯 H02 (12-16 Nov): Unit Tests Base
Objetivo: Tests unitarios para MVP

Día 1 (12 Nov):
Setup:

pytest.ini configurado

conftest.py con fixtures base

fixtures/ con database, user, telegram

Tests Críticos:

test_config/ (settings, logging)

test_database/test_connection.py

test_database/test_models/test_user.py

test_database/test_models/test_reminder.py

Criterio Done Día 1:
✅ pytest funciona
✅ DB fixtures funcionan
✅ Tests config + user/reminder models pasan

Día 2 (13 Nov):
Tests Database:

test_database/test_repositories/test_user_repository.py

test_database/test_repositories/test_reminder_repository.py

test_models/test_user_schemas.py

test_models/test_reminder_schemas.py

Tests Utils:

test_utils/test_datetime_utils.py (crítico para reminders)

test_utils/test_text_utils.py

Criterio Done Día 2:
✅ Repositories CRUD testados
✅ Pydantic schemas validados
✅ Utils datetime funciona
✅ Coverage >80% database + models + utils

Día 3 (14 Nov):
Tests Agents:

test_agents/test_reminder_agent.py

test_agents/test_note_agent.py

test_agents/test_event_agent.py

Tests Adapters:

test_adapters/test_telegram_adapter.py

Tests Core:

test_core/test_thea_manager.py

Resto Models + Database:

test_models/test_note_schemas.py

test_models/test_event_schemas.py

test_database/test_models/test_note.py

test_database/test_models/test_event.py

test_database/test_repositories/ (resto)

Criterio Done Día 3:
✅ Agents principales testeados
✅ TelegramAdapter funciona
✅ CoreManager routing OK
✅ Coverage >85% en unit tests

Criterios Done H02:
✅ pytest configurado

✅ Fixtures base funcionan

✅ Unit tests críticos implementados:

config/ >95%

database/ >90%

models/ >95%

adapters/ >85%

agents/ >85%

core/ >80%

utils/ >95%

✅ Coverage total unit >90%

✅ CI básico ejecuta tests

🔗 H07 (27 Nov - 01 Dic): Integration + E2E
Objetivo: Tests integración y end-to-end completos

Día 1 (27 Nov):
Integration Tests:

test_telegram_flow.py (Telegram → Adapter → Agent → DB)

test_database_flow.py (Repository → Model → DB persist)

test_agent_flow.py (Agent → Repository CRUD completo)

Criterio Done:
✅ Flujos integración funcionan
✅ Coverage integration >80%

Día 2 (28 Nov):
More Integration:

test_adapter_agent.py (Adapter ↔ Agent communication)

test_core_agents.py (CoreManager → múltiples Agents)

E2E Setup:

e2e/conftest.py con fixtures

Mock Telegram client completo

Criterio Done:
✅ Integration completos
✅ E2E setup listo

Día 3-4 (29-30 Nov):
E2E Tests:

test_user_journey/test_new_user_onboarding.py

test_user_journey/test_reminder_lifecycle.py

test_user_journey/test_note_lifecycle.py

test_user_journey/test_multi_agent_flow.py

test_telegram_bot_complete.py

Criterio Done:
✅ E2E críticos pasan
✅ Coverage e2e >70%

Día 5 (01 Dic):
Refinamiento:

Fix flaky tests

Optimize slow tests

Documentation

Criterio Done Día 5:
✅ Todos los tests pasan
✅ No flaky tests
✅ Coverage total >85%
✅ CI/CD completo

Criterios Done H07:
✅ Integration tests completos (>80% coverage)

✅ E2E tests críticos (>70% coverage)

✅ Coverage total proyecto >85%

✅ CI/CD ejecuta suite completa

✅ Tests estables (no flaky)

✅ Performance aceptable (<5 min suite completa)

🔮 H09+ (Ene 2026): Advanced Testing
Test Automation:
Auto-generate tests de Pydantic schemas

Mutation testing (pytest-mutmut)

Property-based testing (hypothesis)

Performance Testing:
Load tests (locust)

Stress tests

Benchmark tests

Security Testing:
SQL injection tests

XSS tests (si web)

Authentication tests

📈 Métricas de Éxito
Hito	Unit Coverage	Integration	E2E	Total	Tiempo Ejecución
H02	>90%	-	-	>85%	<2 min
H07	>90%	>80%	>70%	>85%	<5 min
H09	>95%	>85%	>75%	>90%	<5 min
🚧 Riesgos y Mitigaciones
Riesgo 1: Flaky tests
Mitigación:

Fixtures deterministas (fixed datetimes)

Mock external services

Retry logic en E2E

Test isolation

Riesgo 2: Slow tests
Mitigación:

Parallel execution (pytest-xdist)

DB fixtures rápidos (transaction rollback)

Mock cuando posible

Skip slow tests en CI fast

Riesgo 3: Low coverage
Mitigación:

Coverage gate en CI (fail si <85%)

Review coverage en PRs

Priorizar módulos críticos

📝 Decisiones Técnicas
¿Por qué pytest vs unittest?
Razón: Fixtures, plugins, async support, better DX

¿Por qué 70/20/10 pirámide?
Razón: Balance velocidad/cobertura. Unit tests rápidos, E2E costosos.

¿Por qué >85% coverage total?
Razón: Balance pragmático. 100% no realista, <80% insuficiente.

Última actualización: 11 Nov 2025
Próxima revisión: H02 complete (16 Nov), H07 complete (01 Dic)
Responsable: Álvaro Fernández Mota