import datetime
from typing import Any, Mapping

from pony.orm import commit, db_session

from app.functions.commands.interfaces.ICreateUser import ICreateUser
from app.plugins.pony_db_plugin.models import User

__all__ = ['CreateUser']


class CreateUser(ICreateUser):
    __slots__ = ()

    def __init__(self) -> None:
        pass

    @db_session
    async def __call__(self, data: Mapping[str, Any]) -> None:
        User(**data)
        commit()
