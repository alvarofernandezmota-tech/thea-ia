"""Message protocol for validation and serialization."""
import json
from typing import Any, Callable, Dict, Optional
from .types import Message, MessageType, MessageStatus


class MessageProtocol:
    """Handles message validation and serialization."""
    
    PROTOCOL_VERSION = "1.0"
    
    def __init__(self):
        """Initialize protocol."""
        self._validators: Dict[str, Callable] = {}
        self._serializers: Dict[str, Callable] = {}

    def serialize(self, message: Message, format: str = "json") -> str:
        """Serialize message to string."""
        if format == "json":
            data = message.to_dict()
            data["protocol_version"] = self.PROTOCOL_VERSION
            return json.dumps(data)
        
        # Check custom serializers
        if format in self._serializers:
            return self._serializers[format](message)
        
        raise ValueError(f"Unsupported serialization format: {format}")

    def deserialize(self, data: str, format: str = "json") -> Message:
        """Deserialize message from string."""
        if format == "json":
            parsed = json.loads(data)
            # Remove protocol version before creating message
            parsed.pop("protocol_version", None)
            return Message.from_dict(parsed)
        
        raise ValueError(f"Unsupported deserialization format: {format}")

    def validate(self, message: Message) -> bool:
        """Validate message."""
        # Basic validations
        if not message.sender_id:
            return False
        
        if message.message_type == MessageType.RESPONSE and not message.correlation_id:
            return False
        
        # Check if expired (by checking both property and status)
        if message.is_expired or message.status == MessageStatus.EXPIRED:
            return False
        
        # Run custom validators
        for validator in self._validators.values():
            if not validator(message):
                return False
        
        return True

    def register_validator(self, name: str, validator: Callable[[Message], bool]) -> None:
        """Register custom validator."""
        self._validators[name] = validator

    def register_serializer(self, format: str, serializer: Callable[[Message], str]) -> None:
        """Register custom serializer."""
        self._serializers[format] = serializer

    def create_response(
        self,
        request: Message,
        payload: Dict[str, Any],
        success: bool = True
    ) -> Message:
        """Create response message from request."""
        return Message(
            message_type=MessageType.RESPONSE,
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
            payload=payload,
            priority=request.priority,
            correlation_id=request.message_id,
            status=MessageStatus.PENDING if success else MessageStatus.FAILED,
        )
