NoteAgent
Sistema de gestión de notas inteligente con ML integration, multi-tenant support y conversaciones multi-turn.

📋 Tabla de Contenidos
Características

Arquitectura

Uso

Testing

API Reference

Configuración

✨ Características
Core Features
✅ CRUD Completo - Create, Read, Update, Delete de notas

✅ Búsqueda Avanzada - Por contenido, tags, categoría

✅ Filtros Temporales - Por día, semana, mes

✅ Pin/Unpin - Destacar notas importantes

✅ Auto-categorización - Detección automática de categorías basada en ML

✅ Auto-tagging - Extracción automática de tags relevantes

ML Integration
✅ Person Name Extraction - Detecta nombres de personas

✅ Location Extraction - Identifica ubicaciones

✅ Smart Categorization - Categorías basadas en entities

personal - Detecta personas y ubicaciones personales (casa, familia)

trabajo - Detecta ubicaciones laborales (oficina, reunión)

general - Default para notas sin context específico

Arquitectura
✅ FSM Multi-turn - Conversaciones con estados persistentes

✅ Multi-tenant Support - Aislamiento completo por tenant

✅ Timezone-aware - Manejo correcto de datetimes UTC

✅ Repository Pattern - Abstracción de datos

🏗️ Arquitectura
text
note_agent/
├── __init__.py
├── README.md                          # Este archivo
├── handler.py                         # Handler principal (84% coverage)
├── note_conversation_manager.py       # Conversation manager (85% coverage)
├── model/
│   ├── __init__.py
│   └── note_fsm.py                   # FSM states & transitions (82% coverage)
└── tests/
    ├── e2e/
    │   └── test_note_agent_e2e.py    # 13 tests E2E
    └── unit/
        └── test_note_agent_unit.py   # 34 tests unitarios
Componentes Principales
1. NoteAgent (handler.py)
Handler principal que coordina todas las operaciones.

Métodos públicos:

handle(user_id, message, context) - Punto de entrada principal

reset_state(user_id) - Reinicia FSM del usuario

Métodos privados:

_determine_action() - Detecta intención del usuario

_parse_note_from_message() - Parsea título y contenido

_auto_detect_category() - Categorización automática ML

_auto_extract_tags() - Extracción automática de tags

_format_note_confirmation() - Formatea confirmación

2. NoteFSM (note_fsm.py)
Máquina de estados finitos para conversaciones multi-turn.

Estados:

idle - Estado inicial

awaiting_note_title - Esperando título de nota

awaiting_note_content - Esperando contenido

awaiting_confirmation - Esperando confirmación

awaiting_edit_field - Esperando campo a editar

awaiting_edit_value - Esperando nuevo valor

awaiting_deletion_confirmation - Esperando confirmación de eliminación

3. NoteConversationManager
Gestiona contexto y estado de conversaciones.

💻 Uso
Ejemplo Básico
python
from src.theaia.agents.note_agent.handler import NoteAgent

# Crear instancia
agent = NoteAgent(user_id="user_123")

# Contexto
context = {
    "tenant_id": "tenant_001",
    "user_id": 1
}

# Crear nota (conversación multi-turn)
response1, state1, ctx1 = await agent.handle(1, "Crear nota", context)
# → "¿Cuál es el título de la nota?"

response2, state2, ctx2 = await agent.handle(1, "Reunión con Juan", context)
# → "¿Cuál es el contenido?"

response3, state3, ctx3 = await agent.handle(1, "Discutir proyecto en oficina", context)
# → "Vista previa... ¿Confirmas?"

response4, state4, ctx4 = await agent.handle(1, "sí", context)
# → "✅ Nota creada correctamente"
Búsqueda
python
# Buscar notas
response, state, ctx = await agent.handle(
    1, "buscar proyecto", context
)
# → Lista de notas que contienen "proyecto"

# Filtrar por fecha
response, state, ctx = await agent.handle(
    1, "mostrar notas de hoy", context
)
# → Notas creadas hoy
Pin/Unpin
python
response, state, ctx = await agent.handle(
    1, "fijar nota 5", context
)
# → "📌 Nota fijada correctamente"
Editar
python
# Iniciar edición
response1, _, _ = await agent.handle(1, "editar nota 3", context)
# → "¿Qué campo quieres editar?"

response2, _, _ = await agent.handle(1, "contenido", context)
# → "¿Cuál es el nuevo contenido?"

response3, _, _ = await agent.handle(1, "Nuevo contenido actualizado", context)
# → "✅ Nota actualizada"
🧪 Testing
Cobertura
Componente	Coverage	Status
handler.py	84%	✅ Excelente
note_fsm.py	82%	✅ Muy bueno
note_conversation_manager.py	85%	✅ Excelente
note_repository.py	85%	✅ Excelente
Tests E2E (13 tests)
bash
pytest src/theaia/tests/e2e/test_note_agent_e2e.py -v
Cobertura:

✅ test_create_note_full_flow - Flujo completo de creación

✅ test_list_notes_with_data - Listado de notas

✅ test_search_notes - Búsqueda

✅ test_edit_note_flow - Edición

✅ test_delete_note_flow - Eliminación

✅ test_pin_note_toggle - Pin/Unpin

✅ test_get_note_specific - Obtener nota por ID

✅ test_list_pinned_notes - Listar fijadas

✅ test_filter_notes_by_date_today - Filtro por día

✅ test_filter_notes_by_date_week - Filtro por semana

✅ test_fsm_state_persistence - Persistencia de estado

✅ test_multi_tenant_isolation - Aislamiento multi-tenant

✅ test_note_agent_full_integration - Integración completa

Tests Unitarios (34 tests)
bash
pytest src/theaia/tests/unit/test_note_agent_unit.py -v
Cobertura:

