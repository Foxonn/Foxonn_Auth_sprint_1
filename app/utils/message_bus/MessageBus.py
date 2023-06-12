import asyncio
import logging
import typing as t
from asyncio import AbstractEventLoop

from app.utils.message_bus.EventHandler import EventHandler
from app.utils.message_bus.EventModel import EventModel

__all__ = ['MessageBus']


class MessageBus:
    __slots__ = (
        '_store',
        '_loop',
    )

    def __init__(self, loop: AbstractEventLoop) -> None:
        self._store: t.Dict[t.Type[EventModel], t.Set[EventHandler]] = dict()
        self._loop = loop

    def subscribe(self, event: t.Type[EventModel], event_handler: EventHandler) -> None:
        if event not in self._store:
            self._store[event] = set()
        self._store[event].add(event_handler)

    def publish(self, event: EventModel) -> None:
        try:
            callbacks = self._store[type(event)]
        except KeyError as err:
            logging.error(err)
        else:
            for callback in callbacks:
                self._loop.run_until_complete(callback(event))


if __name__ == '__main__':

    class CustomEvent(EventModel):
        pass


    class CustomEventHandler(EventHandler):
        async def __call__(self, event: EventModel) -> None:
            print(event.info.created_at)


    loop = asyncio.get_event_loop()

    try:
        mb = MessageBus(loop=loop)
        mb.subscribe(event=CustomEvent, event_handler=CustomEventHandler())
        mb.publish(event=CustomEvent())
    finally:
        loop.close()
