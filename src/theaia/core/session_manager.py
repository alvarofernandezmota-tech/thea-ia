# src/theaia/core/session_manager.py

from typing import Any, Dict

class SessionManager:
    """
    Maneja el contexto y estado de sesión para todos los usuarios y agentes en Thea IA.
    Permite conversaciones multi-turno, switch de agente y persistencia FSM/contexto.
    """

    def __init__(self):
        # user_id -> context (dict: puede contener el fsm_state, historial, slots...)
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_context(self, user_id: str) -> Dict[str, Any]:
        """Devuelve el contexto actual del usuario, o lo inicializa si no existe."""
        if user_id not in self.sessions:
            self.sessions[user_id] = self._get_default_context()
        return self.sessions[user_id]

    def update_context(self, user_id: str, context: Dict[str, Any]) -> None:
        """Actualiza el diccionario de contexto completo del usuario."""
        self.sessions[user_id] = context

    def reset_context(self, user_id: str) -> None:
        """Reinicia el contexto de usuario a su estado vacío/inicial."""
        self.sessions[user_id] = self._get_default_context()

    def clear_all_sessions(self) -> None:
        """Borra el contexto de todos los usuarios (sólo dev)."""
        self.sessions = {}

    def _get_default_context(self) -> Dict[str, Any]:
        """Define el contexto base vacío para cualquier usuario/turno."""
        return {
            "fsm_state": None,
            "current_agent": None,
            "history": [],           # Lista de turns [(user, agent, ...)]
            # Puedes añadir aquí slots globales de la conversación (agenda, última consulta, etc).
        }

    def push_history(self, user_id: str, entry: Dict[str, Any]) -> None:
        """Añade un turno/entrada al historial del usuario (útil para debugging o reset inteligente)."""
        ctx = self.get_context(user_id)
        ctx.setdefault("history", []).append(entry)
        self.update_context(user_id, ctx)
