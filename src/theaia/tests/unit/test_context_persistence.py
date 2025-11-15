# Archivo: src/theaia/tests/unit/test_context_persistence.py

"""Tests for context persistence."""

import pytest
from unittest.mock import MagicMock
from src.theaia.database.repositories.context_repository import save_context, load_context


def test_save_and_load_context():
    """Test saving and loading context."""
    # Mock database session
    mock_session = MagicMock()
    
    # Test data
    user_id = "test_user_123"
    conversation_id = "conv_456"
    test_context = {
        "user_id": user_id,
        "intent": "agenda",
        "entities": {"date": "tomorrow"}
    }
    
    # Save context
    result = save_context(
        session=mock_session,
        user_id=user_id,
        conversation_id=conversation_id,
        context=test_context
    )
    
    assert result is True
    
    # Load context
    loaded = load_context(
        session=mock_session,
        user_id=user_id,
        conversation_id=conversation_id
    )
    
    assert loaded is not None
    assert isinstance(loaded, dict)
