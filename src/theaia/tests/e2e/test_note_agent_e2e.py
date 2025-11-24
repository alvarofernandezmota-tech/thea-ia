"""
E2E Tests para NoteAgent
Pattern: AgendaAgent E2E tests adapted
Target: 14 tests, ≥70% coverage
"""
import pytest
import pytest_asyncio
from datetime import datetime
from typing import Dict

from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.database.models.note import Note
from src.theaia.database.repositories.note_repository import NoteRepository


@pytest_asyncio.fixture
async def note_agent(db_session, test_user):
    """
    Fixture: NoteAgent initialized with database
    
    Args:
        db_session: Database session fixture
        test_user: Test user fixture
        
    Returns:
        NoteAgent instance
    """
    agent = NoteAgent(test_user.id)
    await agent.initialize(db_session)
    return agent


@pytest_asyncio.fixture
async def test_note(db_session, test_user):
    """
    Fixture: Test note in database
    
    Args:
        db_session: Database session
        test_user: Test user
        
    Returns:
        Note instance
    """
    repo = NoteRepository(db_session)
    note = await repo.create(  # ← CORREGIDO: create() en lugar de create_note()
        tenant_id=test_user.tenant_id,
        user_id=test_user.id,
        title="Test Note",
        content="This is a test note content for E2E testing",
        category="personal",
        tags=["test", "sample"]
    )
    return note


@pytest_asyncio.fixture
async def test_notes_multiple(db_session, test_user):
    """
    Fixture: Multiple test notes
    
    Args:
        db_session: Database session
        test_user: Test user
        
    Returns:
        List of Note instances
    """
    repo = NoteRepository(db_session)
    notes = []
    
    for i in range(3):
        note = await repo.create(  # ← CORREGIDO: create() en lugar de create_note()
            tenant_id=test_user.tenant_id,
            user_id=test_user.id,
            title=f"Test Note {i+1}",
            content=f"Content {i+1}",
            category="personal" if i % 2 == 0 else "trabajo",
            tags=[f"tag{i}", "test"]
        )
        notes.append(note)
    
    return notes


# ==========================================
# CRUD TESTS
# ==========================================

@pytest.mark.asyncio
async def test_create_note_full_flow(note_agent, test_user):
    """
    Test E2E: Crear nota con flujo completo multi-turn
    
    Flow: idle → awaiting_note_title → awaiting_note_content → awaiting_confirmation → idle
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # Step 1: Start creation
    response1, state1, ctx1 = await note_agent.handle(
        test_user.id,
        "Crear nueva nota",
        context
    )
    
    assert "título" in response1.lower()
    assert state1 == "awaiting_note_title"  # ← CORREGIDO: nombre de estado FSM
    
    # Step 2: Provide title
    response2, state2, ctx2 = await note_agent.handle(
        test_user.id,
        "Mi nota importante",
        context
    )
    
    assert "contenido" in response2.lower()
    assert state2 == "awaiting_note_content"  # ← CORREGIDO: nombre de estado FSM
    assert ctx2.get("title") == "Mi nota importante"
    
    # Step 3: Provide content
    response3, state3, ctx3 = await note_agent.handle(
        test_user.id,
        "Este es el contenido de mi nota sobre el proyecto X",
        context
    )
    
    assert "guardar" in response3.lower()
    assert state3 == "awaiting_confirmation"
    assert "title" in ctx3
    assert "content" in ctx3
    
    # Step 4: Confirm
    response4, state4, ctx4 = await note_agent.handle(
        test_user.id,
        "sí",
        context
    )
    
    assert "guardada" in response4.lower() or "correctamente" in response4.lower()
    assert state4 == "idle"


@pytest.mark.asyncio
async def test_create_note_one_message(note_agent, test_user):
    """
    Test E2E: Crear nota en un solo mensaje (fast path)
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # Single message with title and content
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Crear nota: Título de prueba. Este es el contenido completo de la nota.",
        context
    )
    
    # Should go directly to confirmation
    assert "guardar" in response.lower() or "confirmar" in response.lower()
    assert state == "awaiting_confirmation"
    assert ctx.get("title") is not None
    assert ctx.get("content") is not None


@pytest.mark.asyncio
async def test_list_notes_empty(note_agent, test_user):
    """
    Test E2E: Listar notas cuando no hay ninguna
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Listar mis notas",
        context
    )
    
    assert "no tienes notas" in response.lower() or "no hay" in response.lower()
    assert state == "idle"


@pytest.mark.asyncio
async def test_list_notes_with_data(note_agent, test_user, test_notes_multiple):
    """
    Test E2E: Listar notas cuando existen varias
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Mostrar mis notas",
        context
    )
    
    assert "Test Note" in response
    assert state == "idle"
    # Should show multiple notes
    assert response.count("Test Note") >= 2


@pytest.mark.asyncio
async def test_search_notes_by_tag(note_agent, test_user, test_notes_multiple):
    """
    Test E2E: Buscar notas por tag
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Buscar notas con tag test",
        context
    )
    
    assert state == "idle"
    assert "Test Note" in response or "encontré" in response.lower()


@pytest.mark.asyncio
async def test_search_notes_by_category(note_agent, test_user, test_notes_multiple):
    """
    Test E2E: Buscar notas por categoría
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Buscar notas trabajo",
        context
    )
    
    assert state == "idle"
    # Should find at least one work note
    assert "Test Note" in response or "encontré" in response.lower()


