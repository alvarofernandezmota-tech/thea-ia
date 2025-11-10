Context — User Conversation Context Data Structure
Versión: v1.0
Ubicación: src/theaia/core/context.py
Última actualización: 2025-11-10 16:20 CET (S38)

📖 Overview
UserContext es la estructura de datos que almacena todo el estado de conversación de un usuario.

Responsabilidades:

Almacenar user_id + session_id

Rastrear estado actual + histórico

Mantener slots (datos específicos del dominio)

Guardar message history + intents

Metadata (idioma, timezone, preferencias)

🔑 Clase Principal
python
@dataclass
class UserContext:
    user_id: str
    session_id: str
    created_at: datetime
    current_state: str = "initial"
    
    # History
    message_history: List[Dict] = field(default_factory=list)
    intent_history: List[str] = field(default_factory=list)
    
    # State tracking
    previous_states: List[str] = field(default_factory=list)
    state_transitions: List[Dict] = field(default_factory=list)
    
    # Domain data (slots)
    slots: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    language: str = "es"
    timezone: str = "Europe/Madrid"
    preferences: Dict = field(default_factory=dict)
    last_activity: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) → Dict:
        """Serializar a dict."""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) → UserContext:
        """Deserializar desde dict."""
        return UserContext(**data)
📊 Slots Típicos
python
context.slots = {
    # Agenda
    'meeting_date': '2025-11-15',
    'meeting_time': '14:30',
    'meeting_participants': ['user1@email.com'],
    'meeting_description': 'Reunión importante',
    
    # Notas
    'note_text': 'Tarea pendiente',
    'note_tags': ['trabajo', 'urgente'],
    
    # Recordatorio
    'reminder_message': 'Llamar cliente',
    'reminder_frequency': 'diaria',
    'reminder_priority': 5,
    
    # General
    'original_message': 'Quiero agendar...',
    'disamb_retries': 0,
}
💡 Ejemplo
python
context = UserContext(
    user_id="alvaro_123",
    session_id="sess_abc123",
    created_at=datetime.now()
)

context.slots['meeting_date'] = '2025-11-15'
context.message_history.append({
    'role': 'user',
    'content': 'Agendar reunión',
    'timestamp': datetime.now()
})

print(context.to_dict())
Última actualización: 2025-11-10 16:20 CET