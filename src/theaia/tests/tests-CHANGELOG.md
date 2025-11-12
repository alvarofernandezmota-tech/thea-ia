Changelog - src/tests/
Cambios en la suite de tests de THEA IA.

[Unreleased]
Planificado H07 (27 Nov - 01 Dic)
Integration tests completos

E2E tests críticos

CI/CD pipeline completo

[0.7.0] - 2025-12-01 (H07 Target)
Added
Integration Tests:

test_telegram_flow.py (Telegram → DB)

test_database_flow.py (Repo → Model → DB)

test_agent_flow.py (Agent CRUD completo)

test_adapter_agent.py (Adapter ↔ Agent)

test_core_agents.py (CoreManager routing)

E2E Tests:

test_user_journey/ (onboarding, lifecycles)

test_telegram_bot_complete.py

test_reminder_lifecycle.py

test_note_lifecycle.py

test_multi_agent_flow.py

Coverage
Integration: >80%

E2E: >70%

Total: >85%

[0.2.0] - 2025-11-16 (H02 Target)
Added
Test Infrastructure:

pytest.ini configurado

conftest.py con fixtures globales

fixtures/ (database, user, telegram, datetime)

Unit Tests:

test_config/ (settings, logging, constants)

test_database/test_connection.py

test_database/test_models/ (6 models)

test_database/test_repositories/ (6 repositories)

test_models/ (Pydantic schemas - 7 módulos)

test_adapters/test_telegram_adapter.py

test_agents/ (5 agents)

test_core/test_thea_manager.py

test_utils/ (datetime, text, validators, formatters)

Coverage
Unit: >90%

Total: >85%

CI/CD
GitHub Actions ejecuta tests automáticamente

Coverage report en CI

Fail si coverage <85%

[0.1.0] - 2025-11-03 (H01)
Added
Estructura inicial tests/

Documentación:

README.md

ROADMAP.md

CHANGELOG.md

STRUCTURE.md

DEPENDENCIES.md

TESTING_GUIDE.md

Estrategia testing (70/20/10 pirámide)

Test Markers
v0.2.0:
@pytest.mark.unit

@pytest.mark.database

@pytest.mark.slow

v0.7.0:
@pytest.mark.integration

@pytest.mark.e2e

@pytest.mark.telegram

Última actualización: 11 Nov 2025