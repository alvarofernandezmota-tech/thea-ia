from typing import Tuple, Dict, Any, Optional
from src.theaia.database.repositories.context_repository import load_context, save_context
from src.theaia.agents.agenda_agent import AgendaAgent
from src.theaia.agents.notas_agent import NotasAgent
from src.theaia.agents.fallback_agent import FallbackAgent

class Router:
    def __init__(self):
        self.agents = {
            'agenda': AgendaAgent(),
            'notas': NotasAgent(),
            'fallback': FallbackAgent()
        }
    
    def process_message(self, user_id: str, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """
        Procesa un mensaje de usuario y retorna respuesta, nuevo estado y datos
        """
        # 1. Cargar contexto existente
        context = load_context(user_id)
        current_state = context['state'] if context else 'initial'
        current_data = context['data'] if context else {}
        
        # 2. Detectar intención (simplificado por ahora)
        intent = self._detect_intent(message)
        
        # 3. Seleccionar agente apropiado
        agent = self._select_agent(intent, current_state)
        
        # 4. Procesar mensaje con el agente seleccionado
        response, new_state, new_data = agent.process(
            user_id=user_id,
            message=message,
            current_state=current_state,
            current_data=current_data
        )
        
        # 5. Guardar nuevo contexto
        save_context(user_id, new_state, new_data)
        
        return response, new_state, new_data
    
    def _detect_intent(self, message: str) -> str:
        """
        Detecta la intención del mensaje (versión simplificada)
        """
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['cita', 'agendar', 'reunión', 'meeting']):
            return 'agenda'
        elif any(word in message_lower for word in ['nota', 'recordar', 'apuntar']):
            return 'notas'
        else:
            return 'unknown'
    
    def _select_agent(self, intent: str, current_state: str) -> Any:
        """
        Selecciona el agente apropiado basado en intención y estado
        """
        if intent in self.agents:
            return self.agents[intent]
        else:
            return self.agents['fallback']
