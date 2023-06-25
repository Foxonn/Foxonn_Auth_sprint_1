import typing as t

T = t.TypeVar("T")

__all__ = ['EventHandler']


class EventHandler(t.Generic[T]):
    __slots__ = ()

    async def __call__(self, event: T) -> None:
        raise NotImplementedError()
