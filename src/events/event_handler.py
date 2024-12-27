from .event import Event
from .visitor import Visitor


class EventHandler:
    def __init__(self, visitor: Visitor) -> None:
        self._visitor = visitor

    def add_event(self, event: Event) -> None:
        event.accept(self._visitor)
