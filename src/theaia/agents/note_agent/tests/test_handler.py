import pytest
from unittest.mock import Mock, AsyncMock
from src.theaia.agents.note_agent.handler import NoteAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    agent_instance = NoteAgent(user_id)
    
    # ✅ FIX: Mock debe retornar OBJETO con atributos, NO dict
    mock_note = Mock()
    mock_note.id = 1
    mock_note.title = "lista de la compra"
    mock_note.content = "comprar pan, leche y huevos"
    mock_note.category = "general"
    
    mock_repo = Mock()
    mock_repo.create = AsyncMock(return_value=mock_note)  # ← Retorna objeto Mock
    agent_instance.note_repository = mock_repo
    
    return agent_instance

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("nota")
    assert agent.can_handle("notas")
    assert agent.can_handle("apunte")
    assert agent.can_handle("memoria")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("evento")
    assert not agent.can_handle("ayuda")
    assert not agent.can_handle("agenda")

@pytest.mark.asyncio
async def test_note_flow(agent):
    """Test complete note creation flow with async handler - 4 step flow."""
    ctx = {"tenant_id": "test_tenant"}
    uid = "test_user"
    
    # PASO 1: Iniciar creación nota → awaiting_note_title
    out = await agent.handle(uid, "quiero guardar una nota", ctx)
    assert "título" in out[0].lower() or "nombre" in out[0].lower()
    assert out[1] == "awaiting_note_title"
    
    # PASO 2: Proporcionar título → awaiting_note_content
    out = await agent.handle(uid, "lista de la compra", out[2])
    assert "contenido" in out[0].lower() or "escribir" in out[0].lower()
    assert out[1] == "awaiting_note_content"
    
    # PASO 3: Proporcionar contenido → awaiting_confirmation
    out = await agent.handle(uid, "comprar pan, leche y huevos", out[2])
    assert "guardar" in out[0].lower() or "confirmar" in out[0].lower()
    assert out[1] == "awaiting_confirmation"
    
    # PASO 4: Confirmar → idle (completado)
    out = await agent.handle(uid, "sí", out[2])
    assert "guardad" in out[0].lower() or "creada" in out[0].lower()
    assert out[1] in ["idle", "completed"]
    
    # Verificar que se llamó al repository
    agent.note_repository.create.assert_called_once()
