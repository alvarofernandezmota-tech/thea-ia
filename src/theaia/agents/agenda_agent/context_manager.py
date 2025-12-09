"""
ConversationContextManager - Gestor de contexto conversacional multi-turn

Mantiene el historial de conversación y entidades extraídas para:
- Multi-turn interactions (clarificaciones, actualizaciones)
- Reutilizar información previa
- Mantener estado de la conversación
- Manejar flujos complejos (crear evento → agregar participantes → cambiar hora)

Autor: Álvaro Fernández Mota
Fecha: 09 Dic 2025
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Representa un mensaje en la conversación"""
    text: str
    timestamp: datetime
    intent: str
    confidence: float
    entities: Dict[str, Any]
    response: Optional[str] = None


@dataclass
class ExtractedEntities:
    """Entidades extraídas del mensaje actual"""
    title: Optional[str] = None
    date: Optional[datetime] = None
    time: Optional[str] = None
    participants: List[str] = field(default_factory=list)
    location: Optional[str] = None
    duration: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            "title": self.title,
            "date": self.date,
            "time": self.time,
            "participants": self.participants,
            "location": self.location,
            "duration": self.duration,
        }
    
    def merge(self, other: "ExtractedEntities") -> "ExtractedEntities":
        """Mezcla dos conjuntos de entidades (prioriza las nuevas)"""
        return ExtractedEntities(
            title=other.title or self.title,
            date=other.date or self.date,
            time=other.time or self.time,
            participants=list(set(other.participants + self.participants)) if other.participants else self.participants,
            location=other.location or self.location,
            duration=other.duration or self.duration,
        )


