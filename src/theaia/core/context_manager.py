from typing import Dict, Optional
from src.theaia.core.context import UserContext

class ContextManager:
    """Gestiona todos los contextos de usuario/sesión para Thea IA 2.0."""
    def __init__(self):
        self._contexts: Dict[str, UserContext] = {}

    def create_context(self, user_id: str, session_id: str) -> UserContext:
        context = UserContext(user_id=user_id, session_id=session_id)
        self._contexts[session_id] = context
        return context

    def get_context(self, session_id: str) -> Optional[UserContext]:
        return self._contexts.get(session_id)

    def save_context(self, context: UserContext):
        self._contexts[context.session_id] = context

    def delete_context(self, session_id: str):
        if session_id in self._contexts:
            del self._contexts[session_id]
            return True
        return False

    def list_contexts(self) -> Dict[str, UserContext]:
        return self._contexts

if __name__ == "__main__":
    mgr = ContextManager()
    ctx = mgr.create_context("U100", "S200")
    mgr.save_context(ctx)
    print(mgr.get_context("S200"))
    mgr.delete_context("S200")
    print(mgr.list_contexts())
