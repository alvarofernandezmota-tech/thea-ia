Estructura - src/tests/
Detalle completo estructura testing THEA IA

📊 Overview
text
src/tests/
├── fixtures/        # Fixtures compartidos
├── unit/            # 70% - Tests aislados
├── integration/     # 20% - Tests módulos conectados
└── e2e/             # 10% - Tests flujos completos
📁 Estructura Completa
text
src/tests/
│
├── __init__.py
├── conftest.py                          # Fixtures GLOBALES
├── pytest.ini                           # Config pytest
│
├── fixtures/                            # Fixtures compartidos
│   ├── __init__.py
│   ├── database_fixtures.py             # DB sessions, engines
│   ├── user_fixtures.py                 # Test users (free/pro/business)
│   ├── telegram_fixtures.py             # Mock Telegram updates
│   ├── datetime_fixtures.py             # Fixed datetimes
│   └── agent_fixtures.py                # Mock agents
│
├── unit/                                # Tests unitarios (70%)
│   │
│   ├── __init__.py
│   ├── conftest.py                      # Fixtures unit tests
│   │
│   ├── test_config/                     # Config module
│   │   ├── __init__.py
│   │   ├── test_settings.py
│   │   ├── test_logging.py
│   │   └── test_constants.py
│   │
│   ├── test_database/                   # Database module
│   │   ├── __init__.py
│   │   ├── test_connection.py
│   │   ├── test_base.py
│   │   │
│   │   ├── test_models/                 # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── test_user.py
│   │   │   ├── test_reminder.py
│   │   │   ├── test_note.py
│   │   │   ├── test_event.py
│   │   │   ├── test_task.py
│   │   │   └── test_context.py
│   │   │
│   │   └── test_repositories/           # Repositories CRUD
│   │       ├── __init__.py
│   │       ├── test_base_repository.py
│   │       ├── test_user_repository.py
│   │       ├── test_reminder_repository.py
│   │       ├── test_note_repository.py
│   │       ├── test_event_repository.py
│   │       ├── test_task_repository.py
│   │       └── test_context_repository.py
│   │
│   ├── test_models/                     # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── test_base.py
│   │   ├── test_user_schemas.py
│   │   ├── test_reminder_schemas.py
│   │   ├── test_note_schemas.py
│   │   ├── test_event_schemas.py
│   │   ├── test_task_schemas.py
│   │   ├── test_context_schemas.py
│   │   ├── test_message_schemas.py
│   │   └── test_validators.py
│   │
│   ├── test_adapters/
│   │   ├── __init__.py
│   │   ├── test_base_adapter.py
│   │   └── test_telegram_adapter.py
│   │
│   ├── test_agents/
│   │   ├── __init__.py
│   │   ├── test_base_agent.py
│   │   ├── test_reminder_agent.py
│   │   ├── test_note_agent.py
│   │   ├── test_event_agent.py
│   │   ├── test_task_agent.py
│   │   └── test_context_agent.py
│   │
│   ├── test_core/
│   │   ├── __init__.py
│   │   └── test_thea_manager.py
│   │
│   ├── test_utils/
│   │   ├── __init__.py
│   │   ├── test_datetime_utils.py
│   │   ├── test_text_utils.py
│   │   ├── test_validators.py
│   │   ├── test_formatters.py
│   │   └── test_helpers.py
│   │
│   ├── test_ml/                         # (H06)
│   │   ├── __init__.py
│   │   ├── test_nlp_service.py
│   │   ├── test_intent_classifier.py
│   │   └── test_entity_extractor.py
│   │
│   └── test_services/                   # (H04-H05)
│       ├── __init__.py
│       ├── test_auth_service.py
│       ├── test_payment_service.py
│       └── test_notification_service.py
│
├── integration/                         # Tests integración (20%)
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_telegram_flow.py
│   ├── test_database_flow.py
│   ├── test_agent_flow.py
│   ├── test_adapter_agent.py
│   ├── test_core_agents.py
│   └── test_notification_flow.py        # (H05)
│
└── e2e/                                 # Tests E2E (10%)
    ├── __init__.py
    ├── conftest.py
    │
    ├── test_user_journey/
    │   ├── __init__.py
    │   ├── test_new_user_onboarding.py
    │   ├── test_reminder_lifecycle.py
    │   ├── test_note_lifecycle.py
    │   └── test_multi_agent_flow.py
    │
    ├── test_telegram_bot_complete.py
    └── test_subscription_flow.py         # (H05)
📊 Estadísticas
H02 (MVP):
Archivos test: ~45

Test cases: ~300

LOC tests: ~5,000

Coverage: >85%

H07 (Completo):
Archivos test: ~60

Test cases: ~500

LOC tests: ~8,000

Coverage: >85%

🎯 Organización por Hito
H02:
text
✅ fixtures/
✅ unit/ (completo excepto ml, services)
⏸️ integration/ (básico)
⏸️ e2e/ (ninguno)
H07:
text
✅ fixtures/ (todos)
✅ unit/ (completo)
✅ integration/ (completo)
✅ e2e/ (críticos)
Última actualización: 11 Nov 2025