# src/theaia/core/fsm/transitions.py

from typing import Dict, List, Any, Callable
import logging

logger = logging.getLogger(__name__)

class TransitionConfig:
    """Configuración de transiciones para Thea IA 2.0"""
    
    def __init__(self):
        self.transition_rules = self._build_transition_rules()
    
    def _build_transition_rules(self) -> Dict[str, Dict[str, Any]]:
        """Construye reglas de transición"""
        
        return {
            'request_disambiguation': {
                'source': 'initial',
                'dest': 'awaiting_disambiguation',
                'conditions': ['_has_multiple_intents'],
                'before': ['_prepare_disambiguation'],
                'after': ['_log_disambiguation_request']
            },
            
            'delegate_to_agent': {
                'source': 'initial',
                'dest': 'agent_delegated',
                'conditions': ['_has_single_intent'],
                'before': ['_prepare_agent_delegation'],
                'after': ['_log_agent_delegation']
            },
            
            'resolve_disambiguation': {
                'source': 'awaiting_disambiguation',
                'dest': 'agent_delegated',
                'conditions': ['_user_choice_valid'],
                'before': ['_process_user_choice'],
                'after': ['_log_disambiguation_resolved']
            },
            
            'complete_conversation': {
                'source': 'agent_delegated',
                'dest': 'completed',
                'conditions': ['_agent_task_completed'],
                'after': ['_log_conversation_completed']
            },
            
            'timeout_session': {
                'source': '*',
                'dest': 'session_timeout',
                'conditions': ['_session_expired'],
                'after': ['_log_session_timeout']
            },
            
            'handle_error': {
                'source': '*',
                'dest': 'error_state',
                'conditions': ['_error_occurred'],
                'after': ['_log_error_state']
            },
            
            'reset_conversation': {
                'source': '*',
                'dest': 'initial',
                'before': ['_cleanup_context'],
                'after': ['_log_conversation_reset']
            }
        }
    
    # Condiciones
    def _has_multiple_intents(self, event) -> bool:
        intents = getattr(event, 'candidate_intents', [])
        return len(intents) > 1
    
    def _has_single_intent(self, event) -> bool:
        intents = getattr(event, 'candidate_intents', [])
        return len(intents) == 1
    
    def _user_choice_valid(self, event) -> bool:
        choice = getattr(event, 'user_choice', None)
        valid_choices = ['nota', 'cita', 'recordatorio', 'agenda', 'notas']
        return choice and choice.lower() in valid_choices
    
    def _agent_task_completed(self, event) -> bool:
        return getattr(event, 'task_completed', False)
    
    def _session_expired(self, event) -> bool:
        return getattr(event, 'session_expired', False)
    
    def _error_occurred(self, event) -> bool:
        return getattr(event, 'error', None) is not None
    
    # Callbacks
    def _prepare_disambiguation(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            machine.update_context(disambiguation_active=True)
    
    def _prepare_agent_delegation(self, event):
        machine = getattr(event, 'machine', None)
        agent_name = getattr(event, 'agent_name', None)
        if machine and agent_name:
            machine.active_agent = agent_name
    
    def _process_user_choice(self, event):
        machine = getattr(event, 'machine', None)
        choice = getattr(event, 'user_choice', None)
        if machine and choice:
            machine.update_context(resolved_intent=choice)
    
    def _cleanup_context(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            machine.clear_context()
    
    # Logging callbacks
    def _log_disambiguation_request(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            logger.info(f"Disambiguation requested for user {machine.user_id}")
    
    def _log_agent_delegation(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            logger.info(f"Agent delegation for user {machine.user_id}")
    
    def _log_disambiguation_resolved(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            logger.info(f"Disambiguation resolved for user {machine.user_id}")
    
    def _log_conversation_completed(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            logger.info(f"Conversation completed for user {machine.user_id}")
    
    def _log_session_timeout(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            logger.warning(f"Session timeout for user {machine.user_id}")
    
    def _log_error_state(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            logger.error(f"Error state for user {machine.user_id}")
    
    def _log_conversation_reset(self, event):
        machine = getattr(event, 'machine', None)
        if machine:
            logger.info(f"Conversation reset for user {machine.user_id}")

# Exportaciones
__all__ = ['TransitionConfig']
