Dependencias - src/tests/
Testing dependencies THEA IA

📦 Python Packages
Core Testing:
text
pytest==7.4.3
pytest-asyncio==0.21.1          # Async tests
pytest-cov==4.1.0               # Coverage
Mocking:
text
pytest-mock==3.12.0             # Mocking helper
Database:
text
pytest-postgresql==5.0.0        # PostgreSQL fixtures
Performance:
text
pytest-xdist==3.5.0             # Parallel execution
pytest-timeout==2.2.0           # Timeout tests
pytest-benchmark==4.0.0         # Benchmark tests
Reporting:
text
pytest-html==4.1.1              # HTML reports
🔧 Instalación
bash
pip install pytest pytest-asyncio pytest-cov pytest-mock pytest-postgresql
O desde requirements-test.txt:

bash
pip install -r requirements-test.txt
⚙️ Configuración
pytest.ini:
text
[pytest]
testpaths = src/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests
    database: Database tests
    telegram: Telegram tests

addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=85
🎯 Coverage Config
.coveragerc:
text
[run]
source = src
omit =
    */tests/*
    */migrations/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
Última actualización: 11 Nov 2025