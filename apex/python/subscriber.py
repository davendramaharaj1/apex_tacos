from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict

class Subscriber(ABC):
    '''
    The Subscriber interface declares the update method, used by publishers.
    '''

    @abstractmethod
    def update(self, event: Dict) -> None:
        '''
        Receive update from publisher.
        '''
        pass

    @abstractmethod
    def finish(self) -> None:
        '''
        Subscriber does some logic after Event Source is finished
        '''