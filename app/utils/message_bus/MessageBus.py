import asyncio
import logging
import typing as t

from app.utils.message_bus.EventHandler import EventHandler
from app.utils.message_bus.EventModel import EventModel

__all__ = [
    'MessageBus',
    'message_bus',
]

T = t.TypeVar('T')


class MessageBus:
    __slots__ = (
        '_store',
    )

    def __init__(self) -> None:
        self._store: t.Dict[t.Type[EventModel], t.Set[EventHandler]] = dict()

    def subscribe(self, event: t.Type[EventModel], event_handler: EventHandler) -> None:
        if event not in self._store:
            self._store[event] = set()
        self._store[event].add(event_handler)

    async def publish(self, event: EventModel) -> None:
        try:
            callbacks = self._store[type(event)]
        except KeyError as err:
            logging.error(err)
        else:
            for callback in callbacks:
                await callback(event)


message_bus = MessageBus()

if __name__ == '__main__':

    class CustomEvent(EventModel):
        pass


    class CustomEventHandler(EventHandler):
        async def __call__(self, event: EventModel) -> None:
            print(event.info.created_at)


    loop = asyncio.get_event_loop()

    try:
        mb = MessageBus()
        mb.subscribe(event=CustomEvent, event_handler=CustomEventHandler())
        mb.publish(event=CustomEvent())
    finally:
        loop.close()
