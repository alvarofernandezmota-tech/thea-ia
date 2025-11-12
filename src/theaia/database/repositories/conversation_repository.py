"""
Conversation Repository para THEA IA
Gestión de sesiones FSM (Finite State Machine)

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02 - Database Layer
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.models.conversation import Conversation


class ConversationRepository(BaseRepository[Conversation]):
    """
    Repository para operaciones CRUD de conversaciones FSM.
    
    Extiende BaseRepository con métodos específicos para FSM:
    - get_by_session_id(): Obtener conversación por session_id único
    - get_or_create(): Obtener o crear conversación
    - update_state(): Cambiar estado FSM + context
    - get_active(): Conversaciones activas del usuario
    - close_conversation(): Cerrar conversación
    - update_activity(): Actualizar last_activity
    - get_by_state(): Conversaciones en un estado específico
    
    Example:
        async with get_db() as session:
            conv_repo = ConversationRepository(session)
            conv = await conv_repo.get_or_create(
                user_id=1, tenant_id="default", session_id="tg_123456"
            )
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa ConversationRepository.
        
        Args:
            session: AsyncSession de SQLAlchemy
        """
        super().__init__(Conversation, session)
    
    async def get_by_session_id(
        self,
        session_id: str,
        tenant_id: str
    ) -> Optional[Conversation]:
        """
        Obtiene una conversación por su session_id único.
        
        Args:
            session_id: ID único de la sesión (ej: "telegram_{chat_id}")
            tenant_id: ID del tenant
        
        Returns:
            Conversación encontrada o None
        
        Example:
            conv = await conv_repo.get_by_session_id("telegram_123456", "default")
        """
        stmt = select(Conversation).where(
            Conversation.session_id == session_id,
            Conversation.tenant_id == tenant_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_or_create(
        self,
        user_id: int,
        tenant_id: str,
        session_id: str,
        initial_state: str = "idle"
    ) -> tuple[Conversation, bool]:
        """
        Obtiene una conversación existente o la crea.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            session_id: ID único de la sesión
            initial_state: Estado inicial si se crea (default "idle")
        
        Returns:
            Tuple (Conversation, created: bool)
            - Conversation: Conversación encontrada o creada
            - created: True si fue creada, False si ya existía
        
        Example:
            conv, created = await conv_repo.get_or_create(
                user_id=1,
                tenant_id="default",
                session_id="telegram_123456",
                initial_state="idle"
            )
            if created:
                print("Nueva conversación iniciada")
        """
        # Intentar obtener conversación existente
        conversation = await self.get_by_session_id(session_id, tenant_id)
        
        if conversation:
            # Actualizar actividad
            conversation.last_activity = datetime.now(timezone.utc)
            await self.session.flush()
            await self.session.refresh(conversation)
            return conversation, False
        
        # Crear nueva conversación
        now = datetime.now(timezone.utc)
        conversation = await self.create(
            user_id=user_id,
            tenant_id=tenant_id,
            session_id=session_id,
            current_state=initial_state,
            is_active=True,
            started_at=now,
            last_activity=now,
            context_data={}
        )
        
        return conversation, True
    
    async def update_state(
        self,
        conversation_id: int,
        tenant_id: str,
        new_state: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Conversation]:
        """
        Actualiza el estado FSM y opcionalmente el contexto.
        
        Args:
            conversation_id: ID de la conversación
            tenant_id: ID del tenant
            new_state: Nuevo estado FSM
            context: Contexto adicional a mergear (opcional)
        
        Returns:
            Conversación actualizada o None
        
        Example:
            # Cambiar a estado "awaiting_confirmation"
            conv = await conv_repo.update_state(
                conversation_id=5,
                tenant_id="default",
                new_state="awaiting_confirmation",
                context={"action": "create_event", "title": "Reunión"}
            )
        """
        conversation = await self.get_by_id(conversation_id, tenant_id)
        if not conversation:
            return None
        
        # Actualizar estado
        conversation.current_state = new_state
        conversation.last_activity = datetime.now(timezone.utc)
        
        # Mergear contexto si se proporciona
        if context:
            current_context = conversation.context_data or {}
            current_context.update(context)
            conversation.context_data = current_context
        
        await self.session.flush()
        await self.session.refresh(conversation)
        return conversation
    
    async def get_active(
        self,
        user_id: int,
        tenant_id: str
    ) -> List[Conversation]:
        """
        Obtiene todas las conversaciones activas del usuario.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Lista de conversaciones activas
        
        Example:
            active = await conv_repo.get_active(1, "default")
            print(f"Conversaciones activas: {len(active)}")
        """
        stmt = select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.tenant_id == tenant_id,
            Conversation.is_active == True
        ).order_by(Conversation.last_activity.desc())
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def close_conversation(
        self,
        conversation_id: int,
        tenant_id: str,
        final_state: str = "closed"
    ) -> Optional[Conversation]:
        """
        Cierra una conversación (marca como inactiva).
        
        Args:
            conversation_id: ID de la conversación
            tenant_id: ID del tenant
            final_state: Estado final (default "closed")
        
        Returns:
            Conversación cerrada o None
        
        Example:
            conv = await conv_repo.close_conversation(5, "default")
        """
        conversation = await self.get_by_id(conversation_id, tenant_id)
        if not conversation:
            return None
        
        conversation.is_active = False
        conversation.current_state = final_state
        conversation.last_activity = datetime.now(timezone.utc)
        
        await self.session.flush()
        await self.session.refresh(conversation)
        return conversation
    
    async def update_activity(
        self,
        conversation_id: int,
        tenant_id: str,
        message_id: Optional[str] = None
    ) -> Optional[Conversation]:
        """
        Actualiza last_activity y opcionalmente last_message_id.
        
        Args:
            conversation_id: ID de la conversación
            tenant_id: ID del tenant
            message_id: ID del último mensaje (opcional)
        
        Returns:
            Conversación actualizada o None
        
        Example:
            conv = await conv_repo.update_activity(5, "default", message_id="msg_123")
        """
        conversation = await self.get_by_id(conversation_id, tenant_id)
        if not conversation:
            return None
        
        conversation.last_activity = datetime.now(timezone.utc)
        
        if message_id:
            conversation.last_message_id = message_id
        
        await self.session.flush()
        await self.session.refresh(conversation)
        return conversation
    
    async def get_by_state(
        self,
        tenant_id: str,
        state: str,
        active_only: bool = True
    ) -> List[Conversation]:
        """
        Obtiene conversaciones en un estado específico.
        
        Args:
            tenant_id: ID del tenant
            state: Estado FSM a buscar
            active_only: Si True, solo conversaciones activas
        
        Returns:
            Lista de conversaciones en ese estado
        
        Example:
            # Conversaciones esperando confirmación
            waiting = await conv_repo.get_by_state(
                "default", 
                "awaiting_confirmation"
            )
        """
        stmt = select(Conversation).where(
            Conversation.tenant_id == tenant_id,
            Conversation.current_state == state
        )
        
        if active_only:
            stmt = stmt.where(Conversation.is_active == True)
        
        stmt = stmt.order_by(Conversation.last_activity.desc())
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_inactive_since(
        self,
        tenant_id: str,
        minutes: int = 30
    ) -> List[Conversation]:
        """
        Obtiene conversaciones inactivas hace X minutos.
        
        Útil para timeout automático de conversaciones.
        
        Args:
            tenant_id: ID del tenant
            minutes: Minutos de inactividad
        
        Returns:
            Lista de conversaciones inactivas
        
        Example:
            # Conversaciones sin actividad en 30 minutos
            inactive = await conv_repo.get_inactive_since("default", minutes=30)
            
            # Cerrarlas automáticamente
            for conv in inactive:
                await conv_repo.close_conversation(conv.id, "default", "timeout")
        """
        threshold = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        
        stmt = select(Conversation).where(
            Conversation.tenant_id == tenant_id,
            Conversation.is_active == True,
            Conversation.last_activity < threshold
        )
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def clear_context(
        self,
        conversation_id: int,
        tenant_id: str
    ) -> Optional[Conversation]:
        """
        Limpia el contexto de una conversación.
        
        Args:
            conversation_id: ID de la conversación
            tenant_id: ID del tenant
        
        Returns:
            Conversación actualizada o None
        
        Example:
            conv = await conv_repo.clear_context(5, "default")
        """
        conversation = await self.get_by_id(conversation_id, tenant_id)
        if not conversation:
            return None
        
        conversation.context_data = {}
        
        await self.session.flush()
        await self.session.refresh(conversation)
        return conversation
    
    async def count_by_state(
        self,
        tenant_id: str,
        active_only: bool = True
    ) -> Dict[str, int]:
        """
        Cuenta conversaciones por estado.
        
        Args:
            tenant_id: ID del tenant
            active_only: Si True, solo conversaciones activas
        
        Returns:
            Dict con estado: count
        
        Example:
            counts = await conv_repo.count_by_state("default")
            # {"idle": 10, "awaiting_confirmation": 3, "processing": 1}
        """
        from sqlalchemy import func
        
        stmt = select(
            Conversation.current_state,
            func.count(Conversation.id)
        ).where(
            Conversation.tenant_id == tenant_id
        )
        
        if active_only:
            stmt = stmt.where(Conversation.is_active == True)
        
        stmt = stmt.group_by(Conversation.current_state)
        
        result = await self.session.execute(stmt)
        return {state: count for state, count in result.all()}
