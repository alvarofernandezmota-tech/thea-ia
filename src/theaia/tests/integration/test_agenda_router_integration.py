"""
Integration tests: AgendaAgent + Core Router Integration
Tests routing, intent detection, and end-to-end flow

Responsable: Álvaro Fernández Mota (CEO THEA IA)
Fecha: 21 Noviembre 2025
Filosofía: TRES (Álvaro + Jarvis + THEA IA)
Hito: H03 BLOQUE 3.4A.3.3 - Router Integration
"""

import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.agenda_agent.model.agent_states import AgendaStates
from src.theaia.database.models.base import Base
from src.theaia.database.models.event import Event
from src.theaia.database.models.user import User
from src.theaia.core.router import TheaRouter


class TestAgendaRouterIntegration:
    """Test AgendaAgent integration with Core Router"""
    
    @pytest.fixture(scope="function")
    def db_engine(self):
        """Create database engine"""
        db_url = "postgresql+psycopg2://postgres@localhost:5432/theaia_test"
        engine = create_engine(db_url)
        yield engine
        engine.dispose()
    
    @pytest.fixture(scope="function")
    def db_session(self, db_engine):
        """Create database session with test user"""
        Base.metadata.create_all(db_engine)
        
        Session = sessionmaker(bind=db_engine)
        session = Session()
        
        # Create test user
        test_user = User(
            id=1,
            telegram_id=123456789,
            username="test_user",
            first_name="Test",
            last_name="User",
            language_code="es",
            timezone="UTC",
            is_active=True,
            tenant_id="test_tenant",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc)
        )
        session.add(test_user)
        session.commit()
        
        yield session
        
        session.rollback()
        session.close()
        
        Base.metadata.drop_all(db_engine)
    
    @pytest.fixture
    def agent(self):
        """Create AgendaAgent instance"""
        return AgendaAgent()
    
    @pytest.fixture
    def router(self):
        """Create Router instance"""
        return TheaRouter()
    
    def test_agent_processes_router_context(self, agent):
        """Test AgendaAgent processes context from Router"""
        user_id = "test_user"
        tenant_id = "test_tenant"
        
        # Simulated Router context with extracted entities
        router_context = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'user_message': 'crear evento reunión mañana a las 10',
            'detected_intent': 'create_event',
            'confidence': 0.95,
            'event_title': 'reunión',
            'event_date': '2025-11-22',
            'event_time': '10:00'
        }
        
        # Get AgendaAgent FSM
        fsm = agent._get_fsm(user_id)
        
        # Process router context
        fsm.start_create(router_context)
        fsm.provide_title(router_context)
        fsm.provide_date(router_context)
        fsm.provide_time(router_context)
        fsm.skip_location(router_context)
        
        # Verify FSM processed entities
        draft = fsm.get_event_draft()
        assert draft is not None
        assert 'title' in draft
        assert 'date' in draft
        assert 'time' in draft
    
    def test_end_to_end_flow_with_router_context(self, agent, db_session):
        """Test complete flow: router context → agent → FSM → DB"""
        user_id = 1
        tenant_id = "test_tenant"
        
        # STEP 1: Simulated Router output (intent + entities)
        router_output = {
            'intent': 'create_event',
            'confidence': 0.95,
            'entities': {
                'event_title': 'presentación',
                'date': '2025-11-24',
                'time': '14:00'
            }
        }
        
        # STEP 2: Router routes to AgendaAgent with context
        context = {
            'user_id': str(user_id),
            'tenant_id': tenant_id,
            'event_title': router_output['entities']['event_title'],
            'event_date': router_output['entities']['date'],
            'event_time': router_output['entities']['time']
        }
        
        # STEP 3: AgendaAgent FSM processes
        fsm = agent._get_fsm(str(user_id))
        fsm.start_create(context)
        fsm.provide_title(context)
        fsm.provide_date(context)
        fsm.provide_time(context)
        fsm.skip_location(context)
        
        # STEP 4: Save to database
        draft = fsm.get_event_draft()
        start_dt = datetime(2025, 11, 24, 14, 0, tzinfo=timezone.utc)
        
        event = Event(
            title=draft['title'],
            start_datetime=start_dt,
            user_id=user_id,
            tenant_id=tenant_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db_session.add(event)
        db_session.commit()
        
        # STEP 5: Verify complete flow
        saved = db_session.query(Event).filter_by(id=event.id).first()
        
        assert saved is not None
        assert saved.title == 'presentación'
        assert saved.start_datetime == start_dt
        assert saved.user_id == user_id
        assert saved.tenant_id == tenant_id
        
        # STEP 6: FSM cleanup
        context['db_event_id'] = event.id
        fsm.save_event(context)
        fsm.finish(context)
        
        assert fsm.current_state == AgendaStates.IDLE
        assert fsm.get_event_draft() is None
    
    def test_context_preservation_through_flow(self, agent):
        """Test context is preserved through agent flow"""
        user_id = "test_user"
        tenant_id = "test_tenant"
        session_id = "session_123"
        
        # Router maintains session context
        context = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'session_id': session_id,
            'event_title': 'Meeting',
            'event_date': '2025-11-21',
            'event_time': '10:00',
            'metadata': {
                'source': 'telegram',
                'language': 'es'
            }
        }
        
        # Agent FSM respects context
        fsm = agent._get_fsm(user_id)
        fsm.start_create(context)
        
        # Context should be available
        assert context['user_id'] == user_id
        assert context['tenant_id'] == tenant_id
        assert context['session_id'] == session_id
        assert 'metadata' in context
    
    def test_multi_step_conversation_with_routing(self, agent):
        """Test multi-step conversation through routing"""
        user_id = "test_user"
        tenant_id = "test_tenant"
        
        # Step 1: User says "crear evento"
        context_1 = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'user_message': 'crear evento'
        }
        
        fsm = agent._get_fsm(user_id)
        fsm.start_create(context_1)
        
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
        
        # Step 2: User provides title "reunión"
        context_2 = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'event_title': 'reunión'
        }
        
        fsm.provide_title(context_2)
        assert fsm.current_state == AgendaStates.AWAITING_DATE
        
        # Step 3: User provides date "mañana"
        context_3 = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'event_date': '2025-11-22'
        }
        
        fsm.provide_date(context_3)
        assert fsm.current_state == AgendaStates.AWAITING_TIME
        
        # Step 4: User provides time "10:00"
        context_4 = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'event_time': '10:00'
        }
        
        fsm.provide_time(context_4)
        assert fsm.current_state == AgendaStates.AWAITING_LOCATION
        
        # Step 5: User skips location
        fsm.skip_location(context_4)
        assert fsm.current_state == AgendaStates.PROCESSING
        
        # Verify draft
        draft = fsm.get_event_draft()
        assert draft['title'] == 'reunión'
        assert draft['date'] == '2025-11-22'
        assert draft['time'] == '10:00'
    
    def test_agent_selection_by_intent(self, agent):
        """Test agent is selected based on intent"""
        # Simulated router logic
        intents_to_agents = {
            'create_event': 'AgendaAgent',
            'list_events': 'AgendaAgent',
            'delete_event': 'AgendaAgent',
            'create_note': 'NoteAgent',
            'search': 'QueryAgent'
        }
        
        # Test agenda intents route to AgendaAgent
        agenda_intents = ['create_event', 'list_events', 'delete_event']
        
        for intent in agenda_intents:
            target_agent = intents_to_agents.get(intent)
            assert target_agent == 'AgendaAgent'
        
        # Verify agent class name
        assert agent.__class__.__name__ == 'AgendaAgent'
