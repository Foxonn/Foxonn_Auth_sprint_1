import uuid

from pony.orm import Database
from pony.orm import PrimaryKey
from pony.orm import Required

__all__ = ['User']


class Base(Database):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4, nullable=False)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}>'


class User(Base):
    login = Required(str, unique=True, nullable=False)
    password = Required(str, nullable=False)
