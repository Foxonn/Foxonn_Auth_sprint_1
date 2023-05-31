import uuid
from typing import Any
from typing import Mapping

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import UUID

from app.utils.ioc import ioc
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
        app = ioc.get(Flask)
        db = ioc.get(SQLAlchemy)

        app.config["SQLALCHEMY_DATABASE_URI"] = plugins_settings.dsn  # "sqlite:///example.sqlite"
        db.init_app(app)

        app.app_context().push()

        class User(db.Model):
            __tablename__ = 'users'

            id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
            login = Column(String, unique=True, nullable=False)
            password = Column(String, nullable=False)

            def __init__(self, login: str, password: str) -> None:
                self.login = login
                self.password = password

            def __repr__(self) -> str:
                return f'<User {self.login}>'

        db.create_all()

        admin = User(login='admin', password='password')
        db.session.add(admin)
        db.session.commit()

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(DBPlugin())
