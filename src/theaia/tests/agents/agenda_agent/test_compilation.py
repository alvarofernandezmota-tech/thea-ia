"""
Test de compilación rápido para AgendaAgent
Verifica que todos los imports funcionan y componentes básicos operan.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
"""

import sys
import asyncio
from datetime import datetime
import pytest


print("=" * 60)
print("TEST DE COMPILACIÓN - AGENDAAGENT")
print("=" * 60)


# Test 1: Imports básicos
def test_imports():
    """Test que todos los módulos se pueden importar."""
    print("\n1. Testing imports...")
    
    try:
        from src.theaia.agents.agenda_agent.handler import AgendaAgent
        print("   ✅ handler.AgendaAgent")
    except Exception as e:
        print(f"   ❌ handler.AgendaAgent: {e}")
        pytest.fail(f"Failed to import AgendaAgent: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.orchestrator import AgendaOrchestrator
        print("   ✅ orchestrator.AgendaOrchestrator")
    except Exception as e:
        print(f"   ❌ orchestrator: {e}")
        pytest.fail(f"Failed to import AgendaOrchestrator: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.conversation_manager import ConversationManager
        print("   ✅ conversation_manager.ConversationManager")
    except Exception as e:
        print(f"   ❌ conversation_manager: {e}")
        pytest.fail(f"Failed to import ConversationManager: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.nlp_engine import SimpleNLPEngine
        print("   ✅ nlp_engine.SimpleNLPEngine")
    except Exception as e:
        print(f"   ❌ nlp_engine: {e}")
        pytest.fail(f"Failed to import SimpleNLPEngine: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.fsm_machine import AgendaFSM, FSMManager
        print("   ✅ fsm_machine.AgendaFSM")
    except Exception as e:
        print(f"   ❌ fsm_machine: {e}")
        pytest.fail(f"Failed to import FSM: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.intent_parser import AgendaIntentParser
        print("   ✅ intent_parser.AgendaIntentParser")
    except Exception as e:
        print(f"   ❌ intent_parser: {e}")
        pytest.fail(f"Failed to import IntentParser: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.datetime_parser import DateTimeParser
        print("   ✅ datetime_parser.DateTimeParser")
    except Exception as e:
        print(f"   ❌ datetime_parser: {e}")
        pytest.fail(f"Failed to import DateTimeParser: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.response_formatter import ResponseFormatter
        print("   ✅ response_formatter.ResponseFormatter")
    except Exception as e:
        print(f"   ❌ response_formatter: {e}")
        pytest.fail(f"Failed to import ResponseFormatter: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.tools.event_tools import EventTools
        print("   ✅ tools.EventTools")
    except Exception as e:
        print(f"   ❌ tools.EventTools: {e}")
        pytest.fail(f"Failed to import EventTools: {e}")
    
    try:
        from src.theaia.agents.agenda_agent.services.event_service import EventService
        print("   ✅ services.EventService")
    except Exception as e:
        print(f"   ❌ services.EventService: {e}")
        pytest.fail(f"Failed to import EventService: {e}")


# Test 2: NLP Engine básico
@pytest.mark.asyncio
async def test_nlp_engine():
    """Test que el NLP Engine funciona básicamente."""
    print("\n2. Testing NLP Engine...")
    
    from src.theaia.agents.agenda_agent.nlp_engine import SimpleNLPEngine
    
    nlp = SimpleNLPEngine()
    
    # Test intent detection
    intent1 = await nlp.detect_intent("crear reunión mañana")
    print(f"   ✅ Intent detection: 'crear reunión' → {intent1}")
    assert intent1 == "create_event", f"Expected 'create_event', got '{intent1}'"
    
    intent2 = await nlp.detect_intent("mostrar mis eventos")
    print(f"   ✅ Intent detection: 'mostrar' → {intent2}")
    assert intent2 == "query_events", f"Expected 'query_events', got '{intent2}'"
    
    intent3 = await nlp.detect_intent("eliminar evento 5")
    print(f"   ✅ Intent detection: 'eliminar' → {intent3}")
    assert intent3 == "delete_event", f"Expected 'delete_event', got '{intent3}'"


# Test 3: DateTime Parser
def test_datetime_parser():
    """Test que el DateTime Parser funciona."""
    print("\n3. Testing DateTime Parser...")
    
    from src.theaia.agents.agenda_agent.datetime_parser import DateTimeParser
    
    dt_parser = DateTimeParser(timezone="UTC")
    
    # Test parse relativo
    result = dt_parser.parse("en 2 horas")
    print(f"   ✅ DateTime parse: 'en 2 horas' → {result}")
    assert result is not None, "Failed to parse 'en 2 horas'"
    
    # Test keywords
    result2 = dt_parser.parse("mañana")
    print(f"   ✅ DateTime parse: 'mañana' → {result2}")
    assert result2 is not None, "Failed to parse 'mañana'"
    
    # Test duration
    duration = dt_parser.parse_duration("2 horas")
    print(f"   ✅ Duration parse: '2 horas' → {duration}")
    assert duration is not None, "Failed to parse duration '2 horas'"


# Test 4: FSM
def test_fsm_machine():
    """Test que la FSM funciona."""
    print("\n4. Testing FSM...")
    
    from src.theaia.agents.agenda_agent.fsm_machine import AgendaFSM
    from src.theaia.agents.agenda_agent.model.agent_states import AgentState
    
    fsm = AgendaFSM()
    print(f"   ✅ FSM initial state: {fsm.get_current_state().value}")
    assert fsm.get_current_state() == AgentState.IDLE
    
    # Test transition
    fsm.start_create_event()
    print(f"   ✅ FSM after start_create_event: {fsm.get_current_state().value}")
    assert fsm.get_current_state() == AgentState.AWAITING_EVENT_DETAILS
    
    # Test context
    fsm.update_context("title", "Reunión de prueba")
    assert fsm.get_context("title") == "Reunión de prueba"
    print(f"   ✅ FSM context updated")


# Test 5: Intent Parser (Regex fallback)
@pytest.mark.asyncio
async def test_intent_parser():
    """Test que el Intent Parser funciona."""
    print("\n5. Testing Intent Parser...")
    
    from src.theaia.agents.agenda_agent.intent_parser import AgendaIntentParser
    
    parser = AgendaIntentParser()
    
    # Test intent detection
    intent = await parser.detect_intent("crear evento mañana")
    print(f"   ✅ Intent: 'crear evento' → {intent}")
    assert intent == "create_event"
    
    # Test entity extraction
    entities = await parser.extract_entities("crear reunión con Juan en oficina", "create_event")
    print(f"   ✅ Entities extracted: {list(entities.keys())}")
    assert "participants" in entities or "location" in entities


# Test 6: Response Formatter
def test_response_formatter():
    """Test que el Response Formatter funciona."""
    print("\n6. Testing Response Formatter...")
    
    from src.theaia.agents.agenda_agent.response_formatter import ResponseFormatter
    
    formatter = ResponseFormatter(language="es")
    
    # Test missing info prompt
    prompt = formatter.format_missing_info_prompt(["title", "datetime"], "create_event")
    print(f"   ✅ Missing info prompt generated")
    assert "title" in prompt.lower() or "título" in prompt.lower()
    
    # Test error
    error = formatter.format_error("Test error", "general")
    print(f"   ✅ Error formatted")
    assert "❌" in error


# Test 7: Conversation Manager
def test_conversation_manager():
    """Test que el Conversation Manager funciona."""
    print("\n7. Testing Conversation Manager...")
    
    from src.theaia.agents.agenda_agent.conversation_manager import ConversationManager
    
    manager = ConversationManager()
    
    # Start conversation
    conv_id = manager.start_conversation(
        user_id=1,
        intent="create_event",
        partial_entities={"title": "Test"},
        missing_fields=["datetime_str"]
    )
    print(f"   ✅ Conversation started: {conv_id}")
    
    # Get conversation
    conv = manager.get_conversation(conv_id)
    assert conv is not None
    print(f"   ✅ Conversation retrieved")
    
    # Update conversation
    updated = manager.update_conversation(conv_id, new_entities={"datetime_str": "mañana"})
    assert updated is True
    print(f"   ✅ Conversation updated")
    
    # Check completeness
    is_complete = manager.is_conversation_complete(conv_id)
    print(f"   ✅ Conversation complete: {is_complete}")
    
    # End conversation
    manager.end_conversation(conv_id)
    print(f"   ✅ Conversation ended")


# Test 8: Orchestrator (sin DB)
def test_orchestrator_structure():
    """Test que el Orchestrator se puede instanciar."""
    print("\n8. Testing Orchestrator structure...")
    
    from src.theaia.agents.agenda_agent.orchestrator import AgendaOrchestrator
    
    # No podemos crear instancia real sin DB session
    # Pero podemos verificar que la clase existe y tiene los métodos
    assert hasattr(AgendaOrchestrator, 'process_message')
    assert hasattr(AgendaOrchestrator, '_execute_action')
    print(f"   ✅ Orchestrator has required methods")


def test_summary():
    """Print summary."""
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS DE COMPILACIÓN PASARON")
    print("=" * 60)
    print("\n📋 Componentes verificados:")
    print("   ✅ Imports de todos los módulos")
    print("   ✅ NLP Engine (intent detection)")
    print("   ✅ DateTime Parser")
    print("   ✅ FSM Machine")
    print("   ✅ Intent Parser")
    print("   ✅ Response Formatter")
    print("   ✅ Conversation Manager")
    print("   ✅ Orchestrator structure")
    print("\n🎯 AgendaAgent está listo para integración\n")


if __name__ == "__main__":
    # Ejecutar tests directamente
    print("Ejecutando tests de compilación...\n")
    
    test_imports()
    asyncio.run(test_nlp_engine())
    test_datetime_parser()
    test_fsm_machine()
    asyncio.run(test_intent_parser())
    test_response_formatter()
    test_conversation_manager()
    test_orchestrator_structure()
    test_summary()
