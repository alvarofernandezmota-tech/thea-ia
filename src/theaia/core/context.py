# src/theaia/core/context.py

from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class UserContext:
    user_id: str
    session_id: str
    state: Optional[str] = None                # Estado actual en el FSM
    last_action: Optional[str] = None          # Última acción realizada
    slots: Dict[str, Any] = field(default_factory=dict)   # Slots conversacionales (nombre, fecha, etc)
    memory: Dict[str, Any] = field(default_factory=dict)  # Datos persistentes/largo plazo
    history: list = field(default_factory=list)           # Historial de turnos e interacciones

    def set_slot(self, key: str, value: Any):
        self.slots[key] = value

    def get_slot(self, key: str) -> Any:
        return self.slots.get(key)

    def clear_slots(self):
        self.slots.clear()

    def add_to_history(self, interaction: Dict[str, Any]):
        self.history.append(interaction)

    def get_history(self, n: int = 10) -> list:
        return self.history[-n:]

    def set_state(self, state: str):
        self.state = state

    def get_state(self) -> Optional[str]:
        return self.state

    def store_memory(self, key: str, value: Any):
        self.memory[key] = value

    def get_memory(self, key: str) -> Any:
        return self.memory.get(key)

if __name__ == "__main__":
    ctx = UserContext(user_id="U001", session_id="S001")
    ctx.set_slot('nombre', 'Alvaro')
    ctx.set_state('AGENDA')
    ctx.add_to_history({'user': 'Alvaro', 'action': 'Creó Evento'})
    print(ctx)
