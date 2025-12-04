"""
Core Conversation Manager - Gestor de conversaciones multi-turno
Sistema centralizado de gestión de contexto conversacional.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
Arquitectura: TRES (Álvaro + Jarvis + THEA IA)
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import uuid


@dataclass
class ConversationTurn:
    """Representa un turno en la conversación."""
    turn_id: str
    user_message: str
    bot_response: str
    intent: str
    entities: Dict[str, Any]
    timestamp: datetime
    context_snapshot: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationContext:
    """Contexto completo de una conversación."""
    conversation_id: str
    user_id: str
    active_agent: Optional[str]
    state: str
    data: Dict[str, Any]
    turns: List[ConversationTurn]
    created_at: datetime
    updated_at: datetime
    expires_at: datetime


class CoreConversationManager:
    """
    Manager centralizado para gestión de conversaciones multi-turno.
    
    Características:
    - Gestión de contexto por usuario
    - Historial de turnos
    - Timeout automático de sesiones
    - Soporte para múltiples agentes
    - Persistencia de estado entre mensajes
    """
    
    def __init__(
        self, 
        session_timeout_minutes: int = 30,
        max_turns_per_conversation: int = 50
    ):
        """
        Inicializa el conversation manager.
        
        Args:
            session_timeout_minutes: Tiempo antes de expirar sesión
            max_turns_per_conversation: Máximo de turnos guardados
        """
        self.session_timeout_minutes = session_timeout_minutes
        self.max_turns_per_conversation = max_turns_per_conversation
        
        # Storage en memoria (en producción usar Redis/DB)
        self._conversations: Dict[str, ConversationContext] = {}
    
    
    async def get_or_create_conversation(
        self, 
        user_id: str,
        agent_name: Optional[str] = None
    ) -> ConversationContext:
        """
        Obtiene o crea una conversación para un usuario.
        
        Args:
            user_id: ID del usuario
            agent_name: Agente activo (opcional)
            
        Returns:
            ConversationContext
        """
        # Buscar conversación activa
        active_conv = self._find_active_conversation(user_id)
        
        if active_conv:
            # Extender expiración
            active_conv.expires_at = datetime.now() + timedelta(
                minutes=self.session_timeout_minutes
            )
            active_conv.updated_at = datetime.now()
            return active_conv
        
        # Crear nueva conversación
        return await self._create_conversation(user_id, agent_name)
    
    
    async def add_turn(
        self,
        conversation_id: str,
        user_message: str,
        bot_response: str,
        intent: str,
        entities: Dict[str, Any]
    ) -> ConversationTurn:
        """
        Añade un turno a la conversación.
        
        Args:
            conversation_id: ID de la conversación
            user_message: Mensaje del usuario
            bot_response: Respuesta del bot
            intent: Intent detectado
            entities: Entidades extraídas
            
        Returns:
            ConversationTurn creado
        """
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # Crear turno
        turn = ConversationTurn(
            turn_id=str(uuid.uuid4()),
            user_message=user_message,
            bot_response=bot_response,
            intent=intent,
            entities=entities,
            timestamp=datetime.now(),
            context_snapshot=conv.data.copy()
        )
        
        # Añadir turno
        conv.turns.append(turn)
        
        # Limitar número de turnos
        if len(conv.turns) > self.max_turns_per_conversation:
            conv.turns = conv.turns[-self.max_turns_per_conversation:]
        
        # Actualizar timestamps
        conv.updated_at = datetime.now()
        conv.expires_at = datetime.now() + timedelta(
            minutes=self.session_timeout_minutes
        )
        
        return turn
    
    
    async def update_context(
        self,
        conversation_id: str,
        updates: Dict[str, Any]
    ) -> ConversationContext:
        """
        Actualiza el contexto de la conversación.
        
        Args:
            conversation_id: ID de la conversación
            updates: Dict con campos a actualizar
            
        Returns:
            ConversationContext actualizado
        """
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # Actualizar datos
        conv.data.update(updates)
        conv.updated_at = datetime.now()
        
        return conv
    
    
    async def set_active_agent(
        self,
        conversation_id: str,
        agent_name: str
    ) -> ConversationContext:
        """
        Establece el agente activo.
        
        Args:
            conversation_id: ID de la conversación
            agent_name: Nombre del agente
            
        Returns:
            ConversationContext actualizado
        """
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        conv.active_agent = agent_name
        conv.updated_at = datetime.now()
        
        return conv
    
    
    async def change_state(
        self,
        conversation_id: str,
        new_state: str
    ) -> ConversationContext:
        """
        Cambia el estado de la conversación.
        
        Args:
            conversation_id: ID de la conversación
            new_state: Nuevo estado
            
        Returns:
            ConversationContext actualizado
        """
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        conv.state = new_state
        conv.updated_at = datetime.now()
        
        return conv
    
    
    async def get_last_turns(
        self,
        conversation_id: str,
        n: int = 5
    ) -> List[ConversationTurn]:
        """
        Obtiene los últimos N turnos.
        
        Args:
            conversation_id: ID de la conversación
            n: Número de turnos
            
        Returns:
            Lista de turnos
        """
        conv = self._conversations.get(conversation_id)
        if not conv:
            return []
        
        return conv.turns[-n:]
    
    
    async def get_context_value(
        self,
        conversation_id: str,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Obtiene un valor del contexto.
        
        Args:
            conversation_id: ID de la conversación
            key: Clave a buscar
            default: Valor por defecto
            
        Returns:
            Valor encontrado o default
        """
        conv = self._conversations.get(conversation_id)
        if not conv:
            return default
        
        return conv.data.get(key, default)
    
    
    async def clear_conversation(
        self,
        conversation_id: str
    ) -> bool:
        """
        Limpia una conversación.
        
        Args:
            conversation_id: ID de la conversación
            
        Returns:
            True si se limpió correctamente
        """
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False
    
    
    async def cleanup_expired_conversations(self) -> int:
        """
        Limpia conversaciones expiradas.
        
        Returns:
            Número de conversaciones eliminadas
        """
        now = datetime.now()
        expired = [
            conv_id 
            for conv_id, conv in self._conversations.items()
            if conv.expires_at < now
        ]
        
        for conv_id in expired:
            del self._conversations[conv_id]
        
        return len(expired)
    
    
    def _find_active_conversation(self, user_id: str) -> Optional[ConversationContext]:
        """
        Busca conversación activa para un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            ConversationContext o None
        """
        now = datetime.now()
        
        for conv in self._conversations.values():
            if conv.user_id == user_id and conv.expires_at > now:
                return conv
        
        return None
    
    
    async def _create_conversation(
        self,
        user_id: str,
        agent_name: Optional[str]
    ) -> ConversationContext:
        """
        Crea una nueva conversación.
        
        Args:
            user_id: ID del usuario
            agent_name: Agente activo
            
        Returns:
            ConversationContext nuevo
        """
        now = datetime.now()
        
        conv = ConversationContext(
            conversation_id=str(uuid.uuid4()),
            user_id=user_id,
            active_agent=agent_name,
            state="initial",
            data={},
            turns=[],
            created_at=now,
            updated_at=now,
            expires_at=now + timedelta(minutes=self.session_timeout_minutes)
        )
        
        self._conversations[conv.conversation_id] = conv
        
        return conv
    
    
    async def get_conversation_summary(
        self,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Obtiene resumen de la conversación.
        
        Args:
            conversation_id: ID de la conversación
            
        Returns:
            Dict con resumen
        """
        conv = self._conversations.get(conversation_id)
        if not conv:
            return {}
        
        return {
            "conversation_id": conv.conversation_id,
            "user_id": conv.user_id,
            "active_agent": conv.active_agent,
            "state": conv.state,
            "turn_count": len(conv.turns),
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
            "expires_at": conv.expires_at.isoformat(),
            "is_expired": conv.expires_at < datetime.now(),
        }
