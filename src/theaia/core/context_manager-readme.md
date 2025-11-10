ContextManager — Gestor Centralizado de Contextos
Versión: v1.0
Ubicación: src/theaia/core/context_manager.py
Última actualización: 2025-11-10 16:30 CET (S38)

📖 Overview
ContextManager es el gestor centralizado que almacena y gestiona el contexto de todos los usuarios.

Responsabilidades:

Crear/recuperar contextos por user_id

Actualizar contextos con nuevos datos

Limpiar contextos (logout)

Mantener sesiones activas

🔑 Clase Principal
python
class ContextManager:
    def __init__(self, storage_backend='memory'):
        self.storage = self._init_storage(storage_backend)
        # v1.0: Memory (Dict)
        # v1.1: Redis
        # v1.2: PostgreSQL + Redis
    
    def get_or_create(self, user_id: str) → UserContext
    def update(self, user_id: str, context: Dict)
    def clear(self, user_id: str)
    def get_active_sessions() → List[str]
📋 Métodos
get_or_create(user_id)
python
ctx = context_manager.get_or_create("alvaro_123")
# Si no existe: crea nuevo
# Si existe: retorna existente
update(user_id, context)
python
context_manager.update("alvaro_123", {
    'current_state': 'agent_delegated',
    'slots': {'meeting_date': '2025-11-15'}
})
clear(user_id)
python
context_manager.clear("alvaro_123")  # Logout
get_active_sessions()
python
active = context_manager.get_active_sessions()
# Retorna: ["user1", "user2", "user3"]
🔌 Storage Backends
Backend	v	Storage	Persistencia
memory	1.0	Dict	No
redis	1.1	Redis cluster	SÍ (TTL 30min)
postgres	1.2	PostgreSQL + Redis	SÍ (permanente)
💡 Ejemplo
python
from src.theaia.core.context_manager import ContextManager

mgr = ContextManager(storage_backend='memory')

# Get or create
ctx = mgr.get_or_create("alvaro_123")

# Update
mgr.update("alvaro_123", {
    'slots': {'meeting_date': '2025-11-15'}
})

# Get active
users = mgr.get_active_sessions()
print(f"Active users: {users}")

# Clear (logout)
mgr.clear("alvaro_123")
Última actualización: 2025-11-10 16:30 CET