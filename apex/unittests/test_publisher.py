import unittest
from unittest.mock import Mock
from typing import Dict
from python.publisher import Publisher
from python.subscriber import Subscriber


class ConcretePublisher(Publisher):
    def attach(self, id: int, subscriber: Subscriber) -> None:
        if id not in self._subscribers:
            self._subscribers[id] = []
        self._subscribers[id].append(subscriber)

    def detach(self, id: int, subscriber: Subscriber) -> None:
        if id in self._subscribers:
            self._subscribers[id].remove(subscriber)
            if not self._subscribers[id]:
                del self._subscribers[id]

    def notify(self, event: Dict) -> None:
        id = event.get('id')
        if id in self._subscribers:
            for subscriber in self._subscribers[id]:
                subscriber.update(event)

    def notify_finish(self, id: int) -> None:
        if id in self._subscribers:
            for subscriber in self._subscribers[id]:
                subscriber.finish()
                
                # remove subscriber
                self.detach(1, subscriber)

class TestPublisher(unittest.TestCase):
    
    def setUp(self):
        self.publisher = ConcretePublisher()
        self.subscriber = Mock(spec=Subscriber)
        self.event = {'id': 1, 'data': 'test event'}

    def test_attach_subscriber(self):
        # Act
        self.publisher.attach(1, self.subscriber)
        
        # Assert
        self.assertIn(1, self.publisher._subscribers)
        self.assertIn(self.subscriber, self.publisher._subscribers[1])

    def test_detach_subscriber(self):
        # Arrange
        self.publisher.attach(1, self.subscriber)
        
        # Act
        self.publisher.detach(1, self.subscriber)
        
        # Assert
        self.assertNotIn(1, self.publisher._subscribers)

    def test_notify_subscribers(self):
        # Arrange
        self.publisher.attach(1, self.subscriber)
        
        # Act
        self.publisher.notify(self.event)
        
        # Assert
        self.subscriber.update.assert_called_with(self.event)

    def test_notify_finish(self):
        # Arrange
        self.publisher.attach(1, self.subscriber)
        
        # Act
        self.publisher.notify_finish(1)
        
        # Assert
        self.subscriber.finish.assert_called()
        self.assertNotIn(1, self.publisher._subscribers)
