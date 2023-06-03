from typing import Any, Mapping

__all__ = ['ICreateUser']


class ICreateUser:
    __slots__ = ()

    async def __call__(self, data: Mapping[str, Any]) -> None:
        raise NotImplementedError()
