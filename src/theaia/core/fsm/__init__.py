"""
Finite State Machine package for Thea IA conversation management.
"""

from .conversation_manager import ConversationManager
from .state_machine import BaseStateMachine, ConversationStateMachine

__all__ = [
    'ConversationManager',
    'BaseStateMachine', 
    'ConversationStateMachine'
]