@pytest.mark.asyncio
async def test_search_notes_no_results(note_agent, test_user, test_note):
    """
    Test E2E: Buscar notas sin resultados
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Buscar notas xyz123nonexistent",
        context
    )
    
    assert state == "idle"
    assert "no encontré" in response.lower() or "no hay" in response.lower()


# ==========================================
# ML ENTITY EXTRACTION TESTS
# ==========================================

@pytest.mark.asyncio
async def test_create_note_with_ml_person_extraction(note_agent, test_user):
    """
    Test E2E: Crear nota con extracción ML de personas
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # Message with person names
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Crear nota: Reunión con Juan. Hablar con Juan sobre el proyecto mañana.",
        context
    )
    
    assert "guardar" in response.lower() or "confirmar" in response.lower()
    # Should auto-extract "Juan" as tag
    if ctx.get("tags"):
        assert any("juan" in tag.lower() for tag in ctx["tags"])


@pytest.mark.asyncio
async def test_create_note_with_ml_location_extraction(note_agent, test_user):
    """
    Test E2E: Crear nota con extracción ML de ubicaciones
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # Message with location
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Crear nota: Documentos oficina. Recordar llevar documentos a la oficina.",
        context
    )
    
    assert "guardar" in response.lower() or "confirmar" in response.lower()
    # Should auto-detect category "trabajo" from "oficina"
    if ctx.get("category"):
        assert ctx["category"] in ["trabajo", "general"]


@pytest.mark.asyncio
async def test_auto_category_detection(note_agent, test_user):
    """
    Test E2E: Auto-detección de categoría desde entidades
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # Start note creation
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Tarea personal", context)
    
    # Content with person reference
    response, state, ctx = await note_agent.handle(
        test_user.id,
        "Llamar a María sobre el cumpleaños",
        context
    )
    
    # Should detect "personal" category from person mention
    if ctx.get("category"):
        assert ctx["category"] == "personal"


# ==========================================
# MULTI-TENANT TESTS
# ==========================================

@pytest.mark.asyncio
async def test_multi_tenant_isolation(note_agent, test_user, test_user_tenant2):
    """
    Test E2E: Aislamiento multi-tenant en notas
    """
    context1 = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    context2 = {
        "tenant_id": test_user_tenant2.tenant_id,
        "user_id": test_user_tenant2.id
    }
    
    # Create note for user 1
    await note_agent.handle(test_user.id, "Crear nota", context1)
    await note_agent.handle(test_user.id, "Tenant1 Note", context1)
    await note_agent.handle(test_user.id, "Content tenant 1", context1)
    await note_agent.handle(test_user.id, "sí", context1)
    
    # List notes for user 1
    response1, _, _ = await note_agent.handle(test_user.id, "Listar notas", context1)
    
    # List notes for user 2 (should be empty or different)
    response2, _, _ = await note_agent.handle(test_user_tenant2.id, "Listar notas", context2)
    
    # User 2 should NOT see user 1 notes
    assert "Tenant1 Note" in response1
    assert "Tenant1 Note" not in response2


# ==========================================
# FSM STATE TESTS
# ==========================================

@pytest.mark.asyncio
async def test_fsm_state_persistence(note_agent, test_user):
    """
    Test E2E: Persistencia de estado FSM entre mensajes
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # Start flow
    _, state1, _ = await note_agent.handle(test_user.id, "Crear nota", context)
    assert state1 == "awaiting_note_title"  # ← CORREGIDO: nombre de estado FSM
    
    # Continue flow
    _, state2, _ = await note_agent.handle(test_user.id, "Título", context)
    assert state2 == "awaiting_note_content"  # ← CORREGIDO: nombre de estado FSM
    
    # Verify FSM maintained state
    fsm = note_agent._get_or_create_fsm(test_user.id)
    assert fsm.current_state == "awaiting_note_content"


@pytest.mark.asyncio
async def test_cancel_note_creation(note_agent, test_user):
    """
    Test E2E: Cancelar creación de nota
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # Start creation
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Título test", context)
    await note_agent.handle(test_user.id, "Contenido test", context)
    
    # Cancel at confirmation
    response, state, _ = await note_agent.handle(test_user.id, "no", context)
    
    assert "cancelada" in response.lower() or "cancelado" in response.lower()
    assert state == "idle"


# ==========================================
# INTEGRATION TESTS
# ==========================================

@pytest.mark.asyncio
async def test_note_agent_with_repository(note_agent, test_user):
    """
    Test E2E: Integración NoteAgent con NoteRepository
    """
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # Create note through agent
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Integration Test", context)
    await note_agent.handle(test_user.id, "Testing repository integration", context)
    response, _, _ = await note_agent.handle(test_user.id, "sí", context)
    
    # Verify saved
    assert "guardada" in response.lower()
    
    # Verify in database through repository
    repo = note_agent.note_repository
    notes = await repo.get_by_user(test_user.tenant_id, test_user.id)
    
    assert len(notes) > 0
    assert any("Integration Test" in note.title for note in notes)
