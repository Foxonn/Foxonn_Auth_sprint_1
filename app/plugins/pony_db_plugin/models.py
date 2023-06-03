import datetime
import uuid

from pony.orm import Database, PrimaryKey, Required, Optional

__all__ = [
    'db',
    'User',
]

db = Database()


class User(db.Entity):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4, nullable=False)
    login = Required(str, unique=True, nullable=False)
    password = Required(str, nullable=False)
    created_at = Optional(datetime.datetime, default=datetime.datetime.utcnow)
    updated_at = Required(datetime.datetime)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}>'
