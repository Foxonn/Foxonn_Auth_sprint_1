from pony.orm import Database, db_session

from app.exceptions import UserNotFoundError
from app.functions.query.interfaces import IIdentificationUser
from app.plugins.pony_db_plugin.models import User

__all__ = ['IdentificationUser']


class IdentificationUser(IIdentificationUser):
    __slots__ = ()

    async def __call__(self, login: str, password: str) -> User:
        with db_session:
            if user := User.get(login=login, password=password):
                return user
            raise UserNotFoundError()
