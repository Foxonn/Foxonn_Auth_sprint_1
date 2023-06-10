import typing as t

__all__ = ['IGetHistoryLogin']


class IGetHistoryLogin:
    __slots__ = ()

    async def __call__(self, user_id: str) -> t.Sequence[t.Mapping[str, t.Any]]:
        raise NotImplementedError()
