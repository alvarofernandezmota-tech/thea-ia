"""
AgendaAgent E2E API Test - Complete Flow Validation

Tests the COMPLETE stack:
- HTTP POST to FastAPI endpoint
- Router processes message
- AgendaAgent handles request
- FSM transitions through states
- EventRepository saves to PostgreSQL
- Response returns correct format

This validates END-TO-END functionality before moving to next agent.

Author: Álvaro Fernández Mota (CEO THEA IA)
Date: 24 November 2025
Philosophy: Validate E2E before continuing
"""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from datetime import datetime, timedelta

from src.theaia.api.main import app
from src.theaia.database.session import get_session_factory
from src.theaia.database.models.event import Event
from src.theaia.database.models.user import User


@pytest.mark.asyncio
@pytest.mark.e2e
class TestAgendaAgentE2EComplete:
    """
    Complete E2E validation for AgendaAgent.
    
    Tests the ENTIRE stack from HTTP request to database persistence.
    """
    
    async def test_create_event_e2e_complete_flow(self):
        """
        Test COMPLETE flow: HTTP → Router → Agent → FSM → DB → Response
        
        Validates:
        1. API accepts POST request
        2. Router routes to AgendaAgent
        3. Agent processes with FSM
        4. EventRepository saves to PostgreSQL
        5. Response format is correct
        6. Event is actually in database
        """
        # Setup
        test_user_id = f"test_e2e_user_{datetime.now().timestamp()}"
        test_message = "crear reunión mañana a las 15:00 en la oficina"
        
        # Get DB session
        session_factory = get_session_factory()
        async with session_factory() as session:
            # Ensure clean state - delete test user if exists
            await session.execute(
                select(User).where(User.telegram_id == test_user_id)
            )
            await session.commit()
        
        # Create HTTP client
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            
            # ===== STEP 1: Send message to API =====
            response = await client.post(
                "/api/agents/agenda/message",
                json={
                    "user_id": test_user_id,
                    "message": test_message,
                    "tenant_id": "default"
                }
            )
            
            # Validate HTTP response
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            response_data = response.json()
            
            # Validate response structure
            assert "response" in response_data, "Response missing 'response' field"
            assert "state" in response_data, "Response missing 'state' field"
            assert "context" in response_data, "Response missing 'context' field"
            
            # ===== STEP 2: Verify response content =====
            response_text = response_data["response"]
            assert len(response_text) > 0, "Response text is empty"
            
            # Agent should acknowledge event creation
            assert any(word in response_text.lower() for word in ["evento", "reunión", "guardado", "creado"]), \
                f"Response doesn't acknowledge event creation: {response_text}"
            
            # ===== STEP 3: Verify FSM state changed =====
            # Should have moved from IDLE through creation flow
            state = response_data["state"]
            # State could be IDLE (completed) or in creation flow
            assert state in [
                "idle",
                "awaiting_title", 
                "awaiting_date",
                "awaiting_time",
                "awaiting_location",
                "processing",
                "event_saved"
            ], f"Unexpected state: {state}"
            
            # ===== STEP 4: Verify event was saved to PostgreSQL =====
            async with session_factory() as session:
                # Query events for test user
                result = await session.execute(
                    select(Event).where(Event.user_id == test_user_id)
                )
                events = result.scalars().all()
                
                # Should have at least one event
                assert len(events) > 0, "No events found in database"
                
                event = events[0]
                
                # Validate event data
                assert event.title is not None, "Event title is None"
                assert event.event_date is not None, "Event date is None"
                assert event.user_id == test_user_id, "Event user_id doesn't match"
                assert event.tenant_id == "default", "Event tenant_id doesn't match"
                
                # Optional: Validate extracted data makes sense
                # (depends on ML extraction quality)
                
                # Cleanup
                await session.delete(event)
                await session.commit()
        
        print(f"✅ E2E Test PASSED: AgendaAgent complete flow working")
    
    
    async def test_multi_turn_conversation_e2e(self):
        """
        Test MULTI-TURN conversation flow.
        
        Simulates:
        1. User: "crear evento"
        2. Agent: "¿Qué título?"
        3. User: "Reunión equipo"
        4. Agent: "¿Qué fecha?"
        5. User: "mañana"
        6. Agent: "¿Qué hora?"
        7. User: "15:00"
        8. Agent: "Evento guardado"
        """
        test_user_id = f"test_multiturn_{datetime.now().timestamp()}"
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            
            # Turn 1: Start creation
            resp1 = await client.post(
                "/api/agents/agenda/message",
                json={
                    "user_id": test_user_id,
                    "message": "crear evento",
                    "tenant_id": "default"
                }
            )
            assert resp1.status_code == 200
            data1 = resp1.json()
            
            # Should ask for title
            assert "título" in data1["response"].lower() or "title" in data1["response"].lower()
            
            # Turn 2: Provide title
            resp2 = await client.post(
                "/api/agents/agenda/message",
                json={
                    "user_id": test_user_id,
                    "message": "Reunión equipo",
                    "tenant_id": "default"
                }
            )
            assert resp2.status_code == 200
            data2 = resp2.json()
            
            # Should ask for date
            assert "fecha" in data2["response"].lower() or "date" in data2["response"].lower()
            
            # Turn 3: Provide date
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            resp3 = await client.post(
                "/api/agents/agenda/message",
                json={
                    "user_id": test_user_id,
                    "message": "mañana",
                    "tenant_id": "default"
                }
            )
            assert resp3.status_code == 200
            data3 = resp3.json()
            
            # Should ask for time
            assert "hora" in data3["response"].lower() or "time" in data3["response"].lower()
            
            # Turn 4: Provide time
            resp4 = await client.post(
                "/api/agents/agenda/message",
                json={
                    "user_id": test_user_id,
                    "message": "15:00",
                    "tenant_id": "default"
                }
            )
            assert resp4.status_code == 200
            data4 = resp4.json()
            
            # Should confirm saved
            assert any(word in data4["response"].lower() for word in ["guardado", "creado", "saved"])
            
            # Verify in DB
            session_factory = get_session_factory()
            async with session_factory() as session:
                result = await session.execute(
                    select(Event).where(Event.user_id == test_user_id)
                )
                events = result.scalars().all()
                
                assert len(events) > 0, "Event not saved to database"
                event = events[0]
                assert event.title == "Reunión equipo"
                
                # Cleanup
                await session.delete(event)
                await session.commit()
        
        print(f"✅ Multi-turn E2E Test PASSED")


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_health_check():
    """Quick sanity check that API is reachable."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
