from publisher import Publisher
from subscriber import Subscriber
from typing import Dict

class EventManager(Publisher, Subscriber):
    '''
    Top Level publisher in the APEX backend
    '''

    def __init__(self) -> None:
        super().__init__()

    # Add subscriber
    def attach(self, id: int, subscriber: Subscriber) -> None:
        if id not in self._subscribers:
            self._subscribers[id] = []
        self._subscribers[id].append(subscriber)
    
    # Remove subscriber
    def detach(self, id: int, subscriber: Subscriber) -> None:
        if id in self._subscribers:
            self._subscribers[id].remove(subscriber)
    
    # API Endpoint for Upstream
    def forward_event(self, id: int, event: Dict) -> None:
        for subscriber in self._subscribers[id]:
            subscriber.update(event)

    # Notify subscribers of incoming event
    def notify(self, event: Dict) -> None:
        # Extract id from event
        id = event['id']

        # Forward Event downstream
        self.forward_event(id, event)