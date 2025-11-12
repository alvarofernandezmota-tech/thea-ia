"""
Database Package - THEA IA PostgreSQL Async

Exports:
- Models: User, Event, Note, Conversation, MessageHistory
- Session: engine, get_db, init_db, close_db
- Connection: get_async_engine, test_connection
- Repositories: UserRepository, EventRepository, NoteRepository, 
                ConversationRepository, MessageHistoryRepository

Example:
    from src.theaia.database import get_db, UserRepository
    
    async with get_db() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(123456, "default")
"""

# Models
from src.theaia.database.models import (
    Base,
    BaseModel,
    User,
    Event,
    Note,
    Conversation,
    MessageHistory,
)

# Session & Engine
from src.theaia.database.session import (
    engine,
    AsyncSessionLocal,
    get_db,
    init_db,
    close_db,
)

# Connection utilities
from src.theaia.database.connection import (
    get_async_engine,
    test_connection,
)

# Repositories
from src.theaia.database.repositories import (
    BaseRepository,
    UserRepository,
    EventRepository,
    NoteRepository,
    ConversationRepository,
    MessageHistoryRepository,
)


__all__ = [
    # Models
    'Base',
    'BaseModel',
    'User',
    'Event',
    'Note',
    'Conversation',
    'MessageHistory',
    
    # Session & Engine
    'engine',
    'AsyncSessionLocal',
    'get_db',
    'init_db',
    'close_db',
    
    # Connection
    'get_async_engine',
    'test_connection',
    
    # Repositories
    'BaseRepository',
    'UserRepository',
    'EventRepository',
    'NoteRepository',
    'ConversationRepository',
    'MessageHistoryRepository',
]
