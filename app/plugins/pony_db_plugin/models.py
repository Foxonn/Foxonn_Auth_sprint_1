import datetime
import uuid

from pony.orm import Database
from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Set

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
    fingerprints = Set("Fingerprints")

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}>'


class HistoryLogin(db.Entity):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4, nullable=False)
    user = Required(User)
    fingerprint = Required(bytes, nullable=False)
    created_at = Optional(datetime.datetime)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}>'


class Fingerprints(db.Entity):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4, nullable=False)
    user = Required(User)
    fingerprint = Required(bytes, nullable=False, unique=True)
    created_at = Optional(datetime.datetime)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}>'
