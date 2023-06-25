import logging
import typing as t

from app.utils.event_bus.EventHandler import EventHandler

__all__ = [
    'EventBus',
    'event_bus',
]

T = t.TypeVar('T')


class EventBus:
    __slots__ = (
        '_store',
    )

    def __init__(self) -> None:
        self._store: t.Dict[t.Type[t.Any], t.Set[EventHandler]] = dict()

    def subscribe(self, event: t.Any, event_handler: EventHandler) -> None:
        if event not in self._store:
            self._store[event] = set()
        self._store[event].add(event_handler)

    async def publish(self, event: t.Any) -> None:
        try:
            callbacks = self._store[type(event)]
        except KeyError as err:
            logging.error(err)
        else:
            for callback in callbacks:
                await callback(event)


event_bus = EventBus()
