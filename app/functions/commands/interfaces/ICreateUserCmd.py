import typing as t

__all__ = ['ICreateUserCmd']


class ICreateUserCmd:
    __slots__ = ()

    async def __call__(self, data: t.Mapping[str, t.Any]) -> None:
        raise NotImplementedError()
