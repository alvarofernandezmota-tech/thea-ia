"""
Advanced Message Broker
Sistema avanzado de broker de mensajes con routing, filtering y persistence.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from collections import defaultdict
import uuid


class BrokerMessageType(Enum):
    """Tipos de mensajes en el broker"""
    DIRECT = "direct"
    TOPIC = "topic"
    FANOUT = "fanout"


@dataclass
class BrokerMessage:
    """Mensaje en el broker"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    message_type: BrokerMessageType = BrokerMessageType.DIRECT
    topic: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    headers: Dict[str, str] = field(default_factory=dict)


class AdvancedMessageBroker:
    """Broker avanzado de mensajes con routing y filtering"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._topic_subscribers: Dict[str, List[str]] = defaultdict(list)
        self._message_history: List[BrokerMessage] = []
        self._max_history = 1000
        self._filters: List[Callable] = []
    
    def subscribe(self, topic: str, subscriber_id: str, callback: Callable) -> bool:
        """Suscribirse a un topic"""
        if subscriber_id not in self._topic_subscribers[topic]:
            self._topic_subscribers[topic].append(subscriber_id)
            self._subscribers[f"{topic}:{subscriber_id}"] = [callback]
            return True
        return False
    
    def unsubscribe(self, topic: str, subscriber_id: str) -> bool:
        """Desuscribirse de un topic"""
        if subscriber_id in self._topic_subscribers[topic]:
            self._topic_subscribers[topic].remove(subscriber_id)
            key = f"{topic}:{subscriber_id}"
            if key in self._subscribers:
                del self._subscribers[key]
            return True
        return False
    
    def publish(
        self,
        sender: str,
        message_type: BrokerMessageType,
        topic: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ) -> BrokerMessage:
        """Publicar mensaje"""
        message = BrokerMessage(
            sender=sender,
            message_type=message_type,
            topic=topic,
            payload=payload,
            headers=headers or {}
        )
        
        if not self._apply_filters(message):
            return message
        
        self._add_to_history(message)
        self._route_message(message)
        
        return message
    
    def _route_message(self, message: BrokerMessage) -> None:
        """Rutear mensaje según tipo"""
        if message.message_type == BrokerMessageType.DIRECT:
            self._route_direct(message)
        elif message.message_type == BrokerMessageType.TOPIC:
            self._route_topic(message)
        elif message.message_type == BrokerMessageType.FANOUT:
            self._route_fanout(message)
    
    def _route_direct(self, message: BrokerMessage) -> None:
        """Routing directo"""
        key = f"{message.topic}:{message.payload.get('receiver')}"
        if key in self._subscribers:
            for callback in self._subscribers[key]:
                try:
                    callback(message)
                except Exception:
                    pass
    
    def _route_topic(self, message: BrokerMessage) -> None:
        """Routing por topic"""
        if message.topic in self._topic_subscribers:
            for subscriber_id in self._topic_subscribers[message.topic]:
                key = f"{message.topic}:{subscriber_id}"
                if key in self._subscribers:
                    for callback in self._subscribers[key]:
                        try:
                            callback(message)
                        except Exception:
                            pass
    
    def _route_fanout(self, message: BrokerMessage) -> None:
        """Routing fanout (broadcast)"""
        for callbacks in self._subscribers.values():
            for callback in callbacks:
                try:
                    callback(message)
                except Exception:
                    pass
    
    def add_filter(self, filter_func: Callable[[BrokerMessage], bool]) -> None:
        """Agregar filtro de mensajes"""
        self._filters.append(filter_func)
    
    def _apply_filters(self, message: BrokerMessage) -> bool:
        """Aplicar filtros al mensaje"""
        for filter_func in self._filters:
            try:
                if not filter_func(message):
                    return False
            except Exception:
                return False
        return True
    
    def _add_to_history(self, message: BrokerMessage) -> None:
        """Agregar mensaje al historial"""
        self._message_history.append(message)
        if len(self._message_history) > self._max_history:
            self._message_history = self._message_history[-self._max_history:]
    
    def get_history(self, limit: int = 100) -> List[BrokerMessage]:
        """Obtener historial de mensajes"""
        return self._message_history[-limit:]
    
    def get_subscribers(self, topic: str) -> List[str]:
        """Obtener suscriptores de un topic"""
        return self._topic_subscribers.get(topic, []).copy()
    
    def get_statistics(self) -> Dict[str, int]:
        """Obtener estadísticas del broker"""
        return {
            "total_messages": len(self._message_history),
            "total_topics": len(self._topic_subscribers),
            "total_subscribers": sum(len(subs) for subs in self._topic_subscribers.values())
        }
