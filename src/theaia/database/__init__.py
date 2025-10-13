
# src/theaia/database/__init__.py

"""
Database package initializer.

This module exposes the SQLAlchemy engine for use across the application.
"""

from .connection import engine

# Optionally expose session factory if defined in connection.py
from .connection import get_session  # if you have this function

# Import repositories to ensure they are registered or available when database package is imported
from .repositories.user_repository import UserRepository  # example
from .repositories.event_repository import EventRepository
from .repositories.note_repository import NoteRepository
from .repositories.context_repository import ContextRepository
