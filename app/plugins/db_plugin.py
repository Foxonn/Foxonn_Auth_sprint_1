import uuid
from typing import Any
from typing import Mapping

from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager.impl import plugins_manager

__all__ = ['DBPlugin']


class PluginsSettingsModel(BaseModel):
    dsn: str


class DBPlugin(IPlugin):
    __slots__ = (
        '__dsn',
    )

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return 'db'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        plugins_settings = PluginsSettingsModel(**plugins_settings)
        engine = create_engine(url=plugins_settings.dsn, convert_unicode=True)
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        Base = declarative_base()
        Base.query = db_session.query_property()

        class User(Base):
            __tablename__ = 'users'

            id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
            login = Column(String, unique=True, nullable=False)
            password = Column(String, nullable=False)

            def __repr__(self):
                return f'<User {self.login}>'

        Base.metadata.create_all(bind=engine)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(DBPlugin())
