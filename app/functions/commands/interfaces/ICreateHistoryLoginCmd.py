import typing as t

from app.plugins.pony_db_plugin.models import User

__all__ = ['ICreateHistoryLoginCmd']


class ICreateHistoryLoginCmd:
    __slots__ = ()

    async def __call__(self, user: User, fingerprint: t.Any) -> None:
        raise NotImplementedError()
