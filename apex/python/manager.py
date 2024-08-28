from python.publisher import Publisher
from python.subscriber import Subscriber
from typing import Dict

class EventManager(Publisher):
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
        if id in self._subscribers and subscriber in self._subscribers[id]:
            self._subscribers[id].remove(subscriber)
            if not self._subscribers[id]:  # Optionally, clean up empty lists
                del self._subscribers[id]

    # Notify subscribers of an event
    def notify(self, event: Dict) -> None:
        id = event.get('id')
        if id in self._subscribers:
            for subscriber in self._subscribers[id]:
                subscriber.update(event)
        else:
            # Handle missing id in subscribers, maybe log a warning
            pass

    # Notify subscribers that this publisher is done
    def notify_finish(self, id: int) -> None:
        if id in self._subscribers:
            for subscriber in self._subscribers[id]:
                subscriber.finish()

                # remove subscriber
                self.detach(1, subscriber)
    
    # API Endpoint for Upstream to notify subscribers of an event
    def forward_event(self, event: Dict) -> None:
        self.notify(event=event)
    
    # API Endpoint for Upstream to inform subscribers 
    # that their Event Source (Tacos Object) is finished
    def finish(self) -> None:
        self.notify_finish()