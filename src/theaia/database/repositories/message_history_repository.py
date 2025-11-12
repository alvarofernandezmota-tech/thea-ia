"""
MessageHistory Repository para THEA IA
Auditoría de mensajes y análisis ML (intent, entities)

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02 - Database Layer
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.models.message_history import MessageHistory


class MessageHistoryRepository(BaseRepository[MessageHistory]):
    """
    Repository para auditoría de mensajes y análisis ML.
    
    Extiende BaseRepository con métodos específicos para historial:
    - add_message(): Crear registro de mensaje
    - get_recent(): Mensajes recientes de conversación
    - get_conversation_history(): Todo el historial de conversación
    - get_by_intent(): Filtrar por intent detectado
    - get_statistics(): Estadísticas ML (intents, confidence)
    - analyze_performance(): Métricas de rendimiento
    
    Example:
        async with get_db() as session:
            msg_repo = MessageHistoryRepository(session)
            await msg_repo.add_message(
                conversation_id=1,
                tenant_id="default",
                user_message="Quiero crear un evento",
                intent_detected="create_event"
            )
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa MessageHistoryRepository.
        
        Args:
            session: AsyncSession de SQLAlchemy
        """
        super().__init__(MessageHistory, session)
    
    async def add_message(
        self,
        conversation_id: int,
        tenant_id: str,
        message_id: str,
        user_message: Optional[str] = None,
        bot_response: Optional[str] = None,
        intent_detected: Optional[str] = None,
        entities_extracted: Optional[Dict[str, Any]] = None,
        confidence_score: Optional[float] = None,
        processing_time_ms: Optional[int] = None
    ) -> MessageHistory:
        """
        Crea un registro de mensaje en el historial.
        
        Args:
            conversation_id: ID de la conversación
            tenant_id: ID del tenant
            message_id: ID único del mensaje
            user_message: Mensaje del usuario (opcional)
            bot_response: Respuesta del bot (opcional)
            intent_detected: Intent ML detectado (opcional)
            entities_extracted: Entidades NER extraídas (opcional)
            confidence_score: Confianza del modelo ML (0-1)
            processing_time_ms: Tiempo de procesamiento en ms
        
        Returns:
            MessageHistory creado
        
        Example:
            msg = await msg_repo.add_message(
                conversation_id=1,
                tenant_id="default",
                message_id="msg_123",
                user_message="Crear evento mañana a las 15:00",
                bot_response="¿Qué título tiene el evento?",
                intent_detected="create_event",
                entities_extracted={"datetime": "2025-11-13T15:00:00Z"},
                confidence_score=0.95,
                processing_time_ms=120
            )
        """
        return await self.create(
            conversation_id=conversation_id,
            tenant_id=tenant_id,
            message_id=message_id,
            user_message=user_message,
            bot_response=bot_response,
            intent_detected=intent_detected,
            entities_extracted=entities_extracted,
            confidence_score=confidence_score,
            processing_time_ms=processing_time_ms
        )
    
    async def get_recent(
        self,
        conversation_id: int,
        tenant_id: str,
        limit: int = 10
    ) -> List[MessageHistory]:
        """
        Obtiene los N mensajes más recientes de una conversación.
        
        Args:
            conversation_id: ID de la conversación
            tenant_id: ID del tenant
            limit: Número máximo de mensajes (default 10)
        
        Returns:
            Lista de mensajes ordenados por fecha (más reciente primero)
        
        Example:
            # Últimos 10 mensajes
            recent = await msg_repo.get_recent(1, "default", limit=10)
            
            # Context para LLM
            context = "\n".join([
                f"User: {msg.user_message}\nBot: {msg.bot_response}"
                for msg in reversed(recent)
            ])
        """
        stmt = select(MessageHistory).where(
            MessageHistory.conversation_id == conversation_id,
            MessageHistory.tenant_id == tenant_id
        ).order_by(MessageHistory.created_at.desc()).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_conversation_history(
        self,
        conversation_id: int,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[MessageHistory]:
        """
        Obtiene todo el historial de una conversación con paginación.
        
        Args:
            conversation_id: ID de la conversación
            tenant_id: ID del tenant
            skip: Registros a saltar
            limit: Máximo de registros
        
        Returns:
            Lista completa de mensajes ordenados por fecha
        
        Example:
            history = await msg_repo.get_conversation_history(1, "default")
        """
        stmt = select(MessageHistory).where(
            MessageHistory.conversation_id == conversation_id,
            MessageHistory.tenant_id == tenant_id
        ).order_by(MessageHistory.created_at.asc()).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_intent(
        self,
        tenant_id: str,
        intent: str,
        limit: int = 100,
        min_confidence: Optional[float] = None
    ) -> List[MessageHistory]:
        """
        Obtiene mensajes por intent detectado.
        
        Útil para análisis de qué intents son más comunes.
        
        Args:
            tenant_id: ID del tenant
            intent: Intent a buscar (ej: "create_event")
            limit: Máximo de registros
            min_confidence: Confianza mínima (opcional)
        
        Returns:
            Lista de mensajes con ese intent
        
        Example:
            # Todos los "create_event" con confianza > 0.8
            events = await msg_repo.get_by_intent(
                "default", 
                "create_event",
                min_confidence=0.8
            )
        """
        stmt = select(MessageHistory).where(
            MessageHistory.tenant_id == tenant_id,
            MessageHistory.intent_detected == intent
        )
        
        if min_confidence is not None:
            stmt = stmt.where(MessageHistory.confidence_score >= min_confidence)
        
        stmt = stmt.order_by(MessageHistory.created_at.desc()).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_statistics(
        self,
        tenant_id: str,
        hours: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de análisis ML.
        
        Args:
            tenant_id: ID del tenant
            hours: Limitar a últimas X horas (opcional)
        
        Returns:
            Dict con estadísticas:
            - total_messages: Total de mensajes
            - intent_distribution: Dict intent -> count
            - avg_confidence: Confianza promedio
            - avg_processing_time_ms: Tiempo procesamiento promedio
        
        Example:
            stats = await msg_repo.get_statistics("default", hours=24)
            print(f"Confianza promedio: {stats['avg_confidence']:.2f}")
        """
        stmt = select(MessageHistory).where(
            MessageHistory.tenant_id == tenant_id
        )
        
        if hours:
            threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
            stmt = stmt.where(MessageHistory.created_at >= threshold)
        
        result = await self.session.execute(stmt)
        messages = list(result.scalars().all())
        
        if not messages:
            return {
                "total_messages": 0,
                "intent_distribution": {},
                "avg_confidence": 0.0,
                "avg_processing_time_ms": 0
            }
        
        # Intent distribution
        intent_counts = {}
        for msg in messages:
            if msg.intent_detected:
                intent_counts[msg.intent_detected] = intent_counts.get(msg.intent_detected, 0) + 1
        
        # Avg confidence
        confidences = [msg.confidence_score for msg in messages if msg.confidence_score is not None]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Avg processing time
        times = [msg.processing_time_ms for msg in messages if msg.processing_time_ms is not None]
        avg_time = sum(times) / len(times) if times else 0
        
        return {
            "total_messages": len(messages),
            "intent_distribution": intent_counts,
            "avg_confidence": avg_confidence,
            "avg_processing_time_ms": avg_time
        }
    
    async def analyze_performance(
        self,
        tenant_id: str,
        hours: int = 24
    ) -> Dict[str, Any]:
        """
        Analiza rendimiento del sistema ML.
        
        Args:
            tenant_id: ID del tenant
            hours: Últimas X horas
        
        Returns:
            Dict con métricas de rendimiento:
            - messages_per_hour: Mensajes por hora
            - slow_queries: Mensajes lentos (>500ms)
            - low_confidence: Mensajes con confianza baja (<0.5)
            - failed_detections: Sin intent detectado
        
        Example:
            perf = await msg_repo.analyze_performance("default", hours=24)
            if perf["slow_queries"] > 10:
                print("⚠️ Muchos queries lentos")
        """
        threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        stmt = select(MessageHistory).where(
            and_(
                MessageHistory.tenant_id == tenant_id,
                MessageHistory.created_at >= threshold
            )
        )
        
        result = await self.session.execute(stmt)
        messages = list(result.scalars().all())
        
        if not messages:
            return {
                "messages_per_hour": 0,
                "slow_queries": 0,
                "low_confidence": 0,
                "failed_detections": 0
            }
        
        # Messages per hour
        messages_per_hour = len(messages) / hours
        
        # Slow queries (>500ms)
        slow_queries = sum(
            1 for msg in messages 
            if msg.processing_time_ms and msg.processing_time_ms > 500
        )
        
        # Low confidence (<0.5)
        low_confidence = sum(
            1 for msg in messages 
            if msg.confidence_score and msg.confidence_score < 0.5
        )
        
        # Failed detections (no intent)
        failed_detections = sum(
            1 for msg in messages 
            if not msg.intent_detected
        )
        
        return {
            "messages_per_hour": round(messages_per_hour, 2),
            "slow_queries": slow_queries,
            "low_confidence": low_confidence,
            "failed_detections": failed_detections,
            "total_analyzed": len(messages)
        }
    
    async def delete_old_messages(
        self,
        tenant_id: str,
        days: int = 90
    ) -> int:
        """
        Elimina mensajes antiguos (limpieza).
        
        Args:
            tenant_id: ID del tenant
            days: Días de antigüedad (default 90)
        
        Returns:
            Número de mensajes eliminados
        
        Example:
            # Limpiar mensajes de hace más de 90 días
            deleted = await msg_repo.delete_old_messages("default", days=90)
            print(f"Eliminados {deleted} mensajes antiguos")
        """
        threshold = datetime.now(timezone.utc) - timedelta(days=days)
        
        stmt = select(MessageHistory).where(
            and_(
                MessageHistory.tenant_id == tenant_id,
                MessageHistory.created_at < threshold
            )
        )
        
        result = await self.session.execute(stmt)
        old_messages = list(result.scalars().all())
        
        for msg in old_messages:
            await self.session.delete(msg)
        
        return len(old_messages)
