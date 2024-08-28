import unittest
from typing import Dict
from python.subscriber import Subscriber

class TestSubscriber(unittest.TestCase):
    
    def test_subscriber_update(self):
        class ConcreteSubscriber(Subscriber):
            def update(self, event: Dict) -> None:
                self.received_event = event
            
            def finish(self) -> None:
                pass

        subscriber = ConcreteSubscriber()
        event = {'id': 1, 'data': 'test event'}
        
        # Act
        subscriber.update(event)
        
        # Assert
        self.assertEqual(subscriber.received_event, event)

    def test_subscriber_finish(self):
        class ConcreteSubscriber(Subscriber):
            def update(self, event: Dict) -> None:
                pass
            
            def finish(self) -> None:
                self.finished = True

        subscriber = ConcreteSubscriber()
        
        # Act
        subscriber.finish()
        
        # Assert
        self.assertTrue(hasattr(subscriber, 'finished'))
        self.assertTrue(subscriber.finished)
