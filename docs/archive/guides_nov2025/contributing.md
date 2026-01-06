🤝 Contributing — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 19:19 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

👋 ¡Gracias por Contribuir!
THEA IA es un proyecto open source y aceptamos contribuciones de toda la comunidad.

🚀 Guía Rápida
1. Fork & Clone
bash
# Fork en GitHub: https://github.com/thea-ia/thea-ia/fork

# Clone tu fork
git clone https://github.com/YOUR-USERNAME/thea-ia.git
cd thea-ia

# Añade upstream
git remote add upstream https://github.com/thea-ia/thea-ia.git
2. Crea Rama
bash
# Sync con upstream
git fetch upstream
git checkout -b feature/mi-feature upstream/main

# o para bugfix
git checkout -b bugfix/issue-123 upstream/main
3. Realiza Cambios
bash
# Edita archivos
# Instala dev dependencies
pip install -r requirements-dev.txt

# Ejecuta tests
pytest tests/ -v

# Verifica linting
black src/
flake8 src/
mypy src/
4. Commit & Push
bash
# Sigue convención de commits
git commit -m "feat: Add new agent for support tickets"
# o
git commit -m "fix: Resolve FSM state timeout issue"

# Push a tu fork
git push origin feature/mi-feature
5. Pull Request
Abre PR en https://github.com/thea-ia/thea-ia/pulls

Describe cambios claramente

Linkea issues relacionados: Closes #123

Espera revisión de maintainers

📋 Tipos de Contribución
🐛 Reportar Bugs
text
**Descripción:**
[Describe el bug]

**Pasos para reproducir:**
1. ...
2. ...

**Comportamiento esperado:**
[¿Qué debería pasar?]

**Logs/Stack trace:**
[Pega error]

**Entorno:**
- OS: [Windows/Linux/macOS]
- Python: 3.10.x
- Docker: [sí/no]
→ Abre issue: https://github.com/thea-ia/thea-ia/issues/new

✨ Sugerir Features
text
**Descripción:**
[¿Qué quieres agregar?]

**Caso de uso:**
[¿Por qué es útil?]

**Alternativas consideradas:**
[¿Hay otras formas?]
→ Abre issue con label enhancement

📚 Mejorar Documentación
Typos/claridad

Ejemplos faltantes

Traducción a otros idiomas

Mejoras en formato

→ Edit directamente y abre PR

🔧 Código
Áreas de interés:

Nuevos agentes

Adapters (WhatsApp, Slack, etc.)

ML/NLP improvements

Observabilidad

Tests & coverage

✅ Checklist antes de PR
 Tests pasan: pytest tests/ -v

 Linting: black src/ + flake8 src/

 Type hints: mypy src/

 Docstrings en funciones públicas

 README.md actualizado (si aplica)

 CHANGELOG.md entrada

 Commit message sigue convención

 Squashed commits innecesarios

 No hay conflictos con main

📝 Estilo de Código
Python
python
# Type hints
def get_intent(text: str) -> str:
    """Extract intent from text."""
    ...

# Docstrings (Google style)
def train_model(data_path: str, output_path: str) -> Model:
    """Train intent detection model.
    
    Args:
        data_path: Path to training data JSON.
        output_path: Path to save trained model.
    
    Returns:
        Trained model instance.
    
    Raises:
        FileNotFoundError: If data_path doesn't exist.
    """
    ...

# Comments
# ✓ Bueno: Explica POR QUÉ
# Reset pool cada hora para evitar stale connections
pool_recycle = 3600

# ✗ Malo: Explica QUÉ (es obvio)
# Reseteamos pool
pool_recycle = 3600
Commit Messages
text
feat: Add WhatsApp adapter support
^--- Type (feat, fix, docs, test, refactor, style)

Add WhatsApp integration through TwilioAdapter.
Supports text, media, and interactive messages.

Closes #456
Co-authored-by: Jane Doe <jane@example.com>
Tipos:

feat: Nueva feature

fix: Bugfix

docs: Documentación

test: Tests

refactor: Cambio código sin behavior

style: Formateo (sin funcionalidad)

perf: Performance

chore: Build, deps, etc.

🧪 Testing
Estructura
text
tests/
├── unit/          # Tests unitarios
├── integration/   # Tests integración
└── e2e/          # Tests end-to-end
Escribir Tests
python
import pytest
from src.theaia.agents.agenda import AgendaAgent

class TestAgendaAgent:
    @pytest.fixture
    def agent(self):
        return AgendaAgent()
    
    def test_schedule_appointment(self, agent):
        """Test scheduling appointment."""
        result = agent.handle(
            intent="schedule",
            entities={"date": "2025-11-15", "time": "10:00"},
            context={}
        )
        
        assert result["status"] == "success"
        assert "appointment_id" in result
    
    def test_invalid_date(self, agent):
        """Test error handling for invalid date."""
        with pytest.raises(ValueError):
            agent.handle(
                intent="schedule",
                entities={"date": "invalid", "time": "10:00"},
                context={}
            )
Ejecutar Tests
bash
# Todos los tests
pytest tests/

# Con coverage
pytest tests/ --cov=src/theaia --cov-report=html

# Específicos
pytest tests/unit/test_fsm.py -v
pytest tests/unit/test_fsm.py::TestFSM::test_transition -v

# Solo rápidos (skip lentos)
pytest tests/ -m "not slow"
🔄 Revisión & Merge
Flujo:

Abres PR

Maintainer revisa

Solicita cambios (si aplica)

Rebesan basado en feedback

Aprobado ✓

Merge a main

Incluido en siguiente release

SLA:

Features: revisión en 48h

Bugfixes: revisión en 24h

Docs: revisión en 72h

🎓 Recursos Útiles
Repo: https://github.com/thea-ia/thea-ia

Issues: https://github.com/thea-ia/thea-ia/issues

Discussions: https://github.com/thea-ia/thea-ia/discussions

Architecture: docs/architecture/

API Docs: http://localhost:8000/docs

📜 Código de Conducta
Por favor lee: CODE_OF_CONDUCT.md

Resumen:

Sé respetuoso

No discriminación

Bienvenidas todas las contribuciones

Reporta abuso a: conduct@thea-ia.com

📌 Meta-información
Campo	Valor
Archivo	docs/guides/contributing.md
Versión	v0.14.0
Última revisión	2025-11-09 19:19 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
¡Gracias por ayudarnos a mejorar THEA IA!

Última actualización: 2025-11-09 19:19 CET