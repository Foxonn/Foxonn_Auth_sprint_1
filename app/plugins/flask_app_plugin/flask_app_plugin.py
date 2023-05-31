from typing import Any
from typing import Mapping

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager import plugins_manager

__all__ = ['FlaskAppPlugin']


class PluginsSettings(BaseModel):
    dns: str


class FlaskAppPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'flask_app_plugin'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        app = Flask(__name__)
        db = SQLAlchemy()
        ioc.set(Flask, app)
        ioc.set(SQLAlchemy, db)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(FlaskAppPlugin())
