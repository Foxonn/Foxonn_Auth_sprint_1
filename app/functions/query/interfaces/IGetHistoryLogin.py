from typing import Any, Mapping, Sequence

__all__ = ['IGetHistoryLogin']


class IGetHistoryLogin:
    __slots__ = ()

    async def __call__(self, user_id: str) -> Sequence[Mapping[str, Any]]:
        raise NotImplementedError()
