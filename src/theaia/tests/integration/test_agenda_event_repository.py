"""
Integration tests: EventRepository (AgendaAgent full integration)
Tests real CRUD operations with EventRepository

Responsable: Álvaro Fernández Mota (CEO THEA-IA)
Fecha: 21 Noviembre 2025
Filosofía: TRES (Álvaro + Jarvis + THEA IA)
Hito: H03 BLOQUE 3.4A - EventRepository Integration
"""

import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.theaia.database.models.base import Base
from src.theaia.database.models.event import Event
from src.theaia.database.models.user import User
from src.theaia.database.repositories.event_repository import EventRepository


class TestEventRepositoryIntegration:
    """Tests EventRepository direct DB integration - SYNC (no async)"""

    @pytest.fixture(scope="function")
    def db_engine(self):
        """Create database engine"""
        db_url = "postgresql+psycopg2://postgres@localhost:5432/theaia_test"
        engine = create_engine(db_url)
        yield engine
        engine.dispose()

    @pytest.fixture(scope="function")
    def db_session(self, db_engine):
        """Create database session with test users"""
        Base.metadata.create_all(db_engine)
        
        Session = sessionmaker(bind=db_engine)
        session = Session()
        
        # User 1 - tenant1
        test_user1 = User(
            id=1,
            telegram_id=123456789,
            username="user1",
            first_name="User",
            last_name="One",
            language_code="es",
            timezone="UTC",
            is_active=True,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc)
        )
        session.add(test_user1)
        
        # User 2 - tenant2 (para multi-tenant tests)
        test_user2 = User(
            id=2,
            telegram_id=987654321,
            username="user2",
            first_name="User",
            last_name="Two",
            language_code="es",
            timezone="UTC",
            is_active=True,
            tenant_id="tenant2",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc)
        )
        session.add(test_user2)
        session.commit()
        
        yield session
        
        session.rollback()
        session.close()
        
        Base.metadata.drop_all(db_engine)

    @pytest.fixture
    def repo(self, db_session):
        """Create EventRepository instance"""
        return EventRepository(db_session)

    # ==================== CRUD TESTS ====================

    def test_create_event(self, repo):
        """Test creating event in PostgreSQL"""
        event = Event(
            title="Reunión AgendaAgent",
            start_datetime=datetime(2025, 11, 22, 10, 0, tzinfo=timezone.utc),
            user_id=1,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event)
        repo.session.commit()
        
        assert event.id is not None
        assert event.title == "Reunión AgendaAgent"
        assert event.user_id == 1
        assert event.tenant_id == "tenant1"

    def test_get_event_by_id(self, repo):
        """Test retrieving event by ID"""
        # Create event
        event = Event(
            title="Buscar evento",
            start_datetime=datetime(2025, 12, 1, 8, 0, tzinfo=timezone.utc),
            user_id=1,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event)
        repo.session.commit()
        event_id = event.id
        
        # Retrieve it
        event_db = repo.session.query(Event).filter_by(id=event_id).first()
        
        assert event_db is not None
        assert event_db.title == "Buscar evento"
        assert event_db.id == event_id

    def test_update_event(self, repo):
        """Test updating event"""
        # Create
        event = Event(
            title="Evento original",
            start_datetime=datetime(2025, 12, 2, 12, 0, tzinfo=timezone.utc),
            user_id=1,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event)
        repo.session.commit()
        event_id = event.id
        
        # Update
        event.title = "Evento actualizado"
        event.updated_at = datetime.now(timezone.utc)
        repo.session.commit()
        
        # Verify
        event_db = repo.session.query(Event).filter_by(id=event_id).first()
        assert event_db.title == "Evento actualizado"

    def test_delete_event(self, repo):
        """Test deleting event"""
        # Create
        event = Event(
            title="Evento a eliminar",
            start_datetime=datetime(2025, 12, 3, 12, 0, tzinfo=timezone.utc),
            user_id=1,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event)
        repo.session.commit()
        event_id = event.id
        
        # Delete
        repo.session.delete(event)
        repo.session.commit()
        
        # Verify deleted
        event_db = repo.session.query(Event).filter_by(id=event_id).first()
        assert event_db is None

    # ==================== MULTI-TENANT TESTS ====================

    def test_multi_tenant_isolation(self, repo):
        """Test events are isolated by tenant"""
        # Evento para user 1/tenant1
        event1 = Event(
            title="Evento tenant1",
            start_datetime=datetime(2025, 11, 23, 15, 0, tzinfo=timezone.utc),
            user_id=1,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event1)
        
        # Evento para user 2/tenant2
        event2 = Event(
            title="Evento tenant2",
            start_datetime=datetime(2025, 11, 23, 16, 0, tzinfo=timezone.utc),
            user_id=2,
            tenant_id="tenant2",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event2)
        repo.session.commit()
        
        # Query tenant1 events
        tenant1_events = repo.session.query(Event).filter_by(tenant_id="tenant1").all()
        # Query tenant2 events
        tenant2_events = repo.session.query(Event).filter_by(tenant_id="tenant2").all()
        
        # Verify isolation
        assert len(tenant1_events) == 1
        assert len(tenant2_events) == 1
        assert tenant1_events[0].tenant_id == "tenant1"
        assert tenant2_events[0].tenant_id == "tenant2"

    def test_user_events_isolation(self, repo):
        """Test events are isolated by user within tenant"""
        # User 1 crea 2 eventos
        for i in range(2):
            event = Event(
                title=f"User1 evento {i}",
                start_datetime=datetime(2025, 11, 25, 10+i, 0, tzinfo=timezone.utc),
                user_id=1,
                tenant_id="tenant1",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            repo.session.add(event)
        repo.session.commit()
        
        # Verificar que user 1 tiene 2 eventos
        user1_events = repo.session.query(Event).filter_by(user_id=1, tenant_id="tenant1").all()
        assert len(user1_events) == 2
        
        # User 2 no tiene eventos en tenant1
        user2_events = repo.session.query(Event).filter_by(user_id=2, tenant_id="tenant1").all()
        assert len(user2_events) == 0

    # ==================== QUERY TESTS ====================

    def test_list_events_by_date_range(self, repo):
        """Test listing events within date range"""
        # Create events with different dates
        start_date = datetime(2025, 11, 20, 0, 0, tzinfo=timezone.utc)
        end_date = datetime(2025, 11, 25, 23, 59, tzinfo=timezone.utc)
        
        # Event within range
        event1 = Event(
            title="Evento en rango",
            start_datetime=datetime(2025, 11, 22, 10, 0, tzinfo=timezone.utc),
            user_id=1,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event1)
        
        # Event outside range (future)
        event2 = Event(
            title="Evento fuera de rango",
            start_datetime=datetime(2025, 12, 1, 10, 0, tzinfo=timezone.utc),
            user_id=1,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event2)
        repo.session.commit()
        
        # Query by date range
        events_in_range = repo.session.query(Event).filter(
            Event.start_datetime >= start_date,
            Event.start_datetime <= end_date,
            Event.user_id == 1,
            Event.tenant_id == "tenant1"
        ).all()
        
        assert len(events_in_range) == 1
        assert events_in_range[0].title == "Evento en rango"

    def test_event_persistence(self, repo):
        """Test event is actually persisted in PostgreSQL"""
        event = Event(
            title="Persistencia test",
            start_datetime=datetime(2025, 11, 30, 9, 30, tzinfo=timezone.utc),
            user_id=1,
            tenant_id="tenant1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        repo.session.add(event)
        repo.session.commit()
        
        # Count total events in DB
        total_events = repo.session.query(Event).count()
        assert total_events >= 1
        
        # Verify our event is there
        found = repo.session.query(Event).filter_by(title="Persistencia test").first()
        assert found is not None
        assert found.start_datetime == datetime(2025, 11, 30, 9, 30, tzinfo=timezone.utc)
