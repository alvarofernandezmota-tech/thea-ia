"""
Test DEBUG PROFUNDO - Ver extracción de entidades paso a paso
"""

import pytest
from src.theaia.agents.agenda_agent.nlp_engine import SimpleNLPEngine
from src.theaia.agents.agenda_agent.datetime_parser import DateTimeParser
from src.theaia.agents.agenda_agent.orchestrator import AgendaOrchestrator
from src.theaia.agents.agenda_agent.services.event_service import EventService
from src.theaia.agents.agenda_agent.tools.event_tools import EventTools
from src.theaia.database.session import AsyncSessionLocal


@pytest.fixture
async def orchestrator():
    async with AsyncSessionLocal() as session:
        event_service = EventService(session)
        event_tools = EventTools(event_service)
        orch = AgendaOrchestrator(event_service, event_tools, timezone="UTC")
        yield orch


@pytest.mark.asyncio
async def test_debug_nlp_extraction(orchestrator):
    """Test para ver extracción de entidades en detalle."""
    print("\n" + "=" * 60)
    print("🔍 DEBUG: Extracción de Entidades")
    print("=" * 60)
    
    message = "crear evento 'Reunión equipo' mañana a las 10:00"
    print(f"\n📝 MENSAJE: {message}")
    
    # Paso 1: Detectar intent
    print("\n" + "-" * 60)
    print("PASO 1: Detectar Intent")
    print("-" * 60)
    
    intent = await orchestrator.nlp_engine.detect_intent(message)
    print(f"✓ Intent detectado: {intent}")
    
    # Paso 2: Extraer entidades con NLP
    print("\n" + "-" * 60)
    print("PASO 2: Extraer Entidades (NLP)")
    print("-" * 60)
    
    entities = orchestrator.nlp_engine.extract_entities(message, intent)
    print(f"✓ Entidades extraídas:")
    if entities:
        for key, value in entities.items():
            print(f"  • {key}: {value}")
    else:
        print("  ⚠️  VACÍO - No se extrajeron entidades")
    
    # Paso 3: Parsear datetime
    print("\n" + "-" * 60)
    print("PASO 3: Parsear DateTime")
    print("-" * 60)
    
    if entities.get("datetime_str"):
        print(f"✓ String datetime encontrado: '{entities['datetime_str']}'")
        
        parsed_dt = orchestrator.datetime_parser.parse(entities["datetime_str"])
        
        if parsed_dt:
            print(f"✓ DateTime parseado: {parsed_dt}")
            entities["datetime"] = parsed_dt
        else:
            print(f"❌ FALLO: No se pudo parsear '{entities['datetime_str']}'")
    else:
        print("❌ FALLO: No hay 'datetime_str' en entities")
    
    # Paso 4: Ver resultado final
    print("\n" + "-" * 60)
    print("PASO 4: Entidades Finales")
    print("-" * 60)
    
    print(f"✓ Entidades completas:")
    if entities:
        for key, value in entities.items():
            print(f"  • {key}: {value}")
    else:
        print("  ⚠️  VACÍO")
    
    # Verificar campos requeridos
    print("\n" + "-" * 60)
    print("PASO 5: Validación")
    print("-" * 60)
    
    required_fields = ["title", "datetime"]
    missing = [f for f in required_fields if f not in entities or entities[f] is None]
    
    if missing:
        print(f"❌ FALTAN CAMPOS: {missing}")
    else:
        print(f"✅ TODOS LOS CAMPOS PRESENTES")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
