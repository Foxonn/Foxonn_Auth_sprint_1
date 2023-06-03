from typing import Any, Mapping

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

from app.plugins.flask_app_plugin.api.v1.views import init_views
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin, plugins_manager

__all__ = ['FlaskAppPlugin']


class PluginsSettings(BaseModel):
    dns: str


class FlaskAppPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'flask_app'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        app = Flask(__name__)
        db = SQLAlchemy()

        ioc.set(Flask, app)
        ioc.set(SQLAlchemy, db)

        init_views(app=app)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(FlaskAppPlugin())
