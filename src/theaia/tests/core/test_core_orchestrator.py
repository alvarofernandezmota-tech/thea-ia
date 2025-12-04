"""
Tests para CoreOrchestrator
"""

import pytest
from src.theaia.core.orchestrator import CoreOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test inicialización básica."""
    orchestrator = CoreOrchestrator(language="es")
    
    assert orchestrator.language == "es"
    assert orchestrator.intent_parser is not None
    assert orchestrator.nlp_engine is not None
    assert orchestrator.conversation_manager is not None
    assert orchestrator.response_formatter is not None


@pytest.mark.asyncio  
async def test_orchestrator_stats():
    """Test obtener estadísticas."""
    orchestrator = CoreOrchestrator()
    
    stats = orchestrator.get_stats()
    
    assert "total_messages" in stats
    assert "registered_agents" in stats
    assert stats["total_messages"] == 0


@pytest.mark.asyncio
async def test_orchestrator_get_available_agents():
    """Test listar agentes disponibles."""
    orchestrator = CoreOrchestrator()
    
    agents = orchestrator.get_available_agents()
    
    assert isinstance(agents, list)
    # Sin agentes registrados todavía
    assert len(agents) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
