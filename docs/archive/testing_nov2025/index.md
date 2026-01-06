🧪 Testing & Quality Assurance — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: QA Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
Esta guía centraliza toda la estrategia de testing de THEA IA: dónde están los tests, cómo ejecutarlos, qué frameworks usamos, cómo medimos cobertura y cómo se integran en el pipeline CI/CD.

Audiencia:

Desarrolladores que escriben o ejecutan tests

QA/DevOps configurando pipelines automáticos

Auditores validando cobertura y calidad

📍 Ubicación de los tests
Estrategia centralizada
Todos los tests están en src/theaia/tests/, organizados por tipo y módulo:

text
src/theaia/tests/
├── unit/                   # Tests unitarios por módulo
│   ├── test_core_fsm.py
│   ├── test_agents_agenda.py
│   ├── test_adapters_telegram.py
│   └── ...
├── integration/            # Tests de integración entre módulos
│   ├── test_fsm_agents_flow.py
│   ├── test_adapters_integration.py
│   └── ...
├── e2e/                    # Tests end-to-end (flujos completos)
│   ├── test_telegram_full_flow.py
│   ├── test_agenda_create_event.py
│   └── ...
├── fixtures/               # Fixtures compartidos
│   ├── conftest.py
│   ├── mock_data.py
│   └── ...
└── utils/                  # Utilidades y helpers de testing
    ├── test_helpers.py
    └── assertions.py
¿Por qué centralizado?
✅ Evita dispersión y duplicación

✅ Facilita la ejecución global (pytest src/theaia/tests/)

✅ Simplifica configuración de CI/CD

✅ Permite fixtures compartidos sin conflictos

Cada módulo en src/theaia/ NO tiene su propia carpeta tests/, sino que sus tests viven en src/theaia/tests/unit/ o integration/ según el tipo.

🛠️ Frameworks y herramientas
Herramienta	Uso	Comando
pytest	Runner principal de tests	pytest
pytest-cov	Reporte de cobertura	`pytest --cov=src/theaia --cov-

editado pro  alvaro el 8 de noviembre del 2025 a lass 5 dela tarde