"""
Repositories Package - THEA IA Database Layer

Exports todos los repositories para fácil importación.

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02 - Database Layer

Example:
    from src.theaia.database.repositories import (
        UserRepository,
        EventRepository,
        NoteRepository,
        ConversationRepository,
        MessageHistoryRepository
    )
    
    async with get_db() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(123456, "default")
"""

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.repositories.user_repository import UserRepository
from src.theaia.database.repositories.event_repository import EventRepository
from src.theaia.database.repositories.note_repository import NoteRepository
from src.theaia.database.repositories.conversation_repository import ConversationRepository
from src.theaia.database.repositories.message_history_repository import MessageHistoryRepository


__all__ = [
    "BaseRepository",
    "UserRepository",
    "EventRepository",
    "NoteRepository",
    "ConversationRepository",
    "MessageHistoryRepository",
]