class ConversationContext:
    """
    Gestor de contexto para conversaciones multi-turn.
    
    Mantiene:
    - Historial de mensajes
    - Entidades acumuladas
    - Estado actual
    - Información de usuario
    
    Ejemplo de uso:
        context = ConversationContext(user_id="user123")
        
        # Turno 1: Usuario quiere crear evento
        context.add_message(
            text="Quiero agendar una reunión",
            intent="create_event",
            confidence=0.95
        )
        
        # Turno 2: Agrega detalles
        context.add_message(
            text="mañana a las 3pm con Juan",
            intent="create_event",
            confidence=0.98,
            entities={"date": datetime(...), "time": "15:00", "participants": ["Juan"]}
        )
        
        # Obtener entidades acumuladas
        all_entities = context.get_accumulated_entities()
        # → {"date": datetime(...), "time": "15:00", "participants": ["Juan"]}
    """
    
    def __init__(self, user_id: str, max_history: int = 10):
        """
        Inicializa el contexto.
        
        Args:
            user_id: ID único del usuario
            max_history: Máximo de mensajes a mantener en historial
        """
        self.user_id = user_id
        self.max_history = max_history
        
        # Historial y entidades
        self.messages: List[Message] = []
        self.accumulated_entities = ExtractedEntities()
        
        # Estado actual
        self.current_intent: Optional[str] = None
        self.current_action: Optional[str] = None
        self.current_state: str = "idle"  # idle, gathering_info, confirming, executing
        
        # Información de usuario
        self.user_data: Dict[str, Any] = {}
        
        # Sesión
        self.session_start = datetime.now()
        self.last_activity = datetime.now()
    
    def add_message(
        self,
        text: str,
        intent: str,
        confidence: float,
        entities: Optional[Dict[str, Any]] = None,
        response: Optional[str] = None
    ) -> None:
        """
        Agrega un mensaje a la conversación.
        
        Args:
            text: Texto del mensaje
            intent: Intent detectado
            confidence: Confianza del intent (0.0-1.0)
            entities: Entidades extraídas
            response: Respuesta del agente (opcional)
        """
        message = Message(
            text=text,
            timestamp=datetime.now(),
            intent=intent,
            confidence=confidence,
            entities=entities or {},
            response=response
        )
        
        self.messages.append(message)
        self.last_activity = datetime.now()
        
        # Actualizar intent actual
        self.current_intent = intent
        
        # Acumular entidades
        if entities:
            extracted = ExtractedEntities(**{k: v for k, v in entities.items() if k in ExtractedEntities.__dataclass_fields__})
            self.accumulated_entities = self.accumulated_entities.merge(extracted)
        
        # Mantener límite de historial
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        
        logger.debug(f"Message added for user {self.user_id}: intent={intent}, confidence={confidence}")
    
    def get_last_message(self) -> Optional[Message]:
        """Obtiene el último mensaje"""
        return self.messages[-1] if self.messages else None
    
    def get_last_n_messages(self, n: int = 3) -> List[Message]:
        """Obtiene los últimos N mensajes"""
        return self.messages[-n:] if self.messages else []
    
    def get_conversation_history(self) -> str:
        """Retorna historial completo como string formateado"""
        if not self.messages:
            return "No hay historial de conversación"
        
        history = []
        for msg in self.messages:
            history.append(f"[{msg.timestamp.strftime('%H:%M:%S')}] Usuario: {msg.text}")
            if msg.response:
                history.append(f"[{msg.timestamp.strftime('%H:%M:%S')}] Agente: {msg.response}")
        
        return "\n".join(history)
    
    def get_accumulated_entities(self) -> Dict[str, Any]:
        """Obtiene todas las entidades acumuladas en la conversación"""
        return self.accumulated_entities.to_dict()
    
    def get_missing_fields(self, required_fields: List[str]) -> List[str]:
        """
        Identifica qué campos requeridos están faltando.
        
        Args:
            required_fields: Lista de campos requeridos (e.g., ["title", "date", "time"])
            
        Returns:
            Lista de campos faltantes
        """
        missing = []
        entities_dict = self.accumulated_entities.to_dict()
        
        for field in required_fields:
            value = entities_dict.get(field)
            if value is None or (isinstance(value, list) and len(value) == 0):
                missing.append(field)
        
        return missing
    
    def set_state(self, state: str) -> None:
        """
        Actualiza el estado de la conversación.
        
        Estados válidos:
        - "idle": Esperando entrada del usuario
        - "gathering_info": Recolectando información (faltan campos)
        - "confirming": Pidiendo confirmación
        - "executing": Ejecutando la acción
        """
        valid_states = ["idle", "gathering_info", "confirming", "executing"]
        if state not in valid_states:
            logger.warning(f"Invalid state: {state}")
            return
        
        self.current_state = state
        logger.debug(f"State changed for user {self.user_id}: {state}")
    
    def set_action(self, action: str) -> None:
        """Establece la acción actual"""
        self.current_action = action
        logger.debug(f"Action set for user {self.user_id}: {action}")
    
    def update_accumulated_entities(self, **kwargs) -> None:
        """Actualiza entidades acumuladas manualmente"""
        for key, value in kwargs.items():
            if hasattr(self.accumulated_entities, key):
                setattr(self.accumulated_entities, key, value)
    
    def clear_context(self) -> None:
        """Limpia el contexto para comenzar una nueva conversación"""
        self.messages = []
        self.accumulated_entities = ExtractedEntities()
        self.current_intent = None
        self.current_action = None
        self.current_state = "idle"
        logger.info(f"Context cleared for user {self.user_id}")
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Retorna un resumen del contexto actual"""
        return {
            "user_id": self.user_id,
            "current_intent": self.current_intent,
            "current_action": self.current_action,
            "current_state": self.current_state,
            "message_count": len(self.messages),
            "accumulated_entities": self.accumulated_entities.to_dict(),
            "session_duration": (datetime.now() - self.session_start).total_seconds(),
        }
    
    def should_clarify(self, required_fields: List[str]) -> bool:
        """Determina si se debe pedir clarificación"""
        missing = self.get_missing_fields(required_fields)
        return len(missing) > 0
    
    def get_clarification_message(self, required_fields: List[str]) -> str:
        """Genera mensaje de clarificación basado en campos faltantes"""
        missing = self.get_missing_fields(required_fields)
        
        if not missing:
            return ""
        
        field_names = {
            "title": "el nombre o título del evento",
            "date": "la fecha",
            "time": "la hora",
            "participants": "los participantes",
            "location": "la ubicación",
            "duration": "la duración",
        }
        
        missing_names = [field_names.get(f, f) for f in missing]
        
        if len(missing_names) == 1:
            return f"¿Podrías especificar {missing_names[0]}?"
        
        missing_str = ", ".join(missing_names[:-1]) + f" y {missing_names[-1]}"
        return f"¿Podrías especificar {missing_str}?"
    
    def log_interaction(self, user_message: str, agent_response: str, metadata: Optional[Dict] = None) -> None:
        """
        Registra una interacción completa (para auditoría/debugging).
        
        Args:
            user_message: Mensaje del usuario
            agent_response: Respuesta del agente
            metadata: Información adicional (intent, entities, etc.)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": self.user_id,
            "user_message": user_message,
            "agent_response": agent_response,
            "metadata": metadata or {},
        }
        
        logger.info(f"Interaction logged: {log_entry}")


class ContextManagerFactory:
    """Factory para crear y gestionar contextos de múltiples usuarios"""
    
    def __init__(self):
        self.contexts: Dict[str, ConversationContext] = {}
    
    def get_or_create_context(self, user_id: str) -> ConversationContext:
        """Obtiene o crea un contexto para un usuario"""
        if user_id not in self.contexts:
            self.contexts[user_id] = ConversationContext(user_id=user_id)
            logger.info(f"Context created for user {user_id}")
        
        return self.contexts[user_id]
    
    def get_context(self, user_id: str) -> Optional[ConversationContext]:
        """Obtiene contexto de un usuario (sin crear si no existe)"""
        return self.contexts.get(user_id)
    
    def remove_context(self, user_id: str) -> None:
        """Elimina contexto de un usuario"""
        if user_id in self.contexts:
            del self.contexts[user_id]
            logger.info(f"Context removed for user {user_id}")
    
    def get_all_active_users(self) -> List[str]:
        """Retorna lista de usuarios con contextos activos"""
        return list(self.contexts.keys())
    
    def cleanup_inactive_contexts(self, timeout_minutes: int = 30) -> None:
        """Limpia contextos inactivos"""
        now = datetime.now()
        inactive_users = []
        
        for user_id, context in self.contexts.items():
            elapsed = (now - context.last_activity).total_seconds() / 60
            if elapsed > timeout_minutes:
                inactive_users.append(user_id)
        
        for user_id in inactive_users:
            self.remove_context(user_id)
            logger.info(f"Cleaned up inactive context for user {user_id}")