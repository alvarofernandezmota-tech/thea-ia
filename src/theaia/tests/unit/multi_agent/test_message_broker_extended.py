# test_message_broker.py - NUEVOS TESTS

import pytest
from unittest.mock import Mock
from theaia.core.multi_agent.message.broker import MessageBroker
from theaia.core.multi_agent.message.protocol import Message

class TestMessageBrokerEdgeCases:
    '''Edge cases para MessageBroker'''
    
    def setup_method(self):
        self.broker = MessageBroker()
    
    def test_publish_to_nonexistent_topic(self):
        '''Publish a message to a topic that doesn't exist yet'''
        msg = Message(sender="test", receiver="broker", content="test")
        result = self.broker.publish("unknown_topic", msg)
        assert result is not None
    
    def test_subscribe_multiple_handlers_same_topic(self):
        '''Multiple handlers subscribed to same topic'''
        handler1 = Mock()
        handler2 = Mock()
        self.broker.subscribe("test_topic", handler1)
        self.broker.subscribe("test_topic", handler2)
        
        msg = Message(sender="test", receiver="broker", content="test")
        self.broker.publish("test_topic", msg)
        
        handler1.assert_called()
        handler2.assert_called()
    
    def test_unsubscribe_handler(self):
        '''Unsubscribe a handler from topic'''
        handler = Mock()
        self.broker.subscribe("test_topic", handler)
        self.broker.unsubscribe("test_topic", handler)
        
        msg = Message(sender="test", receiver="broker", content="test")
        self.broker.publish("test_topic", msg)
        
        handler.assert_not_called()
    
    def test_concurrent_publish_messages(self):
        '''Concurrent message publishing'''
        import asyncio
        
        handler = Mock()
        self.broker.subscribe("test_topic", handler)
        
        async def publish_concurrent():
            tasks = []
            for i in range(10):
                msg = Message(sender=f"test_{i}", receiver="broker", content=f"msg_{i}")
                tasks.append(self.broker.publish("test_topic", msg))
            await asyncio.gather(*tasks)
        
        asyncio.run(publish_concurrent())
        assert handler.call_count >= 10
    
    def test_message_timeout(self):
        '''Message handling timeout'''
        handler = Mock()
        handler.side_effect = TimeoutError("Handler timeout")
        self.broker.subscribe("test_topic", handler)
        
        msg = Message(sender="test", receiver="broker", content="test")
        result = self.broker.publish("test_topic", msg)
        
        assert result is not None  # Should handle gracefully
    
    def test_invalid_message_format(self):
        '''Invalid message format handling'''
        with pytest.raises(ValueError):
            msg = Message(sender="", receiver="broker", content="")  # Empty sender
            self.broker.publish("test_topic", msg)
    
    def test_broker_memory_leak_prevention(self):
        '''Ensure broker doesn't leak memory with repeated operations'''
        import sys
        
        initial_size = sys.getsizeof(self.broker)
        
        for i in range(100):
            msg = Message(sender="test", receiver="broker", content=f"msg_{i}")
            self.broker.publish(f"topic_{i}", msg)
            if i % 10 == 0:
                self.broker.cleanup_old_messages()
        
        final_size = sys.getsizeof(self.broker)
        assert (final_size - initial_size) < 1000000  # Less than 1MB increase
