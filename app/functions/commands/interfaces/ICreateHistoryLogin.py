from typing import Any

from app.plugins.pony_db_plugin.models import User

__all__ = ['ICreateHistoryLogin']


class ICreateHistoryLogin:
    __slots__ = ()

    async def __call__(self, user: User, content: Any) -> None:
        raise NotImplementedError()
