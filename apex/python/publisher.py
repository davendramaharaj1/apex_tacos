from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict

# Define a generic Publisher
class Publisher(ABC):
    """
    The Publisher interface declares methods for managing subscribers
    """

    def __init__(self) -> None:
        super().__init__()
        self._subscribers = {}
    
    @abstractmethod
    def attach(self, id: int, subscriber: Subscriber) -> None:
        """
        Attach a subscriber to the publisher
        """
        pass

    @abstractmethod
    def detach(self, id: int, subscriber: Subscriber) -> None:
        """
        Detach a subscriber from the publisher
        """
        pass

    @abstractmethod
    def notify(self, event: Dict) -> None:
        """
        Notify subscriber about an event
        """
        pass