"""
Tests para NoteRepository - H02 PHASE 2
Autor: Álvaro Fernández Mota
Fecha: 19 Nov 2025
Hito: H02 - Advanced Persistence PHASE 2
Coverage target: ≥70%
"""

import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.models.note import Note
from src.theaia.database.repositories.note_repository import NoteRepository


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_note_data():
    """Datos de ejemplo para crear notas."""
    return {
        "tenant_id": "test_tenant",
        "user_id": 1,
        "title": "Nota importante",
        "content": "Contenido de la nota de prueba",
        "category": "work",
        "tags": ["urgente", "proyecto"],
        "priority": 2,
        "is_pinned": False
    }


# ============================================================================
# TEST 1-4: CRUD BÁSICO
# ============================================================================

@pytest.mark.asyncio
async def test_create_note_basic(db_session, sample_note_data):
    """Test 1: Crear nota básica"""
    note_repo = NoteRepository(db_session)
    
    note = Note(**sample_note_data)
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)
    
    assert note.id is not None
    assert note.title == sample_note_data["title"]
    assert note.content == sample_note_data["content"]
    assert note.category == "work"
    assert note.tags == ["urgente", "proyecto"]
    assert note.priority == 2
    assert note.is_pinned is False
    assert note.created_at is not None
    assert note.updated_at is not None


@pytest.mark.asyncio
async def test_get_note_by_id(db_session, sample_note_data):
    """Test 2: Obtener nota por ID"""
    note_repo = NoteRepository(db_session)
    
    # Crear nota
    created_note = Note(**sample_note_data)
    db_session.add(created_note)
    await db_session.commit()
    await db_session.refresh(created_note)
    
    # Obtener por ID
    retrieved_note = await note_repo.get_by_id(
        entity_id=created_note.id,
        tenant_id=sample_note_data["tenant_id"]
    )
    
    assert retrieved_note is not None
    assert retrieved_note.id == created_note.id
    assert retrieved_note.title == created_note.title
    
    # Verificar multi-tenant isolation
    wrong_tenant = await note_repo.get_by_id(
        entity_id=created_note.id,
        tenant_id="wrong_tenant"
    )
    assert wrong_tenant is None


@pytest.mark.asyncio
async def test_update_note(db_session, sample_note_data):
    """Test 3: Actualizar nota"""
    note_repo = NoteRepository(db_session)
    
    # Crear nota
    note = Note(**sample_note_data)
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)
    
    # Actualizar
    updated_note = await note_repo.update(
        entity_id=note.id,
        tenant_id=sample_note_data["tenant_id"],
        title="Nota URGENTE",
        priority=3
    )
    
    assert updated_note.title == "Nota URGENTE"
    assert updated_note.priority == 3
    assert updated_note.content == note.content
    assert updated_note.updated_at >= note.updated_at


@pytest.mark.asyncio
async def test_delete_note(db_session, sample_note_data):
    """Test 4: Eliminar nota"""
    note_repo = NoteRepository(db_session)
    
    # Crear nota
    note = Note(**sample_note_data)
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)
    
    # Eliminar
    deleted = await note_repo.delete(
        entity_id=note.id,
        tenant_id=sample_note_data["tenant_id"]
    )
    
    assert deleted is True
    retrieved = await note_repo.get_by_id(note.id, sample_note_data["tenant_id"])
    assert retrieved is None


# ============================================================================
# TEST 5-7: BÚSQUEDA Y FILTROS
# ============================================================================

@pytest.mark.asyncio
async def test_get_by_user(db_session, sample_note_data):
    """Test 5: Obtener notas de un usuario"""
    note_repo = NoteRepository(db_session)
    
    # Crear 5 notas
    for i in range(5):
        note = Note(**{
            **sample_note_data,
            "title": f"Nota {i}",
            "content": f"Contenido {i}"
        })
        db_session.add(note)
    
    await db_session.commit()
    
    # Obtener todas las notas del usuario
    notes = await note_repo.get_by_user(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"]
    )
    
    assert len(notes) == 5
    
    # Verificar paginación
    page1 = await note_repo.get_by_user(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"],
        skip=0,
        limit=3
    )
    assert len(page1) == 3


@pytest.mark.asyncio
async def test_search_notes(db_session, sample_note_data):
    """Test 6: Buscar notas por contenido"""
    note_repo = NoteRepository(db_session)
    
    # Crear notas con diferentes contenidos
    note1 = Note(**{
        **sample_note_data,
        "title": "Reunión con cliente",
        "content": "Discutir proyecto Q4"
    })
    db_session.add(note1)
    
    note2 = Note(**{
        **sample_note_data,
        "title": "Lista de compras",
        "content": "Leche, pan, huevos"
    })
    db_session.add(note2)
    
    note3 = Note(**{
        **sample_note_data,
        "title": "Ideas proyecto",
        "content": "Implementar nueva funcionalidad"
    })
    db_session.add(note3)
    
    await db_session.commit()
    
    # Buscar "proyecto"
    results = await note_repo.search(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"],
        query="proyecto"
    )
    
    assert len(results) == 2
    titles = [n.title for n in results]
    assert "Reunión con cliente" in titles
    assert "Ideas proyecto" in titles


@pytest.mark.asyncio
async def test_get_by_category(db_session, sample_note_data):
    """Test 7: Obtener notas por categoría"""
    note_repo = NoteRepository(db_session)
    
    # Crear notas work
    for i in range(3):
        note = Note(**{
            **sample_note_data,
            "title": f"Work {i}",
            "category": "work"
        })
        db_session.add(note)
    
    # Crear notas personal
    for i in range(2):
        note = Note(**{
            **sample_note_data,
            "title": f"Personal {i}",
            "category": "personal"
        })
        db_session.add(note)
    
    await db_session.commit()
    
    # Buscar por categoría work
    work_notes = await note_repo.get_by_category(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"],
        category="work"
    )
    
    assert len(work_notes) == 3
    
    # Buscar por categoría personal
    personal_notes = await note_repo.get_by_category(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"],
        category="personal"
    )
    
    assert len(personal_notes) == 2


# ============================================================================
# TEST 8-10: TAGS
# ============================================================================

@pytest.mark.asyncio
async def test_get_by_tags(db_session, sample_note_data):
    """Test 8: Obtener notas por tags"""
    note_repo = NoteRepository(db_session)
    
    # Nota con tags ["urgente", "proyecto"]
    note1 = Note(**{
        **sample_note_data,
        "title": "Nota 1",
        "tags": ["urgente", "proyecto"]
    })
    db_session.add(note1)
    
    # Nota con tags ["proyecto", "cliente"]
    note2 = Note(**{
        **sample_note_data,
        "title": "Nota 2",
        "tags": ["proyecto", "cliente"]
    })
    db_session.add(note2)
    
    # Nota con tags ["personal"]
    note3 = Note(**{
        **sample_note_data,
        "title": "Nota 3",
        "tags": ["personal"]
    })
    db_session.add(note3)
    
    await db_session.commit()
    
    # Buscar notas con tag "proyecto" (match any)
    proyecto_notes = await note_repo.get_by_tags(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"],
        tags=["proyecto"],
        match_all=False
    )
    
    assert len(proyecto_notes) == 2
    
    # Buscar notas con tags "urgente" Y "proyecto" (match all)
    urgente_proyecto = await note_repo.get_by_tags(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"],
        tags=["urgente", "proyecto"],
        match_all=True
    )
    
    assert len(urgente_proyecto) == 1
    assert urgente_proyecto[0].title == "Nota 1"


@pytest.mark.asyncio
async def test_add_tags(db_session, sample_note_data):
    """Test 9: Añadir tags a nota"""
    note_repo = NoteRepository(db_session)
    
    # Crear nota con tags iniciales
    note = Note(**{
        **sample_note_data,
        "tags": ["inicial"]
    })
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)
    
    # Añadir más tags
    updated_note = await note_repo.add_tags(
        note_id=note.id,
        tenant_id=sample_note_data["tenant_id"],
        new_tags=["nuevo1", "nuevo2"]
    )
    
    assert len(updated_note.tags) == 3
    assert "inicial" in updated_note.tags
    assert "nuevo1" in updated_note.tags
    assert "nuevo2" in updated_note.tags


@pytest.mark.asyncio
async def test_remove_tags(db_session, sample_note_data):
    """Test 10: Eliminar tags de nota"""
    note_repo = NoteRepository(db_session)
    
    # Crear nota con varios tags
    note = Note(**{
        **sample_note_data,
        "tags": ["tag1", "tag2", "tag3"]
    })
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)
    
    # Eliminar algunos tags
    updated_note = await note_repo.remove_tags(
        note_id=note.id,
        tenant_id=sample_note_data["tenant_id"],
        tags_to_remove=["tag2"]
    )
    
    assert len(updated_note.tags) == 2
    assert "tag1" in updated_note.tags
    assert "tag3" in updated_note.tags
    assert "tag2" not in updated_note.tags


# ============================================================================
# TEST 11-13: PIN Y ESTADÍSTICAS
# ============================================================================

@pytest.mark.asyncio
async def test_pin_operations(db_session, sample_note_data):
    """Test 11: Operaciones de pin/unpin"""
    note_repo = NoteRepository(db_session)
    
    # Crear nota sin pin
    note = Note(**sample_note_data)
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)
    
    assert note.is_pinned is False
    
    # Hacer pin
    pinned_note = await note_repo.toggle_pin(
        note_id=note.id,
        tenant_id=sample_note_data["tenant_id"]
    )
    
    assert pinned_note.is_pinned is True
    
    # Hacer unpin
    unpinned_note = await note_repo.toggle_pin(
        note_id=note.id,
        tenant_id=sample_note_data["tenant_id"]
    )
    
    assert unpinned_note.is_pinned is False


@pytest.mark.asyncio
async def test_get_pinned(db_session, sample_note_data):
    """Test 12: Obtener notas fijadas"""
    note_repo = NoteRepository(db_session)
    
    # Crear 3 notas normales
    for i in range(3):
        note = Note(**{
            **sample_note_data,
            "title": f"Normal {i}",
            "is_pinned": False
        })
        db_session.add(note)
    
    # Crear 2 notas pinned
    for i in range(2):
        note = Note(**{
            **sample_note_data,
            "title": f"Pinned {i}",
            "is_pinned": True
        })
        db_session.add(note)
    
    await db_session.commit()
    
    # Obtener solo las pinned
    pinned_notes = await note_repo.get_pinned(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"]
    )
    
    assert len(pinned_notes) == 2
    for note in pinned_notes:
        assert note.is_pinned is True


@pytest.mark.asyncio
async def test_count_by_category(db_session, sample_note_data):
    """Test 13: Contar notas por categoría"""
    note_repo = NoteRepository(db_session)
    
    # Crear notas de diferentes categorías
    categories = {
        "work": 5,
        "personal": 3,
        "ideas": 2
    }
    
    for category, count in categories.items():
        for i in range(count):
            note = Note(**{
                **sample_note_data,
                "title": f"{category} {i}",
                "category": category
            })
            db_session.add(note)
    
    await db_session.commit()
    
    # Contar por categoría
    counts = await note_repo.count_by_category(
        user_id=sample_note_data["user_id"],
        tenant_id=sample_note_data["tenant_id"]
    )
    
    assert counts["work"] == 5
    assert counts["personal"] == 3
    assert counts["ideas"] == 2
