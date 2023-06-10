import datetime
import typing as t

from app.functions.commands.interfaces.ICreateUser import ICreateUser
from app.plugins.pony_db_plugin.models import User

__all__ = ['CreateUser']


class CreateUser(ICreateUser):
    __slots__ = ()

    async def __call__(self, data: t.Mapping[str, t.Any]) -> None:
        created_at = datetime.datetime.utcnow()
        User(**data, created_at=created_at, updated_at=created_at)