✅ Métodos privados (_parse_note_from_message, _auto_detect_category, etc.)

✅ Error handling (excepciones DB, notas no encontradas)

✅ Edge cases (mensajes vacíos, IDs inválidos)

✅ FSM estados (transiciones, resets, contexto)

✅ Multi-tenant isolation

✅ Multi-turn conversations

✅ Timezone-aware datetimes

Ejecutar Todos los Tests
bash
# Tests completos con coverage
pytest src/theaia/tests/e2e/test_note_agent_e2e.py \
       src/theaia/tests/unit/test_note_agent_unit.py \
       --cov=src/theaia/agents/note_agent \
       --cov-report=term-missing -v

# Resultado: 47/47 tests pasando, 84% coverage
📚 API Reference
NoteAgent.handle()
python
async def handle(
    self,
    user_id: int,
    message: str,
    context: dict
) -> tuple[str, str, dict]:
    """
    Procesa mensaje del usuario y retorna respuesta.
    
    Args:
        user_id: ID del usuario
        message: Mensaje/comando del usuario
        context: Contexto con tenant_id, user_id, etc.
    
    Returns:
        tuple: (response_message, current_state, updated_context)
    
    Examples:
        >>> response, state, ctx = await agent.handle(
        ...     1, "crear nota", {"tenant_id": "t1", "user_id": 1}
        ... )
        >>> print(state)
        'awaiting_note_title'
    """
Acciones Soportadas
Acción	Keywords	Ejemplo
Crear	crear, nueva, agregar nota	"crear nota", "nueva nota"
Listar	listar, mostrar, ver notas	"listar notas", "ver todas"
Buscar	buscar, encontrar	"buscar proyecto"
Editar	editar, modificar, actualizar	"editar nota 5"
Eliminar	borrar, eliminar, quitar	"borrar nota 3"
Obtener	obtener, ver nota [ID]	"ver nota 2"
Pin	fijar, destacar	"fijar nota 4"
Unpin	desfijar	"desfijar nota 4"
Filtrar	notas de hoy/semana/mes	"notas de hoy"
⚙️ Configuración
Variables de Entorno
bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db

# Multi-tenant
TENANT_ID=tenant_001

# ML Models (opcional)
ML_ENTITY_MODEL_PATH=models/entity_extractor
Dependencias
python
# requirements.txt
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.27.0
spacy>=3.5.0
python-dateutil>=2.8.0
🔧 Desarrollo
Añadir Nueva Acción
Agregar keywords en _determine_action():

python
if any(kw in message_lower for kw in ['nueva_accion', 'otro_keyword']):
    return 'nueva_accion'
Implementar handler en handle():

python
elif action == 'nueva_accion':
    return await self._handle_nueva_accion(user_id, message, context)
Crear método privado:

python
async def _handle_nueva_accion(self, user_id, message, context):
    # Implementación
    pass
Agregar tests:

python
@pytest.mark.asyncio
async def test_nueva_accion(note_agent, test_context):
    response, state, ctx = await note_agent.handle(
        1, "trigger nueva_accion", test_context
    )
    assert "expected" in response
Añadir Estado FSM
Definir estado en note_fsm.py:

python
def transition_to_nuevo_estado(self):
    self.current_state = "nuevo_estado"
Actualizar handler para gestionar estado:

python
if current_state == "nuevo_estado":
    # Lógica específica
    pass
📊 Métricas
Performance
Average response time: ~50-100ms (sin ML)

With ML extraction: ~150-300ms

Database queries: 1-3 por operación

Escalabilidad
✅ Soporta múltiples usuarios concurrentes (FSM por usuario)

✅ Multi-tenant sin overhead adicional

✅ Stateless handler (estado en FSM)

🐛 Troubleshooting
Problema: Estado FSM no persiste
Síntoma: El agente "olvida" el contexto entre mensajes.

Solución: Verificar que user_id es consistente:

python
# ❌ INCORRECTO
await agent.handle(1, "crear nota", context)
await agent.handle(2, "título", context)  # Diferente user_id!

# ✅ CORRECTO
await agent.handle(1, "crear nota", context)
await agent.handle(1, "título", context)  # Mismo user_id
Problema: Multi-tenant leaking
Síntoma: Un tenant ve notas de otro tenant.

Solución: Verificar que tenant_id está en contexto:

python
context = {
    "tenant_id": "tenant_001",  # ← REQUERIDO
    "user_id": 1
}
Problema: Timezone issues
Síntoma: Filtros de fecha no funcionan correctamente.

Solución: Asegurar que datetimes son timezone-aware:

python
from datetime import datetime, timezone

# ✅ CORRECTO
now = datetime.now(timezone.utc)

# ❌ INCORRECTO (naive datetime)
now = datetime.now()
📝 Changelog
v1.0.0 (2025-11-24)
✅ CRUD completo implementado

✅ ML integration (person/location extraction)

✅ Auto-categorización y auto-tagging

✅ Multi-tenant support

✅ FSM multi-turn conversations

✅ 47 tests (13 E2E + 34 unit)

✅ 84% code coverage

✅ Production-ready

🤝 Contribuir
Guía de Estilo
Tests obligatorios para nuevas features

Coverage mínimo: 80%

Docstrings en todos los métodos públicos

Type hints en signatures

Pull Request Process
Fork el repositorio

Crear feature branch (git checkout -b feature/nueva-feature)

Commit cambios (git commit -m 'Add nueva feature')

Push a branch (git push origin feature/nueva-feature)

Abrir Pull Request

📄 Licencia
MIT License - Ver LICENSE file para detalles.

👥 Autores
THEA_IA Team - Initial work

🙏 Agradecimientos
spaCy para NLP/ML

SQLAlchemy para ORM

pytest para testing framework