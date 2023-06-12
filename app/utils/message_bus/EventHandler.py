from app.utils.message_bus.EventModel import EventModel

__all__ = ['EventHandler']


class EventHandler:
    __slots__ = ()

    async def __call__(self, event: EventModel) -> None:
        raise NotImplementedError()
