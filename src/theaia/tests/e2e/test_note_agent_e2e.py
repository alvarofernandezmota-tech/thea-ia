"""
E2E Tests para NoteAgent v2.0 - COMPLETO
Pattern: AgendaAgent E2E tests adapted
Target: 19 tests, ≥85% coverage

Funciones testeadas:
- create_note (multi-turn)
- list_notes (listar todas)
- search_notes (buscar por contenido/tag/categoria)
- edit_note (editar contenido) ✨ NEW
- delete_note (eliminar con confirmación) ✨ NEW
- pin_note (toggle pin/unpin) ✨ NEW
- get_note (ver nota específica) ✨ NEW
- list_pinned_notes (solo fijadas) ✨ NEW
- filter_by_date (hoy/semana/mes) ✨ NEW
"""
import pytest
import pytest_asyncio
from datetime import datetime
from typing import Dict
import re

from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.database.models.note import Note
from src.theaia.database.repositories.note_repository import NoteRepository


@pytest_asyncio.fixture
async def note_agent(db_session, test_user):
    """Fixture: NoteAgent initialized with database"""
    agent = NoteAgent(test_user.id)
    await agent.initialize(db_session)
    return agent


@pytest_asyncio.fixture
async def test_note(db_session, test_user):
    """Fixture: Test note in database"""
    repo = NoteRepository(db_session)
    note = await repo.create(
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
    """Fixture: Multiple test notes"""
    repo = NoteRepository(db_session)
    notes = []
    for i in range(3):
        note = await repo.create(
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
# CRUD BÁSICO TESTS (existentes)
# ==========================================

@pytest.mark.asyncio
async def test_create_note_full_flow(note_agent, test_user):
    """Test E2E: Crear nota con flujo completo multi-turn"""
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
    assert state1 == "awaiting_note_title"
    
    # Step 2: Provide title
    response2, state2, ctx2 = await note_agent.handle(
        test_user.id,
        "Mi nota importante",
        context
    )
    assert "contenido" in response2.lower()
    assert state2 == "awaiting_note_content"
    assert ctx2.get("title") == "Mi nota importante"
    
    # Step 3: Provide content
    response3, state3, ctx3 = await note_agent.handle(
        test_user.id,
        "Este es el contenido de mi nota sobre el proyecto X",
        context
    )
    assert "guardar" in response3.lower()
    assert state3 == "awaiting_confirmation"
    
    # Step 4: Confirm
    response4, state4, ctx4 = await note_agent.handle(
        test_user.id,
        "sí",
        context
    )
    assert "guardada" in response4.lower()
    assert state4 == "idle"


@pytest.mark.asyncio
async def test_list_notes_with_data(note_agent, test_user, test_notes_multiple):
    """Test E2E: Listar notas cuando existen varias"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    response, state, _ = await note_agent.handle(
        test_user.id,
        "Mostrar mis notas",
        context
    )
    
    assert "Test Note" in response
    assert state == "idle"
    assert response.count("Test Note") >= 2


@pytest.mark.asyncio
async def test_search_notes(note_agent, test_user, test_notes_multiple):
    """Test E2E: Buscar notas por tag"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    response, state, _ = await note_agent.handle(
        test_user.id,
        "Buscar notas con tag test",
        context
    )
    
    assert state == "idle"
    assert "Test Note" in response or "encontré" in response.lower()


# ==========================================
# FUNCIONES NUEVAS TESTS ✨
# ==========================================

@pytest.mark.asyncio
async def test_edit_note_flow(note_agent, test_user):
    """Test E2E: Editar nota (nueva función)"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }

    # 1. Crea una nota
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Nota a editar", context)
    await note_agent.handle(test_user.id, "Texto original", context)
    response_save, _, _ = await note_agent.handle(test_user.id, "sí", context)

    # Obtén el ID
    match = re.search(r'ID: (\d+)', response_save)
    assert match, "No se pudo extraer ID de la nota creada"
    note_id = int(match.group(1))

    # 2. Inicia edición
    response_edit_start, state_edit, _ = await note_agent.handle(
        test_user.id, 
        f"editar nota {note_id}", 
        context
    )
    assert "Editando nota" in response_edit_start
    assert state_edit == "awaiting_edit_content"

    # 3. Envía nuevo contenido
    response_edited, state_done, _ = await note_agent.handle(
        test_user.id, 
        "Nuevo texto editado", 
        context
    )
    assert "actualizada correctamente" in response_edited
    assert state_done == "idle"

    # 4. Verifica el cambio
    response_verify, _, _ = await note_agent.handle(
        test_user.id, 
        f"ver nota {note_id}", 
        context
    )
    assert "Nuevo texto editado" in response_verify


@pytest.mark.asyncio
async def test_delete_note_flow(note_agent, test_user):
    """Test E2E: Eliminar nota con confirmación (nueva función)"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }

    # 1. Crea una nota
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Nota a eliminar", context)
    await note_agent.handle(test_user.id, "Texto que será eliminado", context)
    response_save, _, _ = await note_agent.handle(test_user.id, "sí", context)

    match = re.search(r'ID: (\d+)', response_save)
    assert match
    note_id = int(match.group(1))

    # 2. Inicia eliminación
    response_delete_start, state_confirm, _ = await note_agent.handle(
        test_user.id, 
        f"borrar nota {note_id}", 
        context
    )
    assert "¿Eliminar nota" in response_delete_start
    assert state_confirm == "awaiting_delete_confirmation"

    # 3. Confirma eliminación
    response_deleted, state_idle, _ = await note_agent.handle(
        test_user.id, 
        "sí", 
        context
    )
    assert "eliminada correctamente" in response_deleted
    assert state_idle == "idle"

    # 4. Verifica que no existe
    response_notfound, _, _ = await note_agent.handle(
        test_user.id, 
        f"ver nota {note_id}", 
        context
    )
    assert "no encontrada" in response_notfound.lower()


@pytest.mark.asyncio
async def test_pin_note_toggle(note_agent, test_user):
    """Test E2E: Fijar/desfijar nota (toggle) (nueva función)"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }

    # 1. Crea una nota
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Nota importante", context)
    await note_agent.handle(test_user.id, "Este es contenido importante", context)
    response_save, _, _ = await note_agent.handle(test_user.id, "sí", context)

    match = re.search(r'ID: (\d+)', response_save)
    assert match
    note_id = int(match.group(1))

    # 2. Fija la nota
    response_pin, state_pin, _ = await note_agent.handle(
        test_user.id, 
        f"fijar nota {note_id}", 
        context
    )
    assert "fijada" in response_pin.lower()
    assert state_pin == "idle"

    # 3. Desfija la nota (toggle)
    response_unpin, state_unpin, _ = await note_agent.handle(
        test_user.id, 
        f"fijar nota {note_id}", 
        context
    )
    assert "desfijada" in response_unpin.lower()
    assert state_unpin == "idle"


@pytest.mark.asyncio
async def test_get_note_specific(note_agent, test_user):
    """Test E2E: Ver nota específica (nueva función)"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }

    # 1. Crea una nota
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Nota test", context)
    await note_agent.handle(test_user.id, "Contenido completo de prueba", context)
    response_save, _, _ = await note_agent.handle(test_user.id, "sí", context)

    match = re.search(r'ID: (\d+)', response_save)
    assert match
    note_id = int(match.group(1))

    # 2. Obtén la nota específica
    response_get, state_get, _ = await note_agent.handle(
        test_user.id, 
        f"ver nota {note_id}", 
        context
    )
    assert "Nota test" in response_get
    assert "Contenido completo de prueba" in response_get
    assert state_get == "idle"


@pytest.mark.asyncio
async def test_list_pinned_notes(note_agent, test_user):
    """Test E2E: Listar solo notas fijadas (nueva función)"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }

    # 1. Crea 3 notas
    note_ids = []
    for i in range(3):
        await note_agent.handle(test_user.id, "Crear nota", context)
        await note_agent.handle(test_user.id, f"Nota {i+1}", context)
        await note_agent.handle(test_user.id, f"Contenido {i+1}", context)
        response_save, _, _ = await note_agent.handle(test_user.id, "sí", context)
        match = re.search(r'ID: (\d+)', response_save)
        if match:
            note_ids.append(int(match.group(1)))

    # 2. Fija solo la primera nota
    if note_ids:
        await note_agent.handle(test_user.id, f"fijar nota {note_ids[0]}", context)

    # 3. Listar solo fijadas
    response_pinned, state_pinned, _ = await note_agent.handle(
        test_user.id, 
        "mostrar notas fijadas", 
        context
    )
    assert "fijadas" in response_pinned.lower()
    assert state_pinned == "idle"


@pytest.mark.asyncio
async def test_filter_notes_by_date_today(note_agent, test_user):
    """Test E2E: Filtrar notas de hoy (nueva función)"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }

    # 1. Crea una nota (hoy)
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Nota de hoy", context)
    await note_agent.handle(test_user.id, "Creada hoy", context)
    await note_agent.handle(test_user.id, "sí", context)

    # 2. Filtra por hoy
    response_today, state_today, _ = await note_agent.handle(
        test_user.id, 
        "mostrar notas de hoy", 
        context
    )
    assert "hoy" in response_today.lower()
    assert state_today == "idle"


@pytest.mark.asyncio
async def test_filter_notes_by_date_week(note_agent, test_user):
    """Test E2E: Filtrar notas de esta semana (nueva función)"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }

    # 1. Crea una nota
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Nota semanal", context)
    await note_agent.handle(test_user.id, "De esta semana", context)
    await note_agent.handle(test_user.id, "sí", context)

    # 2. Filtra por semana
    response_week, state_week, _ = await note_agent.handle(
        test_user.id, 
        "notas de esta semana", 
        context
    )
    assert "semana" in response_week.lower()
    assert state_week == "idle"


# ==========================================
# FSM & MULTI-TENANT TESTS
# ==========================================

@pytest.mark.asyncio
async def test_fsm_state_persistence(note_agent, test_user):
    """Test E2E: Persistencia de estado FSM"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    _, state1, _ = await note_agent.handle(test_user.id, "Crear nota", context)
    assert state1 == "awaiting_note_title"
    
    _, state2, _ = await note_agent.handle(test_user.id, "Título", context)
    assert state2 == "awaiting_note_content"
    
    fsm = note_agent._get_or_create_fsm(test_user.id)
    assert fsm.current_state == "awaiting_note_content"


@pytest.mark.asyncio
async def test_multi_tenant_isolation(note_agent, test_user, test_user_tenant2):
    """Test E2E: Aislamiento multi-tenant"""
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
    
    # List notes for user 2
    response2, _, _ = await note_agent.handle(test_user_tenant2.id, "Listar notas", context2)
    
    # User 2 should NOT see user 1 notes
    assert "Tenant1 Note" in response1
    assert "Tenant1 Note" not in response2


# ==========================================
# INTEGRATION TEST
# ==========================================

@pytest.mark.asyncio
async def test_note_agent_full_integration(note_agent, test_user):
    """Test E2E: Integración completa (create → edit → pin → list)"""
    context = {
        "tenant_id": test_user.tenant_id,
        "user_id": test_user.id
    }
    
    # 1. Crear nota
    await note_agent.handle(test_user.id, "Crear nota", context)
    await note_agent.handle(test_user.id, "Integration Test", context)
    await note_agent.handle(test_user.id, "Initial content", context)
    response_create, _, _ = await note_agent.handle(test_user.id, "sí", context)
    
    match = re.search(r'ID: (\d+)', response_create)
    note_id = int(match.group(1))
    
    # 2. Editar nota
    await note_agent.handle(test_user.id, f"editar nota {note_id}", context)
    await note_agent.handle(test_user.id, "Updated content", context)
    
    # 3. Fijar nota
    await note_agent.handle(test_user.id, f"fijar nota {note_id}", context)
    
    # 4. Listar solo fijadas
    response_pinned, _, _ = await note_agent.handle(
        test_user.id, 
        "mostrar notas fijadas", 
        context
    )
    
    assert "Integration Test" in response_pinned
    assert "fijadas" in response_pinned.lower()
