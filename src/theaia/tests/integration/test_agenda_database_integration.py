"""
Integration tests: AgendaAgent Database Integration (REAL PostgreSQL)
Tests real database operations with EventRepository

Responsable: Álvaro Fernández Mota (CEO THEA IA)
Fecha: 21 Noviembre 2025
Filosofía: TRES (Álvaro + Jarvis + THEA IA)
Hito: H03 BLOQUE 3.4A.3.2 - Database Integration REAL
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


class TestAgendaDatabaseIntegration:
    """Test AgendaAgent database integration with REAL PostgreSQL"""
    
    @pytest.fixture(scope="function")
    def db_engine(self):
        """Create database engine - FORCE psycopg2 (sync driver)"""
        # Hardcoded URL with psycopg2 to avoid async issues
        db_url = "postgresql+psycopg2://postgres@localhost:5432/theaia_test"
        
        engine = create_engine(db_url)
        yield engine
        engine.dispose()
    
    @pytest.fixture(scope="function")
    def db_session(self, db_engine):
        """Create database session with transaction rollback + test user"""
        # Create all tables in POSTGRESQL
        Base.metadata.create_all(db_engine)
        
        # Create session
        Session = sessionmaker(bind=db_engine)
        session = Session()
        
        # Create test user (required for FK constraint) - CAMPOS CORRECTOS
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
        
        # Rollback and cleanup
        session.rollback()
        session.close()
        
        # Drop all tables
        Base.metadata.drop_all(db_engine)
    
    @pytest.fixture
    def agent(self):
        """Create AgendaAgent instance"""
        return AgendaAgent()
    
    def test_create_event_saves_to_database(self, db_session, agent):
        """Test creating event through AgendaAgent saves to REAL DB"""
        user_id = 1  # Integer for FK
        tenant_id = "test_tenant"
        
        # Get FSM and create event
        fsm = agent._get_fsm(str(user_id))
        context = {
            'user_id': str(user_id),
            'tenant_id': tenant_id,
            'event_title': 'Meeting',
            'event_date': '2025-11-21',
            'event_time': '10:00'
        }
        
        # Execute FSM flow
        fsm.start_create(context)
        fsm.provide_title(context)
        fsm.provide_date(context)
        fsm.provide_time(context)
        fsm.skip_location(context)
        
        # Get draft
        draft = fsm.get_event_draft()
        
        # Save to REAL DATABASE using start_datetime
        start_dt = datetime(2025, 11, 21, 10, 0, tzinfo=timezone.utc)
        
        event = Event(
            title=draft['title'],
            start_datetime=start_dt,
            user_id=user_id,
            tenant_id=tenant_id,
            location=draft.get('location'),
            description=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db_session.add(event)
        db_session.commit()
        
        # Verify saved in REAL DB
        saved_event = db_session.query(Event).filter_by(
            user_id=user_id,
            title='Meeting'
        ).first()
        
        assert saved_event is not None
        assert saved_event.title == 'Meeting'
        assert saved_event.user_id == user_id
        assert saved_event.tenant_id == tenant_id
        assert saved_event.start_datetime == start_dt
    
    def test_multi_tenant_isolation(self, db_session):
        """Test events are isolated by tenant in REAL DB"""
        tenant1 = "tenant_1"
        tenant2 = "tenant_2"
        user_id = 1
        
        start_dt = datetime(2025, 11, 21, 10, 0, tzinfo=timezone.utc)
        
        # Create events for tenant 1
        event1 = Event(
            title='Tenant 1 Meeting',
            start_datetime=start_dt,
            user_id=user_id,
            tenant_id=tenant1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db_session.add(event1)
        
        # Create events for tenant 2
        event2 = Event(
            title='Tenant 2 Meeting',
            start_datetime=start_dt,
            user_id=user_id,
            tenant_id=tenant2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db_session.add(event2)
        
        db_session.commit()
        
        # Query tenant 1 events only
        tenant1_events = db_session.query(Event).filter_by(
            user_id=user_id,
            tenant_id=tenant1
        ).all()
        
        # Query tenant 2 events only
        tenant2_events = db_session.query(Event).filter_by(
            user_id=user_id,
            tenant_id=tenant2
        ).all()
        
        # Verify isolation in REAL DB
        assert len(tenant1_events) == 1
        assert len(tenant2_events) == 1
        assert tenant1_events[0].title == 'Tenant 1 Meeting'
        assert tenant2_events[0].title == 'Tenant 2 Meeting'
    
    def test_fsm_with_database_persistence(self, db_session, agent):
        """Test FSM flow with REAL database persistence"""
        user_id = 1
        tenant_id = "test_tenant"
        
        # FSM flow
        fsm = agent._get_fsm(str(user_id))
        context = {
            'user_id': str(user_id),
            'tenant_id': tenant_id,
            'event_title': 'Persistent Event',
            'event_date': '2025-11-21',
            'event_time': '10:00'
        }
        
        fsm.start_create(context)
        fsm.provide_title(context)
        fsm.provide_date(context)
        fsm.provide_time(context)
        fsm.skip_location(context)
        
        # Save to REAL database
        draft = fsm.get_event_draft()
        start_dt = datetime(2025, 11, 21, 10, 0, tzinfo=timezone.utc)
        
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
        
        # Mark as saved
        context['db_event_id'] = event.id
        fsm.save_event(context)
        fsm.finish(context)
        
        # Verify FSM cleaned
        assert fsm.current_state == AgendaStates.IDLE
        assert fsm.get_event_draft() is None
        
        # Verify event in REAL DB
        saved = db_session.query(Event).filter_by(id=event.id).first()
        assert saved is not None
        assert saved.title == 'Persistent Event'
        assert saved.start_datetime == start_dt
