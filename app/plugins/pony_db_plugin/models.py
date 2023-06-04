import datetime
import uuid

from pony.orm import Database, PrimaryKey, Required, Optional, Set

__all__ = [
    'db',
    'User',
    'HistoryLogin',
]

db = Database()


class User(db.Entity):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4, nullable=False)
    login = Required(str, unique=True, nullable=False)
    password = Required(str, nullable=False)
    updated_at = Required(datetime.datetime)
    created_at = Optional(datetime.datetime)

    history_login = Set("HistoryLogin")

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}>'


class HistoryLogin(db.Entity):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4, nullable=False)
    user = Required(User)
    content = Required(str, nullable=False)
    created_at = Optional(datetime.datetime)
