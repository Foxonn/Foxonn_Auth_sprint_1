import datetime
from uuid import uuid4

from app.functions.commands.interfaces import ICreateHistoryLogin
from app.plugins.pony_db_plugin.models import HistoryLogin, User

__all__ = ['CreateHistoryLogin']


class CreateHistoryLogin(ICreateHistoryLogin):
    __slots__ = ()

    async def __call__(self, user: User, content: str) -> None:
        created_at = datetime.datetime.utcnow()
        HistoryLogin(
            id=uuid4(),
            user=user,
            content=content,
            created_at=created_at,
        )
