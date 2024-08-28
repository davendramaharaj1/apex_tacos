import unittest
from unittest.mock import Mock
from typing import Dict
from python.subscriber import Subscriber
from python.manager import EventManager

class TestEventManager(unittest.TestCase):
    
    def setUp(self):
        self.event_manager = EventManager()
        self.subscriber = Mock(spec=Subscriber) # Mock a subscriber class without a concrete implementation
        self.event = {'id': 1, 'data': 'test event'}

    def test_attach_subscriber(self):
        # Act
        self.event_manager.attach(1, self.subscriber)
        
        # Assert
        self.assertIn(1, self.event_manager._subscribers)
        self.assertIn(self.subscriber, self.event_manager._subscribers[1])

    def test_detach_subscriber(self):
        # Arrange
        self.event_manager.attach(1, self.subscriber)
        
        # Act
        self.event_manager.detach(1, self.subscriber)
        
        # Assert
        self.assertNotIn(1, self.event_manager._subscribers)

    def test_notify_subscribers(self):
        # Arrange
        self.event_manager.attach(1, self.subscriber)
        
        # Act
        self.event_manager.forward_event(self.event)
        
        # Assert
        self.subscriber.update.assert_called_with(self.event)

    def test_notify_finish(self):
        # Arrange
        self.event_manager.attach(1, self.subscriber)
        
        # Act
        self.event_manager.notify_finish(1)
        
        # Assert
        self.subscriber.finish.assert_called()
        self.assertNotIn(1, self.event_manager._subscribers)

if __name__ == "__main__":
    unittest.main()
