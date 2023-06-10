import typing as t

from app.plugins.pony_db_plugin.models import User

__all__ = ['ICreateHistoryLogin']


class ICreateHistoryLogin:
    __slots__ = ()

    async def __call__(self, user: User, fingerprint: t.Any) -> None:
        raise NotImplementedError()
