from publisher import Publisher
from subscriber import Subscriber
from typing import Dict
from log import message

class EventManager(Publisher):
    '''
    Top Level publisher in the APEX backend
    '''

    def __init__(self) -> None:
        super().__init__()
        self.pub_m = message()

    # Add subscriber
    def attach(self, id: int, subscriber: Subscriber) -> None:
        if id not in self._subscribers:
            self.pub_m.display_info(f"Subscriber {id} doesn't exist!")
            self._subscribers[id] = []
        self._subscribers[id].append(subscriber)
        self.pub_m.display_info("Subscriber Added!")
    
    # Remove subscriber
    def detach(self, id: int, subscriber: Subscriber) -> None:
        if id in self._subscribers:
            self._subscribers[id].remove(subscriber)
            self.pub_m.display_info(f"Subscriber {id} Removed!")
    
    # API Endpoint for Upstream
    def forward_event(self, id: int, event: Dict) -> None:
        for subscriber in self._subscribers[id]:
            # subscriber.update(event)
            self.pub_m.display_info(f"Subscriber {id} updated!")

    # Notify subscribers of incoming event
    def notify(self, event: Dict) -> None:
        # Extract id from event
        id = event['id']

        # Forward Event downstream
        self.forward_event(id, event)
        self.pub_m.display_info(f"Subscriber {id} notified!")

# if __name__ == "__main__":
#     s = Subscriber()
#     e = EventManager()
#     e.attach(1,s)

#     e.attach(3,s)

#     e.notify({'id': 1})

#     e.detach(1,s)