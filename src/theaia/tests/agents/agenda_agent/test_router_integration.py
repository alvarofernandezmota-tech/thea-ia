"""
Test de integración AgendaAgent con Router
Verifica que AgendaAgent está correctamente conectado al router principal.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
"""

import sys
import os

# Agregar src al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

import pytest
from src.theaia.core.router import TheaRouter


def test_router_imports():
    """Verificar que el router importa correctamente con AgendaAgent."""
    print("\n🧪 Test 1: Importar TheaRouter...")
    
    router = TheaRouter()
    print("   ✅ Router creado correctamente")
    
    assert router is not None
    assert hasattr(router, 'agent_registry')


def test_agenda_intents_registered():
    """Verificar que todos los intents de agenda están registrados."""
    print("\n🧪 Test 2: Verificar AgendaAgent en registry...")
    
    router = TheaRouter()
    
    agenda_intents = [
        "crear_evento", "evento", "agendar", "calendario",
        "listar_eventos", "mis_eventos", "editar_evento",
        "cancelar_evento", "modificar_evento", "eliminar_evento",
        "borrar_evento", "reunion", "cita"
    ]
    
    for intent in agenda_intents:
        assert intent in router.agent_registry, f"Intent '{intent}' no registrado"
        agent_class = router.agent_registry[intent]
        print(f"   ✅ {intent} → {agent_class.__name__}")
        
        # Verificar que todos apuntan a AgendaAgent
        assert agent_class.__name__ == "AgendaAgent", f"Intent '{intent}' no apunta a AgendaAgent"


def test_agenda_agent_class():
    """Verificar que AgendaAgent se puede importar."""
    print("\n🧪 Test 3: Importar AgendaAgent directamente...")
    
    from src.theaia.agents.agenda_agent.handler import AgendaAgent
    
    print("   ✅ AgendaAgent importado correctamente")
    assert AgendaAgent is not None


def test_router_has_nlp_components():
    """Verificar que el router tiene componentes NLP."""
    print("\n🧪 Test 4: Verificar componentes NLP...")
    
    router = TheaRouter()
    
    assert hasattr(router, 'intent_detector'), "Router no tiene intent_detector"
    print("   ✅ intent_detector presente")
    
    assert hasattr(router, 'entity_extractor'), "Router no tiene entity_extractor"
    print("   ✅ entity_extractor presente")
    
    assert hasattr(router, 'session_manager'), "Router no tiene session_manager"
    print("   ✅ session_manager presente")


def test_summary():
    """Resumen de tests."""
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS DE INTEGRACIÓN PASARON")
    print("=" * 60)
    print("\n📋 Verificaciones completadas:")
    print("   ✅ Router importa correctamente")
    print("   ✅ 13 intents de agenda registrados")
    print("   ✅ Todos apuntan a AgendaAgent")
    print("   ✅ AgendaAgent se puede importar")
    print("   ✅ Componentes NLP presentes")
    print("\n🎯 AgendaAgent integrado correctamente al router\n")


if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE INTEGRACIÓN - AGENDAAGENT + ROUTER")
    print("=" * 60)
    
    test_router_imports()
    test_agenda_intents_registered()
    test_agenda_agent_class()
    test_router_has_nlp_components()
    test_summary()
