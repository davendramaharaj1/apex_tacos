from python.publisher import Publisher
from python.subscriber import Subscriber
from typing import Dict
from log import Logger
import logging

class EventManager(Publisher):
    '''
    Top Level publisher in the APEX backend
    '''

    def __init__(self) -> None:
        super().__init__()
        self._pub = Logger("EventManager",logging.DEBUG)

    # Add subscriber
    def attach(self, id: int, subscriber: Subscriber) -> None:
        if id not in self._subscribers:
            self._pub.log_info(f"Subscriber {id} doesn't exist!")
            self._subscribers[id] = []
        self._subscribers[id].append(subscriber)
        self._pub.log_info("Subscriber Added!")
    
    # Remove subscriber
    def detach(self, id: int, subscriber: Subscriber) -> None:
        if id in self._subscribers and subscriber in self._subscribers[id]:
            self._subscribers[id].remove(subscriber)
            self._pub.log_info(f"Subscriber {id} Removed!")
            if not self._subscribers[id]:  # Optionally, clean up empty lists
                del self._subscribers[id]

    # Notify subscribers of an event
    def notify(self, event: Dict) -> None:
        id = event.get('id')
        if id in self._subscribers:
            for subscriber in self._subscribers[id]:
                subscriber.update(event)
                self._pub.log_info(f"Subscriber {id} updated!")
        else:
            # Handle missing id in subscribers, maybe log a warning
            pass

    # Notify subscribers that this publisher is done
    def notify_finish(self, id: int) -> None:
        if id in self._subscribers:
            for subscriber in self._subscribers[id]:
                subscriber.finish()
                # remove subscriber
                self.detach(id, subscriber)
    
    # API Endpoint for Upstream to notify subscribers of an event
    def forward_event(self, event: Dict) -> None:
        self.notify(event=event)
    
    # API Endpoint for Upstream to inform subscribers 
    # that their Event Source (Tacos Object) is finished
    def finish(self, id) -> None:
        self.notify_finish(id)